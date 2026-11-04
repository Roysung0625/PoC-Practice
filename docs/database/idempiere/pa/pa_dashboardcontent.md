# pa_dashboardcontent — 대시보드 콘텐츠

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.pa_dashboardcontent` |
| 한국어 논리명(문서용 해석) | 대시보드 콘텐츠 |
| 원본 논리명 | Dashboard Content |
| 원본 사전 ID | 50010 |
| 분류 | `pa` — 성과·보고서·대시보드 |
| 전체 테넌트 행 수 | 12 |
| 물리 열 수 | 33 |
| 나가는 FK / 들어오는 FK | 8 / 5 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

대시보드에 표시할 창·보고서·목표·차트 등의 콘텐츠와 기본 배치를 정의한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `pa_dashboardcontent_key` | `pa_dashboardcontent_id` |
| UNIQUE | `pa_dashboardcontent_uu_idx` | `pa_dashboardcontent_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `pa_dashboardcontent_id` | Dashboard Content | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `created` | Created | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was created |
| 5 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 6 | `updated` | Updated | timestamp without time zone | 불가 | — | statement_timestamp() | Date this record was updated |
| 7 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 8 | `isactive` | Active | character(1) | 불가 | — | — | The record is active in the system |
| 9 | `name` | Name | character varying(120) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | — | Data entry or display window |
| 11 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 12 | `html` | HTML | text | 허용 | — | — | — |
| 13 | `line` | Line No | numeric | 허용 | — | — | Unique line for this document |
| 14 | `pa_goal_id` | Goal | numeric(10,0) | 허용 | — | — | Performance Goal |
| 15 | `columnno` | Column No | numeric(10,0) | 허용 | — | (1)::numeric | Dashboard content column number |
| 16 | `zulfilepath` | Gadget URI | character varying(255) | 허용 | — | — | URI for Dashboard Gadget |
| 17 | `iscollapsible` | Collapsible | character(1) | 불가 | — | 'Y'::bpchar | Flag to indicate the state of the dashboard panel |
| 18 | `goaldisplay` | Goal Display | character(1) | 허용 | — | 'T'::bpchar | Type of goal display on dashboard |
| 19 | `pa_dashboardcontent_uu` | PA_DashboardContent_UU | uuid | 허용 | — | — | — |
| 20 | `isshowindashboard` | Show in Dashboard | character(1) | 불가 | — | 'Y'::bpchar | Show the dashlet in the dashboard |
| 21 | `ad_process_id` | Process | numeric(10,0) | 허용 | — | NULL::numeric | Process or Report |
| 22 | `isembedreportcontent` | Embed Report Content | character(1) | 불가 | — | 'N'::bpchar | Embed report content into dashboard |
| 23 | `processparameters` | Process Parameters | character varying(2000) | 허용 | — | NULL::character varying | Comma separated process parameter list |
| 24 | `iscollapsedbydefault` | Collapsed By Default | character(1) | 불가 | — | 'N'::bpchar | Flag to set the initial state of collapsible field group. |
| 25 | `ad_user_id` | User/Contact | numeric(10,0) | 허용 | — | 0 | User within the system - Internal or Business Partner Contact |
| 26 | `ad_role_id` | Role | numeric(10,0) | 허용 | — | 0 | Responsibility Role |
| 27 | `isshowinlogin` | Show on Login | character(1) | 허용 | — | 'Y'::bpchar | — |
| 28 | `ad_chart_id` | Chart | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 29 | `isshowtitle` | Show Title | character(1) | 불가 | — | 'Y'::bpchar | — |
| 30 | `ad_statusline_id` | Status Line | numeric(10,0) | 허용 | — | NULL::numeric | — |
| 31 | `ismaximizable` | Maximizable | character(1) | 불가 | — | 'Y'::bpchar | — |
| 32 | `ad_printformat_id` | Print Format | numeric(10,0) | 허용 | — | NULL::numeric | Data Print Format |
| 33 | `help` | Comment/Help | character varying(2000) | 허용 | — | NULL::character varying | Comment or Hint |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 13개 중 10개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_chart"]
    n1["ad_column"]
    n2["ad_printformat"]
    n3["ad_process"]
    n4["ad_role"]
    n5["ad_statusline"]
    n6["ad_user"]
    n7["ad_userdef_field"]
    n8["ad_window"]
    n9["pa_dashboardcontent"]
    n10["pa_goal"]
    n9 -->|"ad_chart_id → ad_chart_id"| n0
    n9 -->|"ad_printformat_id → ad_printformat_id"| n2
    n9 -->|"ad_process_id → ad_process_id"| n3
    n9 -->|"ad_role_id → ad_role_id"| n4
    n9 -->|"ad_statusline_id → ad_statusline_id"| n5
    n9 -->|"ad_user_id → ad_user_id"| n6
    n9 -->|"ad_window_id → ad_window_id"| n8
    n9 -->|"pa_goal_id → pa_goal_id"| n10
    n1 -->|"pa_dashboardcontent_id → pa_dashboardcontent_id"| n9
    n7 -->|"pa_dashboardcontent_id → pa_dashboardcontent_id"| n9
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `adchart_padashboardcontent` <!-- FK_OUT: adempiere.pa_dashboardcontent.adchart_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_chart_id` | [`ad_chart`](../ad/ad_chart.md) | `ad_chart_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprintformat_padashboardconte` <!-- FK_OUT: adempiere.pa_dashboardcontent.adprintformat_padashboardconte --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_printformat_id` | [`ad_printformat`](../ad/ad_printformat.md) | `ad_printformat_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocess_padashboardcontent` <!-- FK_OUT: adempiere.pa_dashboardcontent.adprocess_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_process_id` | [`ad_process`](../ad/ad_process.md) | `ad_process_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adrole_padashboardcontent` <!-- FK_OUT: adempiere.pa_dashboardcontent.adrole_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_role_id` | [`ad_role`](../ad/ad_role.md) | `ad_role_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adstatusline_padashboardconten` <!-- FK_OUT: adempiere.pa_dashboardcontent.adstatusline_padashboardconten --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_statusline_id` | [`ad_statusline`](../ad/ad_statusline.md) | `ad_statusline_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `aduser_padashboardcontent` <!-- FK_OUT: adempiere.pa_dashboardcontent.aduser_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_user_id` | [`ad_user`](../ad/ad_user.md) | `ad_user_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_padashboardcontent` <!-- FK_OUT: adempiere.pa_dashboardcontent.adwindow_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `ad_window_id` | [`ad_window`](../ad/ad_window.md) | `ad_window_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `pagoal_padashboardcontent` <!-- FK_OUT: adempiere.pa_dashboardcontent.pagoal_padashboardcontent --> | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_goal_id` | [`pa_goal`](pa_goal.md) | `pa_goal_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `padashboardcontent_adcolumn` <!-- FK_IN: adempiere.ad_column.padashboardcontent_adcolumn --> | [`ad_column`](../ad/ad_column.md) | `pa_dashboardcontent_id` | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_dashboardcontent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `padashboardcontent_aduserdeffi` <!-- FK_IN: adempiere.ad_userdef_field.padashboardcontent_aduserdeffi --> | [`ad_userdef_field`](../ad/ad_userdef_field.md) | `pa_dashboardcontent_id` | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_dashboardcontent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `padashboardcontacc_padashboard` <!-- FK_IN: adempiere.pa_dashboardcontent_access.padashboardcontacc_padashboard --> | [`pa_dashboardcontent_access`](pa_dashboardcontent_access.md) | `pa_dashboardcontent_id` | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_dashboardcontent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `padashboardcontent_padashboard` <!-- FK_IN: adempiere.pa_dashboardcontent_trl.padashboardcontent_padashboard --> | [`pa_dashboardcontent_trl`](pa_dashboardcontent_trl.md) | `pa_dashboardcontent_id` | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_dashboardcontent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `padashboardcontent_padashpref` <!-- FK_IN: adempiere.pa_dashboardpreference.padashboardcontent_padashpref --> | [`pa_dashboardpreference`](pa_dashboardpreference.md) | `pa_dashboardcontent_id` | [`pa_dashboardcontent`](pa_dashboardcontent.md) | `pa_dashboardcontent_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
