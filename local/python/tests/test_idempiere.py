import json
import time

import psycopg
from psycopg import sql
import pytest
from fastapi.testclient import TestClient

from poc.agent import sample_plan, AgentPlanner
from poc.api import create_app
from poc.catalog import selected_catalog, normalized_catalog, table_index, IDEMPIERE_INVOICE_RULE
from poc.config import PocError, ROOT
from poc.db import execute_query
from poc.sql_policy import validate_sql


@pytest.fixture
def erp_catalog():
    names = ['c_invoice', 'c_invoiceline', 'c_currency', 'c_doctype']
    return {'dataset_id': 'idempiere', 'dataset_label': 'GardenWorld test', 'schema': 'adempiere', 'schema_version': 'erp-v1',
            'tables': {name: [{'name': 'id', 'type': 'numeric'}] for name in names},
            'table_details': {name: {'label': name, 'description': '', 'rows': 1} for name in names},
            'relationships': [['c_invoice', 'c_currency_id', 'c_currency', 'c_currency_id']],
            'tenant': {'ad_client_id': 11}, 'business_rules': [], 'sample_question': '확정 청구액을 월별·통화별로 보여줘'}


def test_erp_policy_keeps_schema_and_function_boundary(erp_catalog):
    tables = set(erp_catalog['tables'])
    validate_sql('SELECT count(*) FROM adempiere.c_invoice', {}, tables, schema='adempiere')
    for query in ['SELECT * FROM tpch.c_invoice', 'SELECT * FROM pg_catalog.pg_class', 'SELECT adempiere.acctbalance(1,2,3)',
                  'DELETE FROM adempiere.c_invoice', 'SELECT * FROM adempiere.unknown_table']:
        with pytest.raises(PocError, match='SQL_REJECTED'):
            validate_sql(query, {}, tables, schema='adempiere')


def test_table_selection_expands_fk_and_rejects_invented_tables(erp_catalog):
    result = selected_catalog(erp_catalog, ['c_invoice'])
    assert set(result['tables']) == {'c_invoice', 'c_currency'}
    for names in [[], ['imaginary'], [123], ['c_invoice'] * 13]:
        with pytest.raises(PocError, match='SCHEMA_SELECTION_INVALID'):
            selected_catalog(erp_catalog, names)


def test_planner_uses_selected_catalog_without_changing_full_schema_hash(erp_catalog, monkeypatch):
    planner = AgentPlanner('test', {}, {})
    calls = []
    def invoke(payload):
        calls.append(payload)
        if payload['phase'] == 'select_tables':
            return {'tables': ['c_invoice', 'c_currency', 'c_doctype']}
        return {'plan': sample_plan(erp_catalog)}
    monkeypatch.setattr(planner, 'invoke', invoke)
    result = planner.plan('청구액', erp_catalog)
    assert [c['phase'] for c in calls] == ['select_tables', 'plan']
    assert 'c_invoiceline' not in calls[1]['catalog']['tables']
    assert 'do not use TO_CHAR' in calls[1]['catalog']['business_rules'][-1]
    assert erp_catalog['business_rules'] == []
    assert result['schema_version'] == erp_catalog['schema_version']
    assert result['schema_selection']['total_tables'] == 4


def test_stale_business_rule_is_normalized_in_model_payload_without_mutation(erp_catalog, monkeypatch):
    stale = "c_invoice.totallines는 세전 청구액, grandtotal은 세금 포함 총액입니다. c_doctype.docbasetype='ARC'인 판매 대변전표는 차감합니다."
    erp_catalog['business_rules'] = [stale]
    before = json.dumps(erp_catalog, sort_keys=True, ensure_ascii=False)
    calls = []
    planner = AgentPlanner('test', {}, {})
    def invoke(payload):
        calls.append(payload)
        return {'tables': ['c_invoice', 'c_currency', 'c_doctype']} if payload['phase'] == 'select_tables' else {'plan': sample_plan(erp_catalog)}
    monkeypatch.setattr(planner, 'invoke', invoke)
    plan = planner.plan('문서 금액', erp_catalog)
    for payload in calls:
        assert IDEMPIERE_INVOICE_RULE in payload['catalog']['business_rules']
        assert stale not in payload['catalog']['business_rules']
    assert normalized_catalog(erp_catalog)['schema_version'] == plan['schema_version'] == 'erp-v1'
    assert json.dumps(erp_catalog, sort_keys=True, ensure_ascii=False) == before


def test_sample_counts_credit_memos_currencies_and_tenant_via_api(postgres_db, tmp_path, erp_catalog):
    admin, reader, role = postgres_db
    with psycopg.connect(admin) as db:
        db.execute('CREATE SCHEMA adempiere')
        db.execute('CREATE TABLE adempiere.c_currency (c_currency_id int, iso_code text)')
        db.execute('CREATE TABLE adempiere.c_doctype (c_doctype_id int, docbasetype text)')
        db.execute('CREATE TABLE adempiere.c_invoice (ad_client_id int, dateinvoiced date, c_currency_id int, c_doctype_id int, issotrx text, docstatus text, totallines numeric)')
        db.execute("INSERT INTO adempiere.c_currency VALUES (1,'USD'),(2,'EUR')")
        db.execute("INSERT INTO adempiere.c_doctype VALUES (1,'ARI'),(2,'ARC')")
        db.execute("""INSERT INTO adempiere.c_invoice VALUES
            (11,'2003-01-01',1,1,'Y','CO',100),(11,'2003-01-02',1,2,'Y','CL',20),
            (11,'2003-01-03',2,1,'Y','CO',30),(11,'2003-01-04',1,1,'Y','DR',999),
            (99,'2003-01-01',1,1,'Y','CO',999),(11,'2003-01-01',1,1,'N','CO',999)""")
        db.execute(sql.SQL('GRANT USAGE ON SCHEMA adempiere TO {}').format(sql.Identifier(role)))
        db.execute(sql.SQL('GRANT SELECT ON ALL TABLES IN SCHEMA adempiere TO {}').format(sql.Identifier(role)))
    path = tmp_path / 'catalog.json'
    path.write_text(json.dumps(erp_catalog))
    settings = {'root': ROOT, 'token': 'test', 'dsn': reader, 'journal': tmp_path / 'jobs.sqlite', 'catalog': path, 'agent_arn': '', 'profile': ''}
    with TestClient(create_app(settings), base_url='http://127.0.0.1') as client:
        client.headers['Authorization'] = 'Bearer test'
        assert client.get('/health').json()['dataset_id'] == 'idempiere'
        plan = client.post('/v1/plans', json={'mode': 'sample'}).json()
        approval = client.post('/v1/executions', json={'plan_id': plan['plan_id'], 'digest': plan['digest']}).json()
        for _ in range(100):
            job = client.get('/v1/jobs/' + approval['request_id']).json()
            if job['status'] in ('succeeded', 'failed'):
                break
            time.sleep(.02)
        assert job['result']['rows'] == [['2003-01-01', 'EUR', '30', 1], ['2003-01-01', 'USD', '80', 2]]
        path.write_text(json.dumps({**erp_catalog, 'schema_version': 'erp-v2'}))
        blocked = client.post('/v1/executions', json={'plan_id': plan['plan_id'], 'digest': plan['digest']}).json()
        assert blocked['error']['code'] == 'SCHEMA_CHANGED'
    with psycopg.connect(admin) as db:
        db.execute('DROP SCHEMA adempiere CASCADE')
