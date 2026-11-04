# m_product_po — 제품 구매 조건

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_product_po` |
| 한국어 논리명(문서용 해석) | 제품 구매 조건 |
| 원본 논리명 | Product Purchasing |
| 원본 사전 ID | 210 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 29 |
| 물리 열 수 | 32 |
| 나가는 FK / 들어오는 FK | 6 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제품과 공급업체별 구매 단가·거래 통화·공급업체 품번·최소 주문량·납기를 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_product_po_pkey` | `m_product_id`, `c_bpartner_id` |
| UNIQUE | `m_product_po_uu_idx` | `m_product_po_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `m_product_po_vendorprodno`: `CREATE UNIQUE INDEX m_product_po_vendorprodno ON adempiere.m_product_po USING btree (c_bpartner_id, vendorproductno)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_product_id` | Product | numeric(10,0) | 불가 | 예 | — | Product, Service, Item |
| 2 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | 예 | — | Identifies a Business Partner |
| 3 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 4 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 5 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 9 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 10 | `iscurrentvendor` | Current vendor | character(1) | 불가 | — | 'Y'::bpchar | Use this Vendor for pricing and stock replenishment |
| 11 | `c_uom_id` | UOM | numeric(10,0) | 허용 | — | — | Unit of Measure |
| 12 | `c_currency_id` | Currency | numeric(10,0) | 허용 | — | — | The Currency for this record |
| 13 | `pricelist` | List Price | numeric | 허용 | — | 0 | List Price |
| 14 | `pricepo` | PO Price | numeric | 허용 | — | 0 | Price based on a purchase order |
| 15 | `priceeffective` | Price effective | timestamp without time zone | 허용 | — | — | Effective Date of Price |
| 16 | `pricelastpo` | Last PO Price | numeric | 허용 | — | 0 | Price of the last purchase order for the product |
| 17 | `pricelastinv` | Last Invoice Price | numeric | 허용 | — | 0 | Price of the last invoice for the product |
| 18 | `vendorproductno` | Partner Product Key | character varying(40) | 불가 | — | — | Product Key of the Business Partner |
| 19 | `upc` | UPC/EAN | character varying(20) | 허용 | — | — | Bar Code (Universal Product Code or its superset European Article Number) |
| 20 | `vendorcategory` | Partner Category | character varying(30) | 허용 | — | — | Product Category of the Business Partner |
| 21 | `discontinued` | Discontinued | character(1) | 허용 | — | 'N'::bpchar | This product is no longer available |
| 22 | `discontinuedby` | — | timestamp without time zone | 허용 | — | — | — |
| 23 | `order_min` | Minimum Order Qty | numeric | 허용 | — | 0 | Minimum order quantity in UOM |
| 24 | `order_pack` | Order Pack Qty | numeric | 허용 | — | 0 | Package order size in UOM (e.g. order set of 5 units) |
| 25 | `costperorder` | Cost per Order | numeric | 허용 | — | 0 | Fixed Cost Per Order |
| 26 | `deliverytime_promised` | Promised Delivery Time | numeric(10,0) | 허용 | — | — | Promised days between order and delivery |
| 27 | `deliverytime_actual` | Actual Delivery Time | numeric(10,0) | 허용 | — | — | Actual days between order and delivery |
| 28 | `qualityrating` | Quality Rating | numeric | 허용 | — | — | Method for rating vendors |
| 29 | `royaltyamt` | Royalty Amount | numeric | 허용 | — | 0 | (Included) Amount for copyright, etc. |
| 30 | `manufacturer` | Manufacturer | character varying(30) | 허용 | — | — | Manufacturer of the Product |
| 31 | `discontinuedat` | Discontinued At | timestamp without time zone | 허용 | — | — | Discontinued At indicates Date when product was discontinued |
| 32 | `m_product_po_uu` | M_Product_PO_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 6개 중 6개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_org"]
    n2["c_bpartner"]
    n3["c_currency"]
    n4["c_uom"]
    n5["m_product"]
    n6["m_product_po"]
    n6 -->|"c_bpartner_id → c_bpartner_id"| n2
    n6 -->|"c_uom_id → c_uom_id"| n4
    n6 -->|"c_currency_id → c_currency_id"| n3
    n6 -->|"m_product_id → m_product_id"| n5
    n6 -->|"ad_client_id → ad_client_id"| n0
    n6 -->|"ad_org_id → ad_org_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `c_buspartner_m_product_po` <!-- FK_OUT: adempiere.m_product_po.c_buspartner_m_product_po --> | [`m_product_po`](m_product_po.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `c_uom_m_product_po` <!-- FK_OUT: adempiere.m_product_po.c_uom_m_product_po --> | [`m_product_po`](m_product_po.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccurrency_mproductpo` <!-- FK_OUT: adempiere.m_product_po.ccurrency_mproductpo --> | [`m_product_po`](m_product_po.md) | `c_currency_id` | [`c_currency`](../c/c_currency.md) | `c_currency_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `m_product_productpo` <!-- FK_OUT: adempiere.m_product_po.m_product_productpo --> | [`m_product_po`](m_product_po.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `m_productpo_client` <!-- FK_OUT: adempiere.m_product_po.m_productpo_client --> | [`m_product_po`](m_product_po.md) | `ad_client_id` | [`ad_client`](../ad/ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `m_productpo_org` <!-- FK_OUT: adempiere.m_product_po.m_productpo_org --> | [`m_product_po`](m_product_po.md) | `ad_org_id` | [`ad_org`](../ad/ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
