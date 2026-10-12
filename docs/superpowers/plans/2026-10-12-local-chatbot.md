# 로컬 분석 챗봇 구현 계획

> 실행 방식: 이 세션에서 직접 TDD로 구현한다. 사용자가 계획 구체화 후 구현을 요청했으므로 추가 승인 대기 없이 진행한다. AGENTS.md에 따라 요청하지 않은 후속 스킬·서브에이전트는 실행하지 않는다.

**Goal:** 사용자가 검토·승인한 SQL로 TPC-H SF1을 조회하여 표·그래프를 제공하는 Windows 로컬 앱을 구성한다.

**Architecture:** Laravel은 대화와 계획 이력을 보관하고 Python 작업 API를 호출한다. Python은 승인된 계획을 검증하고 읽기 전용 PostgreSQL 조회 및 그래프 생성을 담당한다. AWS 어댑터와 수신기는 동일 승인 계약을 사용하되 이번 실행은 로컬 검증으로 제한한다.

**Tech Stack:** Python 3.13/FastAPI/psycopg3/SQLGlot/Plotly/pytest, PostgreSQL 18, Laravel 13/PHP 8.4, Vue 3/TypeScript/Vite/Vitest/Playwright.

**Spec:** [설계](../specs/2026-10-12-local-chatbot.md)

## 공통 제약과 검토 초점

- 기존 Python/Node/AWS 작업 보존. 생성 데이터·비밀값은 `.local`, `.env`로 제외. 서비스는 127.0.0.1:5432/8000/8001.
- SQL 20초, 최대 500행/256KiB, 요청 60초, 동시 조회 2. SQL/조건 수정은 재승인. AWS 유료 호출은 실행하지 않는다.
- 승인 후 매개변수만 변조되는 경우 → digest와 승인 스냅샷 검사(Task 4).
- SQL 완료 후 응답 저장/전송 중 장애 → 재실행 대신 불명 상태 또는 저장 결과 재전송(Task 4, 6).
- CTE·하위 SELECT에 변경/시스템 접근 숨기기 → AST 및 DB 권한 이중 차단(Task 3).
- 500행 이내지만 큰 유니코드/금액 값 → 바이트 제한과 정확한 원본 표현(Task 3, 7).
- 미구성 AWS·만료 인증·시간 초과 → 실패 코드와 화면 표기, 빈 결과 금지(Task 5, 8).

## 파일과 인터페이스

| 구성 | 파일 | 책임 |
|---|---|---|
| Python | `local/python/poc/{config,contracts,db,sql_policy,journal,agent,receiver,charts,api}.py` | 설정/계약/DB/실행/승인/AWS/그래프/HTTP 경계 |
| 적재 | `local/python/poc/dataset.py` | SF1 생성·COPY·스키마 카탈로그 |
| 웹 | `local/web/app/Http/Controllers/AnalysisController.php`, `local/web/app/Services/AnalysisService.php` | 이력·승인·Python 통신 |
| 화면 | `local/web/resources/js/{App.vue,api.ts,types.ts}`, `local/web/resources/css/app.css` | 검토·승인·결과·후속 질문 |
| 운영 | `local/scripts/{Setup-Runtimes,Setup,Common,Start,Stop,Status,Check,Verify-Browser}.ps1` | 런타임·서비스·로그·점검 |
| 검증 | `local/python/tests/`, `local/web/tests/`, `local/web/resources/js/*.test.ts`, `local/web/e2e/` | 실제 동작 시험 |

계획 객체: `plan_id, revision, schema_version, question, interpretation, context, metrics, assumptions, missing_data, answer_steps, sql_steps, sql, params, chart, provenance, digest`.
승인 객체: `approval_id, request_id, plan, expires_at`. 결과: `status, columns, rows, row_count, elapsed_ms, truncated, error`와 별도 Plotly JSON. 오류에는 성공 rows를 넣지 않는다.
Python: `GET /health`, `GET /v1/schema`, `POST /v1/plans`, `POST /v1/executions`, `GET /v1/jobs/{id}`, `POST /v1/query`. 모든 /v1은 서버 전용 Bearer 인증.
Laravel: `GET /api/status`, `GET /api/conversations`, `POST /api/plans`, `POST /api/plans/{id}/revise`, `POST /api/plans/{id}/approve`, `GET /api/jobs/{id}`. 브라우저는 Laravel 세션/CSRF를 사용한다.

## 작업별 TDD

각 작업은 **테스트 작성 → 실패 관찰 → 최소 구현 → 해당 시험과 누적 회귀 시험 → 체크포인트 기록** 순서다. 최초 의존성 오류는 RED 증거로 세지 않으며 테스트 수집 후 기능 부재로 실패해야 한다. Git 저장소가 없어 커밋 대신 아래 체크박스와 검증 문서로 추적한다.

### Task 1: 설정과 실행 기반
- [x] `tests/test_config.py`: 엄격 상한 미보장 시 `COST_POLICY_BLOCKED`, 모델 설정 읽기, 다른 모델 자동 대체 없음, .env 비밀값 제외를 확인한다.
- [x] `config.py`의 `load_shared(root)`, `environment()`, `require_live_aws(policy)`를 구현한다. Python 가상환경과 PHP/Node 도구를 준비한다.
- [x] `python -m pytest tests/test_config.py -q` RED/GREEN을 기록한다.

### Task 2: 실제 DB와 데이터
- [x] `tests/test_dataset.py`: 작은 fixture의 테이블/열/금액 유형·관계, 재적재 시 중복 없음, 카탈로그 날짜·제품군을 확인한다.
- [x] `dataset.py`에 `generate(directory, scale)`, `load_dataset(admin_dsn, directory, reader_role)`와 `read_catalog(dsn)`를 구현한다. 전용 DB/role, 8테이블, PK/FK/index, COPY, ANALYZE, manifest를 추가한다.
- [x] 실제 PostgreSQL에서 작은 시험을 통과한 후 SF1을 한 번 적재하고 생성/적재 행 수를 대조한다.

### Task 3: 안전한 SQL 실행
- [x] `tests/test_sql_policy.py`, `tests/test_db.py`: 정상 집계/CTE, 다중문·변경 CTE·SELECT INTO·잠금·시스템/위험 함수 거부, 누락 매개변수를 검증한다.
- [x] `sql_policy.py`의 `validate_sql(sql, params, tables)` 및 `db.py`의 `execute_query(sql, params, deadline)`를 구현한다.
- [x] 실제 DB fixture는 매출 280.00, 공급원가 차감액 60.00, 공급업체 2개를 기대한다. 501행 잘림, 256KiB 초과, 20초 취소·롤백, 읽기 전용 역할 쓰기 거부를 시험한다.
- [x] 서버 커서로 제한된 결과를 읽고 Decimal/date를 직렬화한다. SQL 오류·시간 초과를 별도 오류로 반환한다.

### Task 4: 승인과 작업 영속성
- [x] `tests/test_journal.py`, `tests/test_regressions.py`: 승인 없는 요청/SQL·params 변조/만료/중복 요청·중복 승인·과거 revision을 거부한다. 재시작 중 실행은 `OUTCOME_UNKNOWN`으로 바뀌고 재실행되지 않는다.
- [x] `contracts.py` canonical digest, `journal.py` SQLite 트랜잭션 claim 및 `api.py`의 백그라운드 작업 수행기를 구현한다. 재전송은 저장된 결과를 반환한다.
- [x] `python -m pytest tests/test_journal.py tests/test_regressions.py -q` 및 앞 작업 회귀를 실행한다.

### Task 5: Agent 경계와 FastAPI
- [x] `tests/test_api.py`, `tests/test_agent.py`: 토큰 누락, 샘플 계획의 출처·순이익 한계, 미구성·비용 차단, malformed Agent 응답, 승인 전 SQL 미실행을 시험한다.
- [x] `agent.py`는 실제 AgentCore SDK 경계만 주입 가능하게 하고, 계획 생성/실행 단계를 분리한다. 자연어 수정은 새 계획이며 샘플 결과를 AI 응답으로 위장하지 않는다.
- [x] `api.py`는 SQLite 작업 상태를 반환하고 긴 실행은 제한된 백그라운드 executor로 수행한다. 재시작 복구·명확한 오류를 구현한다.

### Task 6: SQS/DynamoDB 수신기
- [x] `tests/test_receiver.py`: 만료 요청 미실행, 중복 실행 방지, 결과 저장 후 삭제, 전송 실패 시 outbox 재전송, stale worker 조건부 갱신을 모의 AWS 경계에서 검증한다.
- [x] `receiver.py`에 `process_message(message)`와 결과 outbox를 구현한다. SQS poll20/visibility90, 명시적인 인증·연결 오류와 재접속을 제공한다.
- [x] Lambda 쪽 계약·상태/TTL/대기 시간은 AWS 연동 문서에 기록한다. 이 로컬 작업의 실제 Lambda/Agent 배포·왕복 검증은 별도 AWS 작업의 기록과 구분한다.

### Task 7: 표와 그래프
- [x] `tests/test_charts.py`: 결과에 없는 열, 허용하지 않은 그래프, 정확한 Decimal 원본 보존, 빈 결과를 시험한다.
- [x] `charts.py`의 `build_chart(result, chart_spec)`는 Plotly bar/line JSON만 만들고 원본 rows를 바꾸지 않는다. 임의 HTML/JS는 수용하지 않는다.

### Task 8: Laravel 대화·승인 이력
- [x] PHPUnit Feature 시험으로 계획 저장/수정 시 이전 revision 무효/중복 승인 방지/Python 실패 상태 저장/대화 문맥 전달을 검증한다.
- [x] 마이그레이션·서비스·컨트롤러·라우트를 구현한다. 승인 스냅샷은 변경하지 않고 Python에 전달한다. 토큰은 서버 환경에만 둔다.
- [x] `php artisan test`로 전체 회귀를 통과시킨다.

### Task 9: Vue 검토·승인 화면
- [x] Vitest에서 승인 전 결과 없음, 계획·SQL·가정 표시, 수정 후 재승인, 오류/잘림/표/그래프 표현을 시험한다.
- [x] 질문/샘플 실행/계획 검토/승인/결과/후속 질문 UI와 일관된 한국어 상태 표시를 구현한다. 샘플과 AWS 미구성을 눈에 보이게 구분한다.
- [x] `npm test -- --run`, `npm run typecheck`, `npm run build`와 Playwright 실제 로컬 샘플 흐름을 검증한다.

### Task 10: 운영과 최종 검증
- [x] 시작/상태/중지에서 프로젝트가 소유한 프로세스만 관리하고 다른 작업 디렉터리에서도 동작하는지 실제 점검한다.
- [x] 서비스·로그·설정·적재·토큰·재접속·중단 복구·검증 경계를 `local/README.md`에 작성하고 루트 README를 갱신한다.
- [x] 전체 Python/PHP/Vue 시험, 빌드, SF1 실제 HTTP 승인 조회를 실행하고 `docs/verification/2026-10-12-local.md`에 명령·결과·미검증 항목을 기록한다.

## 자체 검토

설계의 승인/DB/화면/운영/모델/비용 항목을 작업에 배정했다. 위 5개 실패 조건은 Task 3~8에서 검증한다. Python과 Laravel은 동일 계획 JSON을 저장하며 해시 재계산은 Python에만 둔다. AWS 실연결은 모의 테스트로 완료 처리하지 않는다.

## 최종 반영 — 2026-10-12

- writing-plans로 세부 작업을 정리하고 TDD로 구현했다. 위 체크는 이 로컬 구현 범위의 완료 표시다.
- 최종 구현의 함수·파일 이름을 위 표에 반영했다. 작업 수행은 별도 execution 모듈 대신 api와 journal에서 담당한다.
- 최종 전체 Python 시험: 81개 통과, 실패·오류·건너뜀 0개(14.993초). Laravel 7개, Vue 5개, 실제 Chromium 2개 통과. 타입 검사·프로덕션 빌드 완료.
- 운영·브라우저 시험은 기존 앱에 간섭하지 않도록 별도 포트와 상태 DB를 사용한다.
- 비용 정책은 같은 폴더의 별도 AWS 작업에서 지연된 월 25 USD 초과 차단으로 갱신됐다. 엄격 상한 요구 시의 차단 시험은 유지한다.
- AWS 설정·실행 중인 수신기 존재는 실제 왕복 성공의 증거가 아니다. 이 작업은 유료 AWS 호출을 하지 않았다.
- 동기식 계획 생성, 로그인 세션 운영, Plotly 번들 경고와 미재현 네이티브 진단의 한계는 [검증 기록](../../verification/2026-10-12-local.md)에 남겼다.
