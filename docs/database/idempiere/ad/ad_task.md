# ad_task — 운영체제 작업

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_task` |
| 한국어 논리명(문서용 해석) | 운영체제 작업 |
| 원본 논리명 | OS Task |
| 원본 사전 ID | 118 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 3 |
| 물리 열 수 | 17 |
| 나가는 FK / 들어오는 FK | 4 / 9 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

운영체제에서 실행할 작업을 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Operation System Task
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_task_pkey` | `ad_task_id` |
| UNIQUE | `ad_task_uu_idx` | `ad_task_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `ad_task_name`: `CREATE UNIQUE INDEX ad_task_name ON adempiere.ad_task USING btree (ad_client_id, name)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_task_id` | OS Task | numeric(10,0) | 불가 | 예 | — | Operation System Task |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `help` | Comment/Help | character varying(2000) | 허용 | — | — | Comment or Hint |
| 12 | `accesslevel` | Data Access Level | character(1) | 불가 | — | — | Access Level required |
| 13 | `os_command` | OS Command | character varying(2000) | 불가 | — | — | Operating System Command |
| 14 | `entitytype` | Entity Type | character varying(40) | 불가 | — | 'D'::character varying | Dictionary Entity Type; Determines ownership and synchronization |
| 15 | `isserverprocess` | Server Process | character(1) | 허용 | — | 'N'::bpchar | Run this Process on Server only |
| 16 | `ad_task_uu` | AD_Task_UU | uuid | 허용 | — | — | — |
| 17 | `ad_ctxhelp_id` | Context Help | numeric(10,0) | 허용 | — | NULL::numeric | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 13개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_client"]
    n1["ad_ctxhelp"]
    n2["ad_entitytype"]
    n3["ad_menu"]
    n4["ad_org"]
    n5["ad_task"]
    n6["ad_task_access"]
    n7["ad_task_trl"]
    n8["ad_taskinstance"]
    n9["ad_wf_node"]
    n10["ad_workbenchwindow"]
    n5 -->|"ad_ctxhelp_id → ad_ctxhelp_id"| n1
    n5 -->|"entitytype → entitytype"| n2
    n5 -->|"ad_client_id → ad_client_id"| n0
    n5 -->|"ad_org_id → ad_org_id"| n4
    n3 -->|"ad_task_id → ad_task_id"| n5
    n6 -->|"ad_task_id → ad_task_id"| n5
    n7 -->|"ad_task_id → ad_task_id"| n5
    n8 -->|"ad_task_id → ad_task_id"| n5
    n9 -->|"ad_task_id → ad_task_id"| n5
    n10 -->|"ad_task_id → ad_task_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adctxhelp_adtask` <!-- FK_OUT: adempiere.ad_task.adctxhelp_adtask --> | [`ad_task`](ad_task.md) | `ad_ctxhelp_id` | [`ad_ctxhelp`](ad_ctxhelp.md) | `ad_ctxhelp_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `entityt_adtask` <!-- FK_OUT: adempiere.ad_task.entityt_adtask --> | [`ad_task`](ad_task.md) | `entitytype` | [`ad_entitytype`](ad_entitytype.md) | `entitytype` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `taskclient` <!-- FK_OUT: adempiere.ad_task.taskclient --> | [`ad_task`](ad_task.md) | `ad_client_id` | [`ad_client`](ad_client.md) | `ad_client_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `taskorg` <!-- FK_OUT: adempiere.ad_task.taskorg --> | [`ad_task`](ad_task.md) | `ad_org_id` | [`ad_org`](ad_org.md) | `ad_org_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtask_admenu` <!-- FK_IN: adempiere.ad_menu.adtask_admenu --> | [`ad_menu`](ad_menu.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_adtaskaccess` <!-- FK_IN: adempiere.ad_task_access.adtask_adtaskaccess --> | [`ad_task_access`](ad_task_access.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_tasktrl` <!-- FK_IN: adempiere.ad_task_trl.ad_tasktrl --> | [`ad_task_trl`](ad_task_trl.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `ad_task_taskinstance` <!-- FK_IN: adempiere.ad_taskinstance.ad_task_taskinstance --> | [`ad_taskinstance`](ad_taskinstance.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | CASCADE / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_adwfnode` <!-- FK_IN: adempiere.ad_wf_node.adtask_adwfnode --> | [`ad_wf_node`](ad_wf_node.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_adworkbenchwindow` <!-- FK_IN: adempiere.ad_workbenchwindow.adtask_adworkbenchwindow --> | [`ad_workbenchwindow`](ad_workbenchwindow.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_aspclientexception` <!-- FK_IN: adempiere.asp_clientexception.adtask_aspclientexception --> | [`asp_clientexception`](../asp/asp_clientexception.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_asptask` <!-- FK_IN: adempiere.asp_task.adtask_asptask --> | [`asp_task`](../asp/asp_task.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adtask_ppordernode` <!-- FK_IN: adempiere.pp_order_node.adtask_ppordernode --> | [`pp_order_node`](../pp/pp_order_node.md) | `ad_task_id` | [`ad_task`](ad_task.md) | `ad_task_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
