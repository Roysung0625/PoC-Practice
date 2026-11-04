# ad_wf_node — 워크플로 노드

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_wf_node` |
| 한국어 논리명(문서용 해석) | 워크플로 노드 |
| 원본 논리명 | Node |
| 원본 사전 ID | 129 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 262 |
| 물리 열 수 | 63 |
| 나가는 FK / 들어오는 FK | 18 / 15 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

워크플로의 활동·단계·프로세스를 나타내는 노드를 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Workflow Node (activity) step or process
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_wf_node_pkey` | `ad_wf_node_id` |
| UNIQUE | `ad_wf_node_uu_idx` | `ad_wf_node_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_wf_node_id` | Node | numeric(10,0) | 불가 | 예 | — | Workflow Node (activity), step or process |
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
| 12 | `ad_workflow_id` | Workflow | numeric(10,0) | 불가 | — | — | Workflow or combination of tasks |
| 13 | `iscentrallymaintained` | Centrally maintained | character(1) | 불가 | — | 'Y'::bpchar | Information maintained in System Element table |
| 14 | `action` | Action | character(1) | 불가 | — | — | Indicates the Action to be performed |
| 15 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | — | Data entry or display window |
| 16 | `workflow_id` | Workflow | numeric(10,0) | 허용 | — | — | Workflow or tasks |
| 17 | `ad_task_id` | OS Task | numeric(10,0) | 허용 | — | — | Operation System Task |
| 18 | `ad_process_id` | Process | numeric(10,0) | 허용 | — | — | Process or Report |
| 19 | `ad_form_id` | Special Form | numeric(10,0) | 허용 | — | — | Special Form |
| 20 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'U'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 21 | `xposition` | X Position | numeric(10,0) | 불가 | — | 0 | Absolute X (horizontal) position in 1/72 of an inch |
| 22 | `yposition` | Y Position | numeric(10,0) | 불가 | — | 0 | Absolute Y (vertical) position in 1/72 of an inch |
| 23 | `ad_wf_block_id` | Workflow Block | numeric(10,0) | 허용 | — | — | Workflow Transaction Execution Block |
| 24 | `subflowexecution` | Subflow Execution | character(1) | 허용 | — | — | Mode how the sub-workflow is executed |
| 25 | `startmode` | Start Mode | character(1) | 허용 | — | — | Workflow Activity Start Mode  |
| 26 | `finishmode` | Finish Mode | character(1) | 허용 | — | — | Workflow Activity Finish Mode |
| 27 | `limit` | Duration Limit | numeric(10,0) | 불가 | — | 0 | Maximum Duration in Duration Unit |
| 28 | `priority` | Priority | numeric(10,0) | 허용 | — | — | Indicates if this request is of a high, medium or low priority. |
| 29 | `duration` | Duration | numeric(10,0) | 불가 | — | 0 | Normal Duration in Duration Unit |
| 30 | `cost` | Cost | numeric | 불가 | — | 0 | Cost information |
| 31 | `workingtime` | Working Time | numeric(10,0) | 허용 | — | — | Workflow Simulation Execution Time |
| 32 | `waitingtime` | Waiting Time | numeric(10,0) | 불가 | — | 0 | Workflow Simulation Waiting time |
| 33 | `ad_wf_responsible_id` | Workflow Responsible | numeric(10,0) | 허용 | — | — | Responsible for Workflow Execution |
| 34 | `ad_image_id` | Image | numeric(10,0) | 허용 | — | — | Image or Icon |
| 35 | `joinelement` | Join Element | character(1) | 불가 | — | — | Semantics for multiple incoming Transitions |
| 36 | `splitelement` | Split Element | character(1) | 불가 | — | — | Semantics for multiple outgoing Transitions |
| 37 | `waittime` | Wait Time | numeric(10,0) | 허용 | — | — | Time in minutes to wait (sleep) |
| 38 | `ad_column_id` | Column | numeric(10,0) | 허용 | — | — | Column in the table |
| 39 | `attributename` | Attribute Name | character varying(60) | 허용 | — | — | Name of the Attribute |
| 40 | `attributevalue` | Attribute Value | character varying(60) | 허용 | — | — | Value of the Attribute |
| 41 | `docaction` | Document Action | character(2) | 허용 | — | — | The targeted status of the document |
| 42 | `value` | Search Key | character varying(40) | 불가 | — | — | Search key for the record in the format required - must be unique |
| 43 | `dynpriorityunit` | Dynamic Priority Unit | character(1) | 허용 | — | — | Change of priority when Activity is suspended waiting for user |
| 44 | `dynprioritychange` | Dynamic Priority Change | numeric | 허용 | — | — | Change of priority when Activity is suspended waiting for user |
| 45 | `emailrecipient` | EMail Recipient | character(1) | 허용 | — | — | Recipient of the EMail |
| 46 | `email` | EMail Address | character varying(60) | 허용 | — | — | Electronic Mail Address |
| 47 | `r_mailtext_id` | Mail Template | numeric(10,0) | 허용 | — | — | Text templates for mailings |
| 48 | `validto` | Valid to | timestamp without time zone | 허용 | — | — | Valid to including this date (last day) |
| 49 | `ismilestone` | Is Milestone | character(1) | 허용 | — | 'N'::bpchar | — |
| 50 | `issubcontracting` | Is Subcontracting | character(1) | 허용 | — | 'N'::bpchar | — |
| 51 | `unitscycles` | Units by Cycles | numeric | 허용 | — | (0)::numeric | The Units by Cycles are defined for process type  Flow Repetitive Dedicated and  indicated the product to be manufactured on a production line for duration unit. |
| 52 | `movingtime` | Moving Time | numeric(10,0) | 허용 | — | — | — |
| 53 | `overlapunits` | Overlap Units | numeric(10,0) | 허용 | — | — | Overlap Units are number of units that must be completed before they are moved the next activity |
| 54 | `c_bpartner_id` | Business Partner | numeric(10,0) | 허용 | — | — | Identifies a Business Partner |
| 55 | `queuingtime` | Queuing Time | numeric(10,0) | 허용 | — | — | Queue time is the time a job waits at a work center before begin handled. |
| 56 | `s_resource_id` | Resource | numeric(10,0) | 허용 | — | — | Resource |
| 57 | `setuptime` | Setup Time | numeric(10,0) | 허용 | — | — | Setup time before starting Production |
| 58 | `validfrom` | Valid from | timestamp without time zone | 허용 | — | — | Valid from including this date (first day) |
| 59 | `yield` | Yield % | numeric(10,0) | 허용 | — | (100)::numeric | The Yield is the percentage of a lot that is expected to be of acceptable wuality may fall below 100 percent |
| 60 | `ad_wf_node_uu` | AD_WF_Node_UU | uuid | 허용 | — | — | — |
| 61 | `ad_ctxhelp_id` | Context Help | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 62 | `ad_infowindow_id` | Info Window | numeric(10,0) | 허용 | — | NULL::numeric | Info and search/select Window |
| 63 | `isattacheddocumenttoemail` | Attached Document | character(1) | 불가 | — | 'Y'::bpchar | Attached document to Email |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 33개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_column"]
    n1["ad_ctxhelp"]
    n2["ad_form"]
    n3["ad_image"]
    n4["ad_infowindow"]
    n5["ad_process"]
    n6["ad_task"]
    n7["ad_wf_block"]
    n8["ad_wf_node"]
    n9["ad_wf_responsible"]
    n10["ad_window"]
    n8 -->|"ad_column_id → ad_column_id"| n0
    n8 -->|"ad_ctxhelp_id → ad_ctxhelp_id"| n1
    n8 -->|"ad_form_id → ad_form_id"| n2
    n8 -->|"ad_image_id → ad_image_id"| n3
    n8 -->|"ad_infowindow_id → ad_infowindow_id"| n4
    n8 -->|"ad_process_id → ad_process_id"| n5
    n8 -->|"ad_task_id → ad_task_id"| n6
    n8 -->|"ad_wf_block_id → ad_wf_block_id"| n7
    n8 -->|"ad_wf_responsible_id → ad_wf_responsible_id"| n9
    n8 -->|"ad_window_id → ad_window_id"| n10
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adcolumn_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adcolumn_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_column_id` | [`ad_column`](ad_column.md) | `ad_column_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adctxhelp_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adctxhelp_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_ctxhelp_id` | [`ad_ctxhelp`](ad_ctxhelp.md) | `ad_ctxhelp_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adform_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adimage_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adimage_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_image_id` | [`ad_image`](ad_image.md) | `ad_image_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adinfowindow_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adinfowindow_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_infowindow_id` | [`ad_infowindow`](ad_infowindow.md) | `ad_infowindow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocess_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adprocess_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_process_id` | [`ad_process`](ad_process.md) | `ad_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adtask_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfblock_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adwfblock_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_block_id` | [`ad_wf_block`](ad_wf_block.md) | `ad_wf_block_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfresponsible_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adwfresponsible_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_responsible_id` | [`ad_wf_responsible`](ad_wf_responsible.md) | `ad_wf_responsible_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adwindow_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_window_id` | [`ad_window`](ad_window.md) | `ad_window_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.adworkflow_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adworkflow_adwfnodesubflow` <!-- FK_OUT: adempiere.ad_wf_node.adworkflow_adwfnodesubflow --> | [`ad_wf_node`](ad_wf_node.md) | `workflow_id` | [`ad_workflow`](ad_workflow.md) | `ad_workflow_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cbpartner_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.cbpartner_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `c_bpartner_id` | [`c_bpartner`](../c/c_bpartner.md) | `c_bpartner_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.entityt_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rmailtext_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.rmailtext_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `r_mailtext_id` | [`r_mailtext`](../r/r_mailtext.md) | `r_mailtext_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `sresource_adwfnode` <!-- FK_OUT: adempiere.ad_wf_node.sresource_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `s_resource_id` | [`s_resource`](../s/s_resource.md) | `s_resource_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wf_nodeclient` <!-- FK_OUT: adempiere.ad_wf_node.wf_nodeclient --> | [`ad_wf_node`](ad_wf_node.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `wf_nodeorg` <!-- FK_OUT: adempiere.ad_wf_node.wf_nodeorg --> | [`ad_wf_node`](ad_wf_node.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adwfnode_adwfactivity` <!-- FK_IN: adempiere.ad_wf_activity.adwfnode_adwfactivity --> | [`ad_wf_activity`](ad_wf_activity.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adwfeventaudit` <!-- FK_IN: adempiere.ad_wf_eventaudit.adwfnode_adwfeventaudit --> | [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adwfnodepara` <!-- FK_IN: adempiere.ad_wf_node_para.adwfnode_adwfnodepara --> | [`ad_wf_node_para`](ad_wf_node_para.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_wfnodetrl` <!-- FK_IN: adempiere.ad_wf_node_trl.ad_wfnodetrl --> | [`ad_wf_node_trl`](ad_wf_node_trl.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adwfnodenext` <!-- FK_IN: adempiere.ad_wf_nodenext.adwfnode_adwfnodenext --> | [`ad_wf_nodenext`](ad_wf_nodenext.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnodenext_adwfnodenext` <!-- FK_IN: adempiere.ad_wf_nodenext.adwfnodenext_adwfnodenext --> | [`ad_wf_nodenext`](ad_wf_nodenext.md) | `ad_wf_next_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adwizardprocess` <!-- FK_IN: adempiere.ad_wizardprocess.adwfnode_adwizardprocess --> | [`ad_wizardprocess`](ad_wizardprocess.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adworkflow` <!-- FK_IN: adempiere.ad_workflow.adwfnode_adworkflow --> | [`ad_workflow`](ad_workflow.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_aspclientexception` <!-- FK_IN: adempiere.asp_clientexception.adwfnode_aspclientexception --> | [`asp_clientexception`](../asp/asp_clientexception.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_ppordernode` <!-- FK_IN: adempiere.pp_order_node.adwfnode_ppordernode --> | [`pp_order_node`](../pp/pp_order_node.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnext_ppordernodenext` <!-- FK_IN: adempiere.pp_order_nodenext.adwfnext_ppordernodenext --> | [`pp_order_nodenext`](../pp/pp_order_nodenext.md) | `ad_wf_next_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_ppordernodenext` <!-- FK_IN: adempiere.pp_order_nodenext.adwfnode_ppordernodenext --> | [`pp_order_nodenext`](../pp/pp_order_nodenext.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_pporderworkflow` <!-- FK_IN: adempiere.pp_order_workflow.adwfnode_pporderworkflow --> | [`pp_order_workflow`](../pp/pp_order_workflow.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_ppwfnodeasset` <!-- FK_IN: adempiere.pp_wf_node_asset.adwfnode_ppwfnodeasset --> | [`pp_wf_node_asset`](../pp/pp_wf_node_asset.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_ppwfnodeproduct` <!-- FK_IN: adempiere.pp_wf_node_product.adwfnode_ppwfnodeproduct --> | [`pp_wf_node_product`](../pp/pp_wf_node_product.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
