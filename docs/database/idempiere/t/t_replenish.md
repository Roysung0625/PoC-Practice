# t_replenish — 재고 보충 계산 자료

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.t_replenish` |
| 한국어 논리명(문서용 해석) | 재고 보충 계산 자료 |
| 원본 논리명 | T_Replenish |
| 원본 사전 ID | 364 |
| 분류 | `t` — 작업·보고서용 보조 테이블 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

실행 건별 현재고·예약·주문 수량과 보충 수준을 바탕으로 계산한 발주 수량을 저장한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `t_replenish_pkey` | `ad_pinstance_id`, `m_warehouse_id`, `m_product_id` |
| UNIQUE | `t_replenish_uu_idx` | `t_replenish_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_pinstance_id` | Process Instance | numeric(10,0) | 불가 | 예 | — | Instance of the process |
| 2 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | 예 | — | Storage Warehouse and Service Point |
| 3 | `m_product_id` | Product | numeric(10,0) | 불가 | 예 | — | Product, Service, Item |
| 4 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 5 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 6 | `qtyonhand` | On Hand Quantity | numeric | 불가 | — | 0 | On Hand Quantity |
| 7 | `qtyreserved` | Reserved Quantity | numeric | 불가 | — | 0 | Reserved Quantity |
| 8 | `qtyordered` | Ordered Quantity | numeric | 불가 | — | 0 | Ordered Quantity |
| 9 | `replenishtype` | Replenish Type | character(1) | 불가 | — | — | Method for re-ordering a product |
| 10 | `level_min` | Minimum Level | numeric | 불가 | — | 0 | Minimum Inventory level for this product |
| 11 | `level_max` | Maximum Level | numeric | 불가 | — | 0 | Maximum Inventory level for this product |
| 12 | `c_bpartner_id` | Business Partner | numeric(10,0) | 불가 | — | — | Identifies a Business Partner |
| 13 | `order_min` | Minimum Order Qty | numeric | 불가 | — | 0 | Minimum order quantity in UOM |
| 14 | `order_pack` | Order Pack Qty | numeric | 불가 | — | 0 | Package order size in UOM (e.g. order set of 5 units) |
| 15 | `qtytoorder` | Quantity to Order | numeric | 불가 | — | 0 | — |
| 16 | `replenishmentcreate` | Create | character(3) | 허용 | — | — | Create from Replenishment |
| 17 | `m_warehousesource_id` | Source Warehouse | numeric(10,0) | 허용 | — | — | Optional Warehouse to replenish from |
| 18 | `c_doctype_id` | Document Type | numeric(10,0) | 허용 | — | — | Document type or rules |
| 19 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 20 | `updatedby` | Updated By | numeric(10,0) | 허용 | — | — | User who updated this records |
| 21 | `t_replenish_uu` | T_Replenish_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_pinstance"]
    n1["c_doctype"]
    n2["m_product"]
    n3["m_warehouse"]
    n4["t_replenish"]
    n4 -->|"ad_pinstance_id → ad_pinstance_id"| n0
    n4 -->|"c_doctype_id → c_doctype_id"| n1
    n4 -->|"m_product_id → m_product_id"| n2
    n4 -->|"m_warehouse_id → m_warehouse_id"| n3
    n4 -->|"m_warehousesource_id → m_warehouse_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adpinstance_treplenish` <!-- FK_OUT: adempiere.t_replenish.adpinstance_treplenish --> | [`t_replenish`](t_replenish.md) | `ad_pinstance_id` | [`ad_pinstance`](../ad/ad_pinstance.md) | `ad_pinstance_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdoctype_treplenish` <!-- FK_OUT: adempiere.t_replenish.cdoctype_treplenish --> | [`t_replenish`](t_replenish.md) | `c_doctype_id` | [`c_doctype`](../c/c_doctype.md) | `c_doctype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_treplenish` <!-- FK_OUT: adempiere.t_replenish.mproduct_treplenish --> | [`t_replenish`](t_replenish.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_treplenish` <!-- FK_OUT: adempiere.t_replenish.mwarehouse_treplenish --> | [`t_replenish`](t_replenish.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehousesource_treplenish` <!-- FK_OUT: adempiere.t_replenish.mwarehousesource_treplenish --> | [`t_replenish`](t_replenish.md) | `m_warehousesource_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
