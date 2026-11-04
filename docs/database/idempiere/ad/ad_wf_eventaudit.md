# ad_wf_eventaudit — 워크플로 이벤트 감사

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_wf_eventaudit` |
| 한국어 논리명(문서용 해석) | 워크플로 이벤트 감사 |
| 원본 논리명 | Workflow Event Audit |
| 원본 사전 ID | 649 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 13 |
| 물리 열 수 | 23 |
| 나가는 FK / 들어오는 FK | 5 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

워크플로 프로세스와 활동의 이벤트 감사 정보를 기록한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Workflow Process Activity Event Audit Information
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_wf_eventaudit_pkey` | `ad_wf_eventaudit_id` |
| UNIQUE | `ad_wf_eventaudit_uu_idx` | `ad_wf_eventaudit_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_wf_eventaudit_id` | Workflow Event Audit | numeric(10,0) | 불가 | 예 | — | Workflow Process Activity Event Audit Information |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `eventtype` | Event Type | character(2) | 불가 | — | — | Type of Event |
| 10 | `wfstate` | Workflow State | character(2) | 불가 | — | — | State of the execution of the workflow |
| 11 | `ad_wf_process_id` | Workflow Process | numeric(10,0) | 불가 | — | — | Actual Workflow Process Instance |
| 12 | `ad_wf_node_id` | Node | numeric(10,0) | 불가 | — | — | Workflow Node (activity), step or process |
| 13 | `ad_table_id` | Table | numeric(10,0) | 불가 | — | — | Database Table information |
| 14 | `record_id` | Record ID | numeric(10,0) | 불가 | — | — | Direct internal record ID |
| 15 | `ad_wf_responsible_id` | Workflow Responsible | numeric(10,0) | 불가 | — | — | Responsible for Workflow Execution |
| 16 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 17 | `elapsedtimems` | Elapsed Time ms | numeric | 불가 | — | — | Elapsed Time in milli seconds |
| 18 | `attributename` | Attribute Name | character varying(60) | 허용 | — | — | Name of the Attribute |
| 19 | `oldvalue` | Old Value | character varying(2000) | 허용 | — | — | The old file data |
| 20 | `newvalue` | New Value | character varying(2000) | 허용 | — | — | New field value |
| 21 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 22 | `textmsg` | Text Message | character varying(2000) | 허용 | — | — | Text Message |
| 23 | `ad_wf_eventaudit_uu` | AD_WF_EventAudit_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 5개 중 5개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_table"]
    n1["ad_user"]
    n2["ad_wf_eventaudit"]
    n3["ad_wf_node"]
    n4["ad_wf_process"]
    n5["ad_wf_responsible"]
    n2 -->|"ad_table_id → ad_table_id"| n0
    n2 -->|"ad_user_id → ad_user_id"| n1
    n2 -->|"ad_wf_node_id → ad_wf_node_id"| n3
    n2 -->|"ad_wf_process_id → ad_wf_process_id"| n4
    n2 -->|"ad_wf_responsible_id → ad_wf_responsible_id"| n5
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adtable_adwfeventaudit` <!-- FK_OUT: adempiere.ad_wf_eventaudit.adtable_adwfeventaudit --> | [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | `ad_table_id` | [`ad_table`](ad_table.md) | `ad_table_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_adwfeventaudit` <!-- FK_OUT: adempiere.ad_wf_eventaudit.aduser_adwfeventaudit --> | [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | `ad_user_id` | [`ad_user`](ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfnode_adwfeventaudit` <!-- FK_OUT: adempiere.ad_wf_eventaudit.adwfnode_adwfeventaudit --> | [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | `ad_wf_node_id` | [`ad_wf_node`](ad_wf_node.md) | `ad_wf_node_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfprocess_adwfeventaudit` <!-- FK_OUT: adempiere.ad_wf_eventaudit.adwfprocess_adwfeventaudit --> | [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | `ad_wf_process_id` | [`ad_wf_process`](ad_wf_process.md) | `ad_wf_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwfresponsib_adwfeventaudit` <!-- FK_OUT: adempiere.ad_wf_eventaudit.adwfresponsib_adwfeventaudit --> | [`ad_wf_eventaudit`](ad_wf_eventaudit.md) | `ad_wf_responsible_id` | [`ad_wf_responsible`](ad_wf_responsible.md) | `ad_wf_responsible_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
