import json

import pytest

from poc.analysis_documents import Documents, sha
from poc.config import PocError
from poc.contracts import canonical, seal_plan


def make_documents(root, edges, extra=()):
    names = sorted(set(extra) | {name for edge in edges for name in edge})
    directory = root / "docs/database/idempiere"
    directory.mkdir(parents=True)
    files = {}
    for name in names:
        # All incoming/outgoing FK facts stay inside each selected source document.
        relations = [f"{child}.id -> {parent}.id" for child, parent in edges if name in (child, parent)]
        raw = (f"# {name}\nColumn id\n" + "\n".join(relations)).encode()
        (directory / f"{name}.md").write_bytes(raw)
        files[f"{name}.md"] = sha(raw)
    constraints = [{"kind": "f", "validated": True, "name": f"fk_{index}", "source_table": child,
        "source_columns": ["id"], "target_table": parent, "target_columns": ["id"]} for index, (child, parent) in enumerate(edges)]
    snapshot = root / ".local/datasets/idempiere/documentation-snapshot.json"
    snapshot.parent.mkdir(parents=True)
    snapshot.write_text(canonical({"columns": [{"table_name": name, "physical_name": "id", "data_type": "integer"} for name in names], "constraints": constraints}), encoding="utf-8")
    (directory / "manifest.json").write_text(canonical({"captured_at": "2026-11-03", "snapshot_sha256": sha(snapshot.read_bytes()),
        "table_paths": {name: f"{name}.md" for name in names}, "files": files}), encoding="utf-8")
    catalog = {"dataset_id": "idempiere", "schema_version": "fixture", "schema": "adempiere",
        "tables": {name: [{"name": "id", "type": "integer"}] for name in names}}
    return Documents(root), catalog


@pytest.fixture
def inventory(tmp_path):
    return make_documents(tmp_path, [("m_storageonhand", "m_locator"), ("m_locator", "m_warehouse"),
        ("m_warehouse", "third_hop"), ("unrelated_child", "m_locator")])


def test_candidates_only_keep_bidirectional_neighbors_and_source_fk_facts(inventory):
    documents, catalog = inventory
    context, receipt, selection = documents.read(["m_storageonhand"], catalog)
    assert selection["selected_tables"] == ["m_storageonhand"]
    assert selection["available_neighbors"] == ["m_locator", "m_warehouse", "unrelated_child"]
    assert selection["method"] == "host_document_read_with_explicit_bidirectional_fk_expansion"
    assert "m_storageonhand.id -> m_locator.id" in context["documents"][0]["content"]
    assert len(documents.fks) == 4 and context["relationships"] == []
    assert receipt["context_bytes"] == len(canonical(context["documents"]).encode())
    documents.verify_receipt(receipt)
    _, _, child_options = documents.read(["m_locator"], catalog)
    assert "m_storageonhand" in child_options["available_neighbors"]


def test_second_plan_document_request_can_expand_storage_locator_warehouse(inventory):
    documents, catalog = inventory
    first_context, first_receipt, first_selection = documents.read(["m_storageonhand"], catalog)
    # Exactly the additional_tables response supported by the final-plan call loop.
    model_request = {"additional_tables": ["m_locator", "m_warehouse"]}
    assert set(model_request["additional_tables"]).issubset(first_selection["available_neighbors"])
    context, receipt, selection = documents.read(first_selection["candidate_tables"], catalog, model_request["additional_tables"])
    assert selection["selected_tables"] == ["m_storageonhand", "m_locator", "m_warehouse"]
    assert "unrelated_child" not in selection["selected_tables"]
    assert {(fk["source_table"], fk["target_table"]) for fk in context["relationships"]} == {
        ("m_storageonhand", "m_locator"), ("m_locator", "m_warehouse")}
    assert [item["table"] for item in receipt["documents"]] == selection["selected_tables"]
    assert first_receipt["context_sha256"] != receipt["context_sha256"]
    assert len(first_context["documents"]) == 1
    documents.verify_receipt(first_receipt)
    documents.verify_receipt(receipt)


def test_unrequested_neighbor_is_not_read_but_explicit_request_checks_its_hash(inventory):
    documents, catalog = inventory
    (documents.directory / "m_locator.md").write_text("changed neighbor", encoding="utf-8")
    _, receipt, _ = documents.read(["m_storageonhand"], catalog)
    documents.verify_receipt(receipt)
    with pytest.raises(PocError, match="DOCUMENTATION_CHANGED"):
        documents.read(["m_storageonhand"], catalog, ["m_locator"])


@pytest.mark.parametrize("requested", [["third_hop"], ["missing"], {}, "m_locator"])
def test_explicit_expansion_stays_within_two_hops_and_list_contract(inventory, requested):
    documents, catalog = inventory
    with pytest.raises(PocError, match="DOCUMENT_EXPANSION_LIMIT"):
        documents.read(["m_storageonhand"], catalog, requested)


def test_candidate_twelve_and_combined_detail_thirty_two_limits(tmp_path):
    documents, catalog = make_documents(tmp_path, [(f"leaf{i}", "hub") for i in range(33)])
    with pytest.raises(PocError, match="SCHEMA_SELECTION_INVALID"):
        documents.read([f"leaf{i}" for i in range(13)], catalog)
    candidates = [f"leaf{i}" for i in range(12)]
    requested = [f"leaf{i}" for i in range(12, 32)]
    _, receipt, selection = documents.read(candidates, catalog, requested)
    assert len(selection["selected_tables"]) == 32
    assert "hub" in selection["available_neighbors"]  # traversal does not force reading it
    documents.verify_receipt(receipt)
    with pytest.raises(PocError, match="DOCUMENT_EXPANSION_LIMIT"):
        documents.read(candidates, catalog, [*requested, "leaf32"])


def test_explicit_required_document_still_has_exact_128kib_limit(inventory):
    documents, catalog = inventory
    path = documents.directory / "m_locator.md"
    path.write_text("required facts" * 20000, encoding="utf-8")
    manifest_path = documents.directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"]["m_locator.md"] = sha(path.read_bytes())
    manifest_path.write_text(canonical(manifest), encoding="utf-8")
    documents = Documents(documents.root)
    documents.read(["m_storageonhand"], catalog)
    with pytest.raises(PocError, match="DOCUMENT_CONTEXT_LIMIT"):
        documents.read(["m_storageonhand"], catalog, ["m_locator"])


def test_sql_cannot_use_a_reachable_but_unread_table(inventory):
    documents, catalog = inventory
    _, receipt, selection = documents.read(["m_storageonhand"], catalog)
    plan = seal_plan({"contract_version": 2, "schema_version": catalog["schema_version"], "document_evidence": receipt,
        "confirmed_conditions": {}, "schema_selection": selection, "sql": "SELECT id FROM adempiere.m_warehouse", "params": {}, "joins": []})
    with pytest.raises(PocError, match="SQL_REJECTED"):
        documents.verify_plan(plan, catalog, {})
