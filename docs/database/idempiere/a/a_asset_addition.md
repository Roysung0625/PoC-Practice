# a_asset_addition — 자산 취득·증가 전표

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.a_asset_addition` |
| 한국어 논리명(문서용 해석) | 자산 취득·증가 전표 |
| 원본 논리명 | Asset Addition |
| 원본 사전 ID | 53137 |
| 분류 | `a` — 자산·감가상각 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 54 |
| 나가는 FK / 들어오는 FK | 17 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

청구·입고 등의 원천 문서와 연결하여 자산 취득 또는 가치 증가 금액과 회계 처리 상태를 기록한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `a_asset_addition_pkey` | `a_asset_addition_id` |
| UNIQUE | `a_asset_addition_uu_idx` | `a_asset_addition_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `a_asset_addition_id` | Asset Addition | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `a_asset_id` | Asset | numeric(10,0) | 불가 | — | — | Asset used internally or by customers |
| 10 | `assetvalueamt` | Asset value | numeric | 불가 | — | — | Book Value of the asset |
| 11 | `c_invoiceline_id` | Invoice Line | numeric(10,0) | 허용 | — | — | Invoice Detail Line |
| 12 | `a_qty_current` | Current Qty | numeric | 불가 | — | (0)::numeric | — |
| 13 | `description` | Description | character varying(510) | 허용 | — | — | Optional short description of the record |
| 14 | `gl_journalbatch_id` | Journal Batch | numeric(10,0) | 허용 | — | — | General Ledger Journal Batch |
| 15 | `line` | Line No | numeric(10,0) | 허용 | — | — | Unique line for this document |
| 16 | `postingtype` | Posting Type | character(1) | 불가 | — | 'A'::bpchar | The type of posted amount for the transaction |
| 17 | `m_inoutline_id` | Shipment/Receipt Line | numeric(10,0) | 허용 | — | — | Line on Shipment or Receipt document |
| 18 | `documentno` | Document No | character varying(30) | 허용 | — | — | Document sequence number of the document |
| 19 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | — | Invoice Identifier |
| 20 | `a_sourcetype` | Source Type | character varying(3) | 불가 | — | 'INV'::character varying | — |
| 21 | `a_capvsexp` | Capital/Expense | character varying(3) | 불가 | — | 'Cap'::character varying | — |
| 22 | `a_asset_addition_uu` | A_Asset_Addition_UU | uuid | 허용 | — | — | — |
| 23 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 24 | `docstatus` | Document Status | character varying(2) | 불가 | — | 'DR'::character varying | The current status of the document |
| 25 | `docaction` | Document Action | character(2) | 허용 | — | 'CO'::bpchar | The targeted status of the document |
| 26 | `a_createasset` | Create Asset | character(1) | 불가 | — | 'N'::bpchar | — |
| 27 | `isapproved` | Approved | character(1) | 불가 | — | — | Indicates if this document requires approval |
| 28 | `m_matchinv_id` | Match Invoice | numeric(10,0) | 허용 | — | NULL::numeric | Match Shipment/Receipt to Invoice |
| 29 | `m_product_id` | Product | numeric(10,0) | 허용 | — | NULL::numeric | Product, Service, Item |
| 30 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | NULL::numeric | Product Attribute Set Instance |
| 31 | `m_locator_id` | Locator | numeric(10,0) | 허용 | — | NULL::numeric | Warehouse Locator |
| 32 | `c_currency_id` | Currency | numeric(10,0) | 불가 | — | — | The Currency for this record |
| 33 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 불가 | — | — | Currency Conversion Rate Type |
| 34 | `assetsourceamt` | Source Amount | numeric | 허용 | — | — | — |
| 35 | `deltauselifeyears` | Delta Use Life Years | numeric(10,0) | 불가 | — | (0)::numeric | — |
| 36 | `deltauselifeyears_f` | Delta Use Life Years (fiscal) | numeric(10,0) | 불가 | — | (0)::numeric | Delta Use Life Years (fiscal) |
| 37 | `datedoc` | Document Date | timestamp without time zone | 불가 | — | — | Date of the Document |
| 38 | `i_fixedasset_id` | Imported Fixed Asset | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 39 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 40 | `currencyrate` | Rate | numeric | 허용 | — | — | Currency Conversion Rate |
| 41 | `a_accumulated_depr` | Accumulated Depreciation | numeric | 불가 | — | (0)::numeric | — |
| 42 | `a_accumulated_depr_f` | Accumulated Depreciation (fiscal) | numeric | 불가 | — | (0)::numeric | — |
| 43 | `c_project_id` | Project | numeric(10,0) | 허용 | — | NULL::numeric | Financial Project |
| 44 | `processing` | Process Now | character(1) | 허용 | — | NULL::bpchar | — |
| 45 | `a_accumulated_depr_adjust` | Adjust Accumulated Depreciation | character(1) | 불가 | — | 'N'::bpchar | — |
| 46 | `assetamtentered` | Entered Amount | numeric | 불가 | — | (0)::numeric | — |
| 47 | `posted` | Posted | character(1) | 불가 | — | 'N'::bpchar | Posting status |
| 48 | `a_period_start` | A_Period_Start | numeric(10,0) | 불가 | — | (0)::numeric | — |
| 49 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | NULL::numeric | Additional document charges |
| 50 | `processedon` | Processed On | numeric | 허용 | — | — | The date+time (expressed in decimal format) when the document has been processed |
| 51 | `a_salvage_value` | Asset Salvage Value | numeric | 허용 | — | — | — |
| 52 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | NULL::numeric | Document type or rules |
| 53 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 54 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 19개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["a_asset_addition"]
    n2["c_charge"]
    n3["c_conversiontype"]
    n4["c_costcenter"]
    n5["c_currency"]
    n6["c_department"]
    n7["c_doctype"]
    n8["c_invoice"]
    n9["c_invoiceline"]
    n10["c_project"]
    n1 -->|"a_asset_id → a_asset_id"| n0
    n1 -->|"c_charge_id → c_charge_id"| n2
    n1 -->|"c_conversiontype_id → c_conversiontype_id"| n3
    n1 -->|"c_costcenter_id → c_costcenter_id"| n4
    n1 -->|"c_currency_id → c_currency_id"| n5
    n1 -->|"c_department_id → c_department_id"| n6
    n1 -->|"c_doctype_id → c_doctype_id"| n7
    n1 -->|"c_invoice_id → c_invoice_id"| n8
    n1 -->|"c_invoiceline_id → c_invoiceline_id"| n9
    n1 -->|"c_project_id → c_project_id"| n10
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aasset_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.aasset_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `a_asset_id` | [`a_asset`](a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.ccharge_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.cconversiontype_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_conversiontype_id` | [`c_conversiontype`](../c/c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.ccostcenter_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.ccurrency_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.cdepartment_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.cdoctype_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.cinvoice_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_invoice_id` | [`c_invoice`](../c/c_invoice.md) | `c_invoice_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoiceline_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.cinvoiceline_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_invoiceline_id` | [`c_invoiceline`](../c/c_invoiceline.md) | `c_invoiceline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.cproject_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `gljournalbatch_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.gljournalbatch_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `gl_journalbatch_id` | [`gl_journalbatch`](../gl/gl_journalbatch.md) | `gl_journalbatch_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ifixedasset_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.ifixedasset_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `i_fixedasset_id` | [`i_fixedasset`](../i/i_fixedasset.md) | `i_fixedasset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstance_aassetad` <!-- FK_OUT: adempiere.a_asset_addition.mattributesetinstance_aassetad --> | [`a_asset_addition`](a_asset_addition.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](../m/m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minoutline_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.minoutline_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `m_inoutline_id` | [`m_inoutline`](../m/m_inoutline.md) | `m_inoutline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocator_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.mlocator_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `m_locator_id` | [`m_locator`](../m/m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmatchinv_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.mmatchinv_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `m_matchinv_id` | [`m_matchinv`](../m/m_matchinv.md) | `m_matchinv_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_aassetaddition` <!-- FK_OUT: adempiere.a_asset_addition.mproduct_aassetaddition --> | [`a_asset_addition`](a_asset_addition.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aaaddition_aachange` <!-- FK_IN: adempiere.a_asset_change.aaaddition_aachange --> | [`a_asset_change`](a_asset_change.md) | `a_asset_addition_id` | [`a_asset_addition`](a_asset_addition.md) | `a_asset_addition_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aassetaddition_adepreciationex` <!-- FK_IN: adempiere.a_depreciation_exp.aassetaddition_adepreciationex --> | [`a_depreciation_exp`](a_depreciation_exp.md) | `a_asset_addition_id` | [`a_asset_addition`](a_asset_addition.md) | `a_asset_addition_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
