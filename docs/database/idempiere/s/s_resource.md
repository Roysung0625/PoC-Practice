# s_resource — 업무 자원

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.s_resource` |
| 한국어 논리명(문서용 해석) | 업무 자원 |
| 원본 논리명 | Resource |
| 원본 사전 ID | 487 |
| 분류 | `s` — 자원·시간·비용·교육 |
| 전체 테넌트 행 수 | 11 |
| 물리 열 수 | 24 |
| 나가는 FK / 들어오는 FK | 3 / 12 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

업무에 배정하는 자원의 기본 정보를 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Resource
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `s_resource_pkey` | `s_resource_id` |
| UNIQUE | `s_resource_uu_idx` | `s_resource_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `s_resource_id` | Resource | numeric(10,0) | 불가 | 예 | — | Resource |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `s_resourcetype_id` | Resource Type | numeric(10,0) | 불가 | — | — | — |
| 13 | `m_warehouse_id` | Warehouse | numeric(10,0) | 불가 | — | — | Storage Warehouse and Service Point |
| 14 | `isavailable` | Available | character(1) | 불가 | — | 'Y'::bpchar | Resource is available |
| 15 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 16 | `chargeableqty` | Chargeable Quantity | numeric | 허용 | — | 0 | — |
| 17 | `percentutilization` | % Utilization | numeric | 불가 | — | (100)::numeric | — |
| 18 | `dailycapacity` | Daily Capacity | numeric | 허용 | — | — | — |
| 19 | `ismanufacturingresource` | Manufacturing Resource | character(1) | 허용 | — | 'N'::bpchar | — |
| 20 | `waitingtime` | Waiting Time | numeric | 허용 | — | — | Workflow Simulation Waiting time |
| 21 | `manufacturingresourcetype` | Manufacturing Resource Type | character(2) | 허용 | — | — | — |
| 22 | `queuingtime` | Queuing Time | numeric | 허용 | — | — | Queue time is the time a job waits at a work center before begin handled. |
| 23 | `planninghorizon` | Planning Horizon | numeric(10,0) | 허용 | — | (0)::numeric | The planning horizon is the amount of time (Days) an organisation will look into the future when preparing a strategic plan. |
| 24 | `s_resource_uu` | S_Resource_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 15개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_user"]
    n1["ad_wf_node"]
    n2["ad_workflow"]
    n3["i_productplanning"]
    n4["m_product"]
    n5["m_warehouse"]
    n6["pp_cost_collector"]
    n7["pp_mrp"]
    n8["pp_order"]
    n9["s_resource"]
    n10["s_resourcetype"]
    n9 -->|"ad_user_id → ad_user_id"| n0
    n9 -->|"m_warehouse_id → m_warehouse_id"| n5
    n9 -->|"s_resourcetype_id → s_resourcetype_id"| n10
    n1 -->|"s_resource_id → s_resource_id"| n9
    n2 -->|"s_resource_id → s_resource_id"| n9
    n3 -->|"s_resource_id → s_resource_id"| n9
    n4 -->|"s_resource_id → s_resource_id"| n9
    n6 -->|"s_resource_id → s_resource_id"| n9
    n7 -->|"s_resource_id → s_resource_id"| n9
    n8 -->|"s_resource_id → s_resource_id"| n9
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aduser_sresource` <!-- FK_OUT: adempiere.s_resource.aduser_sresource --> | [`s_resource`](s_resource.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `mwarehouse_sresource` <!-- FK_OUT: adempiere.s_resource.mwarehouse_sresource --> | [`s_resource`](s_resource.md) | `m_warehouse_id` | [`m_warehouse`](../m/m_warehouse.md) | `m_warehouse_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresourcetype_sresource` <!-- FK_OUT: adempiere.s_resource.sresourcetype_sresource --> | [`s_resource`](s_resource.md) | `s_resourcetype_id` | [`s_resourcetype`](s_resourcetype.md) | `s_resourcetype_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `sresource_adwfnode` <!-- FK_IN: adempiere.ad_wf_node.sresource_adwfnode --> | [`ad_wf_node`](../ad/ad_wf_node.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_adworkflow` <!-- FK_IN: adempiere.ad_workflow.sresource_adworkflow --> | [`ad_workflow`](../ad/ad_workflow.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_iproductplanning` <!-- FK_IN: adempiere.i_productplanning.sresource_iproductplanning --> | [`i_productplanning`](../i/i_productplanning.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_mproduct` <!-- FK_IN: adempiere.m_product.sresource_mproduct --> | [`m_product`](../m/m_product.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_ppcostcollector` <!-- FK_IN: adempiere.pp_cost_collector.sresource_ppcostcollector --> | [`pp_cost_collector`](../pp/pp_cost_collector.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_ppmrp` <!-- FK_IN: adempiere.pp_mrp.sresource_ppmrp --> | [`pp_mrp`](../pp/pp_mrp.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_pporder` <!-- FK_IN: adempiere.pp_order.sresource_pporder --> | [`pp_order`](../pp/pp_order.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_ppordernode` <!-- FK_IN: adempiere.pp_order_node.sresource_ppordernode --> | [`pp_order_node`](../pp/pp_order_node.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_pporderworkflow` <!-- FK_IN: adempiere.pp_order_workflow.sresource_pporderworkflow --> | [`pp_order_workflow`](../pp/pp_order_workflow.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_ppproductplanning` <!-- FK_IN: adempiere.pp_product_planning.sresource_ppproductplanning --> | [`pp_product_planning`](../pp/pp_product_planning.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_sresourceassignment` <!-- FK_IN: adempiere.s_resourceassignment.sresource_sresourceassignment --> | [`s_resourceassignment`](s_resourceassignment.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_sresunavailable` <!-- FK_IN: adempiere.s_resourceunavailable.sresource_sresunavailable --> | [`s_resourceunavailable`](s_resourceunavailable.md) | `s_resource_id` | [`s_resource`](s_resource.md) | `s_resource_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
