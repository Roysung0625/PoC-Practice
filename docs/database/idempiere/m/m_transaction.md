# m_transaction — 재고 수불 거래

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_transaction` |
| 한국어 논리명(문서용 해석) | 재고 수불 거래 |
| 원본 논리명 | Inventory Transaction |
| 원본 사전 ID | 329 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 28 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 9 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

입출고·이동·실사·생산 등에서 발생한 제품 수량 증감을 보관 위치 및 속성 인스턴스와 함께 기록한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_transaction_pkey` | `m_transaction_id` |
| UNIQUE | `m_transaction_uu_idx` | `m_transaction_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_transaction_id` | Inventory Transaction | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `movementtype` | Movement Type | character(2) | 불가 | — | — | Method of moving the inventory |
| 10 | `m_locator_id` | Locator | numeric(10,0) | 불가 | — | — | Warehouse Locator |
| 11 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 12 | `movementdate` | Movement Date | timestamp without time zone | 불가 | — | — | Date a product was moved in or out of inventory |
| 13 | `movementqty` | Movement Quantity | numeric | 불가 | — | 0 | Quantity of a product moved. |
| 14 | `m_inventoryline_id` | Phys.Inventory Line | numeric(10,0) | 허용 | — | — | Unique line in an Inventory document |
| 15 | `m_movementline_id` | Move Line | numeric(10,0) | 허용 | — | — | Inventory Move document Line |
| 16 | `m_inoutline_id` | Shipment/Receipt Line | numeric(10,0) | 허용 | — | — | Line on Shipment or Receipt document |
| 17 | `m_productionline_id` | Production Line | numeric(10,0) | 허용 | — | — | Document Line representing a production |
| 18 | `c_projectissue_id` | Project Issue | numeric(10,0) | 허용 | — | — | Project Issues (Material, Labor) |
| 19 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 불가 | — | 0 | Product Attribute Set Instance |
| 20 | `pp_cost_collector_id` | Manufacturing Cost Collector | numeric(10,0) | 허용 | — | — | — |
| 21 | `m_transaction_uu` | M_Transaction_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 12개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_projectissue"]
    n1["m_attributesetinstance"]
    n2["m_inoutline"]
    n3["m_inventoryline"]
    n4["m_locator"]
    n5["m_movementline"]
    n6["m_product"]
    n7["m_productionline"]
    n8["m_transaction"]
    n9["m_transactionallocation"]
    n10["pp_cost_collector"]
    n8 -->|"c_projectissue_id → c_projectissue_id"| n0
    n8 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n1
    n8 -->|"m_inoutline_id → m_inoutline_id"| n2
    n8 -->|"m_inventoryline_id → m_inventoryline_id"| n3
    n8 -->|"m_locator_id → m_locator_id"| n4
    n8 -->|"m_movementline_id → m_movementline_id"| n5
    n8 -->|"m_product_id → m_product_id"| n6
    n8 -->|"m_productionline_id → m_productionline_id"| n7
    n8 -->|"pp_cost_collector_id → pp_cost_collector_id"| n10
    n9 -->|"out_m_transaction_id → m_transaction_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `cprojectissue_mtransaction` <!-- FK_OUT: adempiere.m_transaction.cprojectissue_mtransaction --> | [`m_transaction`](m_transaction.md) | `c_projectissue_id` | [`c_projectissue`](../c/c_projectissue.md) | `c_projectissue_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattrsetinst_mtransaction` <!-- FK_OUT: adempiere.m_transaction.mattrsetinst_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minoutline_mtransaction` <!-- FK_OUT: adempiere.m_transaction.minoutline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_inoutline_id` | [`m_inoutline`](m_inoutline.md) | `m_inoutline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_mtransaction` <!-- FK_OUT: adempiere.m_transaction.minventoryline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocator_minventorycount` <!-- FK_OUT: adempiere.m_transaction.mlocator_minventorycount --> | [`m_transaction`](m_transaction.md) | `m_locator_id` | [`m_locator`](m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovementline_mtransaction` <!-- FK_OUT: adempiere.m_transaction.mmovementline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_minventorycount` <!-- FK_OUT: adempiere.m_transaction.mproduct_minventorycount --> | [`m_transaction`](m_transaction.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproductionline_mtransaction` <!-- FK_OUT: adempiere.m_transaction.mproductionline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_productionline_id` | [`m_productionline`](m_productionline.md) | `m_productionline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ppcostcollector_mtransaction` <!-- FK_OUT: adempiere.m_transaction.ppcostcollector_mtransaction --> | [`m_transaction`](m_transaction.md) | `pp_cost_collector_id` | [`pp_cost_collector`](../pp/pp_cost_collector.md) | `pp_cost_collector_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mtransactionout_mtrxalloc` <!-- FK_IN: adempiere.m_transactionallocation.mtransactionout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_transaction_id` | [`m_transaction`](m_transaction.md) | `m_transaction_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mttransaction_mtrxalloc` <!-- FK_IN: adempiere.m_transactionallocation.mttransaction_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_transaction_id` | [`m_transaction`](m_transaction.md) | `m_transaction_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mtransaction_ttransaction` <!-- FK_IN: adempiere.t_transaction.mtransaction_ttransaction --> | [`t_transaction`](../t/t_transaction.md) | `m_transaction_id` | [`m_transaction`](m_transaction.md) | `m_transaction_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
