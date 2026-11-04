# m_inventoryline — 실사 재고행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_inventoryline` |
| 한국어 논리명(문서용 해석) | 실사 재고행 |
| 원본 논리명 | Phys.Inventory Line |
| 원본 사전 ID | 322 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 27 |
| 나가는 FK / 들어오는 FK | 8 / 11 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

재고 실사 문서에 속하는 개별 품목 행을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Unique line in an Inventory document
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_inventoryline_pkey` | `m_inventoryline_id` |
| UNIQUE | `m_inventoryline_uu_idx` | `m_inventoryline_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `m_inventoryline_productlocattr`: `CREATE UNIQUE INDEX m_inventoryline_productlocattr ON adempiere.m_inventoryline USING btree (m_inventory_id, m_locator_id, m_product_id, m_attributesetinstance_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_inventoryline_id` | Phys.Inventory Line | numeric(10,0) | 불가 | 예 | — | Unique line in an Inventory document |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `m_inventory_id` | Phys.Inventory | numeric(10,0) | 불가 | — | — | Parameters for a Physical Inventory |
| 10 | `m_locator_id` | Locator | numeric(10,0) | 허용 | — | — | Warehouse Locator |
| 11 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 12 | `line` | Line No | numeric(10,0) | 허용 | — | — | Unique line for this document |
| 13 | `qtybook` | Quantity book | numeric | 불가 | — | 0 | Book Quantity |
| 14 | `qtycount` | Quantity count | numeric | 불가 | — | 0 | Counted Quantity |
| 15 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 16 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | 0 | Product Attribute Set Instance |
| 17 | `c_charge_id` | Charge | numeric(10,0) | 허용 | — | — | Additional document charges |
| 18 | `inventorytype` | Inventory Type | character(1) | 불가 | — | 'D'::bpchar | Type of inventory difference |
| 19 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 20 | `qtyinternaluse` | Internal Use Qty | numeric | 허용 | — | — | Internal Use Quantity removed from Inventory |
| 21 | `reversalline_id` | Reversal Line | numeric(10,0) | 허용 | — | — | Use to keep the reversal line ID for reversing costing purpose |
| 22 | `qtycsv` | Qty Csv | numeric | 불가 | — | 0 | — |
| 23 | `m_inventoryline_uu` | M_InventoryLine_UU | uuid | 허용 | — | — | — |
| 24 | `currentcostprice` | Current Cost Price | numeric | 허용 | — | (0)::numeric | The currently used cost price |
| 25 | `newcostprice` | New Cost Price | numeric | 허용 | — | (0)::numeric | New current cost price after processing of M_CostDetail |
| 26 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 27 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 18개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_charge"]
    n1["c_costcenter"]
    n2["c_department"]
    n3["i_inventory"]
    n4["m_attributesetinstance"]
    n5["m_inventory"]
    n6["m_inventoryline"]
    n7["m_locator"]
    n8["m_product"]
    n6 -->|"c_charge_id → c_charge_id"| n0
    n6 -->|"c_costcenter_id → c_costcenter_id"| n1
    n6 -->|"c_department_id → c_department_id"| n2
    n6 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n4
    n6 -->|"m_inventory_id → m_inventory_id"| n5
    n6 -->|"m_locator_id → m_locator_id"| n7
    n6 -->|"m_product_id → m_product_id"| n8
    n6 -->|"reversalline_id → m_inventoryline_id"| n6
    n3 -->|"m_costingline_id → m_inventoryline_id"| n6
    n3 -->|"m_inventoryline_id → m_inventoryline_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccharge_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.ccharge_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `c_charge_id` | [`c_charge`](../c/c_charge.md) | `c_charge_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ccostcenter_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.ccostcenter_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.cdepartment_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattrsetinst_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.mattrsetinst_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventory_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.minventory_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `m_inventory_id` | [`m_inventory`](m_inventory.md) | `m_inventory_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocator_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.mlocator_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `m_locator_id` | [`m_locator`](m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.mproduct_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversalline_minventoryline` <!-- FK_OUT: adempiere.m_inventoryline.reversalline_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `reversalline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mcostingline_iinventory` <!-- FK_IN: adempiere.i_inventory.mcostingline_iinventory --> | [`i_inventory`](../i/i_inventory.md) | `m_costingline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_iinventory` <!-- FK_IN: adempiere.i_inventory.minventoryline_iinventory --> | [`i_inventory`](../i/i_inventory.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_mcostdetail` <!-- FK_IN: adempiere.m_costdetail.minventoryline_mcostdetail --> | [`m_costdetail`](m_costdetail.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_minoutlineconfi` <!-- FK_IN: adempiere.m_inoutlineconfirm.minventoryline_minoutlineconfi --> | [`m_inoutlineconfirm`](m_inoutlineconfirm.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversalline_minventoryline` <!-- FK_IN: adempiere.m_inventoryline.reversalline_minventoryline --> | [`m_inventoryline`](m_inventoryline.md) | `reversalline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_milinema` <!-- FK_IN: adempiere.m_inventorylinema.minventoryline_milinema --> | [`m_inventorylinema`](m_inventorylinema.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_mmovlineconfirm` <!-- FK_IN: adempiere.m_movementlineconfirm.minventoryline_mmovlineconfirm --> | [`m_movementlineconfirm`](m_movementlineconfirm.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_mtransaction` <!-- FK_IN: adempiere.m_transaction.minventoryline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_mtrxalloc` <!-- FK_IN: adempiere.m_transactionallocation.minventoryline_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventorylineout_mtrxalloc` <!-- FK_IN: adempiere.m_transactionallocation.minventorylineout_mtrxalloc --> | [`m_transactionallocation`](m_transactionallocation.md) | `out_m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `minventoryline_ttransaction` <!-- FK_IN: adempiere.t_transaction.minventoryline_ttransaction --> | [`t_transaction`](../t/t_transaction.md) | `m_inventoryline_id` | [`m_inventoryline`](m_inventoryline.md) | `m_inventoryline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
