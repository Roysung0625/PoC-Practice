# 구현·검증 기록 — 2026-11-03~04

**현재 AWS runtime v13·DEFAULT13 `READY`, stack `UPDATE_COMPLETE`입니다. v13 실제10문항은 독립 수치9/10, 수동 전체 기준4/10 통과로 종료됐습니다.** run 성공5·partial4·조회 전 실패1이며, 최초 초안9개 통과/1개 거부와 실제1회 보완 실패를 구분합니다. 원본79개·독립golden 전후 동일·시작 소스36개를 보존했습니다. 이후 로컬 보완은 Python661개 통과, 저장된 ERP03~06의 실제 화면 재시각화4건·PNG7개와 API 단독 재시작 복원으로 확인했습니다. 이 사후 확인을 실제 AWS 전체 통과에 합산하지 않습니다.

후속 승인 범위는 **AI 왕복 검증, 웹 서버는 로컬 유지**입니다. 만료된 AWS 배포 계정 로그인을 갱신하고 기존 상태·예산 제어를 확인한 뒤 Agent runtime CloudFormation 갱신을 수행했습니다. v7~v10 실패와 현재 v11의 실제 단건 성공을 아래에 구분해 보존합니다. 사용자가 승인한 `poc-local-login` 비밀번호 재설정·직접 새 비밀번호 설정 후 IAM 로그인을 완료했고, STS로 앱 `poc-chatbot`·수신기 `poc-worker` 역할을 확인했습니다. 사용이 끝난 임시 비밀번호 안내 파일은 삭제했습니다. 로컬 웹 `127.0.0.1:8010`, API `127.0.0.1:8001`, PostgreSQL 연결과 수신기 한 개를 유지합니다.

## 첫 실제 평가: 실패 기록 보존

`.local/analysis-chatbot/evaluation/live-20261103-001/`에 첫 10문항 결과를 보존했습니다. 새 런타임의 해석 응답을 실제로 받았으나 ERP01/03~09의 8문항이 `CONDITIONS_INVALID`로 승인 전에 실패했고, ERP02/10은 참조할 부모 결과가 없어 실패했습니다. SQL 수치 대조는 8개 미검증·2개 검사 실패, 자동 종합 판정은 10개 검사 실패입니다. 원장 SQL 작업 수는 34건으로 유지돼 이 실행에서 SQL을 새로 실행하지 않았습니다.

실패 응답을 덮어쓰지 않고 별도 `diagnostics-20261103-001/interpret-response.json`에 SQL 없는 해석 진단 1회 결과를 남겼습니다. 모델이 `document_type`, `group_by`, `metrics`를 배열로 반환했고, 명시한 전체 기간도 재확인했습니다. 앱의 flat 조건 계약 및 최종 SQL 조건 binding 형식과의 차이를 확인했습니다. 실제 DeepSeek V3.2 호출 9회(평가 8회·별도 진단 1회), 입력 1,670·출력 1,761토큰을 CloudWatch `model_usage`에서 확인했습니다. 이 사용량은 청구 금액 추정치가 아닙니다. 수정 후 실행은 새로운 출력 폴더로 구분합니다.

## v8~v10 실패 보존과 수정 경과

v8 실제 단건 평가의 원본 응답과 독립 SQL 전후 결과는 `.local/analysis-chatbot/evaluation/smoke-v8-20261103-001/`에 보존했습니다. 이 실행은 `MODEL_JSONDecodeError`로 실패했고 SQL은 새로 실행되지 않았습니다. 초기 10문항 실패와 v8 단건 실패를 후속 성공 기록으로 덮어쓰지 않습니다.

v9에서는 공통 엄격 JSON 파서와 비민감 진단을 추가했습니다. 이는 응답 처리·진단을 보완한 것이며, v8 오류의 원인이 확정됐다는 뜻은 아닙니다. 실제 배포 Agent ZIP SHA-256은 `af6f4d779ad1269b9c81c72c9ff098365cda9fd369e221cb457fc994ec36d200`, `aws/runtime/main.py` 소스 SHA-256은 `cc8de09e09b93b25589501e2bf0d368e5d16b9987b24686e0ba27dbf203f7f01`입니다. stack/runtime/DEFAULT 확인 자료는 `.local/aws-deploy/analysis-20261103-v9/`에 보존했습니다.

v9 실제 브라우저는 해석·문서 탐색 이후 `CONDITION_NOT_APPLIED`로 실패했습니다. `.local/analysis-chatbot/evaluation/browser-v9-20261103-001/`에 실패를 보존했습니다. 별도 `diagnostics-v9-20261103-001/`에는 이름 있는 scalar 매개변수의 EQ/IN 검증과 ARC 대변전표 제외 문제를 확인한 자료를 보존했습니다. ARC는 제외할 문서가 아니라 금액에서 차감할 문서라는 계약을 유지합니다.

v10 실제 브라우저의 실패는 `browser-v10-20261103-001/`에 보존했습니다. 조건 근거가 객체 대신 배열로 나오고, IN 목록을 단일 SQL placeholder의 CSV 문자열로 전달한 문제가 있었습니다. 이름 있는 scalar EQ/IN을 호스트가 검증하도록 보완하고, 잘못된 조건 근거 형식은 `CONDITION_BINDINGS_INVALID`로 구분합니다. 거부된 원본·파생 초안은 승인 가능한 계획이나 공개 이벤트가 아닌 비공개 진단으로 저장하며 전체 진단 95KiB를 넘으면 해시·바이트 수만 보존합니다. 선택적 차트 `value_unit:null`은 후처리 전에 생략으로 정규화합니다. 이 과정에서 이전 실패 증거를 삭제하거나 성공으로 전환하지 않았습니다.

## v11 실제 브라우저 단건 성공

| 항목 | 확인 결과 |
| --- | --- |
| 배포 | stack `UPDATE_COMPLETE`, runtime v11 `READY`, DEFAULT `liveVersion=11 / READY` |
| 승인·SQL 왕복 | 브라우저 승인 후 기존 Agent→Lambda→SQS→Windows→PostgreSQL→도구 응답 경로 성공 |
| 실제 원장 | 요청 `1ec1b4f9-11a3-4eea-b2d2-7227b2673f24`, `sql_status=succeeded`, `agent_status=data_returned` |
| 결과 수치 | 3행, 잘림 없음. 별도 ERP01 독립 SQL 사후 대조 `pass` |
| PNG | 실제 웹 다운로드 2개, HTTP 200·image/png·1200×720·기대/실제 SHA-256 일치 |
| 시사점 | `aws_agent_host_checked`, 관측 설명 3개, 단계 `pass` |
| 사람 검토 | 헤더 단위 집계·ARC 차감·통화 분리·금액 해석 한계 확인 |

증거는 `.local/analysis-chatbot/evaluation/browser-v11-20261103-001/report.json`, 화면은 `.local/analysis-chatbot/verification/aws-browser-v11.png`입니다. 보고서의 `before_golden`은 사전 별도 캡처 없음으로 명시돼 있습니다. 따라서 이 단건의 사후 수치 대조를 전후 정답 SQL을 모두 보존한 전체 평가로 설명하지 않습니다.

배포 Agent ZIP SHA-256은 `2e8e354cf31ce30d23718c32bc7a0588c086d9aeb356bdf7e36b3b508f41aa26`, `aws/runtime/main.py` 소스 SHA-256은 `21a383c60bce88a337fe28eefdce7959979c800513c8e0802ddb4a711a4211dc`입니다. `.local/aws-deploy/analysis-20261103-v11/`에 배포 응답을 보존했습니다.

## v11 전체 평가 완료와 v12 후속 검증

`.local/analysis-chatbot/evaluation/live-v11-20261103-002/semantic-review.json`의 `evaluation_finished=true`, `golden_before_after_equal=true`를 확인했습니다. 저장된 SELECT 식으로 의미 매핑을 결정한 후 독립 정답과 대조한 결과 ERP01·ERP08의 수치는 통과했고 나머지 8개는 조회 전 실패로 수치 미검증입니다. ERP01은 금액을 `건`으로 표시하고 시사점에도 잘못된 단위가 전파됐으며, ERP08은 차트에서 `issold` N/Y 그룹 식별을 누락했습니다. 따라서 수치 2/10 통과와 별개로 수동 검토는 2개 실패·8개 미검증입니다. 원본 보고서·턴·SQL·전후 정답·실패 증거를 보존하며 앞의 단건 성공으로 이 실패를 대체하지 않습니다.

v12는 Agent ZIP SHA-256 `4a28ae2c554ef8e5349b6aa0f61a017ad954e3bb483f35d658ff17381f7a7273`, runtime 소스 SHA-256 `77d7a5ed6c7a3029f0fd8f0ad8172b96d79c6bcdf6de34cef19c8657441087a5`로 배포했습니다. `.local/aws-deploy/analysis-20261103-v12/`에 stack `UPDATE_COMPLETE`, runtime 12 `READY`, DEFAULT `liveVersion=12 / READY` 확인 자료를 보존합니다. 최초 전체 평가 `.local/analysis-chatbot/evaluation/live-v12-20261103-003/`는 종료됐습니다. 별도 `semantic-review.json`에서 golden 전후 동일과 원본67개 SHA256 불변을 확인했습니다. SQL SELECT 식으로 먼저 매핑한 수치는 ERP01·02·07·08·10의 5개가 일치했고 나머지5개는 조회 전 실패입니다. ERP02·10은 기간만 변경하고 원래 조건을 계승했지만 시사점 검증 실패, ERP07은 차트 명세 누락과 시사점 실패, ERP08은 차트 렌더링 실패입니다. ERP10의 0행은 정상 결과이며 후처리 실패와 구분합니다. 원본 자동 보고서의 수치 미검증10개는 수정하지 않았고 의미 검토를 별도 추가했습니다. 전체 기준은 ERP01만 통과했습니다.

## v12b 로컬 후속 수정과 전체 평가 종료

AWS 추가 배포 없이 runtime/DEFAULT12 `READY`를 다시 읽어 확인했습니다. Python558개·가시화61개·Vue8개와 웹 빌드 통과 후 소유 API만 재시작했고 웹PID26292·단일수신기PID27764는 유지했습니다. 앱 `poc-chatbot`·수신기 `poc-worker` 일반 IAM 역할도 STS로 확인했습니다. `.local/analysis-chatbot/verification/preflight-v12b-20261103-001-implementation.json`에 비밀설정·DB·토큰을 제외한 host/UI/lock/가시화/평가기32개 SHA256, 서비스 health·PID·runtime12와 SQL작업42건 기준을 기록했습니다.

`.local/analysis-chatbot/evaluation/live-v12b-20261103-001/`의 전체10문항은 각1회로 종료됐습니다. run성공은ERP07·08의2개, 조회전실패는8개(JOIN_NOT_VERIFIED4·부모부재2·MODEL_ValueError1·SQL_REJECTED1)입니다. 독립golden전후는같았으며 별도 의미매핑 수치2/10통과, 전체기준은ERP08만1/10통과입니다. ERP07은수량UOM미검증과요청에없던isactive필터4개를수동검토사항으로남겼습니다. 원본87개와동결소스32개SHA를보존했고 SQL작업은42→44건입니다. 별도작업의기준데이터변경가능성과실제변경확인을구분했으며 이실행에서는golden전후차이가없었습니다.

ERP05는기존CloudWatch의해당시간창document_plan메타데이터에서max_tokens/output2048/text5969/fencedtrue를확인했습니다. JSON파싱전종료계약거부에따른ValueError와일치하며SDK/네트워크예외나JSON문법오류로합치지않았습니다. request_id가null인시간창귀속한계와본문미수집을명시한증거는 `.local/analysis-chatbot/verification/ERP05-v12b-existing-cloudwatch-classification.json`입니다.

별도 `browser-reuse-v12b-20261103-001`에서는브라우저의선그래프재시각화와AI재설명을각1회수행했습니다. 새결과ID·새PNG·원본표동일·실PNG다운로드2회(HTTP200/image/png/1200×720/해시일치)와새로고침복원을확인했고 SQL작업44건을유지했습니다. 새API미동결시점이어서프로세스재시작복원은이기록에서미검증으로구분했습니다. 재설명추천질문일부가issold판매가능여부를판매실적처럼표현한의미한계도남겼습니다.

기본 sandbox의 최초 전체 Python 시험은 Windows TestClient/socketpair 제약으로 멈췄고 본인 pytest 프로세스2개만 확인·종료했습니다. 승인된 unsandbox 고유 basetemp에서558개가 통과했습니다. Vue 최초 실행도 sandbox TEMP rename EPERM으로0개 준비실패했으며 프로젝트 내부 TEMP에서8개가 통과했습니다. 이 경과를 숨기지 않습니다. 자기조인의 서로 다른 i/j 날짜별칭으로 기간상한/하한이 나뉘는 우회는 독립검토로 발견한 뒤 수정됐고, 같은별칭 통과·다른별칭 거부를 재검증했습니다.

문서 투영은 원본 전체 읽기·source hash를 유지하며 중복 FK HTML 주석, 실제 FK 표와 일치하는 중복 Mermaid, 링크 주소만 제거합니다. 모든 열·부모/자식 FK·조회 주의는 유지하고 `projection_version`과 실제 전달 `context_sha256`·바이트 수를 다시 구성해 검증합니다. 투영 없는 과거 승인 계획은 원문 방식으로 검증합니다. 128KiB·후보 12개·상세 32개·2홉 한도는 늘리지 않았습니다. 문서 계획 호출은 90초, 계획 누적은 180초를 유지합니다.

단위·차원은 모델 라벨이 아닌 SQL AST와 실제 물리 열 계보로 검증합니다. 금액의 통화 연결·COUNT의 건 단위를 확인하고 제목·축은 호스트의 중립 표기로 정규화합니다. 증명된 복합 그룹 열은 `label_columns`로 표시하며 manifest의 열·값·복합 라벨을 원본과 대조합니다. 실제 UOM이나 복잡한 단위가 미확정이면 미검증 표시와 함께 단위별 최소·최대 통계 설명을 제외합니다. 승인 전 정규화한 차트를 digest에 고정하며, 저장 결과 재사용 시 차트가 바뀌면 새 턴·PNG를 만들고 SQL·원본 결과는 바꾸거나 재실행하지 않습니다. 평가기 역시 `chart_unit`·`chart_dimensions` 누락/미검증을 통과로 계산하지 않습니다.

## v13 배포와 최종 전체 평가 종료

Agent전용ZIP `9d89ee85f30546a7b94ba0e33485df10cfaf5e13dba958dbd982c7dd710e02bf`와runtime소스 `eacd4dbb97d8bb65f38f69e26cff795976396f57ca4c8b56899d1c87f8e371e4`를검증해배포했습니다. AgentRole의단일S3패키지키와AgentRuntimeArtifact만바뀌고 BeforeContext의키치환외AfterContext동일·리소스교체없음·기존템플릿/다른params보존을확인했습니다. 2026-11-03 23:46JST에stack UPDATE_COMPLETE/runtime13 READY/DEFAULT13 READY 및LambdaKey6270ab...·실제LambdaCodeSha256불변을확인했습니다. 증거는 `.local/aws-deploy/analysis-20261103-v13/`입니다.

v13은plan/document_plan출력상한만4096으로늘리고다른단계2048·계획6호출/180초·도구TTL60초를유지합니다. 4096은항상실제출력하거나과금되는토큰수가아닙니다. max_tokens는MODEL_OUTPUT_TRUNCATED로명시거부하며자동재호출하지않습니다. 실제 full 시작 당시 로컬호스트의승인전5종검증거부에만최대1회초안을보완하고 첫진단·공개plan_attempts·최종digest를보존합니다. 자세한계약은 [공통계약](API_CONTRACT.md)을따릅니다.

최종614개Python·Vue10개·Laravel10개/71assertions·웹빌드통과후소유API만26584로재시작했고 웹26292·수신기27764를유지했습니다. 실제역할/health/SQL작업44건기준과비밀제외36개소스ZIP은 `.local/analysis-chatbot/verification/preflight-v13-20261103-001-implementation.json` 및새평가폴더의 `implementation-before.json`·`source-snapshot.zip`에기록했습니다. 새 `live-v13-20261103-001` full10은 2026-11-04에 종료됐습니다. 별도 `semantic-review.json`은 독립 수치9개 통과·1개 미검증, 자동 종합4개 통과·5개 실패·1개 미검증, 수동4개 통과·5개 실패·1개 미검증입니다. ERP02·10은 원본 ERP01의 나머지 조건/params를 유지하고 기간 술어만 추가해 새 승인 후 조회했습니다. 원본 raw 보고서는 별칭 매핑 전 수치10개 미검증이며 사후 매핑으로 덮어쓰지 않았습니다. SQL 작업44→53건, 독립golden 전후 동일과 원본79개/시작 소스36개 불변을 확인했습니다.

첫 초안은9개 validated이고 ERP09만 JOIN_NOT_VERIFIED로 거부됐습니다. 실제1회 보완을 시도했으나 AWS_CALL_FAILED로 실패했으므로 보완 후 최종 계획/실제run 성공은0입니다. 해당 시간창의 기존 CloudWatch에 완료응답/오류 메타데이터가 없고 로컬이 원 서비스 오류코드를 축약해 보존하지 않아 세부 원인은 미확정입니다. 완료 model_usage48회, Bedrock 입력614,338·출력20,695토큰은 Codex 대화/워커 토큰과 별개이며 실패 보완의 미확인 사용량을 포함했다고 주장하지 않습니다. 추가 유료 모델 호출은 수행하지 않습니다.

## v13 질문별 원본 판정과 사후 검증 경계

수치는 고정된 독립 SQL과 사후에 명시한 의미 기반 열 매핑으로 대조했습니다. 질문 원문과 정답 식은 [고정 평가 사례](../evaluation/idempiere_cases.json), 상세 근거는 로컬 `live-v13-20261103-001/semantic-review.json`에 있습니다. 숫자 일치와 원래 요청 범위·단위·PNG의 정확도는 따로 판단합니다.

| 사례·질문 요약 | 실제 조회 | 독립 수치 | 원본 전체 수동 판정 | 원인·사후 확인 수준 |
| --- | --- | --- | --- | --- |
| ERP01 월·통화별 확정 판매 청구액/건수 | 3행 | 통과 | 통과 | ARC 차감·헤더1회·통화 분리, 실제 PNG/설명 확인 |
| ERP02 나머지 조건 유지·2003년 변경 | 1행 | 통과 | 통과 | ERP01 참조·기간만 변경·새 승인 확인 |
| ERP03 거래처·통화별 grandtotal/건수 | 3행 | 통과 | 실패 | unquoted 거래처_ID→거래처_id와 차트 별칭 불일치, PNG unknown_column. 사후 저장 결과로2PNG·화면/복원 확인 |
| ERP04 판매/구매·상태·통화별 주문 | 4행 | 통과 | 실패 | 당시 chart_dimensions 미검증·중복 라벨 ambiguous_labels. 사후 증명된 복합 차원·통화 분리로2PNG·화면/복원 확인 |
| ERP05 상품·UOM·통화별 수량/행 금액 | 4행 | 통과 | 실패 | quantity 단위 미검증·renderer currency_required. 사후2PNG·화면/복원 확인하되 실제UOM 미검증 유지 |
| ERP06 모든 수금/지급 상태·통화별 합계 | 1행 | 통과 | 실패 | PNG currency_required 및 미요청 날짜1000~9999 필터. 사후1PNG·화면/복원, 원본 계획은 새 범위 가드가 거부 |
| ERP07 저장 재고의 창고·상품·UOM별 합계 | 20행 | 통과 | 실패 | 미요청 isactive 필터4개·실제UOM 미검증. PNG가 있어도 전체 의미 통과 아님 |
| ERP08 활성 상품 유형·판매 가능 여부 | 7행 | 통과 | 통과 | 원본 코드 두 차원·COUNT/건·실제 PNG/설명 확인 |
| ERP09 상품이 있는 청구서 중복 없는 합계 | 조회 없음 | 미검증 | 미검증 | 첫 JOIN 검증 거부→1회 보완 AWS_CALL_FAILED. 세부 서비스 원인 미확정 |
| ERP10 나머지 조건 유지·2099년 변경 | 정상0행 | 통과 | 통과 | ERP01 참조·기간만 변경·새 승인, 실패와 구분·PNG 생략 |

ERP06/07의 추가 필터는 현재 데이터에서 수치가 같았더라도 요청 범위 정확도의 실패입니다. 후속 로컬 보완은 새 계획에서 이를 차단하는 기능이며 원본 SQL을 고쳐 재실행하지 않습니다. 차트4건의 사후 복구도 원본 full의4/10 전체 통과를 바꾸지 않습니다.

## 최종 로컬 개선 효과와 남은 한계

| 문제 | 실제 수정 동작 | 확인된 효과 | 남은 한계 |
| --- | --- | --- | --- |
| ERP03 출력 별칭이 실제 PostgreSQL 결과와 다름 | quoted 원형을 보존하고 unquoted ASCII 접힘을 유일하게 대응 | 저장 거래처 결과2PNG 복구 | 충돌·모호한 별칭은 거부하며 무조건 소문자 대체하지 않음 |
| ERP04 통화가 x축이 되어 상태 그룹이 누락됨 | SQL GROUP BY로 증명된 비통화 차원을 복합 라벨로 구성 | 주문 상태·판매/구매를 구분한2PNG 복구 | 증명하지 못한 그룹은 미검증 유지 |
| ERP05/06 통화 분리와 값 단위를 혼동해 렌더링 거부 | 통화는 partition, 수량/COUNT 단위는 별도 계보로 검증 | 상품2PNG·수금1PNG 복구, COUNT는 ‘건’ 유지 | ERP05 sign_factor 수량 계보 미지원으로 UOM 미검증·단위별 수치 통찰 제외 |
| ERP06/07에 사용자가 요청하지 않은 기간·활성 조건 추가 | immutable baseline과 실제 물리 열·발생 위치를 대조해 승인 전에 UNAPPROVED_SCOPE_FILTER 거부 | 원본2계획 모두 거부, 명시한 단일 기간 조건은 허용 | date/timestamp 범위·isactive에 한정한 가드이며 모든 WHERE 의미를 증명하지 않음. 실제 모델 보완 성공은 재시험하지 않음 |
| 첫 초안 실패가 후속 성공에 가려질 수 있음 | 첫 진단과 plan_attempts·최종 digest를 저장하고 화면/평가기에서 구분 | 실제 첫 초안9통과·1거부, 보완1실패·성공0을 분리 | ERP09 원 서비스 오류코드는 보존되지 않아 원인 미확정 |
| 계획 응답 잘림을 일반 파싱 오류로 표현 | plan/document_plan 상한4096, max_tokens는 MODEL_OUTPUT_TRUNCATED로 거부 | runtime 모의 회귀 및 실제 v13 전체 실행 기록 보존 | 4096은 실제 출력량·과금량 보장이 아니며 자동 재호출하지 않음 |

차트의 저장 원본 기반 독립 검사는 [오프라인 복구 보고서](../../.local/analysis-chatbot/evaluation/offline-v13-chart-contract-20261104-001/report.json), 범위 가드의 원본 거부·정상 조건 허용은 [독립 가드 검사](../../.local/analysis-chatbot/evaluation/final-local-v13b-20261104-001/independent-scope-review.json)에 보존합니다. 이후 실제 Laravel 화면에서 ERP03~06의 ‘다른 그래프로 보기’를 각1회 실행해 **4/4 완료·PNG7개**를 확인했습니다. HTTP200·image/png·1200×720·해시를 검사하고 사례별 대표4PNG를 직접 열어 라벨·단위·값을 확인했습니다. 원본 SQL/params/결과와 기존 실패 턴은 유지됩니다.

소유 Python API만27244→4572로 재시작한 뒤 저장 대화4개·표·결과 JSON과 웹 PNG7개 및 Python 직접 PNG7개의 같은 해시를 확인했고 브라우저 새로고침에서도 복원됐습니다. PHP 웹26292·단일 수신기27764는 유지했습니다. **추가 모델0·승인 SQL0, 기존 SQL 원장53→53**이며 OS/PostgreSQL/웹 프로세스 전체 재시작 검증으로 확대하지 않습니다. [최종 브라우저 보고서](../../.local/analysis-chatbot/evaluation/final-local-v13b-20261104-001/browser-rechart-report.json), [최종 화면](../../.local/analysis-chatbot/verification/final-v13-local-recovery-20261104.jpg)을 남기고 `http://127.0.0.1:8010/` 탭을 결과물로 유지했습니다. 최종 소스/시험/lock/build97개 지문과 ZIP은 같은 검증 폴더에 보존합니다.

## 자동 시험

| 시험 | 결과 | 범위 |
| --- | --- | --- |
| 최신 Python 전체 통합 — v13 사후 로컬 보완 | **661 통과**, 29.58초 | 문서·단위·차원·범위 가드·조건 증거·runtime·평가기. 소스97개 불변 |
| v13 실제 전체 평가 시작 전 Python 통합 | **614 통과**, 37.61초 | 실제 full10 시작 당시 소스의 전체 회귀. 이후661개와 합산하지 않음 |
| 이전 Python 전체 통합 — v11 | **281 통과**, 76.34초 | 조건 증거·JSON·원본 보존 등을 포함한 전체 회귀 |
| 전체 통합 이후 조건 근거 형식 회귀 | **8 통과**, 1.19초 | 신규 1개 포함. binding 배열의 명시적 오류 등 관련 범위 |
| 최신 독립 평가기 회귀 | **43 통과**, 0.39초 | 초안거부·1회보완·최종통과 구분. 전체 통합과 합산하지 않음 |
| 이전 독립 평가기 회귀 | **20 통과**, 0.32초 | 수치·수집·기준 처리 |
| 이전 Python 전체 통합 — JSON 계약 보완 후 | **256 통과**, 73.39초 | 기존·신규 Python, AWS runtime 모의, 독립 평가기. basetemp `test-temp-json-contract-001` |
| 초기 기존·신규 Python + AWS runtime 모의 + 독립 평가기 | **132 통과**, 15.78초 | 로컬 DB fixture, 기존 API, 신규 run·문서·승인·재사용·복구, native 도구, 정답 비교기 |
| 최신 독립 Matplotlib 패키지 | **61 통과**, 9.86초 | 복합 라벨·중복 라벨·통화 축·manifest 포함 |
| 이전 독립 Matplotlib 패키지 | **42 통과**, 3.06초 | 실제 PNG, 한글·음수, 통화 분리, 값 단위, manifest, 잘못된 입력 |
| Laravel | **10 통과 / 71 assertions** | 대화 저장, 중복·소유권, 캐시·복원, 실제 전송 JSON 구조, 참조 선택 |
| Vue | **10 통과** | 대화·계획·상태·후속 참조·승인 전 그래프 기본선택과 단위 미검증 노출 |
| Chrome + 실제 Laravel 화면 + 모의 API | **6 통과** | 승인·표·복원·재시각화·자연스러운 후속 질문·모바일 |
| TypeScript / Vite | **통과** | 최종 소스 빌드 |

초기 통합 실행에서는 총 **196개 자동 시험이 통과**했습니다. Python 전체 실행은 초기132개 → JSON 계약 보완 후256개 → v11 281개 → v12 392개 → v12b 로컬 수정558개 → v13 시작614개 → 최종 로컬 보완661개 순으로 확인했습니다. 281개 이후 조건 근거 8개·평가기 20개와 후속 평가기 37개도 별도 실행한 기록입니다. 서로 중복되는 실행을 합산하지 않습니다. 가시화는 이전42개·58개 이후 최신61개, Vue는 이전7개·8개 이후 최신10개, Laravel은이전9개/63assertions이후10개/71assertions를확인했습니다. 브라우저모의6개는이전결과를유지합니다. 브라우저 모의 API 시험과 실제 PostgreSQL·AWS 검증을 구분합니다. Windows 공용 `%TEMP%` 권한 문제로 초기 기존 시험 32개가 준비 단계에서 실패했고, 프로젝트 내부 `--basetemp`를 지정한 재실행에서 기존 90개가 통과했던 경과도 보존합니다.

라이브 평가 준비 중 결과 수집을 추가 보완했습니다. cleanup·통신 실패가 원본 턴을 덮어쓰지 않도록 별도 증거 파일을 저장하고, 수치 일치와 run·데이터·PNG·시사점·수집 상태를 나눠 판정합니다. 라이브 미검증은 종료 코드 1입니다. 기존 평가기 6개에 회귀 13개를 추가해 **19개 통과 / 0.24초**를 별도로 확인했습니다. 변경 범위는 평가기·평가기 시험·평가 안내 문서이며 AWS runtime 패키지는 바뀌지 않았습니다.

기존 로컬 샘플의 PNG 2개를 실제 `/api/artifacts/{id}`에서 수집해 HTTP 200, `image/png`, 1200×720 크기, 기대·실제 SHA256 일치를 확인했습니다. 증거는 `.local/analysis-chatbot/verification/artifact-download-local-001/`입니다. 이 추가 확인은 AWS·SQL을 실행하지 않았습니다.

```powershell
# 이전 JSON 계약 보완 후 전체 Python 통합: 256 passed / 73.39s
.\.venv\Scripts\python.exe -m pytest local/python/tests aws/tests analysis-chatbot/evaluation/test_evaluator.py -q --tb=short --basetemp=.local/analysis-chatbot/test-temp-json-contract-001

# 이전 검증 실행 기록
.\.venv\Scripts\python.exe -m pytest local/python/tests aws/tests analysis-chatbot/evaluation/test_evaluator.py -q --tb=short --basetemp=.local/analysis-chatbot/test-temp-final-002
.\analysis-chatbot\visualization\.venv\Scripts\python.exe -m pytest analysis-chatbot/visualization/tests -q --tb=short --basetemp=.local/analysis-chatbot/test-temp-viz-final-001

# analysis-chatbot 폴더에서; PHP/Node 실행환경 PATH는 scripts/Setup.ps1 참고
..\.local\runtime\php-8.5.12\php.exe vendor/phpunit/phpunit/phpunit
npm test
npm run build
$env:PLAYWRIGHT_CHANNEL='chrome'
npm run e2e
```

재실행 시 `--basetemp`에는 새 프로젝트 내부 시험 폴더를 사용합니다. 실제 설정·원장·DB가 들어 있는 경로를 지정하지 않습니다.

## 실제 로컬 통합

| 항목 | 상태 | 증거 |
| --- | --- | --- |
| PostgreSQL 연결 | 통과 | `poc_idempiere`, `poc_idempiere_reader`, `transaction_read_only=on`, 기존 청구서 8건 보존 |
| 실제 문서 기반 고정 계획 | 통과 | 실제 테이블 문서 해시/FK·열 확인 → 브라우저에서 승인 |
| SQL → 표 | 통과 | 2002-02 USD 142.5/2건, 2002-08 USD 152/1건, 2003-11 EUR 215.9/1건, 총 3행 |
| 독립 정답 SQL 대조 | 통과 | `ERP01`을 별도로 작성한 CTE 정답 SQL과 비교: 행·값·통화·정렬 일치 |
| 실제 PNG | 통과 | EUR/USD 분리 1200×720 이미지, 한글 제목·축·범례 표시 |
| 재시각화·재설명 | 통과 | 금액 막대 → `invoice_count` 선 그래프 → 건수 설명, `건` 단위 유지 |
| SQL 재실행 방지 | 통과 | 위 재시각화·재설명 전후 기존 원장 SQL 작업 **34 → 34** |
| 대화·표·이미지 복원 | 통과 | 브라우저 새로고침과 웹/API 전체 재시작 후 5개 턴·기존 결과·PNG 복원 |
| 새 파생 결과 | 통과 | 재사용 턴마다 별도 result ID, 원본 데이터·승인 SQL 유지, 차트 문맥 보존 |
| 운영 | 통과 | Setup/Start/Stop/Check, 재사용·소유 프로세스만 중지, 잘못된 상위 DB/API 환경변수 격리·복원 |

첫 브라우저 요청에서는 PHP가 빈 조건 객체를 `[]`로 바꿔 Python에서 422 거부한 문제를 발견했습니다. 실제 전송 객체를 수정하고 회귀 시험을 추가했습니다. 실패 기록은 삭제하지 않았으며, 진단 중 생성한 미승인 작업은 취소했습니다. 이후 실행한 4개 턴이 성공했습니다.

로컬 증거 파일:

- `.local/analysis-chatbot/browser-flow-verification.json`: SQL 작업 수·파생 ID·최종 설명.
- `.local/analysis-chatbot/evaluation/sample-001/`: 독립 SQL 전후 결과와 실제 웹 결과 대조. `ERP01` 통과, 나머지 9개 **미검증**.
- `.local/analysis-chatbot/artifacts/`: 실제 차트와 manifest. 화면에서 이미지 ID로 표시·다운로드합니다.
- `.local/analysis-chatbot/logs/`: 프로세스 로그. 실제 환경·데이터 산출물은 Git에서 제외합니다.

## 정확도·경계 시험에서 수정한 내용

독립 astra-high 검토에서 이전 조인 FK를 재사용한 무관 테이블 연결, self join 별칭 오류, 실제 행을 제한하지 않는 tenant 매개변수 등 5개 문제가 재현됐습니다. 초기 회귀는 5 실패·6 통과였고 수정 후 통과했습니다. 이후 정상 CTE까지 거부한 문제도 positive 회귀로 확인·수정했습니다. 완전한 복합 FK, OR 조건, 잘못된 열·변경된 문서·변경된 승인·기존 v1 승인 API를 통한 v2 우회도 검사합니다.

대변전표 부호, 통화 분리, 빈 결과, 상세 조인 중복, 잘림, 다른 대화 결과 혼입, 한 대화의 동시 작업, 중복 요청, 취소, 재시작, PNG/시사점 실패 후 원본 보존은 로컬 fixture·모의 시험으로 확인했습니다. 설명의 수치는 호스트 계산 근거 문장과 대조하며, 모델이 임의의 인과 설명을 정답처럼 표시하지 못하게 제한합니다.

정답 SQL `ERP05`는 별도 검토에서 행 선택 단위와 수량 종류의 불일치를 찾아 `c_uom_id`에 맞는 `qtyentered`로 수정했습니다. 확인 질문이 다음 평가를 가로막지 않도록 원본 응답을 보존하고 해당 미완료 run을 취소한 뒤 진행하는 시험도 추가했습니다.

## 미검증·범위 제한

| 항목 | 상태 | 다음 확인 |
| --- | --- | --- |
| 신규 runtime 실제 배포 | 통과 | stack `UPDATE_COMPLETE`, runtime v13·DEFAULT 엔드포인트 `READY`, 실제 `liveVersion=13` 확인 |
| 자연어 → AWS 왕복 → PNG → 시사점 | 실제 단건 통과 | v11 브라우저 SQL 왕복·PNG 2개·AWS 시사점, ERP01 별도 사후 수치 대조 통과 |
| v11 대표 질문 10개 정확도 | 평가 종료·전체 실패 | 수치 2/10 통과·8개 조회 전 실패. 수동 검토는 단위·차원 2개 실패·8개 미검증 |
| v12 최초 대표 질문 10개 정확도 | 평가 종료·일부 통과 | 의미 수치5/10, 전체기준1/10. 원본67개 보존 |
| v12b 대표 질문 10개 | 평가 종료·일부 통과 | 수치2/10·자동전체1/10, 원본87개보존 |
| v13 대표 질문 10개 | 평가 종료·일부 통과 | 독립 수치9/10·수동 전체4/10, 원본79개 보존 |
| 실제 AWS 장애·인증 만료·PC 중지 | 미검증 | 현재는 모의 계약/복구 시험. 배포 후 실제 경로 확인 |
| 무인 장기 운영·재부팅 | 미검증 | 초기 범위는 Windows 로그인 세션 |
| 독립 정답 없는 일반 질문 | 미검증 | 구조·값·근거 검사 통과와 업무 의미의 정답 인증은 다름 |

문서로 확인한 물리 FK 조인만 허용합니다. 복잡한 CTE의 조건 계보 등 호스트가 증명하지 못한 구조는 거부합니다. 현재 설명은 계산된 관측 문장 선택 중심이며, 자유로운 원인 추정이나 여러 SQL을 자동 실행하는 심층 조사는 구현 범위에 포함하지 않습니다.

월 25 USD 차단·10 USD 알림·기존 DB·과거 웹을 유지했습니다. 원격 push/merge는 수행하지 않았습니다. AWS Agent 패키지 업로드와 승인된 런타임 갱신은 완료했으며, Lambda·웹 서버는 변경하지 않았습니다.
