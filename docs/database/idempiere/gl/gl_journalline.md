# gl_journalline — 원장 분개 전표 명세

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.gl_journalline` |
| 한국어 논리명(문서용 해석) | 원장 분개 전표 명세 |
| 원본 논리명 | Journal Line |
| 원본 사전 ID | 226 |
| 분류 | `gl` — 총계정원장·예산·분개 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 50 |
| 나가는 FK / 들어오는 FK | 30 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

총계정원장 분개 전표의 개별 분개 행을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: General Ledger Journal Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `gl_journalline_pkey` | `gl_journalline_id` |
| UNIQUE | `gl_journalline_uu_idx` | `gl_journalline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `gl_journalline_id` | Journal Line | numeric(10,0) | 불가 | 예 | — | General Ledger Journal Line |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `gl_journal_id` | Journal | numeric(10,0) | 불가 | — | — | General Ledger Journal |
| 10 | `line` | Line No | numeric(10,0) | 불가 | — | — | Unique line for this document |
| 11 | `isgenerated` | Generated | character(1) | 불가 | — | 'N'::bpchar | This Line is generated |
| 12 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 13 | `amtsourcedr` | Source Debit | numeric | 불가 | — | 0 | Source Debit Amount |
| 14 | `amtsourcecr` | Source Credit | numeric | 불가 | — | 0 | Source Credit Amount |
| 15 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 16 | `currencyrate` | Rate | numeric | 불가 | — | 0 | Currency Conversion Rate |
| 17 | `dateacct` | Account Date | timestamp without time zone | 불가 | — | — | Accounting Date |
| 18 | `amtacctdr` | Accounted Debit | numeric | 불가 | — | 0 | Accounted Debit Amount |
| 19 | `amtacctcr` | Accounted Credit | numeric | 불가 | — | 0 | Accounted Credit Amount |
| 20 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 21 | `qty` | Quantity | numeric | 허용 | — | 0 | Quantity |
| 22 | `c_validcombination_id` | Combination | numeric(10,0) | 허용 | — | — | Valid Account Combination |
| 23 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 불가 | — | — | Currency Conversion Rate Type |
| 24 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 25 | `a_asset_group_id` | Asset Group | numeric(10,0) | 허용 | — | — | Group of Assets |
| 26 | `a_asset_id` | Asset | numeric(10,0) | 허용 | — | — | Asset used internally or by customers |
| 27 | `a_createasset` | Create Asset | character(1) | 허용 | — | 'N'::bpchar | — |
| 28 | `a_processed` | Processed | character(1) | 허용 | — | 'N'::bpchar | — |
| 29 | `gl_journalline_uu` | GL_JournalLine_UU | uuid | 허용 | — | — | — |
| 30 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | NULL::numeric | Performing or initiating organization |
| 31 | `account_id` | Account | numeric(10,0) | 허용 | — | NULL::numeric | Account used |
| 32 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | NULL::numeric | Business Activity |
| 33 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 34 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | NULL::numeric | Marketing Campaign |
| 35 | `c_locfrom_id` | Location From | numeric(10,0) | 허용 | — | NULL::numeric | Location that inventory was moved from |
| 36 | `c_locto_id` | Location To | numeric(10,0) | 허용 | — | NULL::numeric | Location that inventory was moved to |
| 37 | `c_project_id` | Project | numeric(10,0) | 허용 | — | NULL::numeric | Financial Project |
| 38 | `c_salesregion_id` | Sales Region | numeric(10,0) | 허용 | — | NULL::numeric | Sales coverage region |
| 39 | `c_subacct_id` | Sub Account | numeric(10,0) | 허용 | — | NULL::numeric | Sub account for Element Value |
| 40 | `m_product_id` | Product | numeric(10,0) | 허용 | — | NULL::numeric | Product, Service, Item |
| 41 | `user1_id` | User Element List 1 | numeric(10,0) | 허용 | — | NULL::numeric | User defined list element #1 |
| 42 | `user2_id` | User Element List 2 | numeric(10,0) | 허용 | — | NULL::numeric | User defined list element #2 |
| 43 | `alias_validcombination_id` | Alias List | numeric(10,0) | 허용 | — | NULL::numeric | Valid Account Alias List |
| 44 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 45 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 46 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | NULL::numeric | Additional document charges |
| 47 | `m_warehouse_id` | Warehouse | numeric(10,0) | 허용 | — | NULL::numeric | Storage Warehouse and Service Point |
| 48 | `c_employee_id` | Employee | numeric(10,0) | 허용 | — | NULL::numeric | Identifies a Business Partner |
| 49 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | NULL::numeric | Product Attribute Set Instance |
| 50 | `c_tax_id` | Tax | numeric(10,0) | 허용 | — | NULL::numeric | Tax identifier |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 32개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["a_asset_group"]
    n2["ad_client"]
    n3["ad_org"]
    n4["c_activity"]
    n5["c_bpartner"]
    n6["c_campaign"]
    n7["c_elementvalue"]
    n8["c_validcombination"]
    n9["gl_journalline"]
    n9 -->|"a_asset_id → a_asset_id"| n0
    n9 -->|"a_asset_group_id → a_asset_group_id"| n1
    n9 -->|"account_id → c_elementvalue_id"| n7
    n9 -->|"ad_client_id → ad_client_id"| n2
    n9 -->|"ad_org_id → ad_org_id"| n3
    n9 -->|"ad_orgtrx_id → ad_org_id"| n3
    n9 -->|"alias_validcombination_id → c_validcombination_id"| n8
    n9 -->|"c_activity_id → c_activity_id"| n4
    n9 -->|"c_bpartner_id → c_bpartner_id"| n5
    n9 -->|"c_campaign_id → c_campaign_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aasset_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.aasset_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `a_asset_id` | [`a_asset`](../a/a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetgroup_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.aassetgroup_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `a_asset_group_id` | [`a_asset_group`](../a/a_asset_group.md) | `a_asset_group_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `account_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.account_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `account_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adclient_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.adclient_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorg_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.adorg_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.adorgtrx_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aliasvalidcombination_gljourna` <!-- FK_OUT: adempiere.gl_journalline.aliasvalidcombination_gljourna --> | [`gl_journalline`](gl_journalline.md) | `alias_validcombination_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cactivity_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cbpartner_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.ccampaign_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.ccharge_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cconversiontype_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_conversiontype_id` | [`c_conversiontype`](../c/c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.ccostcenter_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.ccurrency_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cdepartment_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cemployee_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cemployee_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_employee_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocfrom_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.clocfrom_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_locfrom_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocto_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.clocto_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_locto_id` | [`c_location`](../c/c_location.md) | `c_location_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cproject_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csalesregion_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.csalesregion_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_salesregion_id` | [`c_salesregion`](../c/c_salesregion.md) | `c_salesregion_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `csubacct_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.csubacct_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_subacct_id` | [`c_subacct`](../c/c_subacct.md) | `c_subacct_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ctax_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.ctax_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_tax_id` | [`c_tax`](../c/c_tax.md) | `c_tax_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuom_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cuom_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cvc_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.cvc_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `c_validcombination_id` | [`c_validcombination`](../c/c_validcombination.md) | `c_validcombination_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `gljournal_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.gljournal_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `gl_journal_id` | [`gl_journal`](gl_journal.md) | `gl_journal_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstance_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.mattributesetinstance_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](../m/m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.mproduct_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.mwarehouse_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user1_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.user1_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `user1_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `user2_gljournalline` <!-- FK_OUT: adempiere.gl_journalline.user2_gljournalline --> | [`gl_journalline`](gl_journalline.md) | `user2_id` | [`c_elementvalue`](../c/c_elementvalue.md) | `c_elementvalue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `gljournalline_ifajournal` <!-- FK_IN: adempiere.i_fajournal.gljournalline_ifajournal --> | [`i_fajournal`](../i/i_fajournal.md) | `gl_journalline_id` | [`gl_journalline`](gl_journalline.md) | `gl_journalline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `gljourbelline_igljournal` <!-- FK_IN: adempiere.i_gljournal.gljourbelline_igljournal --> | [`i_gljournal`](../i/i_gljournal.md) | `gl_journalline_id` | [`gl_journalline`](gl_journalline.md) | `gl_journalline_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
