"""공식 GardenWorld 시드를 별도 DB에 설치하고 분석 카탈로그를 만든다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
from dotenv import set_key

from .config import ROOT
from .catalog import IDEMPIERE_INVOICE_RULE

DATABASE = "poc_idempiere"
OWNER = "poc_idempiere_owner"
READER = "poc_idempiere_reader"
COMMIT = "30af25e9db302a6cdefd9e6c3846f7cedc5ce4d0"
SOURCE = f"https://raw.githubusercontent.com/idempiere/binary.file/{COMMIT}/database/13/Adempiere_pg.jar"
SHA256 = "f6e5f409791c9eb576caf3c36e0bf9747d59d261ff9bdd743e55fcb125b21b9c"
DATA = ROOT / ".local/datasets/idempiere"
DOWNLOADS = ROOT / ".local/downloads/idempiere"
MARKER = f"PoC-Practice iDempiere 13 GardenWorld {SHA256}"


def psql_executable():
    if sys.platform == "win32":
        installed = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "PostgreSQL/18/bin/psql.exe"
        if installed.is_file():
            return str(installed)
    executable = shutil.which("psql")
    if executable:
        return executable
    raise RuntimeError("psql을 찾을 수 없습니다. PostgreSQL 18의 bin 디렉터리를 PATH에 추가하세요.")


def connections():
    admin = json.loads((ROOT / ".local/secrets/postgres.json").read_text(encoding="utf-8-sig"))
    secret_path = ROOT / ".local/secrets/idempiere.json"
    if not secret_path.exists():
        secret_path.write_text(json.dumps({"reader_password": secrets.token_hex(32)}), encoding="utf-8")
    secret = json.loads(secret_path.read_text(encoding="utf-8"))
    base = dict(host="127.0.0.1", port=5432, user="postgres", password=admin["password"], connect_timeout=5)
    reader = make_conninfo(host="127.0.0.1", port=5432, dbname=DATABASE, user=READER, password=secret["reader_password"])
    return base, reader, secret["reader_password"]


def install():
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    package = DOWNLOADS / "Adempiere_pg-13.jar"
    if not package.exists():
        with urllib.request.urlopen(SOURCE, timeout=60) as response, package.open("wb") as output:
            shutil.copyfileobj(response, output)
    if hashlib.sha256(package.read_bytes()).hexdigest() != SHA256:
        raise RuntimeError("공식 시드 체크섬 불일치. 다운로드 파일을 확인하세요.")
    with zipfile.ZipFile(package) as archive:
        original = archive.read("Adempiere_pg.dmp").decode("utf-8")
    # 시드는 전용 NOLOGIN 소유자 역할로 복원한다. 원본은 그대로 보관한다.
    prepared = re.sub(r"^(ALTER [^\n]+ OWNER TO) adempiere;$", rf"\1 {OWNER};", original, flags=re.M)
    # PG18은 기존 날짜 연산자들의 상충하는 교환법칙 힌트를 거부한다.
    # 함수/인자/거래 행은 유지하고 네 연산자의 선택적 최적화 힌트만 제거한다.
    prepared = re.sub(r"CREATE OPERATOR adempiere\.[+-] \(.*?\n\);",
                      lambda m: re.sub(r",\n    COMMUTATOR = OPERATOR\(adempiere\.[+-]\)", "", m.group()), prepared, flags=re.S)
    restore_file = DOWNLOADS / "restore-project.sql"
    restore_file.write_text(prepared, encoding="utf-8")
    base, reader, password = connections()
    with psycopg.connect(**base, dbname="postgres", autocommit=True) as db:
        for role, login in ((OWNER, False), (READER, True)):
            record = db.execute("SELECT rolcanlogin,rolsuper,rolcreatedb,rolcreaterole FROM pg_roles WHERE rolname=%s", [role]).fetchone()
            if record and record != (login, False, False, False):
                raise RuntimeError("동일 이름의 기존 역할 속성이 다릅니다. 자동 변경하지 않습니다.")
            if not record:
                db.execute(sql.SQL("CREATE ROLE {} {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT").format(sql.Identifier(role), sql.SQL("LOGIN" if login else "NOLOGIN")))
                if login:
                    db.execute(sql.SQL("ALTER ROLE {} PASSWORD {}").format(sql.Identifier(role), sql.Literal(password)))
        record = db.execute("SELECT pg_get_userbyid(datdba),shobj_description(oid,'pg_database') FROM pg_database WHERE datname=%s", [DATABASE]).fetchone()
        if record and record != (OWNER, MARKER):
            raise RuntimeError("기존 poc_idempiere DB가 이 설치의 소유가 아닙니다. 덮어쓰지 않습니다.")
        if not record:
            db.execute(sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0 ENCODING 'UTF8'").format(sql.Identifier(DATABASE), sql.Identifier(OWNER)))
            db.execute(sql.SQL("COMMENT ON DATABASE {} IS {}").format(sql.Identifier(DATABASE), sql.Literal(MARKER)))
        db.execute(sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(sql.Identifier(DATABASE)))
        db.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(sql.Identifier(DATABASE), sql.Identifier(READER)))
    with psycopg.connect(**base, dbname=DATABASE) as db:
        exists = db.execute("SELECT to_regclass('adempiere.ad_system') IS NOT NULL").fetchone()[0]
        db.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    if not exists:
        print("GardenWorld 복원 시작 (전용 DB, 단일 트랜잭션)", flush=True)
        env = {**os.environ, "PGPASSWORD": base["password"], "PGOPTIONS": f"-c role={OWNER}", "PGCLIENTENCODING": "UTF8"}
        executable = psql_executable()
        with (DATA / "restore.log").open("w", encoding="utf-8") as log:
            result = subprocess.run([str(executable), "-X", "-h", "127.0.0.1", "-p", "5432", "-U", "postgres", "-d", DATABASE,
                                     "-v", "ON_ERROR_STOP=1", "--single-transaction", "-f", str(restore_file)], env=env, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"복원 실패. 단일 트랜잭션이 롤백되었습니다. {DATA / 'restore.log'} 확인")
    with psycopg.connect(**base, dbname=DATABASE) as db:
        db.execute("REVOKE CREATE ON SCHEMA public FROM PUBLIC")
        db.execute("REVOKE ALL ON SCHEMA adempiere FROM PUBLIC")
        db.execute("REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA adempiere FROM PUBLIC")
        db.execute(sql.SQL("GRANT USAGE ON SCHEMA adempiere TO {}").format(sql.Identifier(READER)))
        db.execute(sql.SQL("GRANT SELECT ON ALL TABLES IN SCHEMA adempiere TO {}").format(sql.Identifier(READER)))
        for option, value in (("default_transaction_read_only", "on"), ("statement_timeout", "20s"), ("lock_timeout", "1s"), ("idle_in_transaction_session_timeout", "30s")):
            db.execute(sql.SQL("ALTER ROLE {} SET {} = {}").format(sql.Identifier(READER), sql.Identifier(option), sql.Literal(value)))
        db.execute(sql.SQL("ALTER ROLE {} IN DATABASE {} SET search_path = pg_catalog, adempiere").format(sql.Identifier(READER), sql.Identifier(DATABASE)))
        db.execute("ANALYZE")
    catalog = make_catalog(reader)
    (DATA / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {"source": SOURCE, "commit": COMMIT, "sha256": SHA256, "database": DATABASE,
                "compatibility": "PG18: four legacy date operators restored without conflicting COMMUTATOR hints; owner mapped to project NOLOGIN role",
                "schema": "adempiere", "tables": len(catalog["tables"]), "views": catalog["view_count"],
                "foreign_keys": len(catalog["relationships"]), "schema_version": catalog["schema_version"],
                "row_counts": {name: meta["rows"] for name, meta in catalog["table_details"].items()}}
    (DATA / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "row_counts"}), flush=True)
    return catalog


def make_catalog(dsn):
    tables, details = {}, {}
    with psycopg.connect(dsn) as db:
        definitions = db.execute("""SELECT lower(tablename), name, description FROM adempiere.ad_table WHERE isview='N'""").fetchall()
        descriptions = {name: {"label": label, "description": description or ""} for name, label, description in definitions}
        for table, column, kind, nullable in db.execute("""SELECT table_name,column_name,data_type,is_nullable FROM information_schema.columns
            WHERE table_schema='adempiere' AND table_name IN (SELECT table_name FROM information_schema.tables WHERE table_schema='adempiere' AND table_type='BASE TABLE')
            ORDER BY table_name,ordinal_position"""):
            tables.setdefault(table, []).append({"name": column, "type": kind, "nullable": nullable == "YES"})
        for table in tables:
            count = db.execute(sql.SQL("SELECT count(*) FROM adempiere.{}").format(sql.Identifier(table))).fetchone()[0]
            details[table] = {**descriptions.get(table, {"label": table, "description": ""}), "rows": count}
        relationships = []
        for child, child_columns, parent, parent_columns in db.execute("""SELECT child.relname,
            array_agg(ca.attname ORDER BY k.n), parent.relname, array_agg(pa.attname ORDER BY k.n)
            FROM pg_constraint f JOIN pg_class child ON child.oid=f.conrelid JOIN pg_class parent ON parent.oid=f.confrelid
            JOIN pg_namespace ns ON ns.oid=child.relnamespace
            CROSS JOIN LATERAL generate_subscripts(f.conkey,1) AS k(n)
            JOIN pg_attribute ca ON ca.attrelid=child.oid AND ca.attnum=f.conkey[k.n]
            JOIN pg_attribute pa ON pa.attrelid=parent.oid AND pa.attnum=f.confkey[k.n]
            WHERE f.contype='f' AND ns.nspname='adempiere' GROUP BY f.oid,child.relname,parent.relname ORDER BY child.relname,f.oid"""):
            relationships.append([child, ",".join(child_columns), parent, ",".join(parent_columns)])
        client = db.execute("SELECT ad_client_id,name FROM adempiere.ad_client WHERE name='GardenWorld'").fetchone()
        if not client:
            raise RuntimeError("GardenWorld 테넌트를 찾지 못했습니다.")
        start, end = db.execute("SELECT min(dateinvoiced)::date,max(dateinvoiced)::date FROM adempiere.c_invoice WHERE ad_client_id=%s", [client[0]]).fetchone()
        views = db.execute("SELECT count(*) FROM information_schema.views WHERE table_schema='adempiere'").fetchone()[0]
    catalog = {"dataset_id": "idempiere", "dataset_label": "iDempiere 13 · GardenWorld 데모", "schema": "adempiere", "database": DATABASE,
               "tables": tables, "table_details": details, "relationships": relationships, "view_count": views,
               "tenant": {"ad_client_id": int(client[0]), "name": client[1]}, "date_range": {"start": str(start), "end": str(end)},
               "limits": {"rows": 500, "bytes": 262144, "sql_seconds": 20},
               "business_rules": ["GardenWorld 공식 데모 데이터이며 실제 기업의 운영 실적이 아닙니다.",
                   f"업무 거래 테이블은 기본적으로 ad_client_id={int(client[0])} (GardenWorld)로 제한합니다. 공통 마스터는 ad_client_id=0일 수 있습니다.",
                   "issotrx='Y'는 판매, 'N'은 구매입니다. 확정 거래 분석은 docstatus IN ('CO','CL')를 사용하고 조건을 설명합니다.",
                   "c_order는 주문, c_invoice는 청구서, c_payment는 결제입니다. 주문액·청구액·현금 수입을 구분합니다.",
                   IDEMPIERE_INVOICE_RULE,
                   "서로 다른 통화는 합산하지 말고 c_currency.iso_code로 구분합니다. 통화 변환을 임의로 가정하지 않습니다.",
                   "전표 헤더 금액을 상세행과 조인한 뒤 합산하면 중복됩니다. 상세 금액은 c_invoiceline.linenetamt를 사용합니다.",
                   "데모 날짜는 과거입니다. 최근 기간을 임의로 데모 기간으로 바꾸지 말고 데이터 부재를 설명합니다.",
                   "테이블 정의가 있어도 rows=0이면 해당 업무의 샘플 행은 없습니다. 원가·순이익을 근거 없이 추정하지 않습니다."],
               "sample_question": "GardenWorld의 확정 판매 청구액과 청구서 수를 월별·통화별로 보여줘"}
    catalog["schema_version"] = hashlib.sha256(json.dumps(catalog, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return catalog


def activate():
    if not (DATA / "catalog.json").exists():
        raise RuntimeError("먼저 설치해야 합니다.")
    _, reader, _ = connections()
    env = ROOT / ".local/app.env"
    backup = DATA / "app-before-idempiere.env"
    if not backup.exists():
        shutil.copy2(env, backup)
    for key, value in {"POC_DB_DSN": reader, "POC_CATALOG_PATH": str(DATA / "catalog.json")}.items():
        set_key(str(env), key, value)
    print("iDempiere 연결 설정 완료. 실행 중인 SQL API를 재시작하세요.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--activate", action="store_true", help="설치 후 챗봇의 기본 DB로 설정")
    args = parser.parse_args()
    install()
    if args.activate:
        activate()


if __name__ == "__main__":
    main()
