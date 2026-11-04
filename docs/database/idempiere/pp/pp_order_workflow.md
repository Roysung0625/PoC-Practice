# pp_order_workflow — 제조 주문 작업 흐름

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pp_order_workflow` |
| 한국어 논리명(문서용 해석) | 제조 주문 작업 흐름 |
| 원본 논리명 | Manufacturing Order Workflow |
| 원본 사전 ID | 53029 |
| 분류 | `pp` — 제조·생산 계획·제품 구성 |
| 전체 테넌트 행 수 | 2 |
| 물리 열 수 | 47 |
| 나가는 FK / 들어오는 FK | 9 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

제조 주문에 적용한 작업 흐름을 저장한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Manufacturing Order Workflow
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pp_order_workflow_key` | `pp_order_workflow_id` |
| UNIQUE | `pp_order_workflow_uu_idx` | `pp_order_workflow_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `workflowtype` | Workflow Type | character(1) | 허용 | — | 'M'::bpchar | Type of Workflow |
| 2 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 3 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | — | Database Table information |
| 4 | `ad_wf_node_id` | Node | numeric(10,0) | 허용 | — | — | Workflow Node (activity), step or process |
| 5 | `ad_wf_responsible_id` | Workflow Responsible | numeric(10,0) | 허용 | — | — | Responsible for Workflow Execution |
| 6 | `ad_workflowprocessor_id` | Workflow Processor | numeric(10,0) | 허용 | — | — | Workflow Processor Server |
| 7 | `ad_workflow_id` | Workflow | numeric(10,0) | 불가 | — | — | Workflow or combination of tasks |
| 8 | `accesslevel` | Data Access Level | character(1) | 불가 | — | — | Access Level required |
| 9 | `author` | Author | character varying(20) | 불가 | — | — | Author/Creator of the Entity |
| 10 | `cost` | Cost | numeric | 허용 | — | — | Cost information |
| 11 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 12 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 13 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 14 | `documentno` | Document No | character varying(32) | 허용 | — | — | Document sequence number of the document |
| 15 | `duration` | Duration | numeric(10,0) | 불가 | — | (0)::numeric | Normal Duration in Duration Unit |
| 16 | `durationunit` | Duration Unit | character(1) | 불가 | — | 'h'::bpchar | Unit of Duration |
| 17 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 18 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 19 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 20 | `isdefault` | Default | character(1) | 허용 | — | — | Default value |
| 21 | `limit` | Duration Limit | numeric(10,0) | 불가 | — | — | Maximum Duration in Duration Unit |
| 22 | `movingtime` | Moving Time | numeric(10,0) | 허용 | — | — | — |
| 23 | `pp_order_id` | Manufacturing Order | numeric(10,0) | 불가 | — | — | Manufacturing Order |
| 24 | `pp_order_node_id` | Manufacturing Order Activity | numeric(10,0) | 허용 | — | — | Workflow Node (activity), step or process |
| 25 | `pp_order_workflow_id` | Manufacturing Order Workflow | numeric(10,0) | 불가 | 예 | — | — |
| 26 | `priority` | Priority | numeric(10,0) | 불가 | — | — | Indicates if this request is of a high, medium or low priority. |
| 27 | `processtype` | Process Type | character(2) | 허용 | — | — | — |
| 28 | `publishstatus` | Publication Status | character(1) | 불가 | — | 'U'::bpchar | Status of Publication |
| 29 | `qtybatchsize` | Qty Batch Size | numeric | 허용 | — | (1)::numeric | — |
| 30 | `queuingtime` | Queuing Time | numeric(10,0) | 허용 | — | — | Queue time is the time a job waits at a work center before begin handled. |
| 31 | `s_resource_id` | Resource | numeric(10,0) | 허용 | — | — | Resource |
| 32 | `setuptime` | Setup Time | numeric(10,0) | 허용 | — | — | Setup time before starting Production |
| 33 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 34 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 35 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 36 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 37 | `validateworkflow` | Validate Workflow | character(1) | 허용 | — | — | — |
| 38 | `value` | Search Key | character varying(240) | 허용 | — | — | Search key for the record in the format required - must be unique |
| 39 | `version` | Version | numeric(10,0) | 불가 | — | — | Version of the table definition |
| 40 | `waitingtime` | Waiting Time | numeric(10,0) | 불가 | — | — | Workflow Simulation Waiting time |
| 41 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 42 | `workingtime` | Working Time | numeric(10,0) | 허용 | — | — | Workflow Simulation Execution Time |
| 43 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 44 | `yield` | Yield % | numeric(10,0) | 허용 | — | (100)::numeric | The Yield is the percentage of a lot that is expected to be of acceptable wuality may fall below 100 percent |
| 45 | `unitscycles` | Units by Cycles | numeric | 허용 | — | — | The Units by Cycles are defined for process type  Flow Repetitive Dedicated and  indicated the product to be manufactured on a production line for duration unit. |
| 46 | `overlapunits` | Overlap Units | numeric | 허용 | — | — | Overlap Units are number of units that must be completed before they are moved the next activity |
| 47 | `pp_order_workflow_uu` | PP_Order_Workflow_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 14개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_entitytype"]
    n1["ad_table"]
    n2["ad_wf_node"]
    n3["ad_wf_responsible"]
    n4["ad_workflow"]
    n5["ad_workflowprocessor"]
    n6["pp_cost_collector"]
    n7["pp_order"]
    n8["pp_order_node"]
    n9["pp_order_workflow"]
    n10["s_resource"]
    n9 -->|"ad_table_id → ad_table_id"| n1
    n9 -->|"ad_wf_node_id → ad_wf_node_id"| n2
    n9 -->|"ad_wf_responsible_id → ad_wf_responsible_id"| n3
    n9 -->|"ad_workflow_id → ad_workflow_id"| n4
    n9 -->|"ad_workflowprocessor_id → ad_workflowprocessor_id"| n5
    n9 -->|"entitytype → entitytype"| n0
    n9 -->|"pp_order_id → pp_order_id"| n7
    n9 -->|"pp_order_node_id → pp_order_node_id"| n8
    n9 -->|"s_resource_id → s_resource_id"| n10
    n6 -->|"pp_order_workflow_id → pp_order_workflow_id"| n9
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.adtable_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `ad_table_id` | [`ad_table`](../ad/ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.adwfnode_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `ad_wf_node_id` | [`ad_wf_node`](../ad/ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfresponsible_pporderworkflo` <!-- FK_OUT: adempiere.pp_order_workflow.adwfresponsible_pporderworkflo --> | [`pp_order_workflow`](pp_order_workflow.md) | `ad_wf_responsible_id` | [`ad_wf_responsible`](../ad/ad_wf_responsible.md) | `ad_wf_responsible_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.adworkflow_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `ad_workflow_id` | [`ad_workflow`](../ad/ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflowprocessor_pporderwor` <!-- FK_OUT: adempiere.pp_order_workflow.adworkflowprocessor_pporderwor --> | [`pp_order_workflow`](pp_order_workflow.md) | `ad_workflowprocessor_id` | [`ad_workflowprocessor`](../ad/ad_workflowprocessor.md) | `ad_workflowprocessor_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.entityt_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `entitytype` | [`ad_entitytype`](../ad/ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporder_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.pporder_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_id` | [`pp_order`](pp_order.md) | `pp_order_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ppordernode_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.ppordernode_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_node_id` | [`pp_order_node`](pp_order_node.md) | `pp_order_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_pporderworkflow` <!-- FK_OUT: adempiere.pp_order_workflow.sresource_pporderworkflow --> | [`pp_order_workflow`](pp_order_workflow.md) | `s_resource_id` | [`s_resource`](../s/s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `pporderworkflow_ppcostcollecto` <!-- FK_IN: adempiere.pp_cost_collector.pporderworkflow_ppcostcollecto --> | [`pp_cost_collector`](pp_cost_collector.md) | `pp_order_workflow_id` | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporderworkflow_ppordernode` <!-- FK_IN: adempiere.pp_order_node.pporderworkflow_ppordernode --> | [`pp_order_node`](pp_order_node.md) | `pp_order_workflow_id` | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporderworkflow_ppordernodeass` <!-- FK_IN: adempiere.pp_order_node_asset.pporderworkflow_ppordernodeass --> | [`pp_order_node_asset`](pp_order_node_asset.md) | `pp_order_workflow_id` | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporderworkflow_ppordernodepro` <!-- FK_IN: adempiere.pp_order_node_product.pporderworkflow_ppordernodepro --> | [`pp_order_node_product`](pp_order_node_product.md) | `pp_order_workflow_id` | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pporderworkflow_pporderworkflo` <!-- FK_IN: adempiere.pp_order_workflow_trl.pporderworkflow_pporderworkflo --> | [`pp_order_workflow_trl`](pp_order_workflow_trl.md) | `pp_order_workflow_id` | [`pp_order_workflow`](pp_order_workflow.md) | `pp_order_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
