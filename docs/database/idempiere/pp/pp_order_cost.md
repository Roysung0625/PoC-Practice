# pp_order_cost — 제조 주문 원가

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pp_order_cost` |
| 한국어 논리명(문서용 해석) | 제조 주문 원가 |
| 원본 논리명 | Manufacturing Order Cost |
| 원본 사전 ID | 53024 |
| 분류 | `pp` — 제조·생산 계획·제품 구성 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 24 |
| 나가는 FK / 들어오는 FK | 7 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제조할 제품의 원가 요소별 원가 기록을 제조 주문에 연결한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: In the Cost Tab we have a record for each Cost Element defined in the Product to be produced, for these Organization, Warehouse, Cost Type and Resource.
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pp_order_cost_key` | `pp_order_cost_id` |
| UNIQUE | `pp_order_cost_uu_idx` | `pp_order_cost_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 2 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 3 | `ad_workflow_id` | Workflow | numeric(10,0) | 허용 | — | — | Workflow or combination of tasks |
| 4 | `c_acctschema_id` | Accounting Schema | numeric(10,0) | 불가 | — | — | Rules for accounting |
| 5 | `costingmethod` | Costing Method | character(1) | 허용 | — | 'x'::bpchar | Indicates how Costs will be calculated |
| 6 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 7 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 8 | `cumulatedamt` | Accumulated Amt | numeric | 허용 | — | — | Total Amount |
| 9 | `cumulatedamtpost` | Cumulated Amt Post | numeric | 허용 | — | — | — |
| 10 | `cumulatedqty` | Accumulated Qty | numeric | 허용 | — | — | Total Quantity |
| 11 | `cumulatedqtypost` | Cumulated Qty Post | numeric | 허용 | — | — | — |
| 12 | `currentcostprice` | Current Cost Price | numeric | 허용 | — | — | The currently used cost price |
| 13 | `currentcostpricell` | Current Cost Price Lower Level | numeric | 허용 | — | — | Current Price Lower Level Is the sum of the costs of the components of this product manufactured for this level. |
| 14 | `currentqty` | Current Quantity | numeric | 허용 | — | — | Current Quantity |
| 15 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 16 | `m_attributesetinstance_id` | Attribute Set Instance | numeric(10,0) | 허용 | — | — | Product Attribute Set Instance |
| 17 | `m_costelement_id` | Cost Element | numeric(10,0) | 허용 | — | — | Product Cost Element |
| 18 | `m_costtype_id` | Cost Type | numeric(10,0) | 불가 | — | — | Type of Cost (e.g. Current, Plan, Future) |
| 19 | `m_product_id` | Product | numeric(10,0) | 불가 | — | — | Product, Service, Item |
| 20 | `pp_order_cost_id` | Manufacturing Order Cost | numeric(10,0) | 불가 | 예 | — | — |
| 21 | `pp_order_id` | Manufacturing Order | numeric(10,0) | 불가 | — | — | Manufacturing Order |
| 22 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 23 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 24 | `pp_order_cost_uu` | PP_Order_Cost_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_workflow"]
    n1["c_acctschema"]
    n2["m_attributesetinstance"]
    n3["m_costelement"]
    n4["m_costtype"]
    n5["m_product"]
    n6["pp_order"]
    n7["pp_order_cost"]
    n7 -->|"ad_workflow_id → ad_workflow_id"| n0
    n7 -->|"c_acctschema_id → c_acctschema_id"| n1
    n7 -->|"m_attributesetinstance_id → m_attributesetinstance_id"| n2
    n7 -->|"m_costelement_id → m_costelement_id"| n3
    n7 -->|"m_costtype_id → m_costtype_id"| n4
    n7 -->|"m_product_id → m_product_id"| n5
    n7 -->|"pp_order_id → pp_order_id"| n6
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adworkflow_ppordercost` <!-- FK_OUT: adempiere.pp_order_cost.adworkflow_ppordercost --> | [`pp_order_cost`](pp_order_cost.md) | `ad_workflow_id` | [`ad_workflow`](../ad/ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cacctschema_ppordercost` <!-- FK_OUT: adempiere.pp_order_cost.cacctschema_ppordercost --> | [`pp_order_cost`](pp_order_cost.md) | `c_acctschema_id` | [`c_acctschema`](../c/c_acctschema.md) | `c_acctschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mattributesetinstance_pporderc` <!-- FK_OUT: adempiere.pp_order_cost.mattributesetinstance_pporderc --> | [`pp_order_cost`](pp_order_cost.md) | `m_attributesetinstance_id` | [`m_attributesetinstance`](../m/m_attributesetinstance.md) | `m_attributesetinstance_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcostelement_ppordercost` <!-- FK_OUT: adempiere.pp_order_cost.mcostelement_ppordercost --> | [`pp_order_cost`](pp_order_cost.md) | `m_costelement_id` | [`m_costelement`](../m/m_costelement.md) | `m_costelement_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mcosttype_ppordercost` <!-- FK_OUT: adempiere.pp_order_cost.mcosttype_ppordercost --> | [`pp_order_cost`](pp_order_cost.md) | `m_costtype_id` | [`m_costtype`](../m/m_costtype.md) | `m_costtype_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mproduct_ppordercost` <!-- FK_OUT: adempiere.pp_order_cost.mproduct_ppordercost --> | [`pp_order_cost`](pp_order_cost.md) | `m_product_id` | [`m_product`](../m/m_product.md) | `m_product_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporder_ppordercost` <!-- FK_OUT: adempiere.pp_order_cost.pporder_ppordercost --> | [`pp_order_cost`](pp_order_cost.md) | `pp_order_id` | [`pp_order`](pp_order.md) | `pp_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
