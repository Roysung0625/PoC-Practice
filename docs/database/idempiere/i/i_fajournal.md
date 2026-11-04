# i_fajournal — 고정자산 분개 가져오기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.i_fajournal` |
| 한국어 논리명(문서용 해석) | 고정자산 분개 가져오기 |
| 원본 논리명 | FA Journal |
| 원본 사전 ID | 53117 |
| 분류 | `i` — 데이터 가져오기 준비 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 72 |
| 나가는 FK / 들어오는 FK | 24 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

자산 식별자와 감가상각 여부, 분개 차대변 금액을 포함한 고정자산 관련 분개 가져오기 데이터를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `i_fajournal_key` | `i_fajournal_id` |
| UNIQUE | `i_fajournal_uu_idx` | `i_fajournal_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `c_subacct_id` | Sub Account | numeric(10,0) | 허용 | — | — | Sub account for Element Value |
| 2 | `userelement1_id` | User Column 1 | numeric(10,0) | 허용 | — | — | User defined accounting Element |
| 3 | `userelement2_id` | User Column 2 | numeric(10,0) | 허용 | — | — | User defined accounting Element |
| 4 | `i_fajournal_id` | FA Journal | numeric(10,0) | 불가 | 예 | — | — |
| 5 | `ad_client_id` | Tenant | numeric(10,0) | 허용 | — | — | Tenant for this installation. |
| 6 | `ad_orgdoc_id` | Document Org | numeric(10,0) | 허용 | — | — | Document Organization (independent from account organization) |
| 7 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 8 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 9 | `a_asset_id` | Asset | numeric(10,0) | 허용 | — | — | Asset used internally or by customers |
| 10 | `a_entry_type` | Entry Type | character varying(3) | 허용 | — | — | — |
| 11 | `accountvalue` | Account Key | character varying(80) | 허용 | — | — | Key of Account Element |
| 12 | `account_id` | Account | numeric(10,0) | 허용 | — | — | Account used |
| 13 | `acctschemaname` | Account Schema Name | character varying(120) | 허용 | — | — | Name of the Accounting Schema |
| 14 | `amtacctcr` | Accounted Credit | numeric | 허용 | — | — | Accounted Credit Amount |
| 15 | `amtacctdr` | Accounted Debit | numeric | 허용 | — | — | Accounted Debit Amount |
| 16 | `amtsourcecr` | Source Credit | numeric | 허용 | — | — | Source Credit Amount |
| 17 | `amtsourcedr` | Source Debit | numeric | 허용 | — | — | Source Debit Amount |
| 18 | `bpartnervalue` | Business Partner Key | character varying(80) | 허용 | — | — | Key of the Business Partner |
| 19 | `batchdescription` | Batch Description | character varying(510) | 허용 | — | — | Description of the Batch |
| 20 | `batchdocumentno` | Batch Document No | character varying(60) | 허용 | — | — | Document Number of the Batch |
| 21 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 허용 | — | — | Rules for accounting |
| 22 | `gl_budget_id` | Budget | numeric(10,0) | 허용 | — | — | General Ledger Budget |
| 23 | `doctypename` | Document Type Name | character varying(120) | 허용 | — | — | Name of the Document Type |
| 24 | `description` | Description | character varying(510) | 허용 | — | — | Optional short description of the record |
| 25 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 26 | `currencyratetype` | Currency Rate Type | character(1) | 허용 | — | — | — |
| 27 | `currencyrate` | Rate | numeric | 허용 | — | — | Currency Conversion Rate |
| 28 | `createdby` | Created By | numeric(10,0) | 허용 | — | — | User who created this records |
| 29 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 30 | `conversiontypevalue` | Currency Type Key | character varying(40) | 허용 | — | — | Key value for the Currency Conversion Rate Type |
| 31 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 32 | `processed` | Processed | character(1) | 허용 | — | — | The document has been processed |
| 33 | `postingtype` | Posting Type | character(1) | 허용 | — | — | The type of posted amount for the transaction |
| 34 | `orgvalue` | Org Key | character varying(40) | 허용 | — | — | Key of the Organization |
| 35 | `orgtrxvalue` | Trx Org Key | character varying(40) | 허용 | — | — | Key of the Transaction Organization |
| 36 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 37 | `line` | Line No | numeric(10,0) | 허용 | — | — | Unique line for this document |
| 38 | `journaldocumentno` | Journal Document No | character varying(60) | 허용 | — | — | Document number of the Journal |
| 39 | `isdepreciated` | Depreciate | character varying(1) | 허용 | — | — | The asset will be depreciated |
| 40 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | — | User defined list element #2 |
| 41 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | — | User defined list element #1 |
| 42 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | — | User who updated this records |
| 43 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 44 | `upc` | UPC/EAN | character varying(30) | 허용 | — | — | Bar Code (Universal Product Code or its superset European Article Number) |
| 45 | `sku` | SKU | character varying(30) | 허용 | — | — | Stock Keeping Unit |
| 46 | `qty` | Quantity | numeric | 허용 | — | — | Quantity |
| 47 | `projectvalue` | Project Key | character varying(40) | 허용 | — | — | Key of the Project |
| 48 | `productvalue` | Product Key | character varying(40) | 허용 | — | — | Key of the Product |
| 49 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 50 | `i_isimported` | Imported | character(1) | 불가 | — | — | Has this import been processed |
| 51 | `i_errormsg` | Import Error Message | character varying(2000) | 허용 | — | — | Messages generated from import process |
| 52 | `iso_code` | ISO Currency Code | character varying(3) | 허용 | — | — | Three letter ISO 4217 Code of the Currency |
| 53 | `gl_journal_id` | Journal | numeric(10,0) | 허용 | — | — | General Ledger Journal |
| 54 | `gl_journalline_id` | Journal Line | numeric(10,0) | 허용 | — | — | General Ledger Journal Line |
| 55 | `gl_journalbatch_id` | Journal Batch | numeric(10,0) | 허용 | — | — | General Ledger Journal Batch |
| 56 | `gl_category_id` | GL Category | numeric(10,0) | 허용 | — | — | General Ledger Category |
| 57 | `clientvalue` | Tenant Key | character varying(80) | 허용 | — | — | Key of the Tenant |
| 58 | `categoryname` | Category Name | character varying(120) | 허용 | — | — | Name of the Category |
| 59 | `c_validcombination_id` | Combination | numeric(10,0) | 허용 | — | — | Valid Account Combination |
| 60 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 61 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 62 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 63 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 64 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 허용 | — | — | Currency Conversion Rate Type |
| 65 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 66 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 67 | `c_locfrom_id` | Location From | numeric(10,0) | 허용 | — | — | Location that inventory was moved from |
| 68 | `c_locto_id` | Location To | numeric(10,0) | 허용 | — | — | Location that inventory was moved to |
| 69 | `c_period_id` | Period | numeric(10,0) | 허용 | — | — | Period of the Calendar |
| 70 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 71 | `c_salesregion_id` | Sales Region | numeric(10,0) | 허용 | — | — | Sales coverage region |
| 72 | `i_fajournal_uu` | I_FAJournal_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 24개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["c_acctschema"]
    n2["c_activity"]
    n3["c_bpartner"]
    n4["c_campaign"]
    n5["c_currency"]
    n6["c_doctype"]
    n7["c_elementvalue"]
    n8["c_location"]
    n9["i_fajournal"]
    n9 -->|"account_id → c_elementvalue_id"| n7
    n9 -->|"ad_orgdoc_id → ad_org_id"| n0
    n9 -->|"ad_orgtrx_id → ad_org_id"| n0
    n9 -->|"c_acctschema_id → c_acctschema_id"| n1
    n9 -->|"c_activity_id → c_activity_id"| n2
    n9 -->|"c_bpartner_id → c_bpartner_id"| n3
    n9 -->|"c_campaign_id → c_campaign_id"| n4
    n9 -->|"c_currency_id → c_currency_id"| n5
    n9 -->|"c_doctype_id → c_doctype_id"| n6
    n9 -->|"c_locfrom_id → c_location_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `account_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.account_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `account_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgdoc_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.adorgdoc_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `ad_orgdoc_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.adorgtrx_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cacctschema_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cactivity_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cbpartner_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.ccampaign_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.ccurrency_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cdoctype_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocfrom_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.clocfrom_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_locfrom_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocto_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.clocto_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_locto_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cperiod_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cperiod_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_period_id` | [`c_period`](../c/c_period.md) | `c_period_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cproject_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.csalesregion_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_salesregion_id` | [`c_salesregion`](../c/c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuom_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cuom_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cvalidcombination_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.cvalidcombination_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `c_validcombination_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glbudget_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.glbudget_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `gl_budget_id` | [`gl_budget`](../gl/gl_budget.md) | `gl_budget_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `glcategory_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.glcategory_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `gl_category_id` | [`gl_category`](../gl/gl_category.md) | `gl_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `gljournal_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.gljournal_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `gl_journal_id` | [`gl_journal`](../gl/gl_journal.md) | `gl_journal_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `gljournalbatch_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.gljournalbatch_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `gl_journalbatch_id` | [`gl_journalbatch`](../gl/gl_journalbatch.md) | `gl_journalbatch_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `gljournalline_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.gljournalline_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `gl_journalline_id` | [`gl_journalline`](../gl/gl_journalline.md) | `gl_journalline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.mproduct_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user1_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.user1_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `user1_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user2_ifajournal` <!-- FK_OUT: adempiere.i_fajournal.user2_ifajournal --> | [`i_fajournal`](i_fajournal.md) | `user2_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
