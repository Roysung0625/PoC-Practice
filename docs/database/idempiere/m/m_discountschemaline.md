# m_discountschemaline — 가격표 할인 규칙행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_discountschemaline` |
| 한국어 논리명(문서용 해석) | 가격표 할인 규칙행 |
| 원본 논리명 | Discount Price List |
| 원본 사전 ID | 477 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 11 |
| 물리 열 수 | 43 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

가격표에 적용하는 거래 할인 체계의 개별 행을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Line of the price list trade discount schema
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_discountschemaline_pkey` | `m_discountschemaline_id` |
| UNIQUE | `m_discountschemaline_uu_idx` | `m_discountschemaline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_discountschemaline_id` | Discount Price List | numeric(10,0) | 불가 | 예 | — | Line of the price list trade discount schema |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `m_discountschema_id` | Discount Schema | numeric(10,0) | 불가 | — | — | Schema to calculate the trade discount percentage |
| 10 | `seqno` | Sequence | numeric(10,0) | 불가 | — | — | Method of ordering records; lowest number comes first |
| 11 | `m_product_category_id` | Product Category | numeric(10,0) | 허용 | — | — | Category of a Product |
| 12 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 13 | `m_product_id` | Product | numeric(10,0) | 허용 | — | — | Product, Service, Item |
| 14 | `conversiondate` | Conversion Date | timestamp without time zone | 불가 | — | — | Date for selecting conversion rate |
| 15 | `list_base` | List price Base | character(1) | 불가 | — | — | Price used as the basis for price list calculations |
| 16 | `list_addamt` | List price Surcharge Amount | numeric | 불가 | — | 0 | List Price Surcharge Amount |
| 17 | `list_discount` | List price Discount % | numeric | 불가 | — | — | Discount from list price as a percentage |
| 18 | `list_rounding` | List price Rounding | character(1) | 불가 | — | — | Rounding rule for final list price |
| 19 | `list_minamt` | List price min Margin | numeric | 불가 | — | 0 | Minimum margin for a product |
| 20 | `list_maxamt` | List price max Margin | numeric | 불가 | — | 0 | Maximum margin for a product |
| 21 | `list_fixed` | Fixed List Price | numeric | 허용 | — | 0 | Fixes List Price (not calculated) |
| 22 | `std_base` | Standard price Base | character(1) | 불가 | — | — | Base price for calculating new standard price |
| 23 | `std_addamt` | Standard price Surcharge Amount | numeric | 불가 | — | 0 | Amount added to a price as a surcharge |
| 24 | `std_discount` | Standard price Discount % | numeric | 불가 | — | — | Discount percentage to subtract from base price |
| 25 | `std_rounding` | Standard price Rounding | character(1) | 불가 | — | — | Rounding rule for calculated price |
| 26 | `std_minamt` | Standard price min Margin | numeric | 불가 | — | 0 | Minimum margin allowed for a product |
| 27 | `std_maxamt` | Standard max Margin | numeric | 불가 | — | 0 | Maximum margin allowed for a product |
| 28 | `std_fixed` | Fixed Standard Price | numeric | 허용 | — | 0 | Fixed Standard Price (not calculated) |
| 29 | `limit_base` | Limit price Base | character(1) | 불가 | — | — | Base price for calculation of the new price |
| 30 | `limit_addamt` | Limit price Surcharge Amount | numeric | 불가 | — | 0 | Amount added to the converted/copied price before multiplying |
| 31 | `limit_discount` | Limit price Discount % | numeric | 불가 | — | — | Discount in percent to be subtracted from base, if negative it will be added to base price |
| 32 | `limit_rounding` | Limit price Rounding | character(1) | 불가 | — | — | Rounding of the final result |
| 33 | `limit_minamt` | Limit price min Margin | numeric | 불가 | — | 0 | Minimum difference to original limit price; ignored if zero |
| 34 | `limit_maxamt` | Limit price max Margin | numeric | 불가 | — | 0 | Maximum difference to original limit price; ignored if zero |
| 35 | `limit_fixed` | Fixed Limit Price | numeric | 허용 | — | 0 | Fixed Limit Price (not calculated) |
| 36 | `c_conversiontype_id` | Currency Type | numeric(10,0) | 불가 | — | — | Currency Conversion Rate Type |
| 37 | `classification` | Classification | character varying(12) | 허용 | — | — | Classification for grouping |
| 38 | `group2` | Group2 | character varying(255) | 허용 | — | — | — |
| 39 | `group1` | Group1 | character varying(255) | 허용 | — | — | — |
| 40 | `m_discountschemaline_uu` | M_DiscountSchemaLine_UU | uuid | 허용 | — | — | — |
| 41 | `description` | Description | character varying(255) | 허용 | — | NULL::character varying | Optional short description of the record |
| 42 | `isignoreiscurrentvendor` | Ignore Current Vendor Flag | character(1) | 불가 | — | 'N'::bpchar | take all PO prices into account |
| 43 | `vendorcategory` | Partner Category | character varying(30) | 허용 | — | NULL::character varying | Product Category of the Business Partner |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_bpartner"]
    n1["c_conversiontype"]
    n2["m_discountschema"]
    n3["m_discountschemaline"]
    n4["m_product"]
    n5["m_product_category"]
    n3 -->|"c_bpartner_id → c_bpartner_id"| n0
    n3 -->|"c_conversiontype_id → c_conversiontype_id"| n1
    n3 -->|"m_discountschema_id → m_discountschema_id"| n2
    n3 -->|"m_product_category_id → m_product_category_id"| n5
    n3 -->|"m_product_id → m_product_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cbpartner_mdiscountsline` <!-- FK_OUT: adempiere.m_discountschemaline.cbpartner_mdiscountsline --> | [`m_discountschemaline`](m_discountschemaline.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cconversiontype_mdiscschline` <!-- FK_OUT: adempiere.m_discountschemaline.cconversiontype_mdiscschline --> | [`m_discountschemaline`](m_discountschemaline.md) | `c_conversiontype_id` | [`c_conversiontype`](../c/c_conversiontype.md) | `c_conversiontype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mdiscountschema_mdsline` <!-- FK_OUT: adempiere.m_discountschemaline.mdiscountschema_mdsline --> | [`m_discountschemaline`](m_discountschemaline.md) | `m_discountschema_id` | [`m_discountschema`](m_discountschema.md) | `m_discountschema_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mprodcategory_mdiscountsline` <!-- FK_OUT: adempiere.m_discountschemaline.mprodcategory_mdiscountsline --> | [`m_discountschemaline`](m_discountschemaline.md) | `m_product_category_id` | [`m_product_category`](m_product_category.md) | `m_product_category_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mdiscountsline` <!-- FK_OUT: adempiere.m_discountschemaline.mproduct_mdiscountsline --> | [`m_discountschemaline`](m_discountschemaline.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
