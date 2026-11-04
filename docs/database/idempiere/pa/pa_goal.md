# pa_goal — 성과 목표

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pa_goal` |
| 한국어 논리명(문서용 해석) | 성과 목표 |
| 원본 논리명 | Goal |
| 원본 사전 ID | 440 |
| 분류 | `pa` — 성과·보고서·대시보드 |
| 전체 테넌트 행 수 | 4 |
| 물리 열 수 | 29 |
| 나가는 FK / 들어오는 FK | 5 / 3 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

측정하고 관리할 성과 목표를 정의한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Performance Goal
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pa_goal_pkey` | `pa_goal_id` |
| UNIQUE | `pa_goal_uu_idx` | `pa_goal_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `pa_goal_id` | Goal | numeric(10,0) | 불가 | 예 | — | Performance Goal |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `seqno` | Sequence | numeric(10,0) | 불가 | — | 0 | Method of ordering records; lowest number comes first |
| 10 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `note` | Note | character varying(2000) | 허용 | — | — | Optional additional user defined information |
| 13 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | — | User within the system - Internal or Business Partner Contact |
| 14 | `pa_colorschema_id` | Color Schema | numeric(10,0) | 불가 | — | — | Performance Color Schema |
| 15 | `issummary` | Summary Level | character(1) | 불가 | — | 'N'::bpchar | This is a summary entity |
| 16 | `pa_goalparent_id` | Parent Goal | numeric(10,0) | 허용 | — | — | Parent Goal |
| 17 | `pa_measure_id` | Measure | numeric(10,0) | 허용 | — | — | Concrete Performance Measurement |
| 18 | `relativeweight` | Relative Weight | numeric | 허용 | — | — | Relative weight of this step (0 = ignored) |
| 19 | `measuretarget` | Measure Target | numeric | 불가 | — | 0 | Target value for measure |
| 20 | `measurescope` | Measure Scope | character(1) | 불가 | — | — | Performance Measure Scope |
| 21 | `measuredisplay` | Measure Display | character(1) | 허용 | — | — | Measure Scope initially displayed |
| 22 | `datefrom` | Date From | timestamp without time zone | 허용 | — | — | Starting date for a range |
| 23 | `dateto` | Date To | timestamp without time zone | 허용 | — | — | End date of a date range |
| 24 | `measureactual` | Measure Actual | numeric | 허용 | — | 0 | Actual value that has been measured. |
| 25 | `goalperformance` | Performance Goal | numeric | 허용 | — | — | Target achievement from 0..1 |
| 26 | `datelastrun` | Date Last Run | timestamp without time zone | 허용 | — | — | Date the process was last run. |
| 27 | `ad_role_id` | Role | numeric(10,0) | 허용 | — | — | Responsibility Role |
| 28 | `charttype` | Chart Type | character varying(2) | 불가 | — | 'BC'::character varying | Type of chart to render |
| 29 | `pa_goal_uu` | PA_Goal_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 7개 중 7개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_role"]
    n1["ad_user"]
    n2["pa_colorschema"]
    n3["pa_dashboardcontent"]
    n4["pa_goal"]
    n5["pa_goalrestriction"]
    n6["pa_measure"]
    n4 -->|"ad_role_id → ad_role_id"| n0
    n4 -->|"ad_user_id → ad_user_id"| n1
    n4 -->|"pa_colorschema_id → pa_colorschema_id"| n2
    n4 -->|"pa_goalparent_id → pa_goal_id"| n4
    n4 -->|"pa_measure_id → pa_measure_id"| n6
    n3 -->|"pa_goal_id → pa_goal_id"| n4
    n5 -->|"pa_goal_id → pa_goal_id"| n4
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adrole_pagoal` <!-- FK_OUT: adempiere.pa_goal.adrole_pagoal --> | [`pa_goal`](pa_goal.md) | `ad_role_id` | [`ad_role`](../ad/ad_role.md) | `ad_role_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_pagoal` <!-- FK_OUT: adempiere.pa_goal.aduser_pagoal --> | [`pa_goal`](pa_goal.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pacolorschema_pagoal` <!-- FK_OUT: adempiere.pa_goal.pacolorschema_pagoal --> | [`pa_goal`](pa_goal.md) | `pa_colorschema_id` | [`pa_colorschema`](pa_colorschema.md) | `pa_colorschema_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pagoalparent_pagoal` <!-- FK_OUT: adempiere.pa_goal.pagoalparent_pagoal --> | [`pa_goal`](pa_goal.md) | `pa_goalparent_id` | [`pa_goal`](pa_goal.md) | `pa_goal_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pameasure_pagoal` <!-- FK_OUT: adempiere.pa_goal.pameasure_pagoal --> | [`pa_goal`](pa_goal.md) | `pa_measure_id` | [`pa_measure`](pa_measure.md) | `pa_measure_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `pagoal_padashboardcontent` <!-- FK_IN: adempiere.pa_dashboardcontent.pagoal_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_goal_id` | [`pa_goal`](pa_goal.md) | `pa_goal_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pagoalparent_pagoal` <!-- FK_IN: adempiere.pa_goal.pagoalparent_pagoal --> | [`pa_goal`](pa_goal.md) | `pa_goalparent_id` | [`pa_goal`](pa_goal.md) | `pa_goal_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pagoal_pagoalrestriction` <!-- FK_IN: adempiere.pa_goalrestriction.pagoal_pagoalrestriction --> | [`pa_goalrestriction`](pa_goalrestriction.md) | `pa_goal_id` | [`pa_goal`](pa_goal.md) | `pa_goal_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
