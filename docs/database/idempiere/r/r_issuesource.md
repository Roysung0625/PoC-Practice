# r_issuesource — 문제 발생 출처

[전체 일람](../TABLE_INDEX.md) · [분류 일람](README.md) · [AI 사용 안내](../README.md) · [외래키 읽는 법](../RELATIONSHIPS.md)

## 기본 정보

| 항목 | 내용 |
|---|---|
| 물리명 | `adempiere.r_issuesource` |
| 한국어 논리명(문서용 해석) | 문제 발생 출처 |
| 원본 논리명 | — |
| 원본 사전 ID | 미등록 |
| 분류 | `r` — 요청·지원·상태 관리 |
| 전체 테넌트 행 수 | 0 |
| 물리 열 수 | 13 |
| 나가는 FK / 들어오는 FK | 3 / 0 |
| 구조·행 수 확인 시점 | 2026-11-03T23:29:01+09:00 |

## 의미와 쓰임

문제 관련 시스템·프로젝트·사용자를 통계 및 프로파일 정보와 연결한다. 상세 수집 방식은 확인이 필요하다.

- 설명 근거: 역할을 확정할 사전 정보 부족: 구조에 따른 잠정 해석, 확인 필요.
- 한국어 이름과 개요는 문서용 해석입니다. 공식 한국어 번역으로 간주하지 않습니다.
- 원본 설명: —
- 원본 도움말: —
- PostgreSQL 테이블 주석: —

## 키와 열

### 기본키·고유 제약조건

| 종류 | 제약조건 | 열(순서 유지) |
|---|---|---|
| PRIMARY KEY | `r_issuesource_pkey` | `r_issuesource_id` |

### 별도 고유 인덱스

PK·UNIQUE 제약조건의 인덱스와 별도로 존재하는 고유 인덱스입니다. 식·조건·열 순서는 원본 정의를 따릅니다.

- `r_issuesource_spo`: `CREATE UNIQUE INDEX r_issuesource_spo ON adempiere.r_issuesource USING btree (r_issuesystem_id, r_issueproject_id, r_issueuser_id)`

### 열 목록

원본 논리명·설명은 `AD_Column`에서 가져왔습니다. 기본값은 실제 PostgreSQL 메타데이터이며, 비어 있는 항목은 `—`로 표시합니다.

| 순서 | 물리명 | 원본 논리명 | PostgreSQL 타입 | NULL | PK | 기본값 | 설명 |
|---:|---|---|---|---|---|---|---|
| 1 | `r_issuesource_id` | — | numeric(10,0) | 불가 | 예 | — | — |
| 2 | `ad_client_id` | — | numeric(10,0) | 불가 | — | — | — |
| 3 | `ad_org_id` | — | numeric(10,0) | 불가 | — | — | — |
| 4 | `isactive` | — | character(1) | 불가 | — | 'Y'::bpchar | — |
| 5 | `created` | — | timestamp without time zone | 불가 | — | now() | — |
| 6 | `createdby` | — | numeric(10,0) | 불가 | — | — | — |
| 7 | `updated` | — | timestamp without time zone | 불가 | — | now() | — |
| 8 | `updatedby` | — | numeric(10,0) | 불가 | — | — | — |
| 9 | `r_issuesystem_id` | — | numeric(10,0) | 불가 | — | — | — |
| 10 | `r_issueproject_id` | — | numeric(10,0) | 불가 | — | — | — |
| 11 | `r_issueuser_id` | — | numeric(10,0) | 불가 | — | — | — |
| 12 | `statisticsinfo` | — | character varying(60) | 허용 | — | — | — |
| 13 | `profileinfo` | — | character varying(60) | 허용 | — | — | — |

## 외래키 흐름

화살표는 **FK를 가진 자식 → 참조되는 부모**입니다. 업무 처리의 시간 순서나 무조건적인 1:N 관계를 뜻하지 않습니다.

주변 관계 3개 중 3개를 그림으로 표시합니다. **전체 관계는 아래 두 표에 모두 포함**합니다.

```mermaid
flowchart LR
    n0["r_issueproject"]
    n1["r_issuesource"]
    n2["r_issuesystem"]
    n3["r_issueuser"]
    n1 -->|"r_issueproject_id → r_issueproject_id"| n0
    n1 -->|"r_issuesystem_id → r_issuesystem_id"| n2
    n1 -->|"r_issueuser_id → r_issueuser_id"| n3
```

### 이 테이블이 참조하는 부모 — 나가는 FK

| 제약조건 | 참조하는 쪽(자식) | 자식 열 | 참조받는 쪽(부모) | 부모 열 | 삭제 / 갱신 | 검증 / 지연 가능 |
|---|---|---|---|---|---|---|
| `rissueproject_rissuesource` <!-- FK_OUT: adempiere.r_issuesource.rissueproject_rissuesource --> | [`r_issuesource`](r_issuesource.md) | `r_issueproject_id` | [`r_issueproject`](r_issueproject.md) | `r_issueproject_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissuesystem_rissuesource` <!-- FK_OUT: adempiere.r_issuesource.rissuesystem_rissuesource --> | [`r_issuesource`](r_issuesource.md) | `r_issuesystem_id` | [`r_issuesystem`](r_issuesystem.md) | `r_issuesystem_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |
| `rissueuser_rissuesource` <!-- FK_OUT: adempiere.r_issuesource.rissueuser_rissuesource --> | [`r_issuesource`](r_issuesource.md) | `r_issueuser_id` | [`r_issueuser`](r_issueuser.md) | `r_issueuser_id` | NO ACTION / NO ACTION | 완료 / 가능 (초기 지연) |

### 이 테이블을 참조하는 자식 — 들어오는 FK

해당 방향의 물리 FK 제약조건은 없습니다. 이름이 비슷한 열만으로 관계를 추가하지 않습니다.

## 조회 시 주의

- FK 표의 자식 열과 부모 열을 같은 순서로 대응시킵니다. 복합 FK는 모든 열의 동등 조건을 `AND`로 연결합니다.
- 테이블 이름이나 `_id` 열 이름만으로 물리 FK가 있다고 가정하지 않습니다. FK 미선언은 업무 관계가 없다는 뜻도 아닙니다.
- 자식이 여러 행인 테이블과 조인하면 부모의 금액·건수가 중복될 수 있습니다. 집계 단위를 먼저 정합니다.
- `ad_client_id`가 있습니다. 업무 분석에서는 대상 테넌트를 명시합니다. GardenWorld는 `11`, 시스템 공통 설정은 `0`일 수 있으므로 일괄 필터 적용 전에 테이블 역할을 확인합니다.
- 수집 시점에 0행입니다. 이 표만으로 거래 실적·처리 결과를 계산할 수 없습니다.
- 행 수는 위 확인 시점의 전체 테넌트 값입니다. 최신 업무 실적이나 현재 실행 결과로 재사용하지 않습니다.
