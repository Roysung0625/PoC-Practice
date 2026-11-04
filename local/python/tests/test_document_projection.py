"""Actual Markdown evidence stays complete while redundant presentation is removed."""
import copy
import json
from pathlib import Path
import re

import pytest

from poc.analysis_documents import DOCUMENT_PROJECTION_VERSION, Documents, project_document, sha
from poc.config import PocError
from poc.contracts import canonical


SOURCE = """# child — 자식 업무명

[전체 일람](TABLE_INDEX.md)

## 기본 정보
| 물리명 | `adempiere.child` |
| 한국어 논리명 | 자식 업무명 |

## 열 목록
| 물리명 | 원본 논리명 | PostgreSQL 타입 | 설명 |
| `parent_id` | Parent document | numeric(10,0) | 부모 문서 식별자 |
| `amount` | Document amount | numeric | 세금 포함 여부를 확인할 금액 |

## 외래키 흐름
화살표는 자식 → 부모입니다.
```mermaid
flowchart LR
    n0["child"]
    n1["parent"]
    n0 -->|"parent_id → parent_id"| n1
```

### 나가는 FK
| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `parent_fk` <!-- FK_OUT: adempiere.child.parent_fk --> | [`child`](child.md) | `parent_id` | [`parent`](parent.md) | `parent_id` | NO ACTION / NO ACTION | 완료 / 가능 |

### 들어오는 FK
| `line_fk` <!-- FK_IN: adempiere.line.line_fk --> | [`line`](line.md) | `child_id` | [`child`](child.md) | `child_id` | CASCADE / NO ACTION | 완료 / 가능 |

## 조회 시 주의
- 조인으로 금액이 중복되지 않도록 집계 단위를 확인합니다.
<!-- business warning: keep this non-FK comment -->
"""


@pytest.fixture
def document_fixture(tmp_path):
    directory = tmp_path / "docs/database/idempiere"
    directory.mkdir(parents=True)
    (directory / "child.md").write_text(SOURCE, encoding="utf-8")
    snapshot = tmp_path / ".local/datasets/idempiere/documentation-snapshot.json"
    snapshot.parent.mkdir(parents=True)
    snapshot.write_text(canonical({"columns": [{"table_name": "child", "physical_name": "parent_id", "data_type": "numeric"}], "constraints": []}), encoding="utf-8")
    manifest = {"snapshot_sha256": sha(snapshot.read_bytes()), "captured_at": "2026-11-03", "table_paths": {"child": "child.md"}, "files": {"child.md": sha((directory / "child.md").read_bytes())}}
    (directory / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    return Documents(tmp_path), {"tables": {"child": [{"name": "parent_id", "type": "numeric"}]}}, directory


def test_projection_retains_column_meanings_all_fk_rows_and_business_warnings():
    projected = project_document(SOURCE)
    assert "```mermaid" not in projected
    assert "FK_OUT:" not in projected and "FK_IN:" not in projected
    assert "(parent.md)" not in projected
    for fact in ("자식 업무명", "adempiere.child", "Parent document", "numeric(10,0)", "부모 문서 식별자", "세금 포함 여부를 확인할 금액", "parent_fk", "line_fk", "`line`", "`parent`", "CASCADE / NO ACTION", "완료 / 가능", "집계 단위를 확인", "business warning: keep"):
        assert fact in projected
    assert project_document(SOURCE) == projected


def test_unique_or_unrecognized_diagram_is_not_removed():
    unique = SOURCE.replace('n0 -->|"parent_id → parent_id"| n1', 'n0 -->|"amount → parent_id"| n1')
    assert "```mermaid" in project_document(unique)
    extra_fact = SOURCE.replace('flowchart LR', 'flowchart LR\n    note["유일한 업무 설명"]')
    assert 'note["유일한 업무 설명"]' in project_document(extra_fact)


def test_read_receipt_hashes_source_and_exact_delivered_projection(document_fixture):
    documents, catalog, directory = document_fixture
    before = (directory / "child.md").read_bytes()
    context, receipt, selection = documents.read(["child"], catalog)
    delivered = canonical(context["documents"]).encode()
    assert receipt["projection_version"] == DOCUMENT_PROJECTION_VERSION
    assert receipt["context_sha256"] == sha(delivered)
    assert receipt["context_bytes"] == len(delivered)
    assert context["documents"][0]["sha256"] == sha(before)
    assert context["documents"][0]["content"] == project_document(before.decode())
    assert (directory / "child.md").read_bytes() == before
    assert selection["max_hops"] == 2
    documents.verify_receipt(receipt)


@pytest.mark.parametrize("field,value", [("context_sha256", "0" * 64), ("context_bytes", 1), ("projection_version", "unknown-version")])
def test_tampered_projected_receipt_is_rejected(document_fixture, field, value):
    documents, catalog, _ = document_fixture
    _, receipt, _ = documents.read(["child"], catalog)
    receipt[field] = value
    with pytest.raises(PocError):
        documents.verify_receipt(receipt)


def test_original_source_change_even_in_removed_anchor_is_rejected(document_fixture):
    documents, catalog, directory = document_fixture
    _, receipt, _ = documents.read(["child"], catalog)
    path = directory / "child.md"
    path.write_text(SOURCE.replace("FK_OUT: adempiere.child.parent_fk", "FK_OUT: changed_anchor"), encoding="utf-8")
    with pytest.raises(PocError, match="DOCUMENTATION_CHANGED"):
        documents.verify_receipt(receipt)
    with pytest.raises(PocError, match="DOCUMENTATION_CHANGED"):
        documents.read(["child"], catalog)


def test_receipt_without_projection_version_verifies_original_full_content(document_fixture):
    documents, catalog, directory = document_fixture
    _, receipt, _ = documents.read(["child"], catalog)
    del receipt["projection_version"]
    original_docs = [{**item, "content": (directory / item["path"]).read_bytes().decode("utf-8-sig")} for item in receipt["documents"]]
    receipt["context_sha256"] = sha(canonical(original_docs).encode())
    receipt["context_bytes"] = sum(len(canonical(item).encode()) for item in original_docs)
    documents.verify_receipt(receipt)
    projected = copy.deepcopy(receipt)
    projected["projection_version"] = DOCUMENT_PROJECTION_VERSION
    with pytest.raises(PocError, match="DOCUMENT_RECEIPT_MISMATCH"):
        documents.verify_receipt(projected)


def test_context_limit_remains_128_kib_and_candidate_limit_twelve(document_fixture):
    documents, catalog, directory = document_fixture
    with pytest.raises(PocError, match="SCHEMA_SELECTION_INVALID"):
        documents.read([f"t{i}" for i in range(13)], catalog)
    path = directory / "child.md"
    path.write_text(SOURCE + "업무 의미 보존" * 20000, encoding="utf-8")
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["files"]["child.md"] = sha(path.read_bytes())
    manifest_path.write_text(canonical(manifest), encoding="utf-8")
    documents = Documents(documents.root)
    with pytest.raises(PocError, match="DOCUMENT_CONTEXT_LIMIT"):
        documents.read(["child"], catalog)


REAL_GROUPS = {
    "ERP03_required_plus_possible_line": ["c_invoice", "c_bpartner", "c_currency", "c_doctype", "c_invoiceline"],
    "ERP05_required": ["c_invoice", "c_invoiceline", "m_product", "c_currency", "c_doctype"],
    "ERP05_required_plus_possible_uom": ["c_invoice", "c_invoiceline", "m_product", "c_currency", "c_doctype", "c_uom"],
}


@pytest.mark.parametrize("group,names", REAL_GROUPS.items())
def test_actual_erp_documents_fit_without_dropping_fact_rows(group, names):
    # These are question/independent-SQL requirements plus stated possibilities,
    # not an assertion about the unavailable failed-run model selection response.
    directory = Path(__file__).resolve().parents[3] / "docs/database/idempiere"
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8-sig"))
    original_docs, projected_docs, comments_diagrams_only = [], [], []
    for name in names:
        relative = manifest["table_paths"][name]
        raw = (directory / relative).read_bytes()
        assert sha(raw) == manifest["files"][relative]
        source = raw.decode("utf-8-sig")
        projected = project_document(source)
        assert "```mermaid" not in projected  # every actual diagram was proven redundant
        # Every Markdown table row remains: column names/logical labels/types,
        # all outgoing/incoming FK rows, constraints and metadata are preserved.
        source_rows = [line for line in source.splitlines() if line.startswith("|")]
        projected_rows = [line for line in projected.splitlines() if line.startswith("|")]
        assert len(projected_rows) == len(source_rows)
        for before, after in zip(source_rows, projected_rows):
            before_display = re.sub(r"<!--[ \t]*FK_(?:OUT|IN):[^\r\n>]*-->", "", before)
            before_display = re.sub(r"(?<!!)\[([^\]\r\n]+)\]\([^\)\r\n]*\)", r"\1", before_display)
            assert before_display == after
        assert source[source.index("## 조회 시 주의"):].strip() == projected[projected.index("## 조회 시 주의"):].strip()
        item = {"table": name, "path": relative, "sha256": sha(raw)}
        original_docs.append({**item, "content": source})
        projected_docs.append({**item, "content": projected})
        compact = re.sub(r"<!--[ \t]*FK_(?:OUT|IN):[^\r\n>]*-->", "", source)
        compact = re.sub(r"```mermaid\n.*?```\n", "", compact, flags=re.S)
        comments_diagrams_only.append({**item, "content": re.sub(r"\n{3,}", "\n\n", compact)})
    sizes = {"raw": len(canonical(original_docs).encode()), "comments_mermaid_only": len(canonical(comments_diagrams_only).encode()), "projection": len(canonical(projected_docs).encode())}
    print(group, json.dumps(sizes))
    assert sizes["projection"] < sizes["raw"]
    assert sizes["projection"] <= 131072
