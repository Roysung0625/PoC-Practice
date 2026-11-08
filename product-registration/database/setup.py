"""Install the local registration schema and its separate, minimal API credential."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets

from dotenv import set_key
import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

ROOT = Path(__file__).resolve().parents[2]
OWNER, API, READER = "poc_registration_owner", "poc_registration_api", "poc_idempiere_reader"
SCHEMA = Path(__file__).with_name("schema.sql")


def install(admin_dsn, *, env_path=None, secret_path=None):
    """Idempotent only for the exact installed schema; refuse silently replacing objects."""
    options = conninfo_to_dict(admin_dsn)
    if options.get("host", "") not in ("127.0.0.1", "localhost", "::1"):
        raise RuntimeError("登録 DB はローカル接続に限定します。")
    name = options.get("dbname", "")
    if name != "poc_idempiere" and not name.startswith("poc_registration_test_"):
        raise RuntimeError("登録専用の対象 DB 名を確認してください。")
    secret_path = Path(secret_path or ROOT / ".local/secrets/registration.json")
    env_path = Path(env_path or ROOT / ".local/registration.env")
    schema_text = SCHEMA.read_text(encoding="utf-8")
    marker = "PoC-Practice registration v1 sha256=" + hashlib.sha256(schema_text.encode()).hexdigest()
    password = None
    if secret_path.exists():
        password = json.loads(secret_path.read_text(encoding="utf-8"))["api_password"]
    with psycopg.connect(admin_dsn, connect_timeout=5) as db:
        for role, login in ((OWNER, False), (API, True)):
            record = db.execute("SELECT rolcanlogin,rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname=%s", [role]).fetchone()
            if record is not None and record != (login, False, False, False, False, False):
                raise RuntimeError("既存の登録ロール属性が一致しません。自動変更しません。")
            if db.execute("SELECT EXISTS(SELECT 1 FROM pg_auth_members m JOIN pg_roles r ON r.oid=m.member WHERE r.rolname=%s)", [role]).fetchone()[0]:
                raise RuntimeError("登録ロールに不要な継承権限があります。")
            if record is None:
                db.execute(sql.SQL("CREATE ROLE {} {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS").format(sql.Identifier(role), sql.SQL("LOGIN" if login else "NOLOGIN")))
                if login:
                    password = password or secrets.token_urlsafe(36)
                    db.execute(sql.SQL("ALTER ROLE {} PASSWORD {}").format(sql.Identifier(role), sql.Literal(password)))
            elif login and not password:
                raise RuntimeError("既存ロールの資格情報がありません。既存パスワードを上書きしません。")
        row = db.execute("SELECT obj_description(oid,'pg_namespace') FROM pg_namespace WHERE nspname='poc_registration'").fetchone()
        if row is None:
            db.execute(schema_text, prepare=False)
            db.execute(sql.SQL("COMMENT ON SCHEMA poc_registration IS {}").format(sql.Literal(marker)))
        elif row[0] != marker:
            raise RuntimeError("既存の登録スキーマとソースが一致しません。変更内容を確認してください。")
        db.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(sql.Identifier(name), sql.Identifier(API)))
        for option, value in (("statement_timeout", "15s"), ("lock_timeout", "5s"), ("idle_in_transaction_session_timeout", "30s")):
            db.execute(sql.SQL("ALTER ROLE {} SET {} = {}").format(sql.Identifier(API), sql.Identifier(option), sql.Literal(value)))
        db.execute(sql.SQL("ALTER ROLE {} IN DATABASE {} SET search_path=pg_catalog,poc_registration").format(sql.Identifier(API), sql.Identifier(name)))
        if db.execute("SELECT EXISTS(SELECT 1 FROM pg_roles WHERE rolname=%s)", [READER]).fetchone()[0]:
            db.execute(sql.SQL("GRANT USAGE ON SCHEMA poc_registration TO {}").format(sql.Identifier(READER)))
            db.execute(sql.SQL("GRANT SELECT ON poc_registration.registered_product_provenance TO {}").format(sql.Identifier(READER)))
        if db.execute("SELECT has_table_privilege(%s,'adempiere.m_product','INSERT,UPDATE,DELETE,TRUNCATE') OR has_table_privilege(%s,'poc_registration.registration_request','INSERT,UPDATE,DELETE,TRUNCATE') OR has_schema_privilege(%s,'adempiere','USAGE')", [API, API, API]).fetchone()[0]:
            raise RuntimeError("登録 API ロールに不要な直接アクセス権限があります。")
        # Persist the generated credential atomically before commit. A failed
        # commit can reuse this secret; a failed file write rolls the DB back.
        secret_path.parent.mkdir(parents=True, exist_ok=True)
        if not secret_path.exists():
            temporary = secret_path.with_suffix(".json.tmp")
            temporary.write_text(json.dumps({"api_password": password}), encoding="utf-8")
            temporary.replace(secret_path)
    # No credential values are printed, including on retries.
    env_path.parent.mkdir(parents=True, exist_ok=True)
    api_options = {k: v for k, v in options.items() if k in {"host", "port", "dbname", "sslmode"}}
    dsn = make_conninfo(**api_options, user=API, password=password)
    set_key(str(env_path), "POC_REGISTRATION_DB_DSN", dsn)
    return {"database": name, "schema": "poc_registration", "api_role": API, "tables": 3, "env_file": str(env_path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--admin-secret", type=Path, default=ROOT / ".local/secrets/postgres.json")
    parser.add_argument("--database", default="poc_idempiere")
    args = parser.parse_args()
    dsn = os.getenv("POC_REGISTRATION_ADMIN_DSN", "")
    if not dsn:
        secret = json.loads(args.admin_secret.read_text(encoding="utf-8-sig"))
        dsn = make_conninfo(host="127.0.0.1", port=5432, dbname=args.database, user="postgres", password=secret["password"])
    try:
        print(json.dumps(install(dsn), ensure_ascii=False))
    except psycopg.Error:
        raise SystemExit("登録 DB の準備に失敗しました。接続先と管理権限を確認してください。") from None


if __name__ == "__main__":
    main()
