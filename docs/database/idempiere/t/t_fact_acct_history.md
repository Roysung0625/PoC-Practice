# t_fact_acct_history — 회계 전기 이력 자료

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.t_fact_acct_history` |
| 한국어 논리명(문서용 해석) | 회계 전기 이력 자료 |
| 원본 논리명 | Accounting Fact History |
| 원본 사전 ID | 200420 |
| 분류 | `t` — 작업·보고서용 보조 테이블 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 57 |
| 나가는 FK / 들어오는 FK | 0 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

회계 전기 레코드와 동일한 계정·차대변 금액·업무 차원 등의 이력 정보를 저장한다. 이력 생성 및 보존 조건은 확인이 필요하다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

PostgreSQL에 선언된 PRIMARY KEY·UNIQUE 제약조건이 없습니다. 별도 고유 인덱스 유무는 이 목록의 범위가 아닙니다.

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `fact_acct_id` | Accounting Fact | numeric(10,0) | 허용 | — | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 허용 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 허용 | — | — | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 허용 | — | — | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 허용 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 허용 | — | — | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | — | User who updated this records |
| 9 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | — | Rules for accounting |
| 10 | `account_id` | Account | numeric(10,0) | 허용 | — | — | Account used |
| 11 | `datetrx` | Transaction Date | timestamp without time zone | 허용 | — | — | Transaction Date |
| 12 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 13 | `c_period_id` | Period | numeric(10,0) | 허용 | — | — | Period of the Calendar |
| 14 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | — | Database Table information |
| 15 | `record_id` | Record ID | numeric(10,0) | 허용 | — | — | Direct internal record ID |
| 16 | `line_id` | Line ID | numeric(10,0) | 허용 | — | — | Transaction line ID (internal) |
| 17 | `gl_category_id` | GL Category | numeric(10,0) | 허용 | — | — | General Ledger Category |
| 18 | `gl_budget_id` | Budget | numeric(10,0) | 허용 | — | — | General Ledger Budget |
| 19 | `c_tax_id` | Tax | numeric(10,0) | 허용 | — | — | Tax identifier |
| 20 | `m_locator_id` | Locator | numeric(10,0) | 허용 | — | — | Warehouse Locator |
| 21 | `postingtype` | Posting Type | character(1) | 허용 | — | — | The type of posted amount for the transaction |
| 22 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 23 | `amtsourcedr` | Source Debit | numeric | 허용 | — | — | Source Debit Amount |
| 24 | `amtsourcecr` | Source Credit | numeric | 허용 | — | — | Source Credit Amount |
| 25 | `amtacctdr` | Accounted Debit | numeric | 허용 | — | — | Accounted Debit Amount |
| 26 | `amtacctcr` | Accounted Credit | numeric | 허용 | — | — | Accounted Credit Amount |
| 27 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 28 | `qty` | Quantity | numeric | 허용 | — | — | Quantity |
| 29 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 30 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 31 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 32 | `c_locfrom_id` | Location From | numeric(10,0) | 허용 | — | — | Location that inventory was moved from |
| 33 | `c_locto_id` | Location To | numeric(10,0) | 허용 | — | — | Location that inventory was moved to |
| 34 | `c_salesregion_id` | Sales Region | numeric(10,0) | 허용 | — | — | Sales coverage region |
| 35 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 36 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 37 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 38 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | — | User defined list element #1 |
| 39 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | — | User defined list element #2 |
| 40 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 41 | `a_asset_id` | Asset | numeric(10,0) | 허용 | — | — | Asset used internally or by customers |
| 42 | `c_subacct_id` | Sub Account | numeric(10,0) | 허용 | — | — | Sub account for Element Value |
| 43 | `userelement1_id` | User Column 1 | numeric(10,0) | 허용 | — | — | User defined accounting Element |
| 44 | `userelement2_id` | User Column 2 | numeric(10,0) | 허용 | — | — | User defined accounting Element |
| 45 | `c_projectphase_id` | Project Phase | numeric(10,0) | 허용 | — | — | Phase of a Project |
| 46 | `c_projecttask_id` | Project Task | numeric(10,0) | 허용 | — | — | Actual Project Task in a Phase |
| 47 | `fact_acct_uu` | Fact_Acct_UU | uuid | 허용 | — | — | — |
| 48 | `customfieldtext1` | Text Column 1 | character varying(255) | 허용 | — | NULL::character varying | User defined accounting Element |
| 49 | `customfieldtext2` | Text Column 2 | character varying(255) | 허용 | — | NULL::character varying | User defined accounting Element |
| 50 | `customfieldtext3` | Text Column 3 | character varying(255) | 허용 | — | NULL::character varying | User defined accounting Element |
| 51 | `customfieldtext4` | Text Column 4 | character varying(255) | 허용 | — | NULL::character varying | User defined accounting Element |
| 52 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 53 | `m_warehouse_id` | Warehouse | numeric(10,0) | 허용 | — | — | Storage Warehouse and Service Point |
| 54 | `c_employee_id` | Employee | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 55 | `c_department_id` | Department | numeric(10,0) | 허용 | — | — | — |
| 56 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | — | — |
| 57 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | — | Product Attribute Set Instance |

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
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
