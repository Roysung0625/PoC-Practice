# iDempiere 독립 정답 평가

`idempiere_cases.json`의 10개 질문·SQL은 모델 생성 SQL과 별도로 작성한 정답 기준이다. GardenWorld(11), 날짜·문서 상태·대변전표·통화·행 단위를 질문에 명시한다. 상세 조인 중복, 후속 기간 변경, 빈 결과를 포함한다. 실제 DB에 없는 경계 사례는 Python 단위 시험 fixture로 추가 검증한다.

## 전체 10문항 재실행 전 기준 명확화

v7~v10 실행 이후 새 전체 10문항 평가를 시작하기 전에 질문과 평가 기준의 일치를 읽기 검토했다. 질문에 정렬을 요구하지 않았던 `ERP01`, `ERP02`, `ERP04`, `ERP06`, `ERP10`은 `ordered=false`로 바꿔 과잉 정렬 기준을 제거했다. 행 수와 값은 중복 개수를 포함한 행 집합(multiset)으로 계속 대조하므로 누락·추가·중복 행이나 다른 정답 값을 허용하는 변경이 아니다. 정렬을 명시한 나머지 문항의 순서 검사는 유지한다.

출력 열과 코드 표현 요구도 다음과 같이 질문에 명시했다.

| 문항 | 명확히 한 요구 |
| --- | --- |
| ERP03 | 거래처 ID와 거래처 이름을 함께 출력 |
| ERP05 | 상품 ID와 상품 이름, 수량 단위 ID와 통화를 함께 출력 |
| ERP07 | 창고와 상품 각각의 ID·이름을 구분해 출력 |
| ERP04 | 판매·구매 구분과 문서 상태를 `issotrx`·`docstatus` 원본 코드로 표시 |
| ERP06 | 입금 여부와 문서 상태를 `isreceipt`·`docstatus` 원본 코드로 표시 |
| ERP08 | 상품 유형과 판매 가능 여부를 `producttype`·`issold` 원본 코드로 표시 |

독립 정답 SQL, 매개변수, 출력 필드 정의와 정답 값은 변경하지 않았다. 변경 전 케이스 파일의 SHA-256은 `c6fa184266fc6529a06295887a7f18e471e658d60e1dfcf4a662386e02043945`, 변경 후 SHA-256은 `56205718cb78ed39ccbe4589c742d7a106a01bc9ccb2bd6a3823ff6a60263350`다. 기존 v7~v10 실행의 질문·응답·실패 증거는 그대로 보존하며 이번 기준 변경으로 이전 실패를 폐기하거나 성공으로 전환하지 않는다. 수정한 질문은 새 출력 폴더에서 수행할 이후 전체 평가에 적용한다.

로컬 정답만 캡처:

```powershell
.\.venv\Scripts\python.exe analysis-chatbot\scripts\evaluate_idempiere.py --output .local\analysis-chatbot\evaluation\golden-001
```

이 명령은 읽기 전용 정답 SQL 10개를 실행하지만 모델 정확도는 모두 **미검증**으로 표시한다. 조회 결과를 정답으로 재사용하는 검증을 하지 않는다.

실제 챗봇 결과와 대조:

```powershell
.\.venv\Scripts\python.exe analysis-chatbot\scripts\evaluate_idempiere.py --responses .local\analysis-chatbot\responses.json --output .local\analysis-chatbot\evaluation\compare-001
```

responses 파일은 `ERP01` 등 질문 ID를 키로 하고 저장된 턴(내부 `result`) 또는 원본 결과를 값으로 갖는다. 별칭이 다른 경우 `--mappings`로 사람이 검토한 의미 기반 매핑을 명시한다. 정답 값으로 열 매핑을 추측하지 않는다.

새 AWS runtime 배포를 승인·완료한 뒤 `--live`를 명시하면 웹 API에서 질문 → 계획 → 승인 → 조회까지 한 번씩 진행한다. 이 모드는 유료 모델 호출과 실제 승인 조회를 수행한다. ERP02/ERP10은 ERP01의 같은 대화 결과를 참조한다. 확인 질문과 실패는 그대로 저장하고 자동 재시도하지 않는다. 계획, 전체 턴, 전후 정답, 비교 보고서를 새 실행 폴더에 저장한다. 기존 폴더 덮어쓰기는 거부한다.

`pass`(통과), `mismatch`(불일치), `unverified`(미검증), `not_applicable`(적용 없음), `error`(검사 실패)를 구분한다. SQL 수치 대조와 사람의 계획·문서·시사점 검토를 분리한다. 모델 결과가 없는 항목이나 확인 질문을 성공으로 계산하지 않는다. AWS 미배포 상태에서 라이브 평가 완료를 주장하지 않는다.

보고서의 `summary`는 독립 SQL 수치 대조만 집계한다. 각 문항의 `stages`와 `stage_summary`는 run 종료 상태, 원본 데이터, 차트 단위(`chart_unit`)·차원(`chart_dimensions`) 검증, 실제 PNG 수집, 호스트 검증 시사점, 수집 오류를 구분한다. `automated_summary`는 이 단계와 수치 검사가 모두 통과한 문항만 통과로 집계한다. 원본 표가 정답과 같아도 run이 `partial`이거나 차트·시사점이 실패하면 자동 종합 판정은 실패다. 의미 정확도에 대한 `human_review`는 여전히 별도 미검증 항목이다.

차트 단위·차원 검증의 누락이나 미검증은 `unverified`이며 수치·PNG 검사가 통과해도 자동 종합 통과로 처리하지 않는다. 보고된 `error`·`mismatch`와 원래 검증 증거를 보존하고, 뒤에 나타난 `pass`로 실패를 가리지 않는다. 정상 0행 결과에 차트 산출물이 없을 때만 두 차트 검증을 `not_applicable`로 처리하며, 이 경우에도 명시적인 검증 실패는 유지한다. 이 규칙은 v12 새 평가부터 적용하는 평가기 보강이며, 기존 v11 이하 실행 보고서와 실패 증거를 수정하거나 재판정하지 않는다.

라이브 실행과 저장 응답 비교는 실패 또는 미검증이 하나라도 남으면 종료 코드 1을 반환한다. 따라서 모든 문항이 확인 질문으로 멈췄거나 열 매핑이 없어 미검증인 실행도 종료 코드 0으로 표시하지 않는다. 명시적인 정답 캡처만 수행하는 기본 모드는 정답 SQL이 정상 실행되면 미검증 표시와 함께 종료 코드 0을 유지한다. `--responses`만으로는 실제 PNG 바이트 수집과 웹 전송을 검증할 수 없으므로 해당 단계는 미검증으로 남는다.

각 라이브 문항은 접수 응답, 승인 전 계획, 승인 요청·응답, 원본 최종 턴을 각각 저장한다. 폴링 오류가 나면 마지막으로 받은 턴과 ID·이벤트를 보존한다. 종료 요청 실패는 `ERPxx-cleanup-error.json`, 다른 수집 오류는 `ERPxx-collection-error.json`에 별도로 남기며 원본 턴을 오류 객체로 덮어쓰지 않는다. 정답이나 모델 질문을 자동 재시도하지 않는다.

PNG는 응답의 UUID 산출물 ID로 같은 웹 API의 `/api/artifacts/{id}`만 호출해 `artifacts/ERPxx-UUID.png`에 수집한다. 모델 응답에 들어 있는 URL·파일 경로를 따라가지 않는다. `ERPxx-artifacts.json`에 HTTP 상태, Content-Type, PNG signature·IHDR 크기, 기대/실제 SHA256, 상대 파일 경로를 기록한다. 바이트 검증 실패는 원본을 `.response.bin`으로 보존하고 실패로 판정하며, 다운로드 실패도 별도 항목으로 남긴다. 0행 정상 결과는 PNG 없음이 `not_applicable`이다.

평가기는 서버나 수신기를 시작하지 않는다. 실행 전에 운영 스크립트로 기존 공유 원장과 단일 수신기 상태를 확인해야 한다. 실제 AWS 인증·배포·수신기의 준비 상태는 수치 평가 통과만으로 증명되지 않는다.

수정 후 한 질문의 연결을 먼저 확인하려면 새 출력 경로와 `--live --case ERP01`을 지정한다. 여러 ID를 지정하려면 `--case`를 반복한다. 후속 질문 ERP02/ERP10은 부모 ERP01도 함께 명시해야 한다. 부분 실행의 `selected_cases`와 전체 가용 문항 수를 보고서에 남기며, 1문항 통과를 전체 10문항 통과로 표시하지 않는다. 전체 평가는 `--case` 없이 새 폴더에서 실행한다. 이전 실패 폴더는 보존한다.


## 2026-11-03 실행 증거의 구분

v12 최초 전체 평가 `live-v12-20261103-003`의 원본 보고서는 열 별칭 때문에 수치10개를 미검증으로 남겼다. 원본67개 SHA256을 유지한 채 저장된 SELECT 식·조건·지표 의미로 `semantic-mappings.json`을 먼저 정하고, 저장된 독립 golden과 대조한 `semantic-review.json`을 별도로 추가했다. 수치5개는 일치했고 조회 전 실패5개는 미검증이며, 전체 기준은 ERP01만 통과했다. 이 사후 검토가 원본 실패를 지우거나 모델 SQL을 정답으로 사용한 것은 아니다.

AWS runtime12를 유지하고 로컬 후속 수정 후 실행한 `live-v12b-20261103-001`는 종료됐다. run성공2개·조회전실패8개, 의미수치2/10통과, 자동전체기준은ERP08만1/10통과다. ERP07은수량단위미검증과요청에없던active필터4개를별도검토사항으로유지했다. golden전후는같았고원본87개와소스32개를보존했다. 구현 SHA256·lock·UI빌드·실행역할·health·PID·SQL작업 기준은 `.local/analysis-chatbot/verification/preflight-v12b-20261103-001-implementation.json`에 기록했다. 비밀설정·토큰·DSN·원본 DB는 지문에서 제외했다. 같은 DB가 다른 작업으로 변경될 가능성과 실제 변경 확인을 구분한다. golden 전후가 다르면 기준 데이터 변경에 따른 수치검사 실패로 보존하고 모델 SQL 오답으로 단정하지 않는다. 최종 판정은 [검증 기록](../docs/VERIFICATION.md)을 따른다.


## v13 계획 보완 이력의 분리

`live-v13-20261103-001`는 새 runtime13과 동결 소스로 전체10문항을 각1회 완료했다. 독립 수치9/10, 수동 전체4/10이며 첫 초안9개 통과·1개 거부·실제1회 보완 실패로 구분한다. 호스트의 승인 전 초안 보완은 별도 모델 호출이며 최대1회·기존6호출/180초 안에서 수행한다. 평가기가 실패한 질문을 다시 보내거나 SQL을 자동 재실행하는 기능은 추가하지 않았다. `implementation-before.json`과 `source-snapshot.zip`으로 비밀을 제외한 시작 소스36개를 고정한다.

새 보고서는 문항별 `planning`과 `planning_summary`를 추가한다. `initial_plan_rejected`, `initial_plan_passed`, `repair_count`, `final_plan_validated`, `final_plan_validated_after_repair`를 기록한다. `outcome`의 `first_attempt_validated`와 `repaired_validated`는 합치지 않는다. `completed_after_repair`는 보완한 계획의 run 성공이며, `automated_pass_after_repair`는 수치·단위·차원·PNG·시사점·수집까지 자동 기준을 통과했을 때만true다. `first_attempt_automated_pass`도 별도로 집계한다. 모델 보완 실패는 `repair_failed`, 시작했지만 완료 증거가 없으면 `repair_incomplete`다. 보완을 시작하지 않은 `plan_repair_skipped`는 횟수에 포함하지 않는다.

최종 요약이 첫 거부 이벤트와 충돌하면 메타데이터 mismatch로 실패를 유지한다. 시도 메타데이터가 없는 과거 실행은 미검증으로 남기고 처음부터 통과한 것으로 추정하지 않는다. 기존 v12/v12b 보고서·실패 원본은 이 보강으로 변경하지 않는다.
