# 승인 SQL 계획 — `plans`

<!-- table-id: sqlite:.local/jobs.sqlite#main.plans -->

[전체 일람](../../index.md) · [운영 공통 주의](../../operational-stores.md)

물리 식별자: `.local/jobs.sqlite#main.plans`. 파일 DB·스키마·물리 테이블을 함께 식별합니다. 논리명 ‘승인 SQL 계획’은 소스 사용 흐름을 설명한 추론명이며 DB의 공식 논리명이 아닙니다.

메타데이터 확인: 2026-11-03T23:33:22+09:00. SQLite URI `mode=ro`, `query_only=ON`의 `sqlite_master`/PRAGMA만 조회했습니다. 업무 행은 읽지 않았습니다.

근거: [생성/선언 소스](../../../../local/python/poc/journal.py) · [메타데이터 근거](../../metadata-evidence.json).

## 한 행과 사용 흐름

- 한 행: 계획 ID와 개정별 봉인 SQL 계획 한 건.
- 흐름: 계획 생성→digest 검증→저장→승인 시 최신 개정 조회.
- 조건·보존: 계획 payload와 digest를 함께 보존한다. 개정만 바꾸거나 승인 근거를 수동 수정하지 않는다.

## 컬럼

NULL은 SQLite가 보고한 `notnull` 플래그 그대로입니다. rowid 테이블의 TEXT/복합 PRIMARY KEY는 명시적 NOT NULL과 다를 수 있으므로 PK라는 이유로 NULL 금지로 바꾸어 기록하지 않습니다. 타입은 SQLite 선언 타입이며 UUID/JSON의 강제 검증을 의미하지 않습니다.

| 순서 | 물리명 | 논리 설명(추론) | 선언 타입 | NULL(notnull) | 기본값 | PK 순서 |
|---:|---|---|---|---|---|---:|
| 1 | `plan_id` | 승인 대상 계획 ID | `TEXT` | 허용(0) | `미지정` | 1 |
| 2 | `revision` | 계획 개정 번호 | `INTEGER` | 허용(0) | `미지정` | 2 |
| 3 | `digest` | 계획 내용 SHA-256 | `TEXT` | 허용(0) | `미지정` | 0 |
| 4 | `payload` | 구조화 JSON 내용 | `TEXT` | 허용(0) | `미지정` | 0 |

## 키와 인덱스

PRIMARY KEY 순서: `plan_id` → `revision`.

생성 원인은 SQLite PRAGMA의 `pk`=PRIMARY KEY, `u`=UNIQUE 제약, `c`=CREATE INDEX입니다.

| 인덱스 | UNIQUE | 열 순서 | 생성 원인 | 조건 |
|---|---|---|---|---|
| `sqlite_autoindex_plans_1` | 예 | plan_id → revision | pk | 없음 |

## 물리 FK: 나가는 방향과 들어오는 방향

| 방향 | 자식 열 | 부모 테이블·열 | ON DELETE | ON UPDATE |
|---|---|---|---|---|
| 없음 | 물리 FK 선언 없음 | 논리 관계와 구분 | 해당 없음 | 해당 없음 |

## 논리 연결과 주의

jobs.plan_id,revision → plans.plan_id,revision (논리 연결; 물리 FK 없음)

물리 FK가 없으면 삭제/갱신 전파를 DB가 보장하지 않습니다. 서로 다른 SQLite 파일과 JSON 안 참조는 애플리케이션 검증에 의존합니다. Laravel FK 선언은 확인했지만 실행 중 연결에서의 외래키 동작 시험은 이번 범위에서 수행하지 않았습니다.
