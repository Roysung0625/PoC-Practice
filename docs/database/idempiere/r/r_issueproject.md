# r_issueproject — 문제 관련 프로젝트

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.r_issueproject` |
| 한국어 논리명(문서용 해석) | 문제 관련 프로젝트 |
| 원본 논리명 | Issue Project |
| 원본 사전 ID | 842 |
| 분류 | `r` — 요청·지원·상태 관리 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 16 |
| 나가는 FK / 들어오는 FK | 2 / 2 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

문제 보고와 관련된 프로젝트·자산 및 시스템 상태·통계 정보를 연결한다.

- 설명 근거: 물리명·열·외래키 구조를 근거로 보수적으로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `r_issueproject_pkey` | `r_issueproject_id` |
| UNIQUE | `r_issueproject_uu_idx` | `r_issueproject_uu` |

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `r_issueproject_id` | Issue Project | numeric(10,0) | 불가 | 예 | — | Implementation Projects |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `name` | Name | character varying(120) | 불가 | — | — | Alphanumeric identifier of the entity |
| 10 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 11 | `a_asset_id` | Asset | numeric(10,0) | 허용 | — | — | Asset used internally or by customers |
| 12 | `c_project_id` | Project | numeric(10,0) | 허용 | — | — | Financial Project |
| 13 | `statisticsinfo` | Statistics | character varying(60) | 허용 | — | — | Information to help profiling the system for solving support issues |
| 14 | `profileinfo` | Profile | character varying(4000) | 허용 | — | — | Information to help profiling the system for solving support issues |
| 15 | `systemstatus` | System Status | character(1) | 불가 | — | — | Status of the system - Support priority depends on system status |
| 16 | `r_issueproject_uu` | R_IssueProject_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["a_asset"]
    n1["ad_issue"]
    n2["c_project"]
    n3["r_issueproject"]
    n4["r_issuesource"]
    n3 -->|"a_asset_id → a_asset_id"| n0
    n3 -->|"c_project_id → c_project_id"| n2
    n1 -->|"r_issueproject_id → r_issueproject_id"| n3
    n4 -->|"r_issueproject_id → r_issueproject_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `aasset_rissueproject` <!-- FK_OUT: adempiere.r_issueproject.aasset_rissueproject --> | [`r_issueproject`](r_issueproject.md) | `a_asset_id` | [`a_asset`](../a/a_asset.md) | `a_asset_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `cproject_rissueproject` <!-- FK_OUT: adempiere.r_issueproject.cproject_rissueproject --> | [`r_issueproject`](r_issueproject.md) | `c_project_id` | [`c_project`](../c/c_project.md) | `c_project_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rissueproject_adissue` <!-- FK_IN: adempiere.ad_issue.rissueproject_adissue --> | [`ad_issue`](../ad/ad_issue.md) | `r_issueproject_id` | [`r_issueproject`](r_issueproject.md) | `r_issueproject_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissueproject_rissuesource` <!-- FK_IN: adempiere.r_issuesource.rissueproject_rissuesource --> | [`r_issuesource`](r_issuesource.md) | `r_issueproject_id` | [`r_issueproject`](r_issueproject.md) | `r_issueproject_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
