# r_issueknown — 알려진 문제

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.r_issueknown` |
| 한국어 논리명(문서용 해석) | 알려진 문제 |
| 원본 논리명 | Known Issue |
| 원본 사전 ID | 839 |
| 분류 | `r` — 요청·지원·상태 관리 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 21 |
| 나가는 FK / 들어오는 FK | 3 / 1 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

이미 알려진 문제 정보를 관리한다.

- 설명 근거: 원본 애플리케이션 사전 명칭·설명을 한국어로 해석.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: Known Issue
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `r_issueknown_pkey` | `r_issueknown_id` |
| UNIQUE | `r_issueknown_uu_idx` | `r_issueknown_uu` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `r_knownissue_alt`: `CREATE UNIQUE INDEX r_knownissue_alt ON adempiere.r_issueknown USING btree (issuesummary, releaseno, sourceclassname, sourcemethodname, loggername, lineno)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `r_issueknown_id` | Known Issue | numeric(10,0) | 불가 | 예 | — | Known Issue |
| 2 | `ad_client_id` | Tenant | numeric(10,0) | 불가 | — | — | Tenant for this installation. |
| 3 | `ad_org_id` | Organization | numeric(10,0) | 불가 | — | — | Organizational entity within tenant |
| 4 | `isactive` | Active | character(1) | 불가 | — | 'Y'::bpchar | The record is active in the system |
| 5 | `created` | Created | timestamp without time zone | 불가 | — | now() | Date this record was created |
| 6 | `createdby` | Created By | numeric(10,0) | 불가 | — | — | User who created this records |
| 7 | `updated` | Updated | timestamp without time zone | 불가 | — | now() | Date this record was updated |
| 8 | `updatedby` | Updated By | numeric(10,0) | 불가 | — | — | User who updated this records |
| 9 | `issuesummary` | Issue Summary | character varying(255) | 불가 | — | — | Issue Summary |
| 10 | `releaseno` | Release No | character varying(10) | 불가 | — | — | Internal Release Number |
| 11 | `sourceclassname` | Source Class | character varying(60) | 허용 | — | — | Source Class Name |
| 12 | `sourcemethodname` | Source Method | character varying(60) | 허용 | — | — | Source Method Name |
| 13 | `loggername` | Logger | character varying(60) | 허용 | — | — | Logger Name |
| 14 | `lineno` | Line | numeric(10,0) | 허용 | — | 0 | Line No |
| 15 | `description` | Description | character varying(255) | 허용 | — | — | Optional short description of the record |
| 16 | `issuestatus` | Issue Status | character varying(2000) | 허용 | — | — | Current Status of the Issue |
| 17 | `r_issuestatus_id` | Issue Status | numeric(10,0) | 허용 | — | — | Status of an Issue |
| 18 | `r_request_id` | Request | numeric(10,0) | 허용 | — | — | Request from a Business Partner or Prospect |
| 19 | `processing` | Process Now | character(1) | 허용 | — | — | — |
| 20 | `r_issuerecommendation_id` | Issue Recommendation | numeric(10,0) | 허용 | — | — | Recommendations how to fix an Issue |
| 21 | `r_issueknown_uu` | R_IssueKnown_UU | uuid | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 4개 중 4개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["ad_issue"]
    n1["r_issueknown"]
    n2["r_issuerecommendation"]
    n3["r_issuestatus"]
    n4["r_request"]
    n1 -->|"r_issuerecommendation_id → r_issuerecommendation_id"| n2
    n1 -->|"r_issuestatus_id → r_issuestatus_id"| n3
    n1 -->|"r_request_id → r_request_id"| n4
    n0 -->|"r_issueknown_id → r_issueknown_id"| n1
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rissuerecommendation_rissuekno` <!-- FK_OUT: adempiere.r_issueknown.rissuerecommendation_rissuekno --> | [`r_issueknown`](r_issueknown.md) | `r_issuerecommendation_id` | [`r_issuerecommendation`](r_issuerecommendation.md) | `r_issuerecommendation_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissuestatus_rissueknown` <!-- FK_OUT: adempiere.r_issueknown.rissuestatus_rissueknown --> | [`r_issueknown`](r_issueknown.md) | `r_issuestatus_id` | [`r_issuestatus`](r_issuestatus.md) | `r_issuestatus_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rrequest_rissueknown` <!-- FK_OUT: adempiere.r_issueknown.rrequest_rissueknown --> | [`r_issueknown`](r_issueknown.md) | `r_request_id` | [`r_request`](r_request.md) | `r_request_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rknownissue_adissue` <!-- FK_IN: adempiere.ad_issue.rknownissue_adissue --> | [`ad_issue`](../ad/ad_issue.md) | `r_issueknown_id` | [`r_issueknown`](r_issueknown.md) | `r_issueknown_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
