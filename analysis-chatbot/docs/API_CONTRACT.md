# 대화형 분석 공통 계약 v1

이 문서는 웹·기존 Python API·가시화 모듈의 구현 계약이다. 기존 `/v1/plans`, `/v1/executions`, `/v1/jobs`, `/v1/query`는 호환 유지한다. Python 원장은 기존 `.local/jobs.sqlite` 하나를 사용한다. 모든 새 Python API는 기존 Bearer 인증을 사용한다.

## 식별자와 소유권

- `conversation_id`, `turn_id`, `client_request_id`, `run_id`, `result_id`, `artifact_id`: UUID 문자열.
- 웹이 conversation/turn/client_request ID를 정하고, Python이 run/result/artifact ID를 정한다.
- Python은 conversation/turn 연결을 저장하고 서버가 저장된 result ID로만 문맥을 복원한다. 타 대화 result 참조는 거부한다.
- 재시각화·재설명 턴은 새 파생 `result_id`를 만들고 `source_result_id`, 원본 `data_sha256`, 현재 `chart_spec`·`chart_validation`을 저장한다. 원본 데이터와 승인 plan/digest는 유지하고 SQL을 실행하지 않는다. 재시각화 뒤 재설명은 그 턴에 저장된 차트·값 단위를 참조한다. 과거 기본 차트 선택 근거는 현재 정규화 명세 전체가 같을 때만 유지한다. 사용자가 x/y/type 등을 바꾸면 원본 승인 plan은 보존하고 현재 결과의 과거 기본선택 근거를 제외한다.
- 새 SQL 승인 기록과 중복 방지는 기존 journal jobs가 기준이다. Laravel은 승인 결과를 표시용으로만 복제한다.
- 이벤트 ID는 run 안에서 단조 증가 정수, 시간은 UTC ISO 8601 문자열이다.

## Python 비동기 API

`POST /v1/planning-runs` → 202 Run

```json
{"conversation_id":"uuid","turn_id":"uuid","client_request_id":"uuid","question":"질문","mode":"agent","source_result_id":null,"confirmed_conditions":{}}
```

mode는 `agent` 또는 명시적인 로컬 연결 검사 `sample`이다. sample은 실제 DB의 고정된 조회를 사용하며 AI 응답으로 표시하지 않는다. 이전 조건은 저장된 같은 대화 문맥과 함께 검증한다. 하나의 대화에 진행 중 run은 하나만 허용한다. 동일 client_request_id+동일 입력은 기존 run, 다른 입력은 충돌이다.

`confirmed_conditions`는 SQL 필터와 날짜·지표 기준의 flat scalar 객체다. 예: `client_id:11`, `issotrx:"Y"`, `docstatus:"CO,CL"`, `start:"2003-01-01"`, `end:"2004-01-01"`, `date_basis:"dateinvoiced"`, `metric_basis:"totallines"`. 집계 차원·여러 지표·표시 방식은 조건 배열로 넣지 않고 질문·해석·저장 계획에 보존한다. 해석 모델에는 실제 카탈로그의 dataset·tenant·date_range·business_rules를 전달한다. 전체 기간은 날짜 필터 생략이며, ARC 차감은 행 제외가 아닌 금액 CASE 규칙이다.

내부 해석 응답의 `condition_changes:[{key,quote}]`는 현재 질문/답변 원문의 인용과 키별 값 연관성을 호스트가 확인한다. 명시한 연도 변경은 정확한 `[연도-01-01, 다음연도-01-01)` 범위를 함께 검사한다. 근거 없는 충돌·부정 지시·제목 변경은 추가 확인 대상으로 남고, 이전 조건 키를 자동 삭제하지 않는다. 부정 표현이 섞인 복잡한 문장이나 기존 기간 제한을 완전히 없애는 요청은 보수적으로 재확인을 요구할 수 있다. 새 SQL은 이 해석과 별개로 계획 승인이 필요하다.

`POST /v1/result-runs` → 202 Run: 위 필드와 `source_result_id`(필수), `action: "rechart" | "reexplain"`, 선택적인 `chart_spec`. SQL을 실행하지 않는다.

`GET /v1/planning-runs/{run_id}?after_event_id=0` → Run (새 이벤트만 반환, 나머지 현재 상태는 항상 반환)

```json
{
  "run_id":"uuid","conversation_id":"uuid","turn_id":"uuid",
  "status":"running","phase":"interpreting","question":"질문",
  "interpretation":null,"confirmed_conditions":{},"clarification":null,
  "plan":null,"request_id":null,"result_id":null,"result":null,
  "validation":[],"artifacts":[],"insights":null,"error":null,
  "events":[{"id":1,"at":"2026-11-03T00:00:00+00:00","stage":"accepted","message":"질문을 접수했습니다.","data":{}}],
  "last_event_id":1
}
```

status: `queued`, `running`, `awaiting_answer`, `awaiting_approval`, `succeeded`, `partial`, `failed`, `cancelled`, `interrupted`.
phase: `accepted`, `interpreting`, `researching`, `planning`, `awaiting_answer`, `awaiting_approval`, `executing`, `validating`, `rendering`, `insights`, `complete`, `failed`, `cancelled`, `interrupted`.
`succeeded`, `partial`, `failed`, `cancelled`, `interrupted`는 종료 상태다. `partial`은 원본 표가 보존된 후처리 실패다.

- `POST /v1/planning-runs/{run_id}/answers` body `{ "answer": "..." }` → 202 Run.
- `POST /v1/planning-runs/{run_id}/approve` body `{ "plan_id":"...", "digest":"..." }` → 202 Run. v2 문서 근거와 조건·SQL·schema digest를 다시 검사한다.
- `POST /v1/planning-runs/{run_id}/cancel` body `{}` → Run. 실행 중 SQL의 물리적 취소를 보장하지 않는다.
- `POST /v1/planning-runs/{run_id}/retry-postprocess` body `{ "stage": "visualization" | "insights" | "all" }` → 202 Run. 저장된 원본 result만 사용한다.
- `GET /v1/artifacts/{artifact_id}?conversation_id=uuid` → PNG bytes (소유권 검사). `Content-Type: image/png`, 파일명은 서버 생성.

plan은 기존 plan 필드(`plan_id`, `revision`, `digest`, `sql`, `params`, `interpretation`, `metrics`, `assumptions`, `answer_steps`, `validation`)에 `contract_version:2`, `confirmed_conditions`, `schema_selection`, `document_evidence`, `joins`, `chart`를 추가한다. 웹은 SQL/params/테이블/조건/지표/관계/근거를 모두 보여주고 승인한다.

`document_evidence.projection_version="markdown-evidence-v1"`인 새 계획은 호스트가 원본 MD 전체를 읽고 원본 `documents[].sha256`을 확인한 뒤 결정적으로 투영한다. FK 중복 HTML 주석·실제 FK 표와 일치하는 Mermaid·Markdown 링크 주소만 제거하며 표시 텍스트, 모든 열의 물리/논리명·타입, 부모/자식 FK, 조회 주의를 보존한다. 최종 모델 호출에도 이 실제 문서 근거를 전달한다. `context_sha256`·`context_bytes`는 실제 전달한 documents의 canonical JSON 기준이며 승인 검증 시 같은 투영을 재구성한다. 투영 버전이 없는 과거 저장 계획은 기존 원문 방식으로 검증한다. 원본 MD와 128KiB 한도는 바꾸지 않는다.

차트는 승인 digest를 만들기 전에 `chart_unit`·`chart_dimensions` 검증과 정규화를 수행한다. 단위는 모델 라벨이 아닌 SQL AST·문서의 물리 열 계보로 확인한다. 금액은 연결된 통화 열로 분할하고 임의 `value_unit`을 제거하며, COUNT는 `건`으로 고정한다. 실제 수량 UOM·복잡한 표현식의 단위가 증명되지 않으면 `수량 단위 미검증` 또는 `단위 미검증`으로 표시하고 검증 상태는 `unverified`다. 제목·y축·범례는 금액/건수/수량/조회 값의 호스트 중립 표기로 정규화한다. SQL·params·원본 행을 이 과정에서 바꾸지 않는다. 재사용 턴도 재검증하며 정규화로 차트가 달라지면 새 파생 결과의 PNG를 생성하고 원본 승인 계획과 SQL은 재실행하지 않는다.

`condition_bindings`는 조건 키를 검증 근거에 대응하는 객체다. 배열 등 다른 형식은 `CONDITION_BINDINGS_INVALID`로 거부한다. `kind:"predicate"` 근거의 EQ/IN은 실제 반환 행을 제한하는 물리 열과 값이 일치해야 하며, 리터럴 또는 이름 있는 scalar 매개변수를 호스트가 대조한다. 예를 들어 `docstatus IN (%(status_co)s, %(status_cl)s)`는 각 매개변수 값 `CO`, `CL`을 대조하지만, `IN (%(statuses)s)`에 `"CO,CL"` 하나를 전달하는 것은 두 상태 목록이 아니다. ARC 차감은 CASE 계산 규칙이며 ARC 행을 제외하는 필터로 대체하지 않는다. 검증을 통과하지 못한 계획은 승인 대상으로 저장하지 않는다.

계획 검증 실패 시 원본·파생 초안의 `rejected_plan_diagnostic`을 원장에 비공개로 보존할 수 있다. 해시·바이트 수를 포함한 전체 진단이 95KiB 이하일 때만 초안을 함께 저장하고, 초과하면 해시·바이트 수만 저장한다. 이 진단은 공개 Run 응답·이벤트에서 제외하며 정상 승인 plan/digest로 사용하지 않는다.

result는 기존 `{status, columns:[{name,type}], rows:[[scalar]], row_count, truncated, ...}`를 보존한다. 소비자는 간단한 `columns:[string]` 입력도 지원하며 가시화 전달 시 열 이름으로 정규화할 수 있다. 오류를 빈 결과로 바꾸지 않는다. `validation` 항목은 `{code,status,message,details?}`이며 status는 `pass`, `mismatch`, `unverified`, `not_applicable`, `error`다. 일반 질문에는 독립 정답 대조 `unverified`를 명시한다.

insights는 `{observations:[string], limitations:[string], follow_up_questions:[string], provenance:string}`. 숫자/단위/근거 검증에 실패하면 모델 설명을 검증된 시사점으로 표시하지 않는다.

단위 미검증 차트에서는 단위별 최소·최대 통계와 해당 관측 설명을 근거에 넣지 않는다. 원본 행 수와 미검증 한계 등 확인 가능한 정보만 제공하며, 단위가 미검증인 결과를 전체 검증 통과로 취급하지 않는다.

artifact는 `{artifact_id, result_id, kind:"png", title, width, height, sha256, chart_spec, manifest}`. Python 내부 절대 경로는 웹 응답에 포함하지 않는다.

## Laravel API

같은 출처 세션+CSRF를 사용한다. 웹 SQLite에는 conversation, immutable ordered turns 및 최신 Python 스냅샷/이벤트를 저장한다.

- `GET/POST /api/conversations`, `GET /api/conversations/{id}`
- `POST /api/conversations/{id}/turns`: question, client_request_id, mode(agent 기본), source_result_id?, action?, chart_spec? → 202 저장된 turn.
- Laravel에서 `source_result_id`를 생략하면 해당 대화의 직전 저장 결과를 사용하고, 명시적 `null`은 새 분석이다. Vue는 직전 결과 참조를 표시하며 사용자가 해제할 수 있다. Python API에는 확정된 ID 또는 null을 명시적으로 보낸다. 오래된 결과 선택 시 그 결과의 조건을 계승한다.
- `GET /api/turns/{id}?after_event_id=...`: 저장된 turn ID와 위 Run 필드를 반환한다. 로컬 캐시를 보존하며 오류로 결과를 지우지 않는다.
- `POST /api/turns/{id}/answers|approve|cancel|retry-postprocess`: 위 Python body를 전달한다.
- `GET /api/artifacts/{id}`: Laravel의 저장된 대화/턴 소유권을 먼저 확인하고 Python으로 프록시. `?download=1` 지원.
- `GET /api/status`: 기존 Python health를 표시한다.

브라우저는 활성 run만 1초 간격으로 조회하고 이벤트를 ID로 병합한다. 재설명/재시각화도 새 턴이다. 대화 목록·대화·입력창을 표시한다. 0행, 잘림, 검증 미완료, partial, 재시작 interrupted를 구분한다.

## 독립 가시화 패키지 계약

패키지 디렉터리 `analysis-chatbot/visualization`, import 패키지 `analysis_visualization`.
실행: `<별도 venv python> -m analysis_visualization --input <서버 임시 JSON> --output-dir <서버 작업 디렉터리>`.
입출력 경로는 호스트가 생성한다. 차트 명세에 경로/코드/URL을 넣지 않는다. stdout은 단일 JSON, 진단은 stderr다.

입력:
```json
{"result_id":"uuid","result":{"columns":["month","currency","amount"],"rows":[["2003-01","USD","12.5"]],"row_count":1,"truncated":false},"chart_spec":{"type":"bar","x":"month","y":"amount","title":"월별 금액","x_label":"월","y_label":"문서 금액","currency_column":"currency"}}
```

출력: `{ "status":"succeeded", "artifacts":[{"filename":"chart-001.png","title":"...","width":1200,"height":720,"sha256":"...","chart_spec":{},"manifest":{"currency":"USD","series":[],"font":"Malgun Gothic"}}] }`.
빈 결과는 `{status:"no_data",artifacts:[]}`. 입력 오류는 비정상 exit와 `{status:"failed",error:{code,message}}`.
한 이미지에는 한 통화만 담으며 막대/선 차트만 지원한다. Decimal 검증 후 유한 값만 렌더링한다. 제한500행/1200×720, Agg/Figure API, 맑은 고딕. manifest에 정확한 원본 label/value/단위와 렌더링 값/폰트 정보를 담아 검증 가능하게 한다. 원본 결과 잘림은 거부한다.

`chart_spec.value_unit`은 선택적인 1~40자 단위 문자열이다. 독립 렌더러는 전달받은 명세를 표시하며 SQL 의미 검증은 호출 호스트 책임이다. `currency_column`은 이미지 분할 기준이며 값의 단위와 별개다. `value_unit`을 생략하면 통화가 있을 때 통화 코드를 값의 단위로 사용한다. 예를 들어 청구서 수를 통화별로 나눌 때 `y:"invoice_count", y_label:"건수", value_unit:"건", currency_column:"currency"`를 사용하면 USD·KRW 이미지를 분리하고 각 축·범례의 단위는 `건`으로 표시한다. manifest의 `currency`는 분할 통화, `unit`과 각 `series[].unit`은 실제 값의 단위다. 독립 렌더러에서 통화와 명시적 단위가 모두 없으면 `y_label`(생략 시 y 열 이름)을 단위 표기로 보존하지만, 분석 호스트는 위 단위 검증·미검증 정규화를 먼저 적용한다.

`chart_spec.label_columns`는 호스트가 SQL GROUP BY 출력 계보로 증명한 1~12개 열 이름이다. 중복·없는 열을 허용하지 않으며 x를 포함하고 y와 별도 통화 분할 열을 제외한다. 통화 하나만으로 집계해 `x=currency_column`인 경우 해당 통화 열을 유일한 라벨로 허용한다. 생략하면 `[x]`를 사용한다. 여러 열이면 열 이름·원래 값을 담은 JSON 객체 문자열로 복합 라벨을 만들며 `manifest.label_columns`, `series[].label_columns`, `series[].label_values`를 함께 기록한다. 호스트는 이 값과 label 문자열을 모두 원본 행에 대조한다. 같은 통화 내 중복 라벨은 거부하며 원본 행을 자동 합산하지 않는다. 차원 근거가 불명확하면 `chart_dimensions=unverified`로 남긴다.

복합 라벨 막대그래프는 가로 방향으로 모든 라벨을 표시한다. `manifest.layout`은 `{orientation:"horizontal",label_wrap_width:120,label_font_size:8|9,horizontal_axis_label:"값 표기와 단위",vertical_axis_label:"구분"}`이며 각 `series[].display_label`은 원본 전체 JSON `label`에 120자마다 줄바꿈을 삽입한 문자열이다. 원본·표시 라벨과 실제 두 축 표기를 호스트가 대조한다. 고정1200×720 안에서 8pt 이상 전체 라벨이 잘림·겹침 없이 들어가지 않으면 `label_layout_unreadable`로 실패하고 원본 표를 보존한다. 선그래프 방향은 변경하지 않는다.

분석 계획의 차트가 생략/null인 경우에만 호스트가 SQL 출력순 첫 직접 SUM/COUNT와 완전한 GROUP BY 출력 계보로 기본 막대 명세를 만들 수 있다. `chart_validation`의 `chart_default`는 선택 규칙·선택 열·미표시 집계 열·정규화 명세와 단위 상태를 기록하고 승인 digest에 포함한다. 증명불가이면 명세를 추가하지 않고 `unverified`로 이유를 남긴다. 명시된 잘못된 명세는 기본값으로 덮지 않는다. 선택적 `currency_column:null`은 생략으로 정규화하지만 비어 있는 문자열·잘못된 타입·없는 열은 거부하며 금액은 계속 연결된 ISO 통화 증거를 요구한다.

계획 모델이 선택적 `value_unit:null`을 반환하면 호스트는 생략과 같은 의미로 정규화한 뒤 가시화에 전달한다. 가시화 패키지에는 실제 단위 문자열 또는 필드 생략을 전달하며, `null`을 표시 단위 문자열로 사용하지 않는다.

## 승인 전 초안 검증과 최대 1회 보완

v13 로컬 호스트는 최초 초안의 `JOIN_NOT_VERIFIED`, `SQL_COLUMN_INVALID`, `CONDITION_BINDINGS_INVALID`, `CONDITION_NOT_APPLIED`, `PARAMS_INVALID`, `UNAPPROVED_SCOPE_FILTER` 거부에 한해 같은 문서·확정 조건으로 최대 1회 새 계획을 요청할 수 있다. 기존 계획 최대6호출·누적180초 안에서 수행하며 시간·호출 예산을 늘리지 않는다. 읽기 전용 SQL 정책과 문서/스키마 무결성은 보완 전에 다시 확인한다. 모델 출력 잘림·JSON 오류·추가 문서 요구·무결성 오류·승인 후 SQL 오류를 이 경로로 재시도하지 않는다. 추가 모델 호출은 실제 사용량을 발생시킬 수 있다.

후속 로컬 범위 가드는 원래 확정한 baseline에 없는 date/timestamp 범위와 isactive 조건만 승인 전에 UNAPPROVED_SCOPE_FILTER로 거부한다. 모든 WHERE 의미를 증명하는 기능은 아니다. 모델 SQL에서 새 조건을 읽어 사용자 승인 조건으로 승격하지 않으며, 실제 모델이 이 오류를 보완해 성공하는지는 추가 유료 재시험 없이 미검증으로 남긴다.

공개 `Run.plan_attempts`와 최종 봉인 `plan.plan_attempts`는 다음 요약 배열이다. 최종 계획이 없어도 공개 Run과 이벤트의 거부 기록을 보존한다.

```json
[
  {"attempt":1,"status":"rejected","repair":false,"error_code":"JOIN_NOT_VERIFIED","draft_sha256":"64자리 해시","diagnostic_sha256":"64자리 해시"},
  {"attempt":2,"status":"validated","repair":true,"draft_sha256":"64자리 해시"}
]
```

`attempt`는1 또는2, `status`는 `rejected`·`validated`·`model_failed`, `repair`는 두 번째 시도에서만true다. 두 해시와 `error_code`는 해당 증거가 있을 때만 들어간다. 공개 배열에는 SQL·params·원시 모델 응답·비공개 진단을 넣지 않는다. `planning` 이벤트의 `data.plan_attempt`는 같은 요약이고, 보완 시작은 `data.plan_repair={from_attempt:1,next_attempt:2,error_code,limit:1,execute_sql:false}`다. 입력 크기 때문에 시작하지 않으면 `plan_repair_skipped={reason:"feedback_limit",execute_sql:false}`를 남긴다. 이 단계에서 SQL을 실행하지 않으며, 검증된 최종 계획만 새 digest로 승인한다. 첫 비공개 거부 진단은 바꾸지 않고 추가 진단과 합산95KiB를 넘으면 해시·바이트 수로 제한한다.

Laravel은 공개 배열을 저장·복원하고 승인 계획 또는 최종 계획이 없는 실패 화면에 첫 거부와 보완 결과를 함께 표시한다. 평가기의 `planning.outcome=first_attempt_validated`와 `repaired_validated`는 별도 결과다. `initial_plan_rejected`·`repair_count`·`final_plan_validated_after_repair`를 보존하며, `completed_after_repair`는 run 성공, `automated_pass_after_repair`는 수치·가시화 등 자동 전체 기준까지 통과한 경우다. 과거 기록에 시도 증거가 없으면 미검증으로 남기며 첫 초안 통과로 추정하지 않는다.

v13 AWS runtime의 `plan`·`document_plan` 출력 상한은4096토큰이고 다른 단계는2048이다. 이는 실제 출력량이나 청구 토큰 수가 아니다. `stopReason=max_tokens`는 JSON 파싱 전에 `MODEL_OUTPUT_TRUNCATED`로 명시 거부한다. 정상 종료했지만 잘못된 JSON은 기존 파싱 오류로 구분한다. 이 잘림에 자동 모델 재호출을 추가하지 않는다.

## 실행 제한과 복구

기존 AWS 동시 호출 semaphore 1, SQS 수신기 1, 승인 요청 TTL60초를 공유한다. 계획 최대6호출/누적180초(답변 대기 제외), 문서12후보/32상세/2홉/128KiB. 문서 계획 단일 호스트 호출과 해당 Bedrock 읽기 제한은 90초이며 누적180초를 늘리지 않는다. 다른 분석 모델 단계의 Bedrock 읽기 제한은 45초다. 후처리90초, 가시화15초, 시사점60초. 재시작 시 불확정 실행은 interrupted로 보존하고 SQL을 재시도하지 않는다. AWS 배포는 별도 승인 전까지 수행하지 않는다.
