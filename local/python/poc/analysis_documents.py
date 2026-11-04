"""호스트가 실제 읽은 문서 영수증과 물리 열/FK를 SQL 승인에 결합한다."""
import hashlib
import json
import math
import re
from pathlib import Path

import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope, build_scope, Scope

from .config import PocError
from .contracts import canonical, seal_plan
from .sql_policy import validate_sql
from .catalog import normalized_catalog


def sha(data):
    return hashlib.sha256(data).hexdigest()


DOCUMENT_PROJECTION_VERSION = "markdown-evidence-v1"

# Generic validator constraints, never question-specific SQL or result examples.
HOST_SQL_STRUCTURE_CONSTRAINTS = (
    "현재 승인 경로는 EXISTS, 스칼라 서브쿼리와 WHERE/HAVING의 서브쿼리를 지원하지 않습니다. 해당 구조를 생성하지 마세요.",
    "상세 행의 존재 여부로 헤더 금액을 집계할 때는 하나의 CTE 안에서 헤더와 상세를 물리 FK로 JOIN하고 상세 조건을 적용하세요. "
    "최종 집계에 필요한 헤더 속성과 전체 문서 식별자를 투영하고 DISTINCT 또는 해당 헤더 속성 전체의 GROUP BY로 문서별 중복을 제거하세요. "
    "그 뒤 바깥 SELECT는 해당 CTE만 단일 소스로 읽어 최종 집계하세요. 상세와 직접 JOIN한 중복 행의 헤더 금액을 합산하지 마세요.",
    "JOIN의 ON에는 문서에 있는 실제 FK의 전체 열을 AND로 연결한 등가 조건이 필요합니다. "
    "헤더와 상세에 적용되는 테넌트 조건을 모두 유지하고, 필요한 동일 테넌트 연결 조건도 보존하세요. FK 연결만으로 테넌트 일치를 단정하지 마세요.",
    "모든 확정 필터는 실제 반환 행을 만드는 CTE와 최종 SELECT의 단일 소스 흐름에서 strict AND 조건으로 적용하세요. "
    "미사용 CTE의 필터는 적용 근거가 아닙니다. CTE 결과를 다른 테이블과 바깥에서 JOIN하지 말고 필요한 물리 테이블 JOIN은 CTE 안에서 완료하세요.",
)


def project_document(source, version=DOCUMENT_PROJECTION_VERSION):
    """Keep documented facts; remove only redundant presentation from actual MD."""
    if version != DOCUMENT_PROJECTION_VERSION:
        raise PocError("DOCUMENT_PROJECTION_UNSUPPORTED")
    # These machine anchors duplicate the constraint name and physical tables in
    # the same row. Other HTML comments may contain facts and are retained.
    projected = re.sub(r"<!--[ \t]*FK_(?:OUT|IN):[^\r\n>]*-->", "", source)
    # Preserve displayed table names, labels and inline code; drop link addresses.
    projected = re.sub(r"(?<!!)\[([^\]\r\n]+)\]\([^\)\r\n]*\)", r"\1", projected)
    relations = set()
    for line in projected.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip().replace("`", "") for cell in line.split("|")[1:-1]]
        if len(cells) == 7 and cells[0] not in ("제약조건",):
            relations.add((cells[1], cells[2], cells[3], cells[4]))

    def redundant_diagram(match):
        block = match.group(0)
        nodes = dict(re.findall(r'^\s*(n\d+)\["([^"\r\n]+)"\]\s*$', block, re.M))
        edges = re.findall(r'^\s*(n\d+) -->\|"([^"\r\n]+) → ([^"\r\n]+)"\| (n\d+)\s*$', block, re.M)
        # An unfamiliar or partly documented diagram stays verbatim. Generated
        # diagrams are removable only when every node/edge has the FK-row source.
        statements = [line.strip() for line in block.splitlines()[2:-1] if line.strip()]
        endpoints = {table for relation in relations for table in (relation[0], relation[2])}
        if (nodes and edges and len(statements) == len(nodes) + len(edges)
                and all(table in endpoints for table in nodes.values())
                and all((nodes.get(child), child_columns, nodes.get(parent), parent_columns) in relations
                        for child, child_columns, parent_columns, parent in edges)):
            return ""
        return block

    projected = re.sub(r"(?m)^```mermaid\r?\nflowchart LR\r?\n[\s\S]*?^```[ \t]*(?=\r?$)", redundant_diagram, projected)
    return re.sub(r"\n{3,}", "\n\n", projected)


def row_lineage(tree):
    """The sole-source CTE/subquery chain feeding the final rows, excluding unused CTEs."""
    active = set()
    scope = build_scope(tree)
    while scope is not None:
        # Scalar subqueries can import unfiltered data independently of the row source.
        if scope.subquery_scopes:
            return set()
        active.add(scope.expression)
        sources = list(scope.selected_sources.values())
        scope = sources[0][1] if len(sources) == 1 and isinstance(sources[0][1], Scope) else None
    return active


def predicate_values(operands, params):
    """Only SQL literals and explicitly bound scalar parameters constitute evidence."""
    values = []
    for node in operands:
        if isinstance(node, exp.Literal):
            value = node.this
        elif isinstance(node, exp.Placeholder) and node.name in params:
            value = params[node.name]
            if not isinstance(value, (str, int, float, bool)) or isinstance(value, float) and not math.isfinite(value):
                return None
        else:
            return None
        values.append(str(value))
    return values if values else None


class Documents:
    def __init__(self, root):
        self.root = Path(root)
        self.directory = self.root / "docs/database/idempiere"
        self.snapshot_path = self.root / ".local/datasets/idempiere/documentation-snapshot.json"
        try:
            self.manifest_raw = (self.directory / "manifest.json").read_bytes()
            self.manifest = json.loads(self.manifest_raw)
            raw = self.snapshot_path.read_bytes()
            self.snapshot = json.loads(raw)
        except (OSError, ValueError):
            raise PocError("DOCUMENTATION_UNAVAILABLE") from None
        self.snapshot_hash = sha(raw)
        if self.manifest["snapshot_sha256"] != self.snapshot_hash:
            raise PocError("DOCUMENTATION_SNAPSHOT_MISMATCH")
        self.columns = {}
        for column in self.snapshot["columns"]:
            self.columns.setdefault(column["table_name"], {})[column["physical_name"]] = column["data_type"]
        self.fks = [c for c in self.snapshot["constraints"] if c["kind"] == "f" and c.get("validated")]

    def read(self, candidates, catalog, required_tables=None):
        catalog = normalized_catalog(catalog)
        if not isinstance(candidates, list) or not 1 <= len(candidates) <= 12 or len(set(candidates)) != len(candidates):
            raise PocError("SCHEMA_SELECTION_INVALID")
        if any(n not in catalog["tables"] or n not in self.columns or n not in self.manifest["table_paths"] for n in candidates):
            raise PocError("SCHEMA_SELECTION_INVALID")
        selected, documents, size = [], [], 0
        graph = {}
        for fk in self.fks:
            if set(fk["source_columns"]) & {"createdby", "updatedby", "ad_client_id", "ad_org_id"}:
                continue
            graph.setdefault(fk["source_table"], set()).add(fk["target_table"])
            graph.setdefault(fk["target_table"], set()).add(fk["source_table"])
        reachable, frontier = set(candidates), set(candidates)
        for _ in range(2):
            frontier = set().union(*(graph.get(t, set()) for t in frontier)) - reachable if frontier else set()
            reachable.update(frontier)
        required_tables = [] if required_tables is None else required_tables
        if (not isinstance(required_tables, list) or len(required_tables) > 32
                or any(not isinstance(t, str) or t not in reachable or t not in catalog["tables"]
                    or t not in self.columns or t not in self.manifest["table_paths"] for t in required_tables)
                or len(set(candidates) | set(required_tables)) > 32):
            raise PocError("DOCUMENT_EXPANSION_LIMIT")

        def add(name, required=False):
            nonlocal size
            relative = self.manifest["table_paths"].get(name)
            if not relative or name not in catalog["tables"] or name in selected or len(selected) >= 32:
                return False
            path = (self.directory / relative).resolve()
            if not path.is_relative_to(self.directory.resolve()):
                raise PocError("DOCUMENT_PATH_INVALID")
            raw = path.read_bytes()
            if self.manifest.get("files", {}).get(relative) != sha(raw):
                raise PocError("DOCUMENTATION_CHANGED", "문서 파일이 생성 manifest의 해시와 다릅니다.")
            # Budget the exact UTF-8 model context, including JSON escaping.
            doc = {"table": name, "path": relative, "sha256": sha(raw), "content": project_document(raw.decode("utf-8-sig"))}
            length = len(canonical(doc).encode())
            if size + length + len(documents) + 2 > 131072:
                if required:
                    raise PocError("DOCUMENT_CONTEXT_LIMIT", "필수 문서가 128KiB를 초과합니다. 질문 범위를 줄여주세요.")
                return False
            selected.append(name)
            documents.append(doc)
            size += length
            return True

        for name in candidates:
            add(name, True)
        for name in required_tables:
            if name not in selected and not add(name, True):
                raise PocError("DOCUMENT_CONTEXT_LIMIT")
        evidence = {"manifest_sha256": sha(self.manifest_raw), "snapshot_sha256": self.snapshot_hash,
                    "captured_at": self.manifest["captured_at"], "documents": [{k: d[k] for k in ("table", "path", "sha256")} for d in documents],
                    "context_sha256": sha(canonical(documents).encode()), "context_bytes": len(canonical(documents).encode()),
                    "projection_version": DOCUMENT_PROJECTION_VERSION,
                    "final_call_included": True, "receipt_origin": "host_read"}
        context = {"dataset_id": catalog.get("dataset_id"), "dataset_label": catalog.get("dataset_label"), "schema": catalog.get("schema", "adempiere"), "tables": {n: [{"name": k, "type": v} for k, v in self.columns[n].items()] for n in selected},
                   "business_rules": catalog.get("business_rules", []), "tenant": catalog.get("tenant"), "documents": documents,
                   "host_sql_structure_constraints": list(HOST_SQL_STRUCTURE_CONSTRAINTS),
                   "relationships": [f for f in self.fks if f["source_table"] in selected and f["target_table"] in selected]}
        return context, evidence, {"candidate_tables": candidates, "selected_tables": selected, "available_neighbors": sorted(reachable - set(selected)), "max_hops": 2, "method": "host_document_read_with_explicit_bidirectional_fk_expansion"}

    def verify_receipt(self, evidence):
        if evidence.get("receipt_origin") != "host_read" or evidence.get("snapshot_sha256") != self.snapshot_hash or evidence.get("manifest_sha256") != sha(self.manifest_raw):
            raise PocError("DOCUMENTATION_CHANGED")
        reconstructed = []
        projection_version = evidence.get("projection_version")
        if projection_version is not None and projection_version != DOCUMENT_PROJECTION_VERSION:
            raise PocError("DOCUMENT_PROJECTION_UNSUPPORTED")
        for receipt in evidence.get("documents", []):
            expected = self.manifest["table_paths"].get(receipt["table"])
            if not expected or expected != receipt["path"]:
                raise PocError("DOCUMENTATION_CHANGED")
            path = (self.directory / expected).resolve()
            if not path.is_relative_to(self.directory.resolve()):
                raise PocError("DOCUMENT_PATH_INVALID")
            raw = path.read_bytes()
            if sha(raw) != receipt["sha256"] or self.manifest.get("files", {}).get(expected) != sha(raw):
                raise PocError("DOCUMENTATION_CHANGED")
            content = raw.decode("utf-8-sig")
            if projection_version is not None:
                content = project_document(content, projection_version)
            reconstructed.append({**receipt, "content": content})
        encoded = canonical(reconstructed).encode()
        if sha(encoded) != evidence.get("context_sha256"):
            raise PocError("DOCUMENT_RECEIPT_MISMATCH")
        # Old receipts predate projection and may have counted per-document JSON
        # without list delimiters. Their original full-content hash remains valid.
        if projection_version is not None and (len(encoded) != evidence.get("context_bytes") or len(encoded) > 131072):
            raise PocError("DOCUMENT_RECEIPT_MISMATCH")

    def verify_plan(self, plan, catalog, conditions):
        if plan.get("contract_version") != 2 or seal_plan(plan)["digest"] != plan.get("digest"):
            raise PocError("PLAN_MISMATCH")
        if plan["schema_version"] != catalog["schema_version"]:
            raise PocError("SCHEMA_CHANGED")
        self.verify_receipt(plan["document_evidence"])
        if plan.get("provenance") != "local_sample" and plan["document_evidence"].get("final_call_included") is not True:
            raise PocError("DOCUMENT_EVIDENCE_MISSING")
        if plan.get("confirmed_conditions") != conditions:
            raise PocError("CONDITIONS_CHANGED")
        validate_sql(plan["sql"], plan["params"], set(plan["schema_selection"]["selected_tables"]), schema="adempiere")
        used, joins = self.validate_structure(plan["sql"])
        documented = {r["table"] for r in plan["document_evidence"]["documents"]}
        if not used.issubset(documented):
            raise PocError("DOCUMENT_EVIDENCE_MISSING")
        if plan.get("joins") != joins:
            raise PocError("JOIN_EVIDENCE_MISMATCH")
        if "inactive_date_basis" in plan and plan["inactive_date_basis"] != self.inactive_date_basis(plan, conditions, catalog):
            raise PocError("DATE_BASIS_EVIDENCE_MISMATCH", "날짜 기준 미적용 근거를 호스트에서 재검증하지 못했습니다.")
        self.verify_conditions(plan, conditions, catalog)
        self.verify_scope_filters(plan, conditions)

    def verify_scope_filters(self, plan, baseline):
        """Prove only active/date range restrictions against the pre-SQL baseline.

        This is deliberately not an arbitrary SQL predicate or NL intent verifier.
        Ambiguous occurrences and non-identity expressions require confirmation.
        """
        bindings = plan.get("condition_bindings", {})
        if not isinstance(bindings, dict):
            raise PocError("CONDITION_BINDINGS_INVALID")
        tree = sqlglot.parse_one(plan["sql"], read="postgres")
        schema = {"adempiere": {name: {column: "UNKNOWN" for column in columns} for name, columns in self.columns.items()}}
        try:
            # Analyze a copy only. Expanding identity stars avoids treating an
            # unrelated derived-column filter as an unknown range restriction.
            tree = qualify(tree.copy(), dialect="postgres", schema=schema, validate_qualify_columns=True, identify=False)
        except Exception:
            raise PocError("SQL_COLUMN_INVALID", "실제 스냅샷에 없는 열 또는 모호한 열 참조입니다.") from None
        scopes = {s.expression: s for s in traverse_scope(tree)}
        lineage = row_lineage(tree)
        occurrences = {}
        for expression, scope in scopes.items():
            if expression in lineage:
                for _, source in scope.selected_sources.values():
                    if isinstance(source, exp.Table):
                        occurrences.setdefault(source.name, set()).add((id(expression), source.alias_or_name))

        def reject(kind):
            raise PocError("UNAPPROVED_SCOPE_FILTER", f"{kind} 범위 조건의 승인 근거가 없습니다. "
                "확정 조건과 정확한 물리 열 binding이 필요하며, 필터 대상 테이블이 한 번만 등장하는 경우를 지원합니다. "
                "여러 별칭·함수·OR로 구성된 범위는 현재 조건 계약으로 증명할 수 없어 별도 확인이 필요합니다.")

        def origins(column, depth=0):
            if depth > 16:
                reject("원본이 모호한")
            scope = scopes.get(column.find_ancestor(exp.Select))
            sources = {a: s for a, (_, s) in scope.selected_sources.items()} if scope else {}
            possible = [sources.get(column.table)] if column.table else list(sources.values())
            found = {}
            for source in possible:
                if isinstance(source, exp.Table):
                    if source.db in ("", "adempiere") and not source.catalog:
                        key = (source.name, column.name, id(scope.expression), source.alias_or_name)
                        found[key] = True
                elif isinstance(source, Scope):
                    if not isinstance(source.expression, exp.Select):
                        for branch in source.union_scopes:
                            for projected in branch.expression.selects:
                                if projected.alias_or_name == column.name:
                                    for child in projected.find_all(exp.Column):
                                        found.update({key: False for key in origins(child, depth + 1)})
                        continue
                    projections = source.expression.selects
                    names = source.outer_columns or [item.alias_or_name for item in projections]
                    matches = [item for name, item in zip(names, projections) if name == column.name]
                    if len(matches) != 1:
                        continue
                    projected = matches[0].this if isinstance(matches[0], exp.Alias) else matches[0]
                    for child in projected.find_all(exp.Column):
                        for key, identity in origins(child, depth + 1).items():
                            found[key] = identity and isinstance(projected, exp.Column) and source.expression in lineage
            if len(possible) != 1:
                return {key: False for key in found}
            return found

        def references(physical, binding, kind):
            if not isinstance(binding, dict) or binding.get("kind") != kind or not isinstance(binding.get("column"), str):
                return False
            parts = binding["column"].split(".")
            return (len(parts) in (2, 3) and (len(parts) == 2 or parts[0] == "adempiere")
                    and tuple(parts[-2:]) == physical[:2])

        def strict(predicate, root):
            if predicate is not root and not isinstance(root, (exp.And, exp.Paren)):
                return False
            node = predicate
            while node is not root:
                node = node.parent
                if node is None or node is not root and not isinstance(node, (exp.And, exp.Paren)):
                    return False
            return True

        def temporal(physical):
            kind = str(self.columns.get(physical[0], {}).get(physical[1], "")).lower()
            return bool(re.search(r"\b(?:date|timestamp|timestamptz)\b", kind))

        def active(physical):
            return physical[1] == "isactive" and physical[1] in self.columns.get(physical[0], {})

        roots = []
        for expression, scope in scopes.items():
            if not isinstance(expression, exp.Select) or lineage and expression not in lineage:
                continue
            for key in ("where", "having"):
                clause = expression.args.get(key)
                if clause:
                    roots.append((clause.this, expression, True))
            for join in expression.args.get("joins", []):
                if join.args.get("on"):
                    roots.append((join.args["on"], expression, False))
        period_origins = set()
        range_operators = (exp.GT, exp.GTE, exp.LT, exp.LTE, exp.EQ, exp.NEQ, exp.Between, exp.In, exp.Like)
        for root, select, supported_site in roots:
            covered = set()
            for predicate in root.find_all(exp.Predicate):
                columns = list(predicate.find_all(exp.Column))
                covered.update(id(c) for c in columns)
                dependencies = {}
                for column in columns:
                    dependencies.update(origins(column))
                active_targets = {p for p in dependencies if active(p)}
                date_targets = {p for p in dependencies if temporal(p)} if isinstance(predicate, range_operators) else set()
                # A physical date-key equality is a relationship, not a scalar
                # period restriction. Existing FK validation still proves it.
                if isinstance(predicate, exp.EQ) and isinstance(predicate.this, exp.Column) and isinstance(predicate.expression, exp.Column):
                    date_targets = set()
                if not active_targets and not date_targets:
                    continue
                kind = "활성" if active_targets else "날짜"
                direct = origins(predicate.this) if isinstance(predicate.this, exp.Column) else {}
                if (not supported_site or select not in lineage or not strict(predicate, root)
                        or len(direct) != 1 or len(active_targets | date_targets) != 1):
                    reject(kind)
                physical, identity = next(iter(direct.items()))
                if not identity or len(occurrences.get(physical[0], set())) != 1:
                    reject(kind)
                if active_targets:
                    observed = predicate_values([predicate.expression], plan.get("params", {})) if isinstance(predicate, exp.EQ) else None
                    if ("isactive" not in baseline or not references(physical, bindings.get("isactive"), "predicate")
                            or observed != [str(baseline["isactive"])]):
                        reject(kind)
                else:
                    name = "start" if isinstance(predicate, exp.GTE) else "end" if isinstance(predicate, exp.LT) else None
                    parameter = bindings.get(name, name) if name else None
                    operand = predicate.expression if isinstance(predicate, exp.Binary) else None
                    if (name not in baseline or "date_basis" not in baseline
                            or not references(physical, bindings.get("date_basis"), "column")
                            or not isinstance(parameter, str) or not isinstance(operand, exp.Placeholder) or operand.name != parameter
                            or plan.get("params", {}).get(parameter) != baseline[name]):
                        reject(kind)
                    period_origins.add(physical)
                    if len(period_origins) != 1:
                        reject(kind)
            # Boolean/function disguises of isactive may have no Predicate node.
            for column in root.find_all(exp.Column):
                if id(column) not in covered and any(active(p) for p in origins(column)):
                    reject("활성")

    @staticmethod
    def inactive_date_basis(plan, conditions, catalog=None):
        """Prove an unused canonical date basis without removing or altering a filter.

        This is host evidence for one condition, never a new model binding kind.
        Unresolved columns/expressions fail closed and retain the normal verifier.
        """
        if "date_basis" not in conditions or "start" in conditions or "end" in conditions:
            return None
        bindings = plan.get("condition_bindings", {})
        binding = bindings.get("date_basis") if isinstance(bindings, dict) else None
        if not isinstance(binding, dict) or binding.get("kind") != "column":
            return None
        reference = binding.get("column", "")
        if not isinstance(reference, str):
            return None
        parts = reference.split(".")
        if len(parts) not in (2, 3) or len(parts) == 3 and parts[0] != "adempiere":
            return None
        table, column = parts[-2:]
        types = {table_name: {c["name"]: str(c.get("type", "")).lower() for c in columns if isinstance(c, dict) and "name" in c}
                 for table_name, columns in (catalog or {}).get("tables", {}).items()}

        def temporal(type_name):
            return bool(re.search(r"\b(?:date|timestamp|timestamptz|time|timetz|interval)\b", type_name))

        if not temporal(types.get(table, {}).get(column, "")):
            return None
        labels = {"dateinvoiced": {"청구일", "청구일 dateinvoiced"}, "dateordered": {"주문일", "주문일 dateordered"}, "dateacct": {"회계일"}}
        if conditions["date_basis"] not in labels.get(column, set()) | {column, reference, f"{table}.{column}"}:
            return None
        temporal_names = {name for columns in types.values() for name, kind in columns.items() if temporal(kind)}
        if any(name != "date_basis" and name in temporal_names for name in conditions):
            return None
        date_literal = re.compile(r"(?:^|\D)\d{4}-\d{2}-\d{2}(?:\D|$)|\b\d{2}:\d{2}(?::\d{2})?\b")
        if any(isinstance(value, str) and date_literal.search(value) for value in plan.get("params", {}).values()):
            return None
        try:
            tree = sqlglot.parse_one(plan["sql"], read="postgres")
            scopes = {scope.expression: scope for scope in traverse_scope(tree)}
        except Exception:
            return None
        lineage = row_lineage(tree)
        physical = [source for expression, scope in scopes.items() if expression in lineage
                    for _, source in scope.selected_sources.values() if isinstance(source, exp.Table)]
        if not any(source.name == table and source.db in ("", "adempiere") and not source.catalog for source in physical):
            return None
        # Check the entire statement, including unused CTEs. Never infer temporal
        # absence from only the root WHERE or from a model's declared context.
        for node in tree.walk():
            if isinstance(node, exp.Star) and not isinstance(node.parent, exp.Count):
                return None
            if isinstance(node, exp.Func) and re.search(r"DATE|TIME|INTERVAL|EXTRACT|AGE|EPOCH", node.sql_name(), re.I):
                return None
            if isinstance(node, exp.Anonymous):
                return None
            if isinstance(node, exp.DataType) and temporal(node.sql(dialect="postgres").lower()):
                return None
            if isinstance(node, exp.Literal) and node.is_string and date_literal.search(node.this):
                return None

        def column_type(node, depth=0):
            if depth > 16:
                return None
            scope = scopes.get(node.find_ancestor(exp.Select))
            if scope is None:
                return None
            sources = {alias: source for alias, (_, source) in scope.selected_sources.items()}
            possible = [sources.get(node.table)] if node.table else list(sources.values())
            matches = []
            for source in possible:
                if isinstance(source, exp.Table):
                    kind = types.get(source.name, {}).get(node.name)
                    if kind and source.db in ("", "adempiere") and not source.catalog:
                        matches.append(kind)
                elif isinstance(source, Scope):
                    projected = [item for item in source.expression.selects if item.alias_or_name == node.name]
                    if len(projected) == 1:
                        columns = list(projected[0].find_all(exp.Column))
                        kinds = [column_type(c, depth + 1) for c in columns]
                        if all(kinds):
                            matches.append("timestamp" if any(temporal(k) for k in kinds) else "non_temporal")
            if len(matches) == 1:
                return matches[0]
            # ORDER BY may refer to a SELECT alias, but ambiguous physical names
            # and recursive aliases must not provide an absence proof.
            if not matches and not node.table and node.find_ancestor(exp.Order):
                projected = [item for item in scope.expression.selects if isinstance(item, exp.Alias) and item.alias == node.name]
                if len(projected) == 1:
                    kinds = [column_type(c, depth + 1) for c in projected[0].find_all(exp.Column)]
                    if all(kinds):
                        return "timestamp" if any(temporal(k) for k in kinds) else "non_temporal"
            return None

        kinds = [column_type(node) for node in tree.find_all(exp.Column)]
        if any(kind is None or temporal(kind) for kind in kinds):
            return None
        return {"condition": "date_basis", "value": conditions["date_basis"], "column": f"{table}.{column}",
                "status": "not_applicable", "reason": "no_time_axis_or_filter", "basis": "host_sql_ast_and_catalog"}

    @staticmethod
    def preserve_sql_conditions(plan, conditions, catalog=None):
        """Persist literal business filters and date basis, not only bind parameters."""
        if not isinstance(plan.get("condition_bindings", {}), dict):
            raise PocError("CONDITION_BINDINGS_INVALID", "조건 근거는 키와 검증 형식으로 구성된 객체여야 합니다.")
        tree = sqlglot.parse_one(plan["sql"], read="postgres")
        aliases = {t.alias_or_name: t.name for t in tree.find_all(exp.Table)}
        bindings = dict(plan.get("condition_bindings", {}))
        values = dict(conditions)
        covered = set()
        for name, value in conditions.items():
            try:
                Documents.verify_conditions(plan, {name: value}, catalog)
            except PocError:
                continue
            binding = bindings.get(name, name)
            if isinstance(binding, dict):
                covered.add(binding.get("column", "").split(".")[-1])
            elif isinstance(binding, str):
                covered.add({"client_id": "ad_client_id", "tenant_id": "ad_client_id", "tenant": "ad_client_id", "status": "docstatus", "상태": "docstatus", "currency": "iso_code"}.get(name, name))
        scopes = {scope.expression: scope for scope in traverse_scope(tree)}
        candidates = {}
        for select in row_lineage(tree):
            where = select.args.get("where")
            if not where:
                continue
            for predicate in where.find_all(exp.EQ, exp.In):
                parent = predicate.parent
                strict = True
                while parent is not where:
                    if parent is None or not isinstance(parent, (exp.And, exp.Paren)):
                        strict = False
                        break
                    parent = parent.parent
                column = predicate.this
                literals = predicate.expressions if isinstance(predicate, exp.In) else [predicate.expression]
                observed = predicate_values(literals, plan.get("params", {}))
                if not strict or not isinstance(column, exp.Column) or observed is None:
                    continue
                scope = scopes.get(select)
                sources = scope.sources if scope else {}
                # A bare column in a join or a derived relation is not unambiguous evidence.
                source = sources.get(column.table) if column.table else next(iter(sources.values())) if len(sources) == 1 else None
                if not isinstance(source, exp.Table):
                    continue
                key = column.name
                candidates.setdefault(key, []).append((source.name + "." + key, observed, isinstance(predicate, exp.In)))
        for key, evidence in candidates.items():
            # SQL observation is never authorization for a new active filter.
            if key == "isactive" and key not in conditions:
                continue
            if key not in conditions and key in covered:
                continue
            # Multiple tables or contradictory predicates must not be resolved by choosing one.
            signatures = {(reference, tuple(sorted(observed))) for reference, observed, _ in evidence}
            if len(signatures) != 1:
                continue
            reference, observed, is_in = evidence[0]
            value = values.get(key, ",".join(observed))
            expected = re.split(r"\s*[,·|]\s*", str(value)) if is_in else [str(value)]
            if sorted(expected) != sorted(observed):
                continue
            if key in bindings:
                # Preserve valid parameters/metadata and any already supported binding.
                try:
                    Documents.verify_conditions(plan, {key: value}, catalog)
                    continue
                except PocError:
                    pass
                if isinstance(bindings[key], dict) and bindings[key].get("kind") == "metadata":
                    continue
            candidate = {"kind": "predicate", "column": reference}
            # The same final verifier must accept the host-derived evidence before replacement.
            Documents.verify_conditions({**plan, "condition_bindings": {key: candidate}}, {key: value}, catalog)
            values.setdefault(key, value)
            bindings[key] = candidate
        dates = {c.sql(dialect="postgres") for f in tree.find_all(exp.DateTrunc, exp.TimestampTrunc) for c in f.find_all(exp.Column)}
        if len(dates) == 1 and not any(isinstance(b, dict) and b.get("kind") == "column" and b.get("column", "").split(".")[-1] in {"dateinvoiced", "dateordered", "dateacct"} for b in bindings.values()):
            column = sqlglot.parse_one(next(iter(dates)), read="postgres")
            values.setdefault("date_basis", column.name)
            bindings.setdefault("date_basis", {"kind": "column", "column": aliases.get(column.table, column.table) + "." + column.name})
        return values, bindings

    @staticmethod
    def verify_conditions(plan, conditions, catalog=None):
        bindings = plan.get("condition_bindings", {})
        if not isinstance(bindings, dict):
            raise PocError("CONDITION_BINDINGS_INVALID", "조건 근거는 키와 검증 형식으로 구성된 객체여야 합니다.")
        tree = sqlglot.parse_one(plan["sql"], read="postgres")
        scopes = {scope.expression: scope for scope in traverse_scope(tree)}
        lineage = row_lineage(tree)
        inactive = None
        if "date_basis" in conditions and plan.get("inactive_date_basis") is not None:
            inactive = Documents.inactive_date_basis(plan, conditions, catalog)
            if inactive is None or plan["inactive_date_basis"] != inactive:
                raise PocError("DATE_BASIS_EVIDENCE_MISMATCH", "날짜 기준 미적용 근거를 호스트에서 재검증하지 못했습니다.")

        def column_matches(node, reference):
            parts = reference.split(".")
            if isinstance(node, exp.Column) and parts[-1] == "isactive":
                physical = period_column(node)
                return physical is not None and physical[1] == "isactive" and (len(parts) == 1 or physical[0] == parts[-2])
            if not isinstance(node, exp.Column) or node.name != parts[-1]:
                return False
            scope = scopes.get(node.find_ancestor(exp.Select))
            sources = scope.sources if scope else {}
            source = sources.get(node.table) if node.table else next(iter(sources.values())) if len(sources) == 1 else None
            return isinstance(source, exp.Table) and (len(parts) == 1 or source.name == parts[-2])

        def period_column(node, depth=0):
            """Resolve identity projections while retaining the original table occurrence."""
            if not isinstance(node, exp.Column) or depth > 16:
                return None
            scope = scopes.get(node.find_ancestor(exp.Select))
            sources = {alias: source for alias, (_, source) in scope.selected_sources.items()} if scope else {}
            source = sources.get(node.table) if node.table else next(iter(sources.values())) if len(sources) == 1 else None
            if isinstance(source, exp.Table):
                if source.db not in ("", "adempiere") or source.catalog:
                    return None
                # The same physical table may appear as different self-join aliases.
                # Identity projections retain this original scope/alias occurrence;
                # they must never merge separate date ranges just by table name.
                return source.name, node.name, id(scope.expression), source.alias_or_name
            if not isinstance(source, Scope) or source.expression not in lineage or not isinstance(source.expression, exp.Select):
                return None
            projections = source.expression.selects
            names = source.outer_columns or [item.alias_or_name for item in projections]
            matches = [item for name, item in zip(names, projections) if name == node.name]
            if len(matches) != 1:
                return None
            projected = matches[0].this if isinstance(matches[0], exp.Alias) else matches[0]
            return period_column(projected, depth + 1)

        def period_matches(physical, reference):
            if physical is None or not isinstance(reference, str):
                return False
            parts = reference.split(".")
            return (1 <= len(parts) <= 3 and (len(parts) < 3 or parts[0] == "adempiere")
                    and physical[1] == parts[-1] and (len(parts) == 1 or physical[0] == parts[-2]))

        def strict_filter(node):
            parent = node.parent
            while parent and not isinstance(parent, (exp.Where, exp.Having)):
                if not isinstance(parent, (exp.And, exp.Paren)):
                    return False
                parent = parent.parent
            # A predicate in an unused CTE does not restrict the returned rows.
            return isinstance(parent, (exp.Where, exp.Having)) and parent.parent in lineage

        periods = set()
        basis = bindings.get("date_basis") if "date_basis" in conditions else None
        for name, value in conditions.items():
            binding = bindings.get(name, name)
            applied = False
            if isinstance(binding, str):
                if name in ("start", "end"):
                    placeholders = [p for p in tree.find_all(exp.Placeholder) if p.name == binding]
                    observed = set()
                    for placeholder in placeholders:
                        predicate = placeholder.parent
                        operator = exp.GTE if name == "start" else exp.LT
                        physical = period_column(predicate.this) if isinstance(predicate, operator) else None
                        if (physical is None or predicate.expression is not placeholder
                                or physical[1] not in {"dateinvoiced", "dateordered", "dateacct", "movementdate", "datetrx"}
                                or not strict_filter(predicate) or plan["params"].get(binding) != value
                                or "date_basis" in conditions and (not isinstance(basis, dict) or basis.get("kind") != "column"
                                    or not period_matches(physical, basis.get("column")))):
                            raise PocError("CONDITION_NOT_APPLIED", f"확정 조건 {name}의 기간 열이 날짜 기준과 일치하지 않습니다.")
                        observed.add(physical)
                    periods.update(observed)
                    applied = bool(observed) and len(periods) == 1
                    if not applied:
                        raise PocError("CONDITION_NOT_APPLIED", f"확정 조건 {name}의 SQL 매개변수 적용 근거가 없습니다.")
                    continue
                for placeholder in tree.find_all(exp.Placeholder):
                    predicate = placeholder.parent
                    columns = [c for c in predicate.iter_expressions() if isinstance(c, exp.Column)]
                    semantic = {"client_id": {"ad_client_id"}, "tenant_id": {"ad_client_id"}, "tenant": {"ad_client_id"}, "테넌트": {"ad_client_id"}, "status": {"docstatus"}, "상태": {"docstatus"}, "start": {"dateinvoiced", "dateordered", "dateacct", "movementdate", "datetrx"}, "end": {"dateinvoiced", "dateordered", "dateacct", "movementdate", "datetrx"}, "currency": {"iso_code"}}.get(name, {name})
                    operators = (exp.GTE,) if name == "start" else (exp.LT,) if name == "end" else (exp.EQ,)
                    direction = isinstance(predicate, exp.EQ) or (columns and predicate.this is columns[0])
                    if placeholder.name == binding and isinstance(predicate, operators) and direction and len(columns) == 1 and columns[0].name in semantic and strict_filter(predicate) and plan["params"].get(binding) == value:
                        applied = True
            elif isinstance(binding, dict):
                kind, reference = binding.get("kind"), binding.get("column", "")
                if kind == "metadata":
                    field = binding.get("field")
                    applied = field in ("dataset_id", "dataset_label", "schema") and (catalog or {}).get(field) == value
                elif kind == "column":
                    # Date/metric labels are a closed host vocabulary, not model assertions.
                    vocabulary = {"dateinvoiced": {"청구일", "청구일 dateinvoiced"}, "dateordered": {"주문일", "주문일 dateordered"}, "dateacct": {"회계일"}, "totallines": {"문서 행 합계", "totallines 문서 행 합계"}, "grandtotal": {"문서 총액"}}
                    allowed = vocabulary.get(reference.split(".")[-1], set()) | {reference, reference.split(".")[-1]}
                    applied = value in allowed and any(column_matches(c, reference) and c.find_ancestor(exp.Select) in lineage for c in tree.find_all(exp.Column))
                    if name == "date_basis" and any(key in conditions for key in ("start", "end")):
                        applied = value in allowed and any(period_matches(period_column(c), reference) and c.find_ancestor(exp.Select) in lineage for c in tree.find_all(exp.Column))
                    if name == "date_basis" and inactive is not None:
                        applied = True
                elif kind == "predicate":
                    physical = {column["name"] for columns in (catalog or {}).get("tables", {}).values() for column in columns}
                    semantic = {"client_id": "ad_client_id", "tenant_id": "ad_client_id", "tenant": "ad_client_id", "status": "docstatus", "상태": "docstatus", "currency": "iso_code"}.get(name)
                    if name in physical | {"docstatus", "issotrx", "isactive", "isreceipt", "isdescription"}:
                        semantic = name
                    if semantic is not None and reference.split(".")[-1] != semantic:
                        raise PocError("CONDITION_NOT_APPLIED", f"확정 조건 {name}의 SQL 매개변수 적용 근거가 없습니다.")
                    for predicate in tree.find_all(exp.In, exp.EQ):
                        if not strict_filter(predicate) or not column_matches(predicate.this, reference):
                            continue
                        literals = predicate.expressions if isinstance(predicate, exp.In) else [predicate.expression]
                        observed = predicate_values(literals, plan.get("params", {}))
                        if observed is not None:
                            expected = re.split(r"\s*[,·|]\s*", str(value)) if isinstance(predicate, exp.In) else [str(value)]
                            applied = applied or sorted(observed) == sorted(expected)
            if not applied:
                raise PocError("CONDITION_NOT_APPLIED", f"확정 조건 {name}의 SQL 매개변수 적용 근거가 없습니다.")

    def validate_structure(self, sql):
        tree = sqlglot.parse_one(sql, read="postgres")
        schema = {"adempiere": {name: {column: "UNKNOWN" for column in columns} for name, columns in self.columns.items()}}
        try:
            qualified = qualify(tree.copy(), dialect="postgres", schema=schema, validate_qualify_columns=True, identify=False)
        except Exception:
            raise PocError("SQL_COLUMN_INVALID", "실제 스냅샷에 없는 열 또는 모호한 열 참조입니다.") from None
        used = {t.name for t in qualified.find_all(exp.Table) if t.name in self.columns}
        if not used:
            raise PocError("SCHEMA_SELECTION_INVALID")
        joins = []
        for scope in traverse_scope(qualified):
            physical = {alias: t.name for alias, t in scope.sources.items() if isinstance(t, exp.Table) and t.name in self.columns}
            source = scope.expression.args.get("from") or scope.expression.args.get("from_")
            previous = {source.this.alias_or_name} if source and isinstance(source.this, exp.Table) else set()
            for join in scope.expression.args.get("joins", []):
                target = join.this.alias_or_name
                on = join.args.get("on")
                if target not in physical or not on or join.args.get("kind") == "CROSS" or any(isinstance(n, (exp.Or, exp.Not)) for n in on.walk()):
                    raise PocError("JOIN_NOT_VERIFIED")
                pairs = set()
                for eq in on.find_all(exp.EQ):
                    ancestor = eq.parent
                    valid = eq is on
                    while ancestor:
                        if not isinstance(ancestor, (exp.And, exp.Paren)):
                            break
                        if ancestor is on:
                            valid = True
                            break
                        ancestor = ancestor.parent
                    a, b = eq.left, eq.right
                    if valid and isinstance(a, exp.Column) and isinstance(b, exp.Column) and a.table != b.table:
                        pairs.add((a.table, a.name, b.table, b.name))
                matched = []
                for prior in previous:
                    for left, right in ((target, prior), (prior, target)):
                        for fk in self.fks:
                            if physical.get(left) != fk["source_table"] or physical.get(right) != fk["target_table"]:
                                continue
                            forward = [(left, a, right, b) for a, b in zip(fk["source_columns"], fk["target_columns"])]
                            if forward and all(p in pairs or (p[2], p[3], p[0], p[1]) in pairs for p in forward):
                                matched.append({k: fk[k] for k in ("name", "source_table", "source_columns", "target_table", "target_columns")} | {"source_alias": left, "target_alias": right})
                if not matched:
                    raise PocError("JOIN_NOT_VERIFIED", "새 조인 별칭과 기존 별칭을 연결하는 완전한 실제 외래키가 없습니다.")
                joins.extend(matched)
                previous.add(target)
        return used, sorted(joins, key=lambda j: j["name"])
