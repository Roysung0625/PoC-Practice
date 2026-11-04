"""Offline proof of generic model guidance against the unchanged SQL validators."""
import pytest
from sqlglot.executor import execute

from poc.analysis_documents import Documents, HOST_SQL_STRUCTURE_CONSTRAINTS, sha
from poc.config import PocError
from poc.contracts import canonical, seal_plan


@pytest.fixture
def fixture(tmp_path, request):
    columns = {
        "doc_header": ("document_id", "ad_client_id", "amount", "unit_id"),
        "doc_detail": ("detail_id", "document_id", "ad_client_id", "product_id"),
        "money_unit": ("unit_id", "unit_code"),
    }
    fks = [
        {"kind": "f", "validated": True, "name": "detail_header_fk", "source_table": "doc_detail",
         "source_columns": ["document_id"], "target_table": "doc_header", "target_columns": ["document_id"]},
        {"kind": "f", "validated": True, "name": "header_unit_fk", "source_table": "doc_header",
         "source_columns": ["unit_id"], "target_table": "money_unit", "target_columns": ["unit_id"]},
    ]
    if getattr(request, "param", False):
        fks[0]["source_columns"] = ["document_id", "ad_client_id"]
        fks[0]["target_columns"] = ["document_id", "ad_client_id"]
    directory = tmp_path / "docs/database/idempiere"
    directory.mkdir(parents=True)
    files = {}
    for name, names in columns.items():
        path = directory / f"{name}.md"
        path.write_text(f"# {name}\nColumns: {','.join(names)}", encoding="utf-8")
        files[path.name] = sha(path.read_bytes())
    snapshot = tmp_path / ".local/datasets/idempiere/documentation-snapshot.json"
    snapshot.parent.mkdir(parents=True)
    snapshot.write_text(canonical({"columns": [{"table_name": table, "physical_name": name,
        "data_type": "text" if name == "unit_code" else "numeric"} for table, names in columns.items() for name in names],
        "constraints": fks}), encoding="utf-8")
    (directory / "manifest.json").write_text(canonical({"captured_at": "offline-fixture", "snapshot_sha256": sha(snapshot.read_bytes()),
        "table_paths": {name: f"{name}.md" for name in columns}, "files": files}), encoding="utf-8")
    catalog = {"dataset_id": "idempiere", "schema": "adempiere", "schema_version": "fixture-v1", "tenant": {"ad_client_id": 7},
        "tables": {table: [{"name": name, "type": "text" if name == "unit_code" else "numeric"} for name in names] for table, names in columns.items()}}
    documents = Documents(tmp_path)
    context, receipt, selection = documents.read(list(columns), catalog)
    return documents, catalog, context, receipt, selection


def deduplicated_sql(method="distinct"):
    # Generic synthetic relation names; this SQL is never sent to a model.
    distinct = "DISTINCT " if method == "distinct" else ""
    grouping = " GROUP BY h.document_id,h.amount,u.unit_code" if method == "group_by" else ""
    return f"""WITH eligible_documents AS (
        SELECT {distinct}h.document_id,h.amount,u.unit_code
        FROM adempiere.doc_header h
        JOIN adempiere.doc_detail d ON d.document_id=h.document_id AND d.ad_client_id=h.ad_client_id
        JOIN adempiere.money_unit u ON u.unit_id=h.unit_id
        WHERE h.ad_client_id=7 AND d.ad_client_id=7 AND d.product_id IS NOT NULL{grouping}
    ) SELECT unit_code,SUM(amount) AS total_amount,COUNT(*) AS document_count
      FROM eligible_documents GROUP BY unit_code"""


def verify(fixture, sql):
    documents, catalog, _, receipt, selection = fixture
    _, joins = documents.validate_structure(sql)
    conditions = {"client_id": 7}
    plan = seal_plan({"contract_version": 2, "schema_version": catalog["schema_version"],
        "confirmed_conditions": conditions, "document_evidence": receipt, "schema_selection": selection,
        "sql": sql, "params": {}, "joins": joins,
        "condition_bindings": {"client_id": {"kind": "predicate", "column": "doc_header.ad_client_id"}}})
    documents.verify_plan(plan, catalog, conditions)


def synthetic_tables():
    return {"adempiere": {
        "doc_header": [
            {"document_id": 1, "ad_client_id": 7, "amount": 10, "unit_id": 1},
            {"document_id": 2, "ad_client_id": 7, "amount": 20, "unit_id": 1},
            {"document_id": 3, "ad_client_id": 8, "amount": 999, "unit_id": 1},
            {"document_id": 4, "ad_client_id": 7, "amount": 40, "unit_id": 1},
            {"document_id": 5, "ad_client_id": 7, "amount": 50, "unit_id": 1},
        ],
        "doc_detail": [
            {"detail_id": 1, "document_id": 1, "ad_client_id": 7, "product_id": 100},
            {"detail_id": 2, "document_id": 1, "ad_client_id": 7, "product_id": 101},
            {"detail_id": 3, "document_id": 2, "ad_client_id": 7, "product_id": 102},
            {"detail_id": 4, "document_id": 3, "ad_client_id": 8, "product_id": 103},
            {"detail_id": 5, "document_id": 4, "ad_client_id": 7, "product_id": None},
            {"detail_id": 6, "document_id": 5, "ad_client_id": 8, "product_id": 104},
        ],
        "money_unit": [{"unit_id": 1, "unit_code": "TEST_UNIT"}],
    }}


def test_context_delivers_host_owned_generic_guidance_without_question_or_result_data(fixture):
    documents, catalog, context, _, _ = fixture
    guidance = context["host_sql_structure_constraints"]
    assert tuple(guidance) == HOST_SQL_STRUCTURE_CONSTRAINTS
    joined = " ".join(guidance)
    for term in ("EXISTS", "스칼라", "단일 소스", "DISTINCT", "GROUP BY", "전체 열", "테넌트"):
        assert term in joined
    assert not any(table in joined for table in catalog["tables"])
    # The caller's catalog cannot replace host rules, and one context cannot mutate another.
    guidance.append("caller modification")
    poisoned_catalog = {**catalog, "host_sql_structure_constraints": ["caller override"]}
    next_context, _, _ = documents.read(list(catalog["tables"]), poisoned_catalog)
    assert tuple(next_context["host_sql_structure_constraints"]) == HOST_SQL_STRUCTURE_CONSTRAINTS


@pytest.mark.parametrize("method", ["distinct", "group_by"])
def test_header_dedup_cte_is_approved_and_handles_duplicate_details_without_database(fixture, method):
    sql = deduplicated_sql(method)
    verify(fixture, sql)
    # SQLGlot's pure Python executor runs fabricated dictionaries, with no DB/network.
    result = execute(sql, dialect="postgres", tables=synthetic_tables())
    assert result.columns == ("unit_code", "total_amount", "document_count")
    assert list(result.rows) == [("TEST_UNIT", 30, 2)]


def test_dedup_guidance_is_needed_even_when_unduplicated_join_is_structurally_valid(fixture):
    sql = deduplicated_sql("none")
    verify(fixture, sql)
    # Structural acceptance alone does not prove correct aggregation grain.
    result = execute(sql, dialect="postgres", tables=synthetic_tables())
    assert list(result.rows) == [("TEST_UNIT", 40, 3)]


@pytest.mark.parametrize("sql,code", [
    ("SELECT COUNT(*) FROM adempiere.doc_header h WHERE h.ad_client_id=7 AND EXISTS (SELECT 1 FROM adempiere.doc_detail d WHERE d.document_id=h.document_id AND d.ad_client_id=h.ad_client_id)", "SQL_REJECTED"),
    ("SELECT COUNT(*),(SELECT MAX(amount) FROM adempiere.doc_header) FROM adempiere.doc_header h WHERE h.ad_client_id=7", "CONDITION_NOT_APPLIED"),
    ("SELECT COUNT(*) FROM adempiere.doc_header h WHERE h.ad_client_id=7 AND h.document_id IN (SELECT document_id FROM adempiere.doc_detail)", "CONDITION_NOT_APPLIED"),
    ("WITH unused AS (SELECT document_id FROM adempiere.doc_header h WHERE h.ad_client_id=7) SELECT COUNT(*) FROM adempiere.doc_header", "CONDITION_NOT_APPLIED"),
    ("WITH q AS (SELECT h.document_id,h.amount,h.unit_id FROM adempiere.doc_header h WHERE h.ad_client_id=7) SELECT u.unit_code,SUM(q.amount) FROM q JOIN adempiere.money_unit u ON q.unit_id=u.unit_id GROUP BY u.unit_code", "JOIN_NOT_VERIFIED"),
])
def test_documented_unsupported_shapes_still_fail_existing_verifiers(fixture, sql, code):
    with pytest.raises(PocError, match=code):
        verify(fixture, sql)


@pytest.mark.parametrize("fixture", [True], indirect=True)
def test_all_composite_fk_columns_are_required_inside_cte(fixture):
    verify(fixture, deduplicated_sql())
    sql = deduplicated_sql().replace(" AND d.ad_client_id=h.ad_client_id", "")
    with pytest.raises(PocError, match="JOIN_NOT_VERIFIED"):
        verify(fixture, sql)
