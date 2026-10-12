import json
import secrets
import uuid

import psycopg
from psycopg import sql
import pytest

from poc.config import ROOT


@pytest.fixture(scope="session")
def postgres_db():
    secret = json.loads((ROOT / ".local/secrets/postgres.json").read_text(encoding="utf-8-sig"))
    name = "poc_test_" + uuid.uuid4().hex[:12]
    role = name + "_reader"
    password = secrets.token_hex(24)
    base = {"host": "127.0.0.1", "port": 5432, "user": "postgres", "password": secret["password"]}
    with psycopg.connect(**base, dbname="postgres", autocommit=True) as db:
        db.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0").format(sql.Identifier(name)))
        db.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT").format(sql.Identifier(role), sql.Literal(password)))
    from psycopg.conninfo import make_conninfo
    admin = make_conninfo(**base, dbname=name)
    reader = make_conninfo(host="127.0.0.1", port=5432, dbname=name, user=role, password=password)
    try:
        yield admin, reader, role
    finally:
        with psycopg.connect(**base, dbname="postgres", autocommit=True) as db:
            db.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))
            db.execute(sql.SQL("DROP ROLE {}").format(sql.Identifier(role)))


@pytest.fixture(scope="session")
def loaded_db(postgres_db, tmp_path_factory):
    from poc.dataset import generate, load_dataset
    directory = tmp_path_factory.mktemp("tpch")
    manifest = generate(directory, 0.01)
    admin, reader, role = postgres_db
    load_dataset(admin, directory, role)
    return admin, reader, role, directory, manifest
