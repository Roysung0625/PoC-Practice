# ad_issue — 시스템 오류 보고

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.ad_issue` |
| 한국어 논리명(문서용 해석) | 시스템 오류 보고 |
| 원본 논리명 | System Issue |
| 원본 사전 ID | 828 |
| 분류 | `ad` — 애플리케이션 사전·화면·권한·시스템 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 50 |
| 나가는 FK / 들어오는 FK | 9 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

오류 요약·발생 위치·실행환경·스택 추적 및 관련 요청 정보를 기록한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `ad_issue_pkey` | `ad_issue_id` |
| UNIQUE | `ad_issue_uu_idx` | `ad_issue_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `ad_issue_id` | System Issue | numeric(10,0) | 불가 | 예 | — | Automatically created or manually entered System Issue |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `releaseno` | Release No | character varying(10) | 불가 | — | '.'::character varying | Internal Release Number |
| 10 | `version` | Version | character varying(40) | 불가 | — | — | Version of the table definition |
| 11 | `name` | Name | character varying(60) | 불가 | — | — | Alphanumeric identifier of the entity |
| 12 | `username` | User Name | character varying(60) | 불가 | — | — | — |
| 13 | `supportemail` | Support EMail | character varying(60) | 허용 | — | — | EMail address to send support information and updates to |
| 14 | `dbaddress` | DB Address | character varying(255) | 허용 | — | — | JDBC URL of the database server |
| 15 | `local_host` | Local Host | character varying(120) | 허용 | — | — | Local Host Info |
| 16 | `operatingsysteminfo` | Operating System | character varying(255) | 허용 | — | — | Operating System Info |
| 17 | `releasetag` | Release Tag | character varying(60) | 허용 | — | — | Release Tag |
| 18 | `databaseinfo` | Database | character varying(255) | 허용 | — | — | Database Information |
| 19 | `javainfo` | Java Info | character varying(255) | 허용 | — | — | Java Version Info |
| 20 | `remote_addr` | Remote Addr | character varying(60) | 허용 | — | — | Remote Address |
| 21 | `remote_host` | Remote Host | character varying(120) | 허용 | — | — | Remote host Info |
| 22 | `issuesummary` | Issue Summary | character varying(2000) | 불가 | — | — | Issue Summary |
| 23 | `comments` | Comments | character varying(2000) | 허용 | — | — | Comments or additional information |
| 24 | `sourceclassname` | Source Class | character varying(255) | 허용 | — | — | Source Class Name |
| 25 | `sourcemethodname` | Source Method | character varying(60) | 허용 | — | — | Source Method Name |
| 26 | `loggername` | Logger | character varying(255) | 허용 | — | — | Logger Name |
| 27 | `lineno` | Line | numeric(10,0) | 허용 | — | 0 | Line No |
| 28 | `stacktrace` | Stack Trace | character varying(2000) | 허용 | — | — | System Log Trace |
| 29 | `errortrace` | Error Trace | character varying(2000) | 허용 | — | — | System Error Trace |
| 30 | `record_id` | Record ID | numeric(10,0) | 허용 | — | — | Direct internal record ID |
| 31 | `requestdocumentno` | Request Document No | character varying(30) | 허용 | — | — | iDempiere Request Document No |
| 32 | `a_asset_id` | Asset | numeric(10,0) | 허용 | — | — | Asset used internally or by customers |
| 33 | `r_request_id` | Request | numeric(10,0) | 허용 | — | — | Request from a Business Partner or Prospect |
| 34 | `responsetext` | Response Text | character varying(2000) | 허용 | — | — | Request Response Text |
| 35 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 36 | `processed` | Processed | character(1) | 불가 | — | 'N'::bpchar | The document has been processed |
| 37 | `isvanillasystem` | Vanilla System | character(1) | 허용 | — | 'N'::bpchar | The system was NOT compiled from Source - i.e. standard distribution |
| 38 | `isreproducible` | Reproducible | character(1) | 허용 | — | 'N'::bpchar | Problem can re reproduced in Gardenworld |
| 39 | `r_issueknown_id` | Known Issue | numeric(10,0) | 허용 | — | — | Known Issue |
| 40 | `statisticsinfo` | Statistics | character varying(255) | 허용 | — | — | Information to help profiling the system for solving support issues |
| 41 | `profileinfo` | Profile | character varying(4000) | 허용 | — | — | Information to help profiling the system for solving support issues |
| 42 | `systemstatus` | System Status | character(1) | 불가 | — | — | Status of the system - Support priority depends on system status |
| 43 | `r_issueproject_id` | Issue Project | numeric(10,0) | 허용 | — | — | Implementation Projects |
| 44 | `r_issueuser_id` | Issue User | numeric(10,0) | 허용 | — | — | User who reported issues |
| 45 | `r_issuesystem_id` | Issue System | numeric(10,0) | 허용 | — | — | System creating the issue |
| 46 | `issuesource` | Source | character(1) | 허용 | — | — | Issue Source |
| 47 | `ad_window_id` | Window | numeric(10,0) | 허용 | — | — | Data entry or display window |
| 48 | `ad_process_id` | Process | numeric(10,0) | 허용 | — | — | Process or Report |
| 49 | `ad_form_id` | Special Form | numeric(10,0) | 허용 | — | — | Special Form |
| 50 | `ad_issue_uu` | AD_Issue_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 9개 중 9개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["ad_form"]
    n2["ad_issue"]
    n3["ad_process"]
    n4["ad_window"]
    n5["r_issueknown"]
    n6["r_issueproject"]
    n7["r_issuesystem"]
    n8["r_issueuser"]
    n9["r_request"]
    n2 -->|"a_asset_id → a_asset_id"| n0
    n2 -->|"ad_form_id → ad_form_id"| n1
    n2 -->|"ad_process_id → ad_process_id"| n3
    n2 -->|"ad_window_id → ad_window_id"| n4
    n2 -->|"r_issueproject_id → r_issueproject_id"| n6
    n2 -->|"r_issuesystem_id → r_issuesystem_id"| n7
    n2 -->|"r_issueuser_id → r_issueuser_id"| n8
    n2 -->|"r_issueknown_id → r_issueknown_id"| n5
    n2 -->|"r_request_id → r_request_id"| n9
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aasset_adissue` <!-- FK_OUT: adempiere.ad_issue.aasset_adissue --> | [`ad_issue`](ad_issue.md) | `a_asset_id` | [`a_asset`](../a/a_asset.md) | `a_asset_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adform_adissue` <!-- FK_OUT: adempiere.ad_issue.adform_adissue --> | [`ad_issue`](ad_issue.md) | `ad_form_id` | [`ad_form`](ad_form.md) | `ad_form_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adprocess_adissue` <!-- FK_OUT: adempiere.ad_issue.adprocess_adissue --> | [`ad_issue`](ad_issue.md) | `ad_process_id` | [`ad_process`](ad_process.md) | `ad_process_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `adwindow_adissue` <!-- FK_OUT: adempiere.ad_issue.adwindow_adissue --> | [`ad_issue`](ad_issue.md) | `ad_window_id` | [`ad_window`](ad_window.md) | `ad_window_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissueproject_adissue` <!-- FK_OUT: adempiere.ad_issue.rissueproject_adissue --> | [`ad_issue`](ad_issue.md) | `r_issueproject_id` | [`r_issueproject`](../r/r_issueproject.md) | `r_issueproject_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissuesystem_ad_issue` <!-- FK_OUT: adempiere.ad_issue.rissuesystem_ad_issue --> | [`ad_issue`](ad_issue.md) | `r_issuesystem_id` | [`r_issuesystem`](../r/r_issuesystem.md) | `r_issuesystem_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissueuser_adissue` <!-- FK_OUT: adempiere.ad_issue.rissueuser_adissue --> | [`ad_issue`](ad_issue.md) | `r_issueuser_id` | [`r_issueuser`](../r/r_issueuser.md) | `r_issueuser_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rknownissue_adissue` <!-- FK_OUT: adempiere.ad_issue.rknownissue_adissue --> | [`ad_issue`](ad_issue.md) | `r_issueknown_id` | [`r_issueknown`](../r/r_issueknown.md) | `r_issueknown_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequest_adissue` <!-- FK_OUT: adempiere.ad_issue.rrequest_adissue --> | [`ad_issue`](ad_issue.md) | `r_request_id` | [`r_request`](../r/r_request.md) | `r_request_id` | SET NULL / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- `record_id`는 가리키는 테이블이 메타데이터에 따라 달라질 수 있습니다. 물리 FK 목록에 없는 대상은 별도 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
