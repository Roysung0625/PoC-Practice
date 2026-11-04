# ad_workflow — 워크플로 정의

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_workflow` |
| 한국어 논리명(문서용 해석) | 워크플로 정의 |
| 원본 논리명 | Workflow |
| 원본 사전 ID | 117 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 58 |
| 물리 열 수 | 48 |
| 나가는 FK / 들어오는 FK | 9 / 22 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

업무 흐름과 작업 조합을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Workflow or combination of tasks
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_workflow_pkey` | `ad_workflow_id` |
| UNIQUE | `ad_workflow_uu_idx` | `ad_workflow_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_workflow_name`: `CREATE UNIQUE INDEX ad_workflow_name ON adempiere.ad_workflow USING btree (ad_client_id, name)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_workflow_id` | Workflow | numeric(10,0) | 불가 | 예 | — | Workflow or combination of tasks |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | text | 허용 | — | — | Comment or Hint |
| 12 | `accesslevel` | Data Access Level | character(1) | 불가 | — | — | Access Level required |
| 13 | `ad_wf_node_id` | Node | numeric(10,0) | 허용 | — | — | Workflow Node (activity), step or process |
| 14 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 15 | `durationunit` | Duration Unit | character(1) | 허용 | — | — | Unit of Duration |
| 16 | `author` | Author | character varying(20) | 불가 | — | 'ComPiere'::character varying | Author/Creator of the Entity |
| 17 | `version` | Version | numeric(10,0) | 불가 | — | 0 | Version of the table definition |
| 18 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 19 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 20 | `priority` | Priority | numeric(10,0) | 허용 | — | — | Indicates if this request is of a high, medium or low priority. |
| 21 | `limit` | Duration Limit | numeric(10,0) | 허용 | — | — | Maximum Duration in Duration Unit |
| 22 | `duration` | Duration | numeric(10,0) | 불가 | — | 0 | Normal Duration in Duration Unit |
| 23 | `cost` | Cost | numeric | 불가 | — | — | Cost information |
| 24 | `workingtime` | Working Time | numeric(10,0) | 불가 | — | 0 | Workflow Simulation Execution Time |
| 25 | `waitingtime` | Waiting Time | numeric(10,0) | 불가 | — | 0 | Workflow Simulation Waiting time |
| 26 | `ad_wf_responsible_id` | Workflow Responsible | numeric(10,0) | 허용 | — | — | Responsible for Workflow Execution |
| 27 | `publishstatus` | Publication Status | character(1) | 불가 | — | — | Status of Publication |
| 28 | `ad_workflowprocessor_id` | Workflow Processor | numeric(10,0) | 허용 | — | — | Workflow Processor Server |
| 29 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 30 | `isdefault` | Default | character(1) | 불가 | — | 'N'::bpchar | Default value |
| 31 | `ad_table_id` | Table | numeric(10,0) | 허용 | — | — | Database Table information |
| 32 | `validateworkflow` | Validate Workflow | character(1) | 허용 | — | — | — |
| 33 | `workflowtype` | Workflow Type | character(1) | 불가 | — | 'G'::bpchar | Type of Workflow |
| 34 | `docvaluelogic` | Document Value Logic | character varying(2000) | 허용 | — | — | Logic to determine Workflow Start - If true, a workflow process is started for the document |
| 35 | `isvalid` | Valid | character(1) | 불가 | — | 'N'::bpchar | Element is valid |
| 36 | `s_resource_id` | Resource | numeric(10,0) | 허용 | — | — | Resource |
| 37 | `setuptime` | Setup Time | numeric(10,0) | 허용 | — | — | Setup time before starting Production |
| 38 | `movingtime` | Moving Time | numeric(10,0) | 허용 | — | — | — |
| 39 | `processtype` | Process Type | character(2) | 허용 | — | — | — |
| 40 | `documentno` | Document No | character varying(30) | 허용 | — | — | Document sequence number of the document |
| 41 | `qtybatchsize` | Qty Batch Size | numeric | 허용 | — | (1)::numeric | — |
| 42 | `queuingtime` | Queuing Time | numeric(10,0) | 허용 | — | — | Queue time is the time a job waits at a work center before begin handled. |
| 43 | `isbetafunctionality` | Beta Functionality | character(1) | 불가 | — | 'N'::bpchar | This functionality is considered Beta |
| 44 | `yield` | Yield % | numeric(10,0) | 허용 | — | (100)::numeric | The Yield is the percentage of a lot that is expected to be of acceptable wuality may fall below 100 percent |
| 45 | `unitscycles` | Units by Cycles | numeric | 허용 | — | — | The Units by Cycles are defined for process type  Flow Repetitive Dedicated and  indicated the product to be manufactured on a production line for duration unit. |
| 46 | `overlapunits` | Overlap Units | numeric | 허용 | — | — | Overlap Units are number of units that must be completed before they are moved the next activity |
| 47 | `ad_workflow_uu` | AD_Workflow_UU | uuid | 허용 | — | — | — |
| 48 | `ad_ctxhelp_id` | Context Help | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 31개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_ctxhelp"]
    n2["ad_entitytype"]
    n3["ad_menu"]
    n4["ad_org"]
    n5["ad_table"]
    n6["ad_wf_node"]
    n7["ad_wf_responsible"]
    n8["ad_workflow"]
    n9["ad_workflowprocessor"]
    n10["s_resource"]
    n8 -->|"ad_ctxhelp_id → ad_ctxhelp_id"| n1
    n8 -->|"ad_table_id → ad_table_id"| n5
    n8 -->|"ad_wf_node_id → ad_wf_node_id"| n6
    n8 -->|"ad_wf_responsible_id → ad_wf_responsible_id"| n7
    n8 -->|"ad_workflowprocessor_id → ad_workflowprocessor_id"| n9
    n8 -->|"entitytype → entitytype"| n2
    n8 -->|"s_resource_id → s_resource_id"| n10
    n8 -->|"ad_client_id → ad_client_id"| n0
    n8 -->|"ad_org_id → ad_org_id"| n4
    n3 -->|"ad_workflow_id → ad_workflow_id"| n8
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adctxhelp_adworkflow` <!-- FK_OUT: adempiere.ad_workflow.adctxhelp_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `ad_ctxhelp_id` | [`ad_ctxhelp`](ad_ctxhelp.md) | `ad_ctxhelp_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtable_adworkflow` <!-- FK_OUT: adempiere.ad_workflow.adtable_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adworkflow` <!-- FK_OUT: adempiere.ad_workflow.adwfnode_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfresponsible_adworkflow` <!-- FK_OUT: adempiere.ad_workflow.adwfresponsible_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `ad_wf_responsible_id` | [`ad_wf_responsible`](ad_wf_responsible.md) | `ad_wf_responsible_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflowprocessor_adwf` <!-- FK_OUT: adempiere.ad_workflow.adworkflowprocessor_adwf --> | [`ad_workflow`](ad_workflow.md) | `ad_workflowprocessor_id` | [`ad_workflowprocessor`](ad_workflowprocessor.md) | `ad_workflowprocessor_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adworkflow` <!-- FK_OUT: adempiere.ad_workflow.entityt_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_adworkflow` <!-- FK_OUT: adempiere.ad_workflow.sresource_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `s_resource_id` | [`s_resource`](../s/s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `workflowclient` <!-- FK_OUT: adempiere.ad_workflow.workflowclient --> | [`ad_workflow`](ad_workflow.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `workfloworg` <!-- FK_OUT: adempiere.ad_workflow.workfloworg --> | [`ad_workflow`](ad_workflow.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adworkflow_admenu` <!-- FK_IN: adempiere.ad_menu.adworkflow_admenu --> | [`ad_menu`](ad_menu.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adpackageexpcommon` <!-- FK_IN: adempiere.ad_package_exp_common.adworkflow_adpackageexpcommon --> | [`ad_package_exp_common`](ad_package_exp_common.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adpackageexpdetail` <!-- FK_IN: adempiere.ad_package_exp_detail.adworkflow_adpackageexpdetail --> | [`ad_package_exp_detail`](ad_package_exp_detail.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adprocess` <!-- FK_IN: adempiere.ad_process.adworkflow_adprocess --> | [`ad_process`](ad_process.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfactivity` <!-- FK_IN: adempiere.ad_wf_activity.adworkflow_adwfactivity --> | [`ad_wf_activity`](ad_wf_activity.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfblock` <!-- FK_IN: adempiere.ad_wf_block.adworkflow_adwfblock --> | [`ad_wf_block`](ad_wf_block.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfnode` <!-- FK_IN: adempiere.ad_wf_node.adworkflow_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfnodesubflow` <!-- FK_IN: adempiere.ad_wf_node.adworkflow_adwfnodesubflow --> | [`ad_wf_node`](ad_wf_node.md) | `workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfprocess` <!-- FK_IN: adempiere.ad_wf_process.adworkflow_adwfprocess --> | [`ad_wf_process`](ad_wf_process.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkfow_workflowaccess` <!-- FK_IN: adempiere.ad_workflow_access.adworkfow_workflowaccess --> | [`ad_workflow_access`](ad_workflow_access.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_workflowtrl` <!-- FK_IN: adempiere.ad_workflow_trl.ad_workflowtrl --> | [`ad_workflow_trl`](ad_workflow_trl.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_aspclientexception` <!-- FK_IN: adempiere.asp_clientexception.adworkflow_aspclientexception --> | [`asp_clientexception`](../asp/asp_clientexception.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_aspworkflow` <!-- FK_IN: adempiere.asp_workflow.adworkflow_aspworkflow --> | [`asp_workflow`](../asp/asp_workflow.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_hrprocess` <!-- FK_IN: adempiere.hr_process.adworkflow_hrprocess --> | [`hr_process`](../hr/hr_process.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_iproductplanning` <!-- FK_IN: adempiere.i_productplanning.adworkflow_iproductplanning --> | [`i_productplanning`](../i/i_productplanning.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_pporder` <!-- FK_IN: adempiere.pp_order.adworkflow_pporder --> | [`pp_order`](../pp/pp_order.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_ppordercost` <!-- FK_IN: adempiere.pp_order_cost.adworkflow_ppordercost --> | [`pp_order_cost`](../pp/pp_order_cost.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_ppordernode` <!-- FK_IN: adempiere.pp_order_node.adworkflow_ppordernode --> | [`pp_order_node`](../pp/pp_order_node.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `workflow_ppordernode` <!-- FK_IN: adempiere.pp_order_node.workflow_ppordernode --> | [`pp_order_node`](../pp/pp_order_node.md) | `workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_pporderworkflow` <!-- FK_IN: adempiere.pp_order_workflow.adworkflow_pporderworkflow --> | [`pp_order_workflow`](../pp/pp_order_workflow.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_ppproductplanning` <!-- FK_IN: adempiere.pp_product_planning.adworkflow_ppproductplanning --> | [`pp_product_planning`](../pp/pp_product_planning.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_qmspecification` <!-- FK_IN: adempiere.qm_specification.adworkflow_qmspecification --> | [`qm_specification`](../qm/qm_specification.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
