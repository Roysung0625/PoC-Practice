# t_cashflow — 현금 흐름 보고 자료

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.t_cashflow` |
| 한국어 논리명(문서용 해석) | 현금 흐름 보고 자료 |
| 원본 논리명 | T_CashFlow_ID |
| 원본 사전 ID | 53299 |
| 분류 | `t` — 작업·보고서용 보조 테이블 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 30 |
| 나가는 FK / 들어오는 FK | 0 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

송장·주문·현금 계획 등을 원천으로 한 금액·거래일·확률을 실행 건별로 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `t_cashflow_key` | `t_cashflow_id` |
| UNIQUE | `t_cashflow_uu_idx` | `t_cashflow_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_pinstance_id` | Process Instance | numeric(10,0) | 불가 | — | — | Instance of the process |
| 4 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | NULL::numeric | Rules for accounting |
| 5 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | NULL::numeric | Business Activity |
| 6 | `cashflowsource` | Cash Flow Source | character(1) | 허용 | — | NULL::bpchar | — |
| 7 | `cashflowtype` | Cash Flow Type | character(1) | 허용 | — | NULL::bpchar | — |
| 8 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 9 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | NULL::numeric | Marketing Campaign |
| 10 | `c_cashplanline_id` | Cash Plan Line | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 11 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | NULL::numeric | Additional document charges |
| 12 | `c_elementvalue_id` | Account Element | numeric(10,0) | 허용 | — | NULL::numeric | Account Element |
| 13 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | NULL::numeric | Invoice Identifier |
| 14 | `c_order_id` | Order | numeric(10,0) | 허용 | — | NULL::numeric | Order |
| 15 | `c_project_id` | Project | numeric(10,0) | 허용 | — | NULL::numeric | Financial Project |
| 16 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 17 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 18 | `dateto` | Date To | timestamp without time zone | 허용 | — | — | End date of a date range |
| 19 | `datetrx` | Transaction Date | timestamp without time zone | 불가 | — | — | Transaction Date |
| 20 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 21 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 22 | `issotrx` | Sales Transaction | character(1) | 불가 | — | — | This is a Sales Transaction |
| 23 | `linetotalamt` | Line Total | numeric | 허용 | — | — | Total line amount incl. Tax |
| 24 | `m_product_id` | Product | numeric(10,0) | 허용 | — | NULL::numeric | Product, Service, Item |
| 25 | `name` | Name | character varying(60) | 허용 | — | NULL::character varying | Alphanumeric identifier of the entity |
| 26 | `probability` | Probability | numeric | 허용 | — | — | — |
| 27 | `t_cashflow_id` | T_CashFlow_ID | numeric(10,0) | 불가 | 예 | NULL::numeric | — |
| 28 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 29 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 30 | `t_cashflow_uu` | T_CashFlow_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

### 이 테이블이 참조하는 부모 — 나가는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `issotrx`가 있습니다. 판매(`Y`)와 구매(`N`)를 구분해서 분석합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
