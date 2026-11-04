"""큰 ERP 카탈로그를 테이블 선택 단계와 SQL 계획 단계로 나눈다."""
from .config import PocError

IDEMPIERE_INVOICE_RULE = "c_invoice.totallines는 문서 행 합계이며 세금 포함 가격 설정에 따라 세전액과 다를 수 있습니다. grandtotal은 문서 총액입니다. c_doctype.docbasetype='ARC'인 판매 대변전표는 차감합니다."
_LEGACY_INVOICE_RULE = "c_invoice.totallines는 세전 청구액, grandtotal은 세금 포함 총액입니다. c_doctype.docbasetype='ARC'인 판매 대변전표는 차감합니다."


def normalized_catalog(catalog):
    """Correct a known stale interpretation in memory without rewriting schema identity."""
    if catalog.get("dataset_id") != "idempiere":
        return catalog
    return {**catalog, "business_rules": [IDEMPIERE_INVOICE_RULE if rule == _LEGACY_INVOICE_RULE else rule for rule in catalog.get("business_rules", [])]}


def table_index(catalog):
    catalog = normalized_catalog(catalog)
    return {"dataset_id": catalog["dataset_id"], "dataset_label": catalog["dataset_label"],
            "business_rules": catalog["business_rules"], "tenant": catalog["tenant"],
            "tables": {name: {"label": meta["label"], "description": meta["description"][:120], "rows": meta["rows"]}
                       for name, meta in catalog["table_details"].items()}}


def selected_catalog(catalog, names):
    catalog = normalized_catalog(catalog)
    if not isinstance(names, list) or not 1 <= len(names) <= 12 or any(not isinstance(n, str) or n not in catalog["tables"] for n in names):
        raise PocError("SCHEMA_SELECTION_INVALID", "질문에 필요한 실제 테이블을 선택하지 못했습니다.")
    selected = list(dict.fromkeys(names))
    for child, columns, parent, _ in catalog["relationships"]:
        if child in names and parent not in selected and parent in catalog["tables"] and columns not in ("createdby", "updatedby", "ad_client_id", "ad_org_id") and len(selected) < 32:
            selected.append(parent)
    return {k: v for k, v in catalog.items() if k not in ("tables", "relationships", "table_details")} | {
        "tables": {name: [{"name": c["name"], "type": c["type"]} for c in catalog["tables"][name]] for name in selected},
        "table_details": {name: catalog["table_details"][name] for name in selected},
        "relationships": [r for r in catalog["relationships"] if r[0] in selected and r[2] in selected],
        "selection": {"total_tables": len(catalog["tables"]), "selected_tables": selected,
                      "method": "DeepSeek table selection + one-hop foreign-key parents; no embedding index"}}
