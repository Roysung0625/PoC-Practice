# i_invoice — 송장 가져오기

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.i_invoice` |
| 한국어 논리명(문서용 해석) | 송장 가져오기 |
| 원본 논리명 | Import Invoice |
| 원본 사전 ID | 598 |
| 분류 | `i` — 데이터 가져오기 준비 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 65 |
| 나가는 FK / 들어오는 FK | 22 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

외부 송장 데이터를 시스템 송장으로 등록하기 위한 중간 데이터를 보관한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Import Invoice
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `i_invoice_pkey` | `i_invoice_id` |
| UNIQUE | `i_invoice_uu_idx` | `i_invoice_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `i_invoice_id` | Import Invoice | numeric(10,0) | 불가 | 예 | — | Import Invoice |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 허용 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 허용 | — | — | Organizational entity within tenant |
| 4 | `ad_orgtrx_id` | Trx Organization | numeric(10,0) | 허용 | — | — | Performing or initiating organization |
| 5 | `isactive` | Active | character(1) | 허용 | — | 'Y'::bpchar | The record is active in the system |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 허용 | — | — | User who created this records |
| 8 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 9 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | — | User who updated this records |
| 10 | `i_isimported` | Imported | character(1) | 불가 | — | 'N'::bpchar | Has this import been processed |
| 11 | `i_errormsg` | Import Error Message | character varying(2000) | 허용 | — | — | Messages generated from import process |
| 12 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 13 | `processed` | Processed | character(1) | 허용 | — | 'N'::bpchar | The document has been processed |
| 14 | `m_pricelist_id` | Price List | numeric(10,0) | 허용 | — | — | Unique identifier of a Price List |
| 15 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 16 | `salesrep_id` | Sales Representative | numeric(10,0) | 허용 | — | — | Sales Representative or Company Agent |
| 17 | `issotrx` | Sales Transaction | character(1) | 허용 | — | 'Y'::bpchar | This is a Sales Transaction |
| 18 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 19 | `c_bpartner_location_id` | Partner Location | numeric(10,0) | 허용 | — | — | Identifies the (ship to) address for this Business Partner |
| 20 | `bpartnervalue` | Business Partner Key | character varying(40) | 허용 | — | — | Key of the Business Partner |
| 21 | `name` | Name | character varying(60) | 허용 | — | — | Alphanumeric identifier of the entity |
| 22 | `c_location_id` | Address | numeric(10,0) | 허용 | — | — | Location or Address |
| 23 | `address1` | Address 1 | character varying(60) | 허용 | — | — | Address line 1 for this location |
| 24 | `address2` | Address 2 | character varying(60) | 허용 | — | — | Address line 2 for this location |
| 25 | `postal` | ZIP | character varying(10) | 허용 | — | — | Postal code |
| 26 | `city` | City | character varying(60) | 허용 | — | — | Identifies a City |
| 27 | `c_region_id` | Region | numeric(10,0) | 허용 | — | — | Identifies a geographical Region |
| 28 | `regionname` | Region | character varying(60) | 허용 | — | — | Name of the Region |
| 29 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 30 | `email` | EMail Address | character varying(60) | 허용 | — | — | Electronic Mail Address |
| 31 | `contactname` | Contact Name | character varying(60) | 허용 | — | — | Business Partner Contact Name |
| 32 | `phone` | Phone | character varying(40) | 허용 | — | — | Identifies a telephone number |
| 33 | `c_country_id` | Country | numeric(10,0) | 허용 | — | — | Country  |
| 34 | `countrycode` | ISO Country Code | character(2) | 허용 | — | — | Upper-case two-letter alphanumeric ISO Country code according to ISO 3166-1 |
| 35 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 36 | `doctypename` | Document Type Name | character varying(60) | 허용 | — | — | Name of the Document Type |
| 37 | `c_paymentterm_id` | Payment Term | numeric(10,0) | 허용 | — | — | The terms of Payment (timing, discount) |
| 38 | `paymenttermvalue` | Payment Term Key | character varying(40) | 허용 | — | — | Key of the Payment Term |
| 39 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 40 | `c_campaign_id` | Campaign | numeric(10,0) | 허용 | — | — | Marketing Campaign |
| 41 | `c_activity_id` | Activity | numeric(10,0) | 허용 | — | — | Business Activity |
| 42 | `c_invoice_id` | Invoice | numeric(10,0) | 허용 | — | — | Invoice Identifier |
| 43 | `documentno` | Document No | character varying(30) | 허용 | — | — | Document sequence number of the document |
| 44 | `dateinvoiced` | Date Invoiced | timestamp without time zone | 허용 | — | — | Date printed on Invoice |
| 45 | `dateacct` | Account Date | timestamp without time zone | 허용 | — | — | Accounting Date |
| 46 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 47 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 48 | `productvalue` | Product Key | character varying(40) | 허용 | — | — | Key of the Product |
| 49 | `upc` | UPC/EAN | character varying(30) | 허용 | — | — | Bar Code (Universal Product Code or its superset European Article Number) |
| 50 | `sku` | SKU | character varying(30) | 허용 | — | — | Stock Keeping Unit |
| 51 | `c_tax_id` | Tax | numeric(10,0) | 허용 | — | — | Tax identifier |
| 52 | `taxindicator` | Tax Indicator | character varying(10) | 허용 | — | — | Short form for Tax to be printed on documents |
| 53 | `taxamt` | Tax Amount | numeric | 허용 | — | 0 | Tax Amount for a document |
| 54 | `c_invoiceline_id` | Invoice Line | numeric(10,0) | 허용 | — | — | Invoice Detail Line |
| 55 | `linedescription` | Line Description | character varying(255) | 허용 | — | — | Description of the Line |
| 56 | `qtyordered` | Ordered Quantity | numeric | 허용 | — | 0 | Ordered Quantity |
| 57 | `priceactual` | Unit Price | numeric | 허용 | — | 0 | Actual Price  |
| 58 | `projectvalue` | Project Key | character varying(40) | 허용 | — | — | Key of the Project |
| 59 | `activityvalue` | Activity Key | character varying(40) | 허용 | — | — | Text key for Activity |
| 60 | `chargename` | Charge Name | character varying(60) | 허용 | — | — | Name of the Charge |
| 61 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 62 | `i_invoice_uu` | I_Invoice_UU | uuid | 허용 | — | — | — |
| 63 | `c_1099box_id` | 1099 Box | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 64 | `c_1099box_value` | 1099 Box Value | character varying(40) | 허용 | — | NULL::character varying | — |
| 65 | `iso_code` | ISO Currency Code | character varying(3) | 허용 | — | NULL::character varying | Three letter ISO 4217 Code of the Currency |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 22개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_org"]
    n1["ad_user"]
    n2["c_1099box"]
    n3["c_activity"]
    n4["c_bpartner"]
    n5["c_bpartner_location"]
    n6["c_campaign"]
    n7["c_charge"]
    n8["i_invoice"]
    n8 -->|"ad_org_id → ad_org_id"| n0
    n8 -->|"ad_orgtrx_id → ad_org_id"| n0
    n8 -->|"ad_user_id → ad_user_id"| n1
    n8 -->|"salesrep_id → ad_user_id"| n1
    n8 -->|"c_1099box_id → c_1099box_id"| n2
    n8 -->|"c_activity_id → c_activity_id"| n3
    n8 -->|"c_bpartner_id → c_bpartner_id"| n4
    n8 -->|"c_bpartner_location_id → c_bpartner_location_id"| n5
    n8 -->|"c_campaign_id → c_campaign_id"| n6
    n8 -->|"c_charge_id → c_charge_id"| n7
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adorg_iinvoice` <!-- FK_OUT: adempiere.i_invoice.adorg_iinvoice --> | [`i_invoice`](i_invoice.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adorgtrx_iinvoice` <!-- FK_OUT: adempiere.i_invoice.adorgtrx_iinvoice --> | [`i_invoice`](i_invoice.md) | `ad_orgtrx_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_iinvoice` <!-- FK_OUT: adempiere.i_invoice.aduser_iinvoice --> | [`i_invoice`](i_invoice.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adusersalesrep_iinvoice` <!-- FK_OUT: adempiere.i_invoice.adusersalesrep_iinvoice --> | [`i_invoice`](i_invoice.md) | `salesrep_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `c1099box_iinvoice` <!-- FK_OUT: adempiere.i_invoice.c1099box_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_1099box_id` | [`c_1099box`](../c/c_1099box.md) | `c_1099box_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cactivity_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cactivity_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_activity_id` | [`c_activity`](../c/c_activity.md) | `c_activity_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cbpartner_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbplocation_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cbplocation_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_bpartner_location_id` | [`c_bpartner_location`](../c/c_bpartner_location.md) | `c_bpartner_location_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccampaign_iinvoice` <!-- FK_OUT: adempiere.i_invoice.ccampaign_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_campaign_id` | [`c_campaign`](../c/c_campaign.md) | `c_campaign_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccharge_iinvoice` <!-- FK_OUT: adempiere.i_invoice.ccharge_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccountry_iinvoice` <!-- FK_OUT: adempiere.i_invoice.ccountry_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_country_id` | [`c_country`](../c/c_country.md) | `c_country_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_iinvoice` <!-- FK_OUT: adempiere.i_invoice.ccurrency_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cdoctype_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvliceline_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cinvliceline_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_invoiceline_id` | [`c_invoiceline`](../c/c_invoiceline.md) | `c_invoiceline_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cinvoice_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cinvoice_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_invoice_id` | [`c_invoice`](../c/c_invoice.md) | `c_invoice_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `clocation_iinvoice` <!-- FK_OUT: adempiere.i_invoice.clocation_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_location_id` | [`c_location`](../c/c_location.md) | `c_location_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cpaymentterm_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cpaymentterm_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_paymentterm_id` | [`c_paymentterm`](../c/c_paymentterm.md) | `c_paymentterm_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cproject_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `cregion_iinvoice` <!-- FK_OUT: adempiere.i_invoice.cregion_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_region_id` | [`c_region`](../c/c_region.md) | `c_region_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `ctax_iinvoice` <!-- FK_OUT: adempiere.i_invoice.ctax_iinvoice --> | [`i_invoice`](i_invoice.md) | `c_tax_id` | [`c_tax`](../c/c_tax.md) | `c_tax_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `mpricelist_iinvoice` <!-- FK_OUT: adempiere.i_invoice.mpricelist_iinvoice --> | [`i_invoice`](i_invoice.md) | `m_pricelist_id` | [`m_pricelist`](../m/m_pricelist.md) | `m_pricelist_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `nproduct_iinvoice` <!-- FK_OUT: adempiere.i_invoice.nproduct_iinvoice --> | [`i_invoice`](i_invoice.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

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
