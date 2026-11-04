"""실제 DB·OpenSearch·Dashboards를 대조한다. --faults는 의도한 실패/복구 시험."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json

import psycopg
from psycopg import sql

from seed_data import BATCH, STATE, TABLES, baseline, connect, export_rows, normalize, row_uuid, save, uuids
from search_lab import bulk, documents, request


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def fault_checks(docs):
    trial_ids = [-720031108, -720031109]
    with connect() as db:
        check(db.execute("SELECT count(*) AS n FROM adempiere.m_promotion WHERE m_promotion_id=ANY(%s)", [trial_ids]).fetchone()["n"] == 0, "실패 시험 ID 충돌")
        check(db.execute("SELECT count(*) AS n FROM adempiere.c_campaign WHERE c_campaign_id=-720031109").fetchone()["n"] == 0, "실패 시험 부모 ID 충돌")
    failed = False
    try:
        with connect(write=True) as db:
            for i, pk in enumerate(trial_ids):
                db.execute("""INSERT INTO adempiere.m_promotion
                  (m_promotion_id,ad_client_id,ad_org_id,createdby,updatedby,name,c_campaign_id,m_promotion_uu)
                  VALUES (%s,11,11,101,101,'ROLLBACK TEST',%s,%s)""",
                  [pk, 101 if i == 0 else -720031109, row_uuid("fault-test", i)])
            db.execute("SET CONSTRAINTS ALL IMMEDIATE")
    except psycopg.errors.ForeignKeyViolation:
        failed = True
    check(failed, "잘못된 FK가 실패하지 않음")
    with connect() as db:
        check(db.execute("SELECT count(*) AS n FROM adempiere.m_promotion WHERE m_promotion_id=ANY(%s)", [trial_ids]).fetchone()["n"] == 0, "실패 트랜잭션 일부 커밋됨")
    good = docs["product"][:2]
    invalid = {**good[1], "weight": "INVALID_DOUBLE_FOR_FAILURE_TEST"}
    failed = False
    try:
        bulk("product", [good[0], invalid])
    except RuntimeError as exc:
        check("Bulk 일부 실패" in str(exc), "예상과 다른 Bulk 실패")
        failed = True
    check(failed, "잘못된 매핑 문서가 실패하지 않음")
    response = json.loads((STATE / "bulk-failures.json").read_text(encoding="utf-8"))
    statuses = [next(iter(item.values()))["status"] for item in response["items"]]
    check(statuses[0] == 200 and statuses[1] == 400, f"예상하지 않은 Bulk 결과: {statuses}")
    bulk("product", good)
    return {"foreign_key_transaction_rollback": "PASS", "bulk_partial_failure_statuses": statuses, "bulk_recovery": "PASS"}


def verify(faults=False):
    rows, parents, columns = export_rows()
    docs = documents(rows, parents)
    report = {"verified_at": datetime.now(timezone.utc).isoformat(), "batch": BATCH, "checks": {}, "not_run": ["AWS", "vector_search", "chatbot_integration", "unattended_boot_recovery"]}
    checks = report["checks"]
    if faults:
        checks["failure_recovery"] = fault_checks(docs)
    with connect() as db:
        check(baseline(db) == json.loads((STATE / "baseline.json").read_text(encoding="utf-8")), "기존 데이터 변경")
        checks["original_rows_and_parents_unchanged"] = "PASS"
        totals = {}
        for table in TABLES:
            totals[table] = db.execute(sql.SQL("SELECT count(*) AS n FROM adempiere.{}").format(sql.Identifier(table))).fetchone()["n"]
        checks["database_total_counts"] = totals
        check(totals["m_product"] == 255 and totals["m_promotion"] == 200, "원본/더미 행 수 불일치")
        constraints = db.execute("""SELECT c.relname AS child, p.relname AS parent, co.conname,
          array(SELECT a.attname FROM unnest(co.conkey) WITH ORDINALITY k(attnum,ord) JOIN pg_attribute a ON a.attrelid=co.conrelid AND a.attnum=k.attnum ORDER BY k.ord) AS child_columns,
          array(SELECT a.attname FROM unnest(co.confkey) WITH ORDINALITY k(attnum,ord) JOIN pg_attribute a ON a.attrelid=co.confrelid AND a.attnum=k.attnum ORDER BY k.ord) AS parent_columns
          FROM pg_constraint co JOIN pg_class c ON c.oid=co.conrelid JOIN pg_class p ON p.oid=co.confrelid
          JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND co.contype='f' AND c.relname=ANY(%s)""", [list(TABLES)]).fetchall()
        for fk in constraints:
            joins = sql.SQL(" AND ").join(sql.SQL("s.{} = p.{}").format(sql.Identifier(a),sql.Identifier(b)) for a,b in zip(fk["child_columns"],fk["parent_columns"]))
            nonnull = sql.SQL(" AND ").join(sql.SQL("s.{} IS NOT NULL").format(sql.Identifier(c)) for c in fk["child_columns"])
            q = sql.SQL("SELECT count(*) AS n FROM adempiere.{} s WHERE s.{}=ANY(%s) AND {} AND NOT EXISTS(SELECT 1 FROM adempiere.{} p WHERE {})").format(
                sql.Identifier(fk["child"]),sql.Identifier(fk["child"]+"_uu"),nonnull,sql.Identifier(fk["parent"]),joins)
            check(db.execute(q,[uuids(fk["child"])]).fetchone()["n"] == 0, "고아 FK: " + fk["conname"])
        checks["foreign_keys"] = {"checked": len(constraints), "orphans": 0}
        links = db.execute("""SELECT p.m_promotion_id,l.m_promotionline_id,g.m_promotiongroup_id,gl.m_promotiongroupline_id,pr.m_product_id
          FROM adempiere.m_promotion p JOIN adempiere.m_promotionline l ON l.m_promotion_id=p.m_promotion_id
          JOIN adempiere.m_promotiongroup g ON g.m_promotiongroup_id=l.m_promotiongroup_id
          JOIN adempiere.m_promotiongroupline gl ON gl.m_promotiongroup_id=g.m_promotiongroup_id
          JOIN adempiere.m_product pr ON pr.m_product_id=gl.m_product_id
          WHERE p.m_promotion_uu=ANY(%s) ORDER BY gl.m_promotiongroupline_id""",[uuids("m_promotion")]).fetchall()
        readonly = db.execute("SHOW transaction_read_only").fetchone()["transaction_read_only"]
        can_insert = db.execute("SELECT has_table_privilege(current_user,'adempiere.m_product','INSERT') AS allowed").fetchone()["allowed"]
        check(readonly == "on" and not can_insert, "앱 읽기 전용 권한 변경")
        checks["app_reader_read_only"] = "PASS"
    check(len(links) == 600, "SQL 연결 수 불일치")
    link_keys = list(links[0])
    sql_edges = {tuple(int(r[k]) for k in link_keys) for r in links}
    actual = {}
    for entity in ("product", "promotion"):
        index = "poc-" + entity
        check(request("GET", f"/{index}/_count")["count"] == 200, index + " 개수 불일치")
        hits = request("POST", f"/{index}/_search", body={"size": 500, "track_total_hits": True, "query": {"match_all": {}}})["hits"]
        expected = {str(r["m_"+entity+"_id"]): r for r in docs[entity]}
        actual[entity] = {h["_id"]: h["_source"] for h in hits["hits"]}
        check(actual[entity] == expected, f"{index}: 전체 ID/원본 열/참조/관계 불일치")
        relation = "promotions" if entity == "product" else "products"
        indexed_edges = {tuple(int(r[k]) for k in link_keys) for d in actual[entity].values() for r in d[relation]}
        check(indexed_edges == sql_edges, "독립 SQL JOIN과 색인 관계 불일치")
        checks[index] = {"documents": 200, "all_source_columns_equal": "PASS", "sql_relation_edges": len(indexed_edges)}
        view = request("GET", f"/api/saved_objects/search/{index}-view", dashboards=True)
        pattern = request("GET", f"/api/saved_objects/index-pattern/{index}", dashboards=True)
        check(pattern["attributes"]["title"] == index and not pattern["attributes"].get("timeFieldName"), "인덱스/시간 필터 불일치")
        fields = {f["name"]: f for f in json.loads(pattern["attributes"]["fields"])}
        check(fields["name"]["type"] == "string" and fields["m_"+entity+"_id"]["type"] == "number", "Dashboards 필드 타입 누락")
        check(view["references"][0]["id"] == index, "조회 화면 참조 불일치")
    # 생성 함수가 아닌 실제 SQL 원본의 검색어 포함 집합을 기대값으로 쓴다.
    for entity, word in (("product", "ジョウロ"), ("promotion", "園芸工具")):
        table = "m_" + entity
        expected_ids = {str(r[table+"_id"]) for r in rows[table] if word in (r["name"] or "")}
        response = request("POST", f"/poc-{entity}/_search", body={"size": 500, "query": {"match": {"name": word}}})
        check({h["_id"] for h in response["hits"]["hits"]} == expected_ids, "일본어 검색 결과 불일치: " + word)
        checks["japanese_search_"+entity] = {"query": word, "hits": len(expected_ids)}
    for entity, path, target_col in (("promotion", "products", "m_product_id"), ("product", "promotions", "m_promotion_id")):
        target = int(links[0][target_col])
        own_col = "m_"+entity+"_id"
        expected = {str(int(r[own_col])) for r in links if int(r[target_col]) == target}
        response = request("POST", f"/poc-{entity}/_search", body={"size": 500,"query": {"nested": {"path": path,"query": {"term": {path+"."+target_col: target}}}}})
        check({h["_id"] for h in response["hits"]["hits"]} == expected, "nested 관계 조회 불일치")
        checks["nested_"+entity] = "PASS"
    # 다른 객체의 ID와 이름을 조합하면 일치하지 않아야 한다.
    sample = next(r for r in docs["promotion"] if len(r["products"]) >= 2)
    first, second = sample["products"][:2]
    wrong = request("POST", "/poc-promotion/_search", body={"query": {"bool": {"filter": [
        {"term": {"m_promotion_id": sample["m_promotion_id"]}},
        {"nested": {"path": "products", "query": {"bool": {"filter": [
          {"term": {"products.m_product_id": first["m_product_id"]}}, {"term": {"products.name.keyword": second["name"]}}]}}}}
    ]}}})
    check(wrong["hits"]["total"]["value"] == 0, "nested 객체 사이 조건 혼합")
    checks["nested_cross_object_rejected"] = "PASS"
    nodes = request("GET", "/_nodes/http,transport,jvm,plugins")
    for node in nodes["nodes"].values():
        check(node["jvm"]["mem"]["heap_max_in_bytes"] == 1024**3, "JVM 힙 불일치")
        check(any(p["name"] == "analysis-kuromoji" for p in node["plugins"]), "Kuromoji 누락")
        for endpoint in ("http", "transport"):
            check(all(a.startswith("127.0.0.1:") for a in node[endpoint]["bound_address"]), "외부 바인딩 탐지")
    checks["opensearch_loopback_heap_plugin"] = "PASS"
    checks["dashboards_saved_views"] = "PASS"
    report["status"] = "PASS"
    save(STATE / ("verification-faults.json" if faults else "verification.json"), report)
    print(json.dumps(normalize(report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--faults", action="store_true")
    verify(parser.parse_args().faults)
