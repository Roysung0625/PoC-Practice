"""GardenWorld 일본어 더미. 기존 행 수정 없이 단일 트랜잭션으로 생성한다."""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from uuid import UUID, uuid5

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".local/opensearch"
BATCH = "poc-search-ja-v1"
NAMESPACE = UUID("61224784-1642-4c84-9be9-35de7e2efb31")
TABLES = {"m_product": 200, "m_promotion": 200, "m_promotiongroup": 200,
          "m_promotionline": 200, "m_promotiongroupline": 600}
PARENTS = {"ad_client": [11], "ad_org": [11], "ad_user": [101, 103], "c_campaign": [101, 102],
           "c_uom": [100], "c_taxcategory": [107], "m_product_category": [106, 107, 108, 109, 110]}
CATALOG = [
    (106, "樹木", ["オリーブ苗", "レモン苗", "ブルーベリー苗", "ユーカリ苗", "モミジ苗", "サクラ苗", "キンモクセイ苗", "シマトネリコ苗"]),
    (107, "草花", ["ラベンダー", "ローズマリー", "アジサイ", "ツツジ", "ミント", "タイム", "セージ", "バラ苗"]),
    (108, "園芸工具", ["剪定ばさみ", "ジョウロ", "移植ごて", "園芸手袋", "熊手", "散水ホース", "草取り鎌", "植木鉢スタンド"]),
    (109, "土と肥料", ["有機肥料", "培養土", "腐葉土", "液体肥料", "鉢底石", "赤玉土", "堆肥", "天然防虫剤"]),
    (110, "庭と暮らし", ["ガーデンチェア", "ガーデンテーブル", "プランター", "収納ボックス", "屋外マット", "日よけシェード", "ソーラーライト", "植木鉢"]),
]
VARIANTS = ["コンパクト", "スタンダード", "ワイド", "プレミアム", "プロ仕様"]
USES = ["ベランダ", "家庭菜園", "庭", "玄関", "テラス"]


def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(v) for v in value]
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    return value


def dumps(value):
    return json.dumps(normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(normalize(value), ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def row_uuid(table, position):
    return uuid5(NAMESPACE, f"{BATCH}/{table}/{position}")


def uuids(table):
    return [row_uuid(table, i) for i in range(TABLES[table])]


def connect(write=False):
    if write:
        secret = json.loads((ROOT / ".local/secrets/postgres.json").read_text(encoding="utf-8-sig"))
        db = psycopg.connect(host="127.0.0.1", port=5432, dbname="poc_idempiere", user="postgres",
                              password=secret["password"], connect_timeout=5, row_factory=dict_row)
        db.execute("SET ROLE poc_idempiere_owner")
    else:
        from poc.config import environment
        db = psycopg.connect(environment()["dsn"], connect_timeout=5, row_factory=dict_row)
        db.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
    db.execute("SET LOCAL statement_timeout = '30s'")
    db.execute("SET LOCAL lock_timeout = '5s'")
    if db.execute("SELECT current_database() AS name").fetchone()["name"] != "poc_idempiere":
        db.close()
        raise RuntimeError("대상 DB가 poc_idempiere가 아닙니다.")
    return db


def select_seed(db, table):
    return db.execute(sql.SQL("SELECT * FROM adempiere.{} WHERE {} = ANY(%s) ORDER BY {}").format(
        sql.Identifier(table), sql.Identifier(table + "_uu"), sql.Identifier(table + "_id")), [uuids(table)]).fetchall()


def fingerprint(rows):
    return {"count": len(rows), "sha256": hashlib.sha256(dumps(rows).encode()).hexdigest()}


def registered_product_ids(db):
    """Exclude only products proved by the committed request/audit/outbox registry.

    A missing registry means the original 255-product contract. Permission errors
    and unregistered additions remain failures, rather than silently weakening it.
    """
    if db.execute("SELECT to_regclass('poc_registration.registered_product_provenance') AS relation").fetchone()["relation"] is None:
        return []
    rows = db.execute("SELECT product_id FROM poc_registration.registered_product_provenance ORDER BY product_id").fetchall()
    return [int(row["product_id"]) for row in rows]


def baseline(db):
    result = {}
    registered = set(registered_product_ids(db))
    for table in TABLES:
        rows = db.execute(sql.SQL("SELECT * FROM adempiere.{} WHERE {} IS NULL OR NOT ({} = ANY(%s)) ORDER BY {}").format(
            sql.Identifier(table), sql.Identifier(table + "_uu"), sql.Identifier(table + "_uu"),
            sql.Identifier(table + "_id")), [uuids(table)]).fetchall()
        if table == "m_product":
            rows = [row for row in rows if int(row["m_product_id"]) not in registered]
        result[table] = fingerprint(rows)
    for table, ids in PARENTS.items():
        rows = db.execute(sql.SQL("SELECT * FROM adempiere.{} WHERE {} = ANY(%s) ORDER BY {}").format(
            sql.Identifier(table), sql.Identifier(table + "_id"), sql.Identifier(table + "_id")), [ids]).fetchall()
        if len(rows) != len(ids):
            raise RuntimeError(f"필요한 부모 행 누락: {table}")
        for row in rows:
            if row.get("ad_client_id", 11) not in (0, 11) or row.get("isactive", "Y") != "Y":
                raise RuntimeError(f"부모 테넌트/활성 상태 불일치: {table}")
        result[table] = fingerprint(rows)
    return result


def allocate(db, table, count):
    sequence = db.execute("SELECT ad_sequence_id,currentnext,incrementno FROM adempiere.ad_sequence WHERE lower(name)=%s AND istableid='Y' FOR UPDATE", [table]).fetchall()
    if len(sequence) != 1 or int(sequence[0]["incrementno"]) != 1:
        raise RuntimeError(f"지원되지 않는 AD_Sequence: {table}")
    top = db.execute(sql.SQL("SELECT coalesce(max({}),0) AS top FROM adempiere.{}").format(
        sql.Identifier(table + "_id"), sql.Identifier(table))).fetchone()["top"]
    first = max(int(sequence[0]["currentnext"]), int(top) + 1)
    if first + count > 9999999999:
        raise RuntimeError("numeric(10,0) ID 범위 초과")
    db.execute("UPDATE adempiere.ad_sequence SET currentnext=%s WHERE ad_sequence_id=%s", [first + count, sequence[0]["ad_sequence_id"]])
    return list(range(first, first + count))


def intended_rows(ids):
    rows = {t: [] for t in TABLES}

    def add(table, position, values):
        row = {"ad_client_id": 11, "ad_org_id": 11, "createdby": 101, "updatedby": 101, "isactive": "Y",
               table + "_id": ids[table][position], table + "_uu": row_uuid(table, position), **values}
        rows[table].append(row)

    for i in range(200):
        category, label, names = CATALOG[i // 40]
        name = f"{names[i % 8]} {VARIANTS[(i % 40) // 8]}"
        add("m_product", i, {"value": f"POCJA-{i + 1:04}", "sku": f"POCJA-{i + 1:04}", "name": name,
            "description": f"{USES[i % 5]}で使える{label}のデモ商品。{name}。手入れしやすく、日々の園芸を楽しめます。",
            "documentnote": "検索検証用の架空商品です。実際の販売・在庫を表しません。",
            "c_uom_id": 100, "m_product_category_id": category, "c_taxcategory_id": 107,
            "salesrep_id": 103, "producttype": "I", "classification": "POC-DEMO",
            "group1": label, "group2": USES[i % 5], "weight": Decimal(i % 20 + 1) / 10,
            "volume": Decimal(i % 10 + 1) / 100, "unitsperpack": 1 + i % 4})
        promotion = f"{label} {USES[i % 5]}応援フェア {i + 1:03}"
        add("m_promotion", i, {"name": promotion, "description": f"{label}の対象商品をまとめて探せるデモ企画。{USES[i % 5]}の準備におすすめ。",
            "promotionpriority": 1 + i % 10, "c_campaign_id": 101 + i % 2})
        add("m_promotiongroup", i, {"name": f"{label} 対象商品グループ {i + 1:03}", "description": f"{promotion}の対象商品"})
        add("m_promotionline", i, {"m_promotion_id": ids["m_promotion"][i],
            "m_promotiongroup_id": ids["m_promotiongroup"][i], "ismandatorypl": "Y", "minimumamt": 0})
        for offset in range(1 + i % 5):
            p = (i // 40) * 40 + ((i % 40 + offset) % 40)
            add("m_promotiongroupline", len(rows["m_promotiongroupline"]), {
                "m_product_id": ids["m_product"][p], "m_promotiongroup_id": ids["m_promotiongroup"][i]})
    return rows


def seed():
    STATE.mkdir(parents=True, exist_ok=True)
    with connect(write=True) as db:
        db.execute("SELECT pg_advisory_xact_lock(720031109)")
        snapshot = baseline(db)
        before = STATE / "baseline.json"
        if before.exists():
            if json.loads(before.read_text(encoding="utf-8")) != snapshot:
                raise RuntimeError("기존 행/부모 데이터가 최초 기준과 다릅니다. 자동 덮어쓰기하지 않습니다.")
        else:
            save(before, snapshot)
        existing = {t: select_seed(db, t) for t in TABLES}
        counts = {t: len(r) for t, r in existing.items()}
        present = any(counts.values())
        if present and counts != TABLES:
            raise RuntimeError(f"불완전한 기존 더미 배치입니다: {counts}")
        ids = {}
        for table, count in TABLES.items():
            if present:
                by_uuid = {r[table + "_uu"]: int(r[table + "_id"]) for r in existing[table]}
                ids[table] = [by_uuid[u] for u in uuids(table)]
            else:
                ids[table] = allocate(db, table, count)
        intended = intended_rows(ids)
        for table, rows in intended.items():
            if present:
                by_id = {int(r[table + "_id"]): r for r in existing[table]}
                for row in rows:
                    old = by_id[row[table + "_id"]]
                    if any(old[k] != v for k, v in row.items()):
                        raise RuntimeError(f"기존 더미 행의 내용/소유권 충돌: {table}")
            else:
                columns = list(rows[0])
                statement = sql.SQL("INSERT INTO adempiere.{} ({}) VALUES ({})").format(
                    sql.Identifier(table), sql.SQL(",").join(map(sql.Identifier, columns)),
                    sql.SQL(",").join(sql.Placeholder() for _ in columns))
                with db.cursor() as cursor:
                    cursor.executemany(statement, [[r[k] for k in columns] for r in rows])
        db.execute("SET CONSTRAINTS ALL IMMEDIATE")
        if baseline(db) != snapshot:
            raise RuntimeError("기존 행 보존 검증 실패")
    report = {"batch": BATCH, "action": "reused" if present else "inserted", "counts": TABLES, "ids": ids}
    save(STATE / "seed-manifest.json", report)
    return report


def export_rows():
    with connect() as db:
        rows = {t: select_seed(db, t) for t in TABLES}
        if {t: len(r) for t, r in rows.items()} != TABLES:
            raise RuntimeError("더미 행 수 불일치")
        if baseline(db) != json.loads((STATE / "baseline.json").read_text(encoding="utf-8")):
            raise RuntimeError("기존 행/부모 보존 검증 실패")
        parents = {}
        for table, ids in PARENTS.items():
            parents[table] = db.execute(sql.SQL("SELECT {},name FROM adempiere.{} WHERE {}=ANY(%s)").format(
                sql.Identifier(table + "_id"), sql.Identifier(table), sql.Identifier(table + "_id")), [ids]).fetchall()
        columns = db.execute("SELECT table_name,column_name,data_type,numeric_scale FROM information_schema.columns WHERE table_schema='adempiere' AND table_name=ANY(%s) ORDER BY table_name,ordinal_position", [["m_product", "m_promotion"]]).fetchall()
    save(STATE / "export/rows.json", rows)
    return rows, parents, columns
