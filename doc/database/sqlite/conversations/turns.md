# 웹 질문 차례 — `turns`

<!-- table-id: sqlite:.local/analysis-chatbot/conversations.sqlite#main.turns -->

[전체 일람](../../index.md) · [운영 공통 주의](../../operational-stores.md)

물리 식별자: `.local/analysis-chatbot/conversations.sqlite#main.turns`. 파일 DB·스키마·물리 테이블을 함께 식별합니다. 논리명 ‘웹 질문 차례’은 소스 사용 흐름을 설명한 추론명이며 DB의 공식 논리명이 아닙니다.

메타데이터 확인: 2026-11-03T23:33:22+09:00. SQLite URI `mode=ro`, `query_only=ON`의 `sqlite_master`/PRAGMA만 조회했습니다. 업무 행은 읽지 않았습니다.

근거: [생성/선언 소스](../../../../analysis-chatbot/database/migrations/2026_11_03_000001_create_conversations.php) · [메타데이터 근거](../../metadata-evidence.json).

## 한 행과 사용 흐름

- 한 행: 대화의 순번별 사용자 요청과 마지막 분석 상태 한 건.
- 흐름: 요청 저장→Python API 실행/조회→이벤트 병합→snapshot 보존.
- 조건·보존: 통신 장애 시 기존 결과/이미지를 지우지 않는다. run_id는 외부 SQLite 원장과 논리 연결이며 물리 FK가 아니다.

## 컬럼

NULL은 SQLite가 보고한 `notnull` 플래그 그대로입니다. rowid 테이블의 TEXT/복합 PRIMARY KEY는 명시적 NOT NULL과 다를 수 있으므로 PK라는 이유로 NULL 금지로 바꾸어 기록하지 않습니다. 타입은 SQLite 선언 타입이며 UUID/JSON의 강제 검증을 의미하지 않습니다.

| 순서 | 물리명 | 논리 설명(추론) | 선언 타입 | NULL(notnull) | 기본값 | PK 순서 |
|---:|---|---|---|---|---|---:|
| 1 | `id` | 테이블 행 식별자 | `varchar` | 금지(1) | `미지정` | 1 |
| 2 | `conversation_id` | 대화 ID | `varchar` | 금지(1) | `미지정` | 0 |
| 3 | `position` | 대화 안 질문 순서 | `INTEGER` | 금지(1) | `미지정` | 0 |
| 4 | `client_request_id` | 클라이언트 중복 제어 ID | `varchar` | 금지(1) | `미지정` | 0 |
| 5 | `input` | 사용자 입력 JSON | `TEXT` | 금지(1) | `미지정` | 0 |
| 6 | `input_hash` | 입력 요청 SHA-256 | `varchar` | 금지(1) | `미지정` | 0 |
| 7 | `run_id` | 분석 실행 ID | `varchar` | 허용(0) | `미지정` | 0 |
| 8 | `status` | 처리 상태 | `varchar` | 금지(1) | `미지정` | 0 |
| 9 | `snapshot` | 분석 응답 저장 JSON | `TEXT` | 금지(1) | `'{}'` | 0 |
| 10 | `events` | 누적 이벤트 JSON | `TEXT` | 금지(1) | `'[]'` | 0 |
| 11 | `transport_error` | API 통신 오류 JSON | `TEXT` | 허용(0) | `미지정` | 0 |
| 12 | `created_at` | 생성 시각 | `datetime` | 허용(0) | `미지정` | 0 |
| 13 | `updated_at` | 갱신 시각 | `datetime` | 허용(0) | `미지정` | 0 |

## 키와 인덱스

PRIMARY KEY 순서: `id`.

생성 원인은 SQLite PRAGMA의 `pk`=PRIMARY KEY, `u`=UNIQUE 제약, `c`=CREATE INDEX입니다.

| 인덱스 | UNIQUE | 열 순서 | 생성 원인 | 조건 |
|---|---|---|---|---|
| `turns_run_id_unique` | 예 | run_id | c | 없음 |
| `turns_client_request_id_unique` | 예 | client_request_id | c | 없음 |
| `turns_conversation_id_position_unique` | 예 | conversation_id → position | c | 없음 |
| `sqlite_autoindex_turns_1` | 예 | id | pk | 없음 |

## 물리 FK: 나가는 방향과 들어오는 방향

| 방향 | 자식 열 | 부모 테이블·열 | ON DELETE | ON UPDATE |
|---|---|---|---|---|
| 들어옴 | `artifacts.turn_id` | [turns.id](turns.md) | CASCADE | NO ACTION |
| 나감 | `turns.conversation_id` | [conversations.id](conversations.md) | CASCADE | NO ACTION |

## 논리 연결과 주의

turns.run_id → 다른 파일 DB의 analysis_runs.run_id; source_result_id는 input JSON 안의 논리 참조

물리 FK가 없으면 삭제/갱신 전파를 DB가 보장하지 않습니다. 서로 다른 SQLite 파일과 JSON 안 참조는 애플리케이션 검증에 의존합니다. Laravel FK 선언은 확인했지만 실행 중 연결에서의 외래키 동작 시험은 이번 범위에서 수행하지 않았습니다.
