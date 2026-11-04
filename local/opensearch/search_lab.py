"""DB 생성, 명시적 매핑, Bulk 적재, Dashboards 조회 화면 구성."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json

import httpx

from seed_data import BATCH, STATE, TABLES, dumps, export_rows, normalize, save, seed

BASE = "http://127.0.0.1:9200"
DASHBOARDS = "http://127.0.0.1:5601"
TEXT = {"type": "text", "analyzer": "kuromoji", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}}
REF_FIELDS = {"ad_client_id": "ad_client", "ad_org_id": "ad_org", "createdby": "ad_user", "updatedby": "ad_user",
              "c_uom_id": "c_uom", "m_product_category_id": "m_product_category", "c_taxcategory_id": "c_taxcategory",
              "salesrep_id": "ad_user", "c_campaign_id": "c_campaign"}


def request(method, path, *, body=None, raw=None, dashboards=False, allowed=(200, 201)):
    headers = {"osd-xsrf": "poc-local-search"} if dashboards else {}
    if raw is not None:
        headers["Content-Type"] = "application/x-ndjson"
    with httpx.Client(timeout=90, trust_env=False) as client:
        response = client.request(method, (DASHBOARDS if dashboards else BASE) + path,
                                  json=normalize(body) if body is not None else None, content=raw, headers=headers)
    if response.status_code not in allowed:
        raise RuntimeError(f"{method} {path}: HTTP {response.status_code}: {response.text[:1500]}")
    return response.json() if response.content else {}


def documents(rows, parents):
    parent_lookup = {t: {r[t + "_id"]: r["name"] for r in records} for t, records in parents.items()}
    result = {"product": [], "promotion": []}
    products = {r["m_product_id"]: r for r in rows["m_product"]}
    groups = {r["m_promotiongroup_id"]: r for r in rows["m_promotiongroup"]}
    promotions = {r["m_promotion_id"]: r for r in rows["m_promotion"]}
    product_links = {pk: [] for pk in products}
    promotion_links = {pk: [] for pk in promotions}
    for line in rows["m_promotionline"]:
        promo_id, group_id = line["m_promotion_id"], line["m_promotiongroup_id"]
        for member in rows["m_promotiongroupline"]:
            if member["m_promotiongroup_id"] != group_id:
                continue
            product_id = member["m_product_id"]
            relation = {"m_promotion_id": promo_id, "m_product_id": product_id,
                        "m_promotionline_id": line["m_promotionline_id"], "m_promotiongroup_id": group_id,
                        "m_promotiongroupline_id": member["m_promotiongroupline_id"], "group_name": groups[group_id]["name"]}
            promotion_links[promo_id].append({**relation, "name": products[product_id]["name"], "value": products[product_id]["value"]})
            product_links[product_id].append({**relation, "name": promotions[promo_id]["name"]})
    for entity, table, links, link_name in (("product", "m_product", product_links, "promotions"),
                                           ("promotion", "m_promotion", promotion_links, "products")):
        for row in rows[table]:
            refs = []
            for column, parent in REF_FIELDS.items():
                if row.get(column) is not None:
                    refs.append({"field": column, "table": parent, "id": row[column], "name": parent_lookup[parent][row[column]]})
            related = sorted(links[row[table + "_id"]], key=lambda x: x["m_promotiongroupline_id"])
            if not related:
                raise RuntimeError("상품/프로모션 연결 누락")
            result[entity].append({**row, "entity_type": entity, "seed_batch": BATCH, "parent_refs": refs,
                                   link_name: related, "related_count": len(related)})
    return normalize(result)


def mappings(entity, columns):
    properties = {}
    for column in columns:
        if column["table_name"] != "m_" + entity:
            continue
        name, typ = column["column_name"], column["data_type"]
        if typ == "numeric":
            field = {"type": "long" if column["numeric_scale"] == 0 else "double"}
        elif "timestamp" in typ or typ == "date":
            field = {"type": "date", "format": "strict_date_optional_time||yyyy-MM-dd'T'HH:mm:ss.SSSSSS"}
        elif name in ("name", "description", "help", "documentnote", "group1", "group2"):
            field = TEXT
        else:
            field = {"type": "keyword"}
        properties[name] = field
    relation = {k: {"type": "long"} for k in ("m_product_id", "m_promotion_id", "m_promotionline_id", "m_promotiongroup_id", "m_promotiongroupline_id")}
    relation.update({"name": TEXT, "group_name": TEXT, "value": {"type": "keyword"}})
    properties.update({"entity_type": {"type": "keyword"}, "seed_batch": {"type": "keyword"}, "related_count": {"type": "integer"},
        "parent_refs": {"type": "nested", "properties": {"field": {"type": "keyword"}, "table": {"type": "keyword"}, "id": {"type": "long"}, "name": TEXT}},
        "promotions" if entity == "product" else "products": {"type": "nested", "properties": relation}})
    return {"settings": {"number_of_shards": 1, "number_of_replicas": 0},
            "mappings": {"dynamic": "strict", "_meta": {"owner": BATCH, "schema_version": 1, "entity_type": entity}, "properties": properties}}


def bulk(entity, docs):
    payload = "".join(dumps({"index": {"_index": "poc-" + entity, "_id": str(doc["m_" + entity + "_id"])}}) + "\n" + dumps(doc) + "\n" for doc in docs)
    response = request("POST", "/_bulk?refresh=wait_for", raw=payload.encode())
    failures = [item for item in response.get("items", []) if next(iter(item.values())).get("status", 500) >= 300]
    if response.get("errors") or failures or len(response.get("items", [])) != len(docs):
        save(STATE / "bulk-failures.json", response)
        raise RuntimeError(f"Bulk 일부 실패: {len(failures)}건. 같은 명령으로 재적재할 수 있습니다.")
    return payload


def index_data():
    identity = request("GET", "/")
    if identity.get("cluster_name") != "poc-local-search" or identity["version"]["number"] != "3.9.0":
        raise RuntimeError("승인한 로컬 OpenSearch 3.9.0 클러스터가 아닙니다.")
    rows, parents, columns = export_rows()
    docs = documents(rows, parents)
    for entity, records in docs.items():
        index = "poc-" + entity
        spec = mappings(entity, columns)
        existing = request("GET", f"/{index}/_mapping", allowed=(200, 404))
        if index in existing:
            if existing[index]["mappings"] != spec["mappings"]:
                raise RuntimeError(f"기존 인덱스 소유권/매핑 불일치: {index}")
            hits = request("POST", f"/{index}/_search", body={"size": 1000, "track_total_hits": True, "query": {"match_all": {}}})["hits"]
            expected = {str(d["m_" + entity + "_id"]) for d in records}
            if hits["total"]["value"] > 200 or any(h["_id"] not in expected or h["_source"].get("seed_batch") != BATCH for h in hits["hits"]):
                raise RuntimeError(f"소유권이 다른 문서가 있습니다: {index}")
        else:
            request("PUT", f"/{index}", body=spec)
        save(STATE / f"export/{index}-mapping.json", spec)
        payload = bulk(entity, records)
        (STATE / f"export/{index}.ndjson").write_text(payload, encoding="utf-8", newline="\n")
    save(STATE / "export/documents.json", docs)
    return {"poc-" + e: len(r) for e, r in docs.items()}


def dashboards():
    for entity in ("product", "promotion"):
        index = "poc-" + entity
        fields = request("GET", f"/api/index_patterns/_fields_for_wildcard?pattern={index}", dashboards=True)["fields"]
        request("POST", f"/api/saved_objects/index-pattern/{index}?overwrite=true", dashboards=True,
                body={"attributes": {"title": index, "fields": json.dumps(fields)}})
        columns = ["name", "description", "related_count", "entity_type"]
        columns.insert(1, "value" if entity == "product" else "promotionpriority")
        source = {"indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index", "query": {"query": "", "language": "kuery"}, "filter": []}
        body = {"attributes": {"title": f"{entity.title()} — 日本語デモ200件", "description": "GardenWorld / " + BATCH,
                  "columns": columns, "sort": [["name.keyword", "asc"]], "kibanaSavedObjectMeta": {"searchSourceJSON": json.dumps(source)}},
                "references": [{"name": "kibanaSavedObjectMeta.searchSourceJSON.index", "type": "index-pattern", "id": index}]}
        request("POST", f"/api/saved_objects/search/{index}-view?overwrite=true", dashboards=True, body=body)
    return {e: f"{DASHBOARDS}/app/discover#/view/poc-{e}-view" for e in ("product", "promotion")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["seed", "index", "dashboards", "load"])
    action = parser.parse_args().action
    result = {"action": action, "started_at": datetime.now(timezone.utc).isoformat(), "status": "running"}
    save(STATE / "last-load.json", result)
    try:
        if action == "load":
            request("GET", "/api/status", dashboards=True)
        if action in ("seed", "load"):
            r = seed()
            result["database"] = {k: v for k, v in r.items() if k != "ids"}
            save(STATE / "last-load.json", result)
        if action in ("index", "load"):
            result["indexes"] = index_data()
            save(STATE / "last-load.json", result)
        if action in ("dashboards", "load"):
            result["views"] = dashboards()
        result["status"] = "PASS"
    except Exception as exc:
        result["status"] = "failed"
        result["error_type"] = type(exc).__name__
        save(STATE / "last-load.json", result)
        raise
    result["completed_at"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    save(STATE / "last-load.json", result)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, httpx.HTTPError) as exc:
        raise SystemExit(f"실패: {exc}") from None
