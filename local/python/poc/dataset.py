import json
import hashlib
from pathlib import Path

import duckdb
import psycopg
from psycopg import sql

TABLE_ORDER = ("region", "nation", "supplier", "customer", "part", "partsupp", "orders", "lineitem")


def generate(directory: Path, scale: float = 1.0) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    manifest_path = directory / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["scale"] != scale:
            raise ValueError("다른 스케일 데이터가 있습니다. 별도 출력 경로를 사용하세요.")
        if all((directory / f"{table}.csv").exists() for table in TABLE_ORDER):
            return manifest
    with duckdb.connect(str(directory / "tpch.duckdb")) as db:
        db.execute("INSTALL tpch; LOAD tpch;")
        if not db.execute("SELECT count(*) FROM information_schema.tables WHERE table_name='lineitem'").fetchone()[0]:
            db.execute("CALL dbgen(sf=?)", [scale])
        manifest = {"scale": scale, "generator": f"duckdb-{duckdb.__version__}", "tables": {}}
        for table in TABLE_ORDER:
            columns = [[r[0], r[1]] for r in db.execute(f"DESCRIBE {table}").fetchall()]
            count = db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            target = str(directory / f"{table}.csv").replace("'", "''")
            db.execute(f"COPY {table} TO '{target}' (HEADER, DELIMITER ',')")
            manifest["tables"][table] = {"columns": columns, "count": count}
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


KEYS = {"region": "r_regionkey", "nation": "n_nationkey", "supplier": "s_suppkey", "customer": "c_custkey", "part": "p_partkey", "partsupp": "ps_partkey,ps_suppkey", "orders": "o_orderkey", "lineitem": "l_orderkey,l_linenumber"}
RELATIONS = [
    ("nation", "n_regionkey", "region", "r_regionkey"),
    ("supplier", "s_nationkey", "nation", "n_nationkey"),
    ("customer", "c_nationkey", "nation", "n_nationkey"),
    ("partsupp", "ps_partkey", "part", "p_partkey"),
    ("partsupp", "ps_suppkey", "supplier", "s_suppkey"),
    ("orders", "o_custkey", "customer", "c_custkey"),
    ("lineitem", "l_orderkey", "orders", "o_orderkey"),
    ("lineitem", "l_partkey,l_suppkey", "partsupp", "ps_partkey,ps_suppkey"),
]


def load_dataset(admin_dsn: str, directory: Path, reader_role: str) -> dict:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    with psycopg.connect(admin_dsn) as db:
        db.execute("SELECT pg_advisory_xact_lock(72180420)")
        db.execute("CREATE SCHEMA IF NOT EXISTS tpch")
        db.execute("CREATE TABLE IF NOT EXISTS public.poc_dataset (id int PRIMARY KEY CHECK(id=1), manifest jsonb NOT NULL)")
        previous = db.execute("SELECT manifest FROM public.poc_dataset WHERE id=1").fetchone()
        if previous:
            if previous[0] != manifest:
                raise ValueError("다른 데이터가 적재된 DB입니다. 기존 DB를 덮어쓰지 않습니다.")
            for table, entry in manifest["tables"].items():
                count = db.execute(sql.SQL("SELECT count(*) FROM tpch.{}").format(sql.Identifier(table))).fetchone()[0]
                if count != entry["count"]:
                    raise ValueError(f"적재 데이터 불일치: {table}")
            return manifest
        for table in TABLE_ORDER:
            entry = manifest["tables"][table]
            columns = sql.SQL(',').join(sql.SQL('{} {} NOT NULL').format(sql.Identifier(name), sql.SQL(kind)) for name, kind in entry["columns"])
            db.execute(sql.SQL("CREATE TABLE tpch.{} ({}, PRIMARY KEY ({}))").format(sql.Identifier(table), columns, sql.SQL(KEYS[table])))
            with db.cursor().copy(sql.SQL("COPY tpch.{} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)").format(sql.Identifier(table))) as copy:
                with (directory / f"{table}.csv").open("rb") as source:
                    while block := source.read(1024 * 1024):
                        copy.write(block)
        for child, columns, parent, foreign in RELATIONS:
            db.execute(sql.SQL("ALTER TABLE tpch.{} ADD FOREIGN KEY ({}) REFERENCES tpch.{} ({})").format(sql.Identifier(child), sql.SQL(columns), sql.Identifier(parent), sql.SQL(foreign)))
        for table, column in [("orders", "o_orderdate"), ("lineitem", "l_shipdate"), ("lineitem", "l_partkey"), ("part", "p_type")]:
            db.execute(sql.SQL("CREATE INDEX ON tpch.{} ({})").format(sql.Identifier(table), sql.Identifier(column)))
        db.execute(sql.SQL("REVOKE CREATE ON SCHEMA public FROM PUBLIC"))
        db.execute(sql.SQL("GRANT USAGE ON SCHEMA tpch TO {}").format(sql.Identifier(reader_role)))
        db.execute(sql.SQL("GRANT SELECT ON ALL TABLES IN SCHEMA tpch TO {}").format(sql.Identifier(reader_role)))
        db.execute(sql.SQL("ALTER ROLE {} SET default_transaction_read_only=on").format(sql.Identifier(reader_role)))
        db.execute(sql.SQL("ALTER ROLE {} SET statement_timeout='20s'").format(sql.Identifier(reader_role)))
        db.execute("INSERT INTO public.poc_dataset VALUES (1, %s::jsonb)", [json.dumps(manifest)])
        db.execute("ANALYZE")
    return manifest


def read_catalog(dsn: str) -> dict:
    with psycopg.connect(dsn) as db:
        tables = {}
        for table, column, kind in db.execute("SELECT table_name,column_name,data_type FROM information_schema.columns WHERE table_schema='tpch' ORDER BY table_name,ordinal_position"):
            tables.setdefault(table, []).append({"name": column, "type": kind})
        start, end = db.execute("SELECT min(o_orderdate), max(o_orderdate) FROM tpch.orders").fetchone()
        groups = [r[0] for r in db.execute("SELECT DISTINCT split_part(p_type, ' ', 1) FROM tpch.part ORDER BY 1")]
        catalog = {"tables": tables, "relationships": RELATIONS, "date_range": {"start": str(start), "end": str(end)}, "product_groups": groups, "limits": {"rows": 500, "bytes": 262144, "sql_seconds": 20}, "missing_financial_data": ["판매관리비", "세금", "금융비용"], "supplier_meaning": "공급업체이며 실제 판매자 계정과 동일하지 않음"}
        catalog["schema_version"] = hashlib.sha256(json.dumps(catalog, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        return catalog
