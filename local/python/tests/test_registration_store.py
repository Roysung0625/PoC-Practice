import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo
from psycopg.rows import dict_row
import pytest

from product_registration.store import RegistrationProblem, RegistrationStore, draft_issues, payload_sha256

ROOT = Path(__file__).resolve().parents[3]


def sample(code=None):
    return {"code": code or "GW-" + uuid4().hex[:8].upper(), "name": "鉢植え用オリーブ",
            "description": "ベランダ用の園芸デモ商品", "category": 106, "uom": 100,
            "tax": 107, "usage": "ベランダ", "weight": None, "pack": 1}


def test_store_is_lazy_and_never_falls_back_to_chatbot_dsn(monkeypatch):
    monkeypatch.delenv("POC_REGISTRATION_DB_DSN", raising=False)
    monkeypatch.setenv("POC_DB_DSN", "DO_NOT_USE_CHATBOT_DSN")
    monkeypatch.setattr("product_registration.store.load_dotenv", lambda *a, **k: None)
    store = RegistrationStore()
    with pytest.raises(RegistrationProblem) as caught:
        store.masters()
    assert caught.value.code == "REGISTRATION_UNAVAILABLE"
    assert "DO_NOT_USE_CHATBOT_DSN" not in str(caught.value)


@pytest.mark.parametrize("code", ["GW-ABCD", "GW-A1B2C3D4E5F6"])
def test_code_and_unknown_weight_valid(code):
    assert draft_issues(sample(code)) == []


@pytest.mark.parametrize("field,value,rule", [("code", "POCJA-0001", "CODE-01"), ("code", "GW-abcd", "CODE-01"),
    ("pack", True, "PKG-01"), ("pack", 1.2, "PKG-01"), ("weight", 0, "WGT-01"),
    ("weight", -1, "WGT-01"), ("weight", float("nan"), "WGT-01"), ("tax", True, "REF-01")])
def test_physical_input_errors(field, value, rule):
    draft = sample(); draft[field] = value
    assert any(issue["field"] == field and issue["rule_id"] == rule for issue in draft_issues(draft))


def test_new_uom_reports_exact_subfield_and_base_unit_is_not_a_package():
    draft = sample(); draft["uom"] = {"new": {"code": "PKG", "name": "1鉢"}}
    assert draft_issues(draft) == []
    draft["uom"]["new"]["code"] = "TOO-LONG"
    assert {"field": "uom.new.code", "rule_id": "REF-01", "message": "新規 uom の code は1〜4文字で入力してください。"} in draft_issues(draft)


def test_payload_digest_binds_exact_json_without_key_order_dependency():
    draft = sample()
    assert payload_sha256(draft) == payload_sha256(dict(reversed(list(draft.items()))))
    assert payload_sha256(draft) != payload_sha256({**draft, "weight": 0.1})


@pytest.fixture(scope="module")
def registration_db(tmp_path_factory):
    """Explicitly opt in to a separate cluster and restore the actual GardenWorld DDL/data."""
    dsn = os.getenv("POC_REGISTRATION_TEST_ADMIN_DSN", "")
    source = os.getenv("POC_REGISTRATION_TEST_SOURCE_SQL", "")
    if not dsn or not source:
        pytest.skip("Set isolated PostgreSQL DSN and official prepared GardenWorld SQL to run live storage tests")
    options = conninfo_to_dict(dsn)
    if options.get("host") != "127.0.0.1" or options.get("port") in (None, "5432"):
        pytest.fail("Storage tests require a separate localhost PostgreSQL cluster on a non-production port")
    directory = tmp_path_factory.mktemp("registration-db")
    name = "poc_registration_test_" + uuid4().hex[:12]
    base_options = {**options, "dbname": "postgres"}
    admin = make_conninfo(**{**options, "dbname": name})
    created_roles = []
    roles = ("poc_registration_api", "poc_registration_owner", "poc_idempiere_reader", "poc_idempiere_owner")
    with psycopg.connect(**base_options, autocommit=True) as db:
        # Never reuse unknown API roles or alter another test's global state.
        for role in roles[:2]:
            if db.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", [role]).fetchone():
                pytest.fail("A previous test owns the registration roles; use a clean isolated cluster")
        for role in roles[2:]:
            if not db.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", [role]).fetchone():
                db.execute(sql.SQL("CREATE ROLE {} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE").format(sql.Identifier(role)))
                created_roles.append(role)
        db.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0 ENCODING 'UTF8'").format(sql.Identifier(name)))
    try:
        with psycopg.connect(admin) as db:
            db.execute('CREATE EXTENSION "uuid-ossp"')
        executable = os.getenv("POC_REGISTRATION_TEST_PSQL", r"C:\Program Files\PostgreSQL\18\bin\psql.exe")
        with (directory / "restore.log").open("w", encoding="utf-8") as output:
            result = subprocess.run([executable, "-X", "-d", admin, "-v", "ON_ERROR_STOP=1", "--single-transaction", "-f", source], stdout=output, stderr=subprocess.STDOUT)
        assert result.returncode == 0, "Official GardenWorld fixture restore failed; see the isolated test restore.log"
        spec = importlib.util.spec_from_file_location("registration_setup_test", ROOT / "product-registration/database/setup.py")
        setup = importlib.util.module_from_spec(spec); spec.loader.exec_module(setup)
        env = directory / "registration.env"; secret = directory / "registration.json"
        setup.install(admin, env_path=env, secret_path=secret)
        # Idempotent setup must preserve credential and installed schema.
        before = secret.read_bytes()
        setup.install(admin, env_path=env, secret_path=secret)
        assert hashlib.sha256(before).hexdigest() == hashlib.sha256(secret.read_bytes()).hexdigest()
        password = json.loads(secret.read_text())["api_password"]
        api_dsn = make_conninfo(**{**options, "dbname": name, "user": "poc_registration_api", "password": password})
        yield admin, RegistrationStore(api_dsn), directory
    finally:
        with psycopg.connect(**base_options, autocommit=True) as db:
            db.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))
            for role in roles[:2] + tuple(created_roles):
                if db.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", [role]).fetchone():
                    db.execute(sql.SQL("DROP ROLE {}").format(sql.Identifier(role)))


def counts(admin):
    tables = ("adempiere.m_product", "adempiere.m_product_category", "adempiere.c_uom", "adempiere.c_taxcategory",
              "poc_registration.registration_request", "poc_registration.registration_audit", "poc_registration.indexing_job")
    with psycopg.connect(admin) as db:
        return {table: db.execute(sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(*table.split(".")))).fetchone()[0] for table in tables}


def test_real_registration_atomic_masters_product_audit_job_and_null_weight(registration_db):
    admin, store, _ = registration_db
    before = counts(admin); draft = sample(); suffix = uuid4().hex[:6]
    draft.update(category={"new": {"code": "CAT"+suffix, "name": "観葉植物"+suffix}},
        uom={"new": {"code": "PKG", "name": "1鉢"+suffix}}, tax={"new": {"name": "園芸課税"+suffix}})
    assert store.check(draft) == []
    result = store.register(uuid4(), draft, "rule-v1:" + "a"*600)
    assert result["code"] == draft["code"] and result["index_status"] == "pending"
    after = counts(admin)
    assert all(after[table] == before[table]+1 for table in before)
    product = store.eligible([result["product_id"]])[0]
    assert product["weight"] is None and product["pack"] == 1 and product["uom_name"].startswith("1鉢")
    with psycopg.connect(admin) as db:
        assert db.execute("SELECT ad_client_id,ad_org_id,createdby,updatedby FROM adempiere.m_product WHERE m_product_id=%s", [result["product_id"]]).fetchone() == (11,11,101,101)


def test_real_replay_without_rules_service_and_conflicts(registration_db):
    _, store, _ = registration_db
    request_id=uuid4(); draft=sample(); calls=[]
    expected=store.register(request_id,draft,"v1",validate=lambda: calls.append(1))
    assert store.register(request_id,draft,"v1",validate=lambda: pytest.fail("Replay must not need S3")) == expected
    assert calls == [1] and store.status(request_id) == expected
    for changed,version in (({**draft,"name":"別の商品"},"v1"),(draft,"v2")):
        with pytest.raises(RegistrationProblem) as caught: store.register(request_id,changed,version)
        assert caught.value.code == "IDEMPOTENCY_CONFLICT"
    assert store.status(uuid4()) is None


def test_real_callback_failure_and_db_failure_roll_back_all_writes(registration_db):
    admin,store,_=registration_db
    before=counts(admin)
    def reject(): raise RuntimeError("rule-version-changed")
    with pytest.raises(RuntimeError,match="rule-version-changed"):
        store.register(uuid4(),sample(),"v1",validate=reject)
    assert counts(admin)==before
    draft=sample("GW-ROLL"); draft["category"]={"new":{"code":"ROLL","name":"ロールバック専用"}}
    with psycopg.connect(admin) as db:
        sequence_before=db.execute("SELECT name,currentnext FROM adempiere.ad_sequence WHERE lower(name) IN ('m_product','m_product_category') ORDER BY name").fetchall()
        db.execute("ALTER TABLE adempiere.m_product ADD CONSTRAINT registration_test_failure CHECK(value<>'GW-ROLL')")
    try:
        with pytest.raises(RegistrationProblem): store.register(uuid4(),draft,"v1")
        assert counts(admin)==before
        with psycopg.connect(admin) as db:
            assert db.execute("SELECT name,currentnext FROM adempiere.ad_sequence WHERE lower(name) IN ('m_product','m_product_category') ORDER BY name").fetchall()==sequence_before
    finally:
        with psycopg.connect(admin) as db: db.execute("ALTER TABLE adempiere.m_product DROP CONSTRAINT registration_test_failure")


def test_real_concurrent_same_request_exactly_once_and_duplicate_code(registration_db):
    admin,store,_=registration_db
    before=counts(admin); draft=sample(); request_id=uuid4(); calls=[]
    def register(_): return store.register(request_id,draft,"v1",validate=lambda:calls.append(1))
    with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(register,range(2)))
    assert results[0]==results[1] and calls==[1]
    assert counts(admin)["adempiere.m_product"]==before["adempiere.m_product"]+1
    with pytest.raises(RegistrationProblem) as caught: store.register(uuid4(),draft,"v1")
    assert any(i["rule_id"]=="CODE-01" for i in caught.value.issues)


def test_real_policy_references_and_narrow_role(registration_db):
    admin,store,_=registration_db
    draft=sample(); draft["category"]=9999999999
    assert any(i["field"]=="category" and i["rule_id"]=="REF-01" for i in store.check(draft))
    with store._connection() as db:
        assert db.execute("SELECT current_user AS name").fetchone()["name"]=="poc_registration_api"
    with psycopg.connect(admin) as db:
        assert db.execute("SELECT has_table_privilege('poc_registration_api','adempiere.m_product','INSERT,UPDATE,DELETE'),has_table_privilege('poc_registration_api','adempiere.ad_sequence','UPDATE'),has_table_privilege('poc_registration_api','poc_registration.registration_request','INSERT,UPDATE,DELETE')").fetchone()==(False,False,False)
        assert not db.execute("SELECT has_table_privilege('poc_idempiere_reader','adempiere.m_product','INSERT,UPDATE,DELETE')").fetchone()[0]
    for table,identity in (("ad_client",11),("ad_org",11),("ad_user",101)):
        with psycopg.connect(admin) as db:
            db.execute(sql.SQL("UPDATE adempiere.{} SET isactive='N' WHERE {}=%s").format(sql.Identifier(table),sql.Identifier(table+"_id")),[identity])
        try:
            with pytest.raises(RegistrationProblem) as caught: store.register(uuid4(),sample(),"v1")
            assert caught.value.code=="REGISTRATION_POLICY_INVALID"
        finally:
            with psycopg.connect(admin) as db:
                db.execute(sql.SQL("UPDATE adempiere.{} SET isactive='Y' WHERE {}=%s").format(sql.Identifier(table),sql.Identifier(table+"_id")),[identity])


def test_real_sequence_maximum_and_invalid_increment(registration_db):
    admin,store,_=registration_db
    with psycopg.connect(admin) as db:
        maximum=db.execute("SELECT max(m_product_id) FROM adempiere.m_product").fetchone()[0]
        db.execute("UPDATE adempiere.ad_sequence SET currentnext=1 WHERE lower(name)='m_product' AND istableid='Y'")
    result=store.register(uuid4(),sample(),"v1")
    assert result["product_id"]==maximum+1
    with psycopg.connect(admin) as db:
        assert db.execute("SELECT currentnext FROM adempiere.ad_sequence WHERE lower(name)='m_product' AND istableid='Y'").fetchone()[0]==result["product_id"]+1
        db.execute("UPDATE adempiere.ad_sequence SET incrementno=2 WHERE lower(name)='m_product' AND istableid='Y'")
    before=counts(admin)
    try:
        with pytest.raises(RegistrationProblem) as caught: store.register(uuid4(),sample(),"v1")
        assert caught.value.code=="REGISTRATION_SEQUENCE_INVALID" and counts(admin)==before
    finally:
        with psycopg.connect(admin) as db: db.execute("UPDATE adempiere.ad_sequence SET incrementno=1 WHERE lower(name)='m_product' AND istableid='Y'")


def test_real_master_cross_scope_and_eligible_live_revalidation(registration_db):
    admin,store,_=registration_db
    with psycopg.connect(admin) as db:
        db.execute("INSERT INTO adempiere.m_product_category(m_product_category_id,ad_client_id,ad_org_id,createdby,updatedby,value,name,plannedmargin) VALUES(9999999998,0,11,101,101,'CROSS','Wrong scope',0)")
    try:
        draft=sample();draft["category"]=9999999998
        assert any(i["rule_id"]=="REF-01" for i in store.check(draft))
        assert 9999999998 not in [m["id"] for m in store.masters()["category"]]
    finally:
        with psycopg.connect(admin) as db: db.execute("DELETE FROM adempiere.m_product_category WHERE m_product_category_id=9999999998")
    result=store.register(uuid4(),sample(),"v1")
    assert store.eligible([result["product_id"]])
    with psycopg.connect(admin) as db: db.execute("UPDATE adempiere.m_product SET isactive='N' WHERE m_product_id=%s",[result["product_id"]])
    assert store.eligible([result["product_id"]])==[]


def test_real_outbox_leases_and_stale_failure_never_overwrites_success(registration_db):
    _,store,_=registration_db
    result=store.register(uuid4(),sample(),"v1"); product_id=result["product_id"]
    with ThreadPoolExecutor(max_workers=2) as pool: batches=list(pool.map(lambda _:store.pending(1000),range(2)))
    all_ids=[job["product_id"] for batch in batches for job in batch]
    assert len(all_ids)==len(set(all_ids)) and product_id in all_ids
    job=next(job for batch in batches for job in batch if job["product_id"]==product_id)
    assert not store.mark_index_failed(product_id,"FAILED",str(uuid4()))
    assert store.mark_indexed(product_id,job["lease_token"])
    assert not store.mark_index_failed(product_id,"FAILED",job["lease_token"])
    assert store.status(uuid4()) is None
    assert product_id not in [j["product_id"] for j in store.pending()]


def test_real_baseline_keeps_original_rows_and_catches_unknown_additions(registration_db):
    admin,store,_=registration_db
    path=ROOT/"local/opensearch"; sys.path.insert(0,str(path))
    try:
        from seed_data import baseline,registered_product_ids
        with psycopg.connect(admin,row_factory=dict_row) as db: before=baseline(db)
        result=store.register(uuid4(),sample(),"v1")
        with psycopg.connect(admin,row_factory=dict_row) as db:
            assert result["product_id"] in registered_product_ids(db)
            assert baseline(db)==before
            db.execute("UPDATE adempiere.m_product SET name=name||' unknown edit' WHERE m_product_id=(SELECT min(m_product_id) FROM adempiere.m_product)")
            assert baseline(db)!=before
            db.rollback()
            # An unregistered row is never excluded merely because its code uses GW-.
            db.execute("INSERT INTO adempiere.m_product(m_product_id,ad_client_id,ad_org_id,createdby,updatedby,value,name,c_uom_id,m_product_category_id,c_taxcategory_id) VALUES(9999999998,11,11,101,101,'GW-UNKN','未登録行',100,106,107)")
            assert baseline(db)!=before
            db.rollback()
    finally: sys.path.remove(str(path))


def test_real_original_japanese_seed_rerun_preserves_baseline_with_registry(registration_db,monkeypatch):
    admin,store,directory=registration_db
    path=ROOT/"local/opensearch";sys.path.insert(0,str(path))
    try:
        import seed_data
        monkeypatch.setattr(seed_data,"STATE",directory/"legacy-lab")
        monkeypatch.setattr(seed_data,"connect",lambda write=False:psycopg.connect(admin,row_factory=dict_row))
        first=seed_data.seed()
        assert first["action"]=="inserted" and first["counts"]["m_product"]==200
        original_fingerprint=(seed_data.STATE/"baseline.json").read_bytes()
        store.register(uuid4(),sample(),"v1")
        second=seed_data.seed()
        assert second["action"]=="reused" and second["ids"]==first["ids"]
        assert (seed_data.STATE/"baseline.json").read_bytes()==original_fingerprint
        rows,_,_=seed_data.export_rows()
        assert len(rows["m_product"])==200 and len(rows["m_promotion"] )==200
        with psycopg.connect(admin,row_factory=dict_row) as db:
            total=db.execute("SELECT count(*) AS n FROM adempiere.m_product").fetchone()["n"]
            assert total==255+len(seed_data.registered_product_ids(db))
    finally:sys.path.remove(str(path))
