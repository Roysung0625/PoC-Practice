"""최초 로컬 구성. 실제 비밀값을 출력하지 않는다."""
import json
import secrets

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
from dotenv import set_key, dotenv_values

from .config import ROOT
from .dataset import generate, load_dataset, read_catalog


def main():
    active = dotenv_values(ROOT / ".local/app.env").get("POC_CATALOG_PATH")
    if active:
        from pathlib import Path
        path = Path(active)
        if path.exists() and json.loads(path.read_text(encoding="utf-8")).get("dataset_id") == "idempiere":
            from .idempiere import install
            install()
            return
    secret_path = ROOT / ".local/secrets/postgres.json"
    secret = json.loads(secret_path.read_text(encoding="utf-8-sig"))
    if "reader_password" not in secret:
        secret["reader_password"] = secrets.token_hex(32)
        secret["internal_token"] = secrets.token_hex(32)
        secret_path.write_text(json.dumps(secret), encoding="utf-8")
    base = {"host": "127.0.0.1", "port": 5432, "user": "postgres", "password": secret["password"]}
    with psycopg.connect(**base, dbname="postgres", autocommit=True) as db:
        if not db.execute("SELECT 1 FROM pg_roles WHERE rolname='poc_reader'").fetchone():
            db.execute(sql.SQL("CREATE ROLE poc_reader LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT").format(sql.Literal(secret["reader_password"])))
        if not db.execute("SELECT 1 FROM pg_database WHERE datname='poc_tpch'").fetchone():
            db.execute("CREATE DATABASE poc_tpch TEMPLATE template0 ENCODING 'UTF8'")
        db.execute("REVOKE TEMPORARY ON DATABASE poc_tpch FROM PUBLIC")
    admin_dsn = make_conninfo(**base, dbname="poc_tpch")
    reader_dsn = make_conninfo(host="127.0.0.1", port=5432, dbname="poc_tpch", user="poc_reader", password=secret["reader_password"])
    directory = ROOT / ".local/data/tpch-sf1"
    print("TPC-H SF1 생성 시작", flush=True)
    manifest = generate(directory, 1.0)
    print("PostgreSQL COPY 적재 시작", flush=True)
    load_dataset(admin_dsn, directory, "poc_reader")
    catalog = read_catalog(reader_dsn)
    (ROOT / ".local/catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    app_env = ROOT / ".local/app.env"
    for key, value in {"POC_DB_DSN": reader_dsn, "POC_INTERNAL_TOKEN": secret["internal_token"], "AWS_PROFILE": "poc-practice"}.items():
        set_key(str(app_env), key, value)
    web_env = ROOT / "local/web/.env"
    for key, value in {"APP_NAME": "로컬 데이터 랩", "APP_URL": "http://127.0.0.1:8000", "APP_DEBUG": "false", "POC_API_URL": "http://127.0.0.1:8001", "POC_INTERNAL_TOKEN": secret["internal_token"], "SESSION_DRIVER": "file", "CACHE_STORE": "file", "QUEUE_CONNECTION": "sync", "SESSION_SAME_SITE": "strict"}.items():
        set_key(str(web_env), key, value)
    print(json.dumps({"loaded": {k: v["count"] for k, v in manifest["tables"].items()}, "schema_version": catalog["schema_version"]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
