# m_movementline — 재고 이동행

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.m_movementline` |
| 한국어 논리명(문서용 해석) | 재고 이동행 |
| 원본 논리명 | Move Line |
| 원본 사전 ID | 324 |
| 분류 | `m` — 제품·재고·출하/입고·원가 |
| 전체 테넌트 행 수 | 1 |
| 물리 열 수 | 28 |
| 나가는 FK / 들어오는 FK | 11 / 7 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

재고 이동 문서의 개별 이동 내역을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Inventory Move document Line
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `m_movementline_pkey` | `m_movementline_id` |
| UNIQUE | `m_movementline_uu_idx` | `m_movementline_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `m_movementline_id` | Move Line | numeric(10,0) | 불가 | 예 | — | Inventory Move document Line |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `m_movement_id` | Inventory Move | numeric(10,0) | 불가 | — | — | Movement of Inventory |
| 10 | `m_locator_id` | Locator | numeric(10,0) | 불가 | — | — | Warehouse Locator |
| 11 | `m_locatorto_id` | Locator To | numeric(10,0) | 불가 | — | — | Location inventory is moved to |
| 12 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 13 | `line` | Line No | numeric(10,0) | 허용 | — | — | Unique line for this document |
| 14 | `movementqty` | Movement Quantity | numeric | 불가 | — | 0 | Quantity of a product moved. |
| 15 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 16 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | — | Product Attribute Set Instance |
| 17 | `confirmedqty` | Confirmed Quantity | numeric | 허용 | — | 0 | Confirmation of a received quantity |
| 18 | `scrappedqty` | Scrapped Quantity | numeric | 허용 | — | 0 | The Quantity scrapped due to QA issues |
| 19 | `targetqty` | Target Quantity | numeric | 허용 | — | 0 | Target Movement Quantity |
| 20 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 21 | `m_attributesetinstanceto_id` | Attribute Set Instance To | numeric(10,0) | 허용 | — | — | Target Product Attribute Set Instance |
| 22 | `dd_orderline_id` | Distribution Order Line | numeric(10,0) | 허용 | — | — | — |
| 23 | `reversalline_id` | Reversal Line | numeric(10,0) | 허용 | — | — | Use to keep the reversal line ID for reversing costing purpose |
| 24 | `m_movementline_uu` | M_MovementLine_UU | uuid | 허용 | — | — | — |
| 25 | `qtyentered` | Quantity | numeric | 불가 | — | '1'::numeric | The Quantity Entered is based on the selected UoM |
| 26 | `c_uom_id` | UOM | numeric(10,0) | 불가 | — | NULL::numeric | Unit of Measure |
| 27 | `c_costcenter_id` | Cost Center | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 28 | `c_department_id` | Department | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 17개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["c_costcenter"]
    n1["c_department"]
    n2["c_uom"]
    n3["dd_orderline"]
    n4["m_attributesetinstance"]
    n5["m_locator"]
    n6["m_movement"]
    n7["m_movementline"]
    n8["m_product"]
    n7 -->|"c_costcenter_id → c_costcenter_id"| n0
    n7 -->|"c_department_id → c_department_id"| n1
    n7 -->|"c_uom_id → c_uom_id"| n2
    n7 -->|"dd_orderline_id → dd_orderline_id"| n3
    n7 -->|"m_attributesetinstanceto_id → m_attributesetinstance_id"| n4
    n7 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n4
    n7 -->|"m_locatorto_id → m_locator_id"| n5
    n7 -->|"m_locator_id → m_locator_id"| n5
    n7 -->|"m_movement_id → m_movement_id"| n6
    n7 -->|"m_product_id → m_product_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `ccostcenter_mmovementline` <!-- FK_OUT: adempiere.m_movementline.ccostcenter_mmovementline --> | [`m_movementline`](m_movementline.md) | `c_costcenter_id` | [`c_costcenter`](../c/c_costcenter.md) | `c_costcenter_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cdepartment_mmovementline` <!-- FK_OUT: adempiere.m_movementline.cdepartment_mmovementline --> | [`m_movementline`](m_movementline.md) | `c_department_id` | [`c_department`](../c/c_department.md) | `c_department_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cuom_mmovementline` <!-- FK_OUT: adempiere.m_movementline.cuom_mmovementline --> | [`m_movementline`](m_movementline.md) | `c_uom_id` | [`c_uom`](../c/c_uom.md) | `c_uom_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ddorderline_mmovementline` <!-- FK_OUT: adempiere.m_movementline.ddorderline_mmovementline --> | [`m_movementline`](m_movementline.md) | `dd_orderline_id` | [`dd_orderline`](../dd/dd_orderline.md) | `dd_orderline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstanceto_mmovem` <!-- FK_OUT: adempiere.m_movementline.mattributesetinstanceto_mmovem --> | [`m_movementline`](m_movementline.md) | `m_attributesetinstanceto_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattrsetinst_mmovementline` <!-- FK_OUT: adempiere.m_movementline.mattrsetinst_mmovementline --> | [`m_movementline`](m_movementline.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocator_movementline` <!-- FK_OUT: adempiere.m_movementline.mlocator_movementline --> | [`m_movementline`](m_movementline.md) | `m_locatorto_id` | [`m_locator`](m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mlocatorto_mmovementline` <!-- FK_OUT: adempiere.m_movementline.mlocatorto_mmovementline --> | [`m_movementline`](m_movementline.md) | `m_locator_id` | [`m_locator`](m_locator.md) | `m_locator_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovement_mmovementline` <!-- FK_OUT: adempiere.m_movementline.mmovement_mmovementline --> | [`m_movementline`](m_movementline.md) | `m_movement_id` | [`m_movement`](m_movement.md) | `m_movement_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_mmovementline` <!-- FK_OUT: adempiere.m_movementline.mproduct_mmovementline --> | [`m_movementline`](m_movementline.md) | `m_product_id` | [`m_product`](m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversalline_mmovementline` <!-- FK_OUT: adempiere.m_movementline.reversalline_mmovementline --> | [`m_movementline`](m_movementline.md) | `reversalline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `mmovementline_imovement` <!-- FK_IN: adempiere.i_movement.mmovementline_imovement --> | [`i_movement`](../i/i_movement.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovementline_mcostdetail` <!-- FK_IN: adempiere.m_costdetail.mmovementline_mcostdetail --> | [`m_costdetail`](m_costdetail.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `reversalline_mmovementline` <!-- FK_IN: adempiere.m_movementline.reversalline_mmovementline --> | [`m_movementline`](m_movementline.md) | `reversalline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovementline_mmovlineconfirm` <!-- FK_IN: adempiere.m_movementlineconfirm.mmovementline_mmovlineconfirm --> | [`m_movementlineconfirm`](m_movementlineconfirm.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovementline_mmovementlinema` <!-- FK_IN: adempiere.m_movementlinema.mmovementline_mmovementlinema --> | [`m_movementlinema`](m_movementlinema.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovementline_mtransaction` <!-- FK_IN: adempiere.m_transaction.mmovementline_mtransaction --> | [`m_transaction`](m_transaction.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mmovementline_ttransaction` <!-- FK_IN: adempiere.t_transaction.mmovementline_ttransaction --> | [`t_transaction`](../t/t_transaction.md) | `m_movementline_id` | [`m_movementline`](m_movementline.md) | `m_movementline_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
