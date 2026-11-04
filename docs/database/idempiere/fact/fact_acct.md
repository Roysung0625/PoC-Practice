# fact_acct — 전기 회계 분개

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.fact_acct` |
| 한국어 논리명(문서용 해석) | 전기 회계 분개 |
| 원본 논리명 | Accounting Fact |
| 원본 사전 ID | 270 |
| 분류 | `fact` — 회계 사실·집계 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 57 |
| 나가는 FK / 들어오는 FK | 33 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

업무 문서에서 전기된 회계 분개를 계정·회계 스키마·기간 및 분석 요소별로 저장한다. 거래통화와 회계통화의 차변·대변 금액 및 원 문서 테이블·레코드·행 식별자를 포함한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `fact_acct_pkey` | `fact_acct_id` |
| UNIQUE | `fact_acct_uu_idx` | `fact_acct_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `fact_acct_id` | Accounting Fact | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | — | — | Rules for accounting |
| 10 | `account_id` | Account | numeric(10,0) | 불가 | — | — | Account used |
| 11 | `datetrx` | Transaction Date | timestamp without time zone | 불가 | — | — | Transaction Date |
| 12 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 13 | `c_period_id` | Period | numeric(10,0) | 허용 | — | — | Period of the Calendar |
| 14 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 15 | `record_id` | Record ID | numeric(10,0) | 불가 | — | — | Direct internal record ID |
| 16 | `line_id` | Line ID | numeric(10,0) | 허용 | — | — | Transaction line ID (internal) |
| 17 | `gl_category_id` | GL Category | numeric(10,0) | 허용 | — | — | General Ledger Category |
| 18 | `gl_budget_id` | Budget | numeric(10,0) | 허용 | — | — | General Ledger Budget |
| 19 | `c_tax_id` | Tax | numeric(10,0) | 허용 | — | — | Tax identifier |
| 20 | `m_locator_id` | Locator | numeric(10,0) | 허용 | — | — | Warehouse Locator |
| 21 | `postingtype` | Posting Type | character(1) | 불가 | — | — | The type of posted amount for the transaction |
| 22 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 23 | `amtsourcedr` | Source Debit | numeric | 불가 | — | 0 | Source Debit Amount |
| 24 | `amtsourcecr` | Source Credit | numeric | 불가 | — | 0 | Source Credit Amount |
| 25 | `amtacctdr` | Accounted Debit | numeric | 불가 | — | 0 | Accounted Debit Amount |
| 26 | `amtacctcr` | Accounted Credit | numeric | 불가 | — | 0 | Accounted Credit Amount |
| 27 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 28 | `qty` | Quantity | numeric | 허용 | — | 0 | Quantity |
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
| 52 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | NULL::numeric | Additional document charges |
| 53 | `m_warehouse_id` | Warehouse | numeric(10,0) | 허용 | — | NULL::numeric | Storage Warehouse and Service Point |
| 54 | `c_employee_id` | Employee | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 55 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 56 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 57 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | NULL::numeric | Product Attribute Set Instance |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 36개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["ad_client"]
    n2["ad_org"]
    n3["ad_table"]
    n4["c_bpartner"]
    n5["c_currency"]
    n6["c_location"]
    n7["c_project"]
    n8["fact_acct"]
    n8 -->|"a_asset_id → a_asset_id"| n0
    n8 -->|"ad_client_id → ad_client_id"| n1
    n8 -->|"ad_org_id → ad_org_id"| n2
    n8 -->|"ad_orgtrx_id → ad_org_id"| n2
    n8 -->|"ad_table_id → ad_table_id"| n3
    n8 -->|"c_bpartner_id → c_bpartner_id"| n4
    n8 -->|"c_currency_id → c_currency_id"| n5
    n8 -->|"c_locfrom_id → c_location_id"| n6
    n8 -->|"c_locto_id → c_location_id"| n6
    n8 -->|"c_project_id → c_project_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aasset_factacct` <!-- FK_OUT: adempiere.fact_acct.aasset_factacct --> | [`fact_acct`](fact_acct.md) | `a_asset_id` | [`a_asset`](../a/a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ac_client_fact_acct` <!-- FK_OUT: adempiere.fact_acct.ac_client_fact_acct --> | [`fact_acct`](fact_acct.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_org_fact_acct` <!-- FK_OUT: adempiere.fact_acct.ad_org_fact_acct --> | [`fact_acct`](fact_acct.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_orgtrx_fact_acct` <!-- FK_OUT: adempiere.fact_acct.ad_orgtrx_fact_acct --> | [`fact_acct`](fact_acct.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_factacct` <!-- FK_OUT: adempiere.fact_acct.adtable_factacct --> | [`fact_acct`](fact_acct.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_buspartner_fact_acct` <!-- FK_OUT: adempiere.fact_acct.c_buspartner_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_currency_fact_acct` <!-- FK_OUT: adempiere.fact_acct.c_currency_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_locationfrom_fact_acct` <!-- FK_OUT: adempiere.fact_acct.c_locationfrom_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_locfrom_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_locationto_fact_acct` <!-- FK_OUT: adempiere.fact_acct.c_locationto_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_locto_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_project_fact_acct` <!-- FK_OUT: adempiere.fact_acct.c_project_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_salesregion_factacct` <!-- FK_OUT: adempiere.fact_acct.c_salesregion_factacct --> | [`fact_acct`](fact_acct.md) | `c_salesregion_id` | [`c_salesregion`](../c/c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_uom_fact_acct` <!-- FK_OUT: adempiere.fact_acct.c_uom_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_factacct` <!-- FK_OUT: adempiere.fact_acct.cacctschema_factacct --> | [`fact_acct`](fact_acct.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_factacct` <!-- FK_OUT: adempiere.fact_acct.cactivity_factacct --> | [`fact_acct`](fact_acct.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_factacct` <!-- FK_OUT: adempiere.fact_acct.ccharge_factacct --> | [`fact_acct`](fact_acct.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_factacct` <!-- FK_OUT: adempiere.fact_acct.ccostcenter_factacct --> | [`fact_acct`](fact_acct.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_factacct` <!-- FK_OUT: adempiere.fact_acct.cdepartment_factacct --> | [`fact_acct`](fact_acct.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalue_factacct` <!-- FK_OUT: adempiere.fact_acct.celementvalue_factacct --> | [`fact_acct`](fact_acct.md) | `account_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser1_factacct` <!-- FK_OUT: adempiere.fact_acct.celementvalueuser1_factacct --> | [`fact_acct`](fact_acct.md) | `user1_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `celementvalueuser2_factacct` <!-- FK_OUT: adempiere.fact_acct.celementvalueuser2_factacct --> | [`fact_acct`](fact_acct.md) | `user2_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cemployee_factacct` <!-- FK_OUT: adempiere.fact_acct.cemployee_factacct --> | [`fact_acct`](fact_acct.md) | `c_employee_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_factacct` <!-- FK_OUT: adempiere.fact_acct.cperiod_factacct --> | [`fact_acct`](fact_acct.md) | `c_period_id` | [`c_period`](../c/c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojectphase_factacct` <!-- FK_OUT: adempiere.fact_acct.cprojectphase_factacct --> | [`fact_acct`](fact_acct.md) | `c_projectphase_id` | [`c_projectphase`](../c/c_projectphase.md) | `c_projectphase_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cprojecttask_factacct` <!-- FK_OUT: adempiere.fact_acct.cprojecttask_factacct --> | [`fact_acct`](fact_acct.md) | `c_projecttask_id` | [`c_projecttask`](../c/c_projecttask.md) | `c_projecttask_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `csubacct_factacct` <!-- FK_OUT: adempiere.fact_acct.csubacct_factacct --> | [`fact_acct`](fact_acct.md) | `c_subacct_id` | [`c_subacct`](../c/c_subacct.md) | `c_subacct_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ctax_factacct` <!-- FK_OUT: adempiere.fact_acct.ctax_factacct --> | [`fact_acct`](fact_acct.md) | `c_tax_id` | [`c_tax`](../c/c_tax.md) | `c_tax_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glbudget_factacct` <!-- FK_OUT: adempiere.fact_acct.glbudget_factacct --> | [`fact_acct`](fact_acct.md) | `gl_budget_id` | [`gl_budget`](../gl/gl_budget.md) | `gl_budget_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_factacct` <!-- FK_OUT: adempiere.fact_acct.glcategory_factacct --> | [`fact_acct`](fact_acct.md) | `gl_category_id` | [`gl_category`](../gl/gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `m_product_fact_acct` <!-- FK_OUT: adempiere.fact_acct.m_product_fact_acct --> | [`fact_acct`](fact_acct.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstance_factacct` <!-- FK_OUT: adempiere.fact_acct.mattributesetinstance_factacct --> | [`fact_acct`](fact_acct.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](../m/m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocator_factacct` <!-- FK_OUT: adempiere.fact_acct.mlocator_factacct --> | [`fact_acct`](fact_acct.md) | `m_locator_id` | [`m_locator`](../m/m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_factacct` <!-- FK_OUT: adempiere.fact_acct.mwarehouse_factacct --> | [`fact_acct`](fact_acct.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `so_campaign_fact_acct` <!-- FK_OUT: adempiere.fact_acct.so_campaign_fact_acct --> | [`fact_acct`](fact_acct.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `factacct_ctaxdeclacct` <!-- FK_IN: adempiere.c_taxdeclarationacct.factacct_ctaxdeclacct --> | [`c_taxdeclarationacct`](../c/c_taxdeclarationacct.md) | `fact_acct_id` | [`fact_acct`](fact_acct.md) | `fact_acct_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `factacct_factreconciliation` <!-- FK_IN: adempiere.fact_reconciliation.factacct_factreconciliation --> | [`fact_reconciliation`](fact_reconciliation.md) | `fact_acct_id` | [`fact_acct`](fact_acct.md) | `fact_acct_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `factacct_tinvoicegl` <!-- FK_IN: adempiere.t_invoicegl.factacct_tinvoicegl --> | [`t_invoicegl`](../t/t_invoicegl.md) | `fact_acct_id` | [`fact_acct`](fact_acct.md) | `fact_acct_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
