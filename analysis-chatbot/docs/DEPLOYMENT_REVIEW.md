# 신규 분석 단계 AWS 배포 검토

2026-11-03 사용자가 **AI 왕복 검증을 승인했고 웹 서버는 로컬로 유지**하도록 지정했습니다. AWS에는 Agent runtime만 배포했고 Laravel·Vue·DB·PNG 생성은 Windows에서 실행합니다. **현재 stack `UPDATE_COMPLETE`, runtime v13 `READY`, DEFAULT `liveVersion=13 / READY`입니다.** v11 단건 성공과 v12/v12b 전체 평가의 실패 원본을 보존합니다. v12는 의미 수치5/10·전체 기준1/10, v12b는 의미 수치2/10·전체 기준1/10으로 종료됐습니다. `live-v13-20261103-001`은 독립 수치9/10·수동 전체4/10으로 종료됐습니다. 이후 로컬 차트4사례·7PNG 복구와 API 단독 재시작 복원은 별도 확인이며 실AWS 전체 통과에 합산하지 않습니다. [질문별 결과와 개선 효과](VERIFICATION.md)를 확인합니다.

## 인증 복구

초기 `poc-practice`, `poc-chatbot`, `poc-worker`의 STS 조회에서 세션 만료를 확인했습니다. AWS 로그인 페이지의 400 오류 이후 새 로그인에서 사용자가 배포 계정 인증을 완료했고, `poc-practice`가 선택한 AWS 계정과 일치함을 확인했습니다. 앱 원본 프로필을 root로 덮어쓰는 CLI 제안은 거절했으며 기존 IAM 사용자 구성을 유지했습니다.

사용자가 `poc-local-login` 비밀번호 분실을 알리고 재설정을 승인했습니다. 콘솔 비밀번호만 임시값으로 재설정하고 사용자가 직접 새 비밀번호를 설정했습니다. IAM CLI 로그인과 앱 `poc-chatbot`·수신기 `poc-worker`의 실제 STS 역할 확인을 완료했습니다. 임시 안내는 접근 제한 폴더로 제공한 뒤 비밀번호 변경 완료를 확인하고 삭제했습니다. 비밀번호 값은 이 문서에 기록하지 않습니다. localhost 웹/API와 DB를 재사용하고 단일 수신기를 시작했습니다.

## 이번 실제 배포 기록

- 기존 Agent runtime v6 `READY`, Lambda `Active`, SQS 대기/실행 중 메시지 0/0을 확인했습니다.
- 실제 집계 비용 0.003 USD, 예산 제어 일정 `ENABLED`, 차단 latch·pause 없음, 실패 경보 `OK`를 확인했습니다. 예산 설정은 변경하지 않았습니다.
- `.local/aws-deploy/analysis-20261103/`에 이전 stack/runtime, 업로드 결과, 변경 세트와 속성 대조를 보존했습니다.
- `analysis-runtime-20261103-2155` 변경 세트는 기존 템플릿과 다른 파라미터를 보존하고 `AgentKey`만 변경했습니다. 최종 속성 대조의 변경 대상은 `AgentRole`의 S3 단일 패키지 경로와 `AgentRuntime`의 패키지 경로이며 리소스 교체는 없습니다. 2026-11-03 21:55 JST에 stack `UPDATE_COMPLETE`, 이후 runtime v7과 DEFAULT 엔드포인트 `READY`를 확인했습니다. `stack-after.json`, `runtime-after.json`, `endpoint-after.json`을 보존했습니다.
- 후속 v8도 Agent 전용 변경으로 실제 배포했습니다. Agent ZIP SHA-256은 `2837c9234206863eb2b685710ec4f37659f3db97ca639608e2c2d23c9dbd361b`입니다. v8 실제 평가 단건은 `MODEL_JSONDecodeError`로 실패했고 SQL은 실행되지 않았습니다. 원본 실패는 `.local/analysis-chatbot/evaluation/smoke-v8-20261103-001/`에 보존했습니다.
- v9에서는 모델 응답에 공통 엄격 JSON 파서를 적용하고 비민감 진단을 추가했습니다. 과거 v8 오류의 원인을 확정한 것은 아닙니다. Agent ZIP SHA-256은 `af6f4d779ad1269b9c81c72c9ff098365cda9fd369e221cb457fc994ec36d200`, `aws/runtime/main.py` 소스 SHA-256은 `cc8de09e09b93b25589501e2bf0d368e5d16b9987b24686e0ba27dbf203f7f01`입니다. `.local/aws-deploy/analysis-20261103-v9/`에 변경 세트·stack/runtime/DEFAULT 응답을 보존했고 stack `UPDATE_COMPLETE`, runtime v9 `READY`, DEFAULT `liveVersion=9 / READY`를 확인했습니다.
- v9 실제 브라우저는 `CONDITION_NOT_APPLIED`로 실패했습니다. 별도 진단에서 이름 있는 scalar 매개변수를 사용한 조건 검증과 ARC 제외 문제가 확인돼 보완했습니다. v10 브라우저에서는 `condition_bindings` 배열 및 단일 SQL placeholder에 CSV 값을 전달한 계획이 실패했습니다. 각각 `.local/analysis-chatbot/evaluation/browser-v9-20261103-001/`, `diagnostics-v9-20261103-001/`, `browser-v10-20261103-001/`에 보존했습니다.
- v11은 Agent ZIP `2e8e354cf31ce30d23718c32bc7a0588c086d9aeb356bdf7e36b3b508f41aa26`, `aws/runtime/main.py` 소스 `21a383c60bce88a337fe28eefdce7959979c800513c8e0802ddb4a711a4211dc`로 배포했습니다. `.local/aws-deploy/analysis-20261103-v11/`에서 stack `UPDATE_COMPLETE`, runtime v11 `READY`, DEFAULT `liveVersion=11 / READY`를 확인했습니다. 실제 브라우저 단건의 SQL 왕복·PNG·시사점 성공과 별도 사후 수치 대조는 `.local/analysis-chatbot/evaluation/browser-v11-20261103-001/report.json`에 기록했습니다. 별도 전체 평가 `live-v11-20261103-002/semantic-review.json`은 종료를 확인했으며 수치 2개 통과·8개 미검증, 수동 검토 2개 실패·8개 미검증입니다. 원본 실패 자료를 보존합니다.
- v12는 Agent ZIP `4a28ae2c554ef8e5349b6aa0f61a017ad954e3bb483f35d658ff17381f7a7273`, runtime 소스 `77d7a5ed6c7a3029f0fd8f0ad8172b96d79c6bcdf6de34cef19c8657441087a5`로 배포했습니다. `.local/aws-deploy/analysis-20261103-v12/`에 stack `UPDATE_COMPLETE`, runtime 12 `READY`, DEFAULT `liveVersion=12 / READY` 확인 자료를 보존합니다. `live-v12-20261103-003` 최초 전체 평가는 종료됐고 의미 수치5/10·전체 기준1/10 통과입니다. v12b는 AWS 패키지를 유지한 로컬 변경이며 전체 평가가 종료됐습니다. 의미 수치2/10·전체 기준1/10이고 원본87개와 동결 소스32개를 보존했습니다.
- v13은 Agent ZIP `9d89ee85f30546a7b94ba0e33485df10cfaf5e13dba958dbd982c7dd710e02bf`, runtime 소스 `eacd4dbb97d8bb65f38f69e26cff795976396f57ca4c8b56899d1c87f8e371e4`로 배포했습니다. ZIP 안의 main.py·contract.py는 소스와 바이트/해시가 같았습니다. `analysis-runtime-20261103-234037` 변경세트는 기존 템플릿과 AgentKey 외 모든 파라미터를 보존했습니다. AgentRole의 단일 S3 객체 키와 AgentRuntimeArtifact만 Modify이고 교체는 없으며, BeforeContext의 해당 키를 치환한 값과 AfterContext가 완전히 같았습니다. 23:46 JST에 stack UPDATE_COMPLETE/runtime13 READY/DEFAULT13 READY를 확인했습니다.
- v13 execute의 최초 자동 승인 검토는 이 변경세트 실행의 사용자 승인 근거가 부족하다며 프로세스 시작 전에 거부했습니다. 원래 런타임 배포·AI 검증 승인 질문과 사용자의 로컬 웹 유지 조건 답변을 보완해 동일 명령·프로필·범위로 1회 재검토했고 허용됐습니다. 최초 거부·승인 근거·재검토·실행 결과는 `.local/aws-deploy/analysis-20261103-v13/execution-approval-review.json`에 보존합니다. 우회 명령을 사용하지 않았습니다.
- Lambda는 현재 배포된 `runtime/6270ab07ea5d57f91b18b600a13dc0ffff32f22e2b1979a40659ca83a3fbe093/sql-tool.zip`을 그대로 유지했습니다. 실제 S3 ZIP 해시와 소스를 확인했으며 신규 Agent와 Windows 요청·응답 계약이 호환됩니다. 로컬에서 준비한 다른 Lambda ZIP은 이번에 업로드·배포하지 않았습니다.

## 변경 내용

`aws/runtime/main.py`에 다음 단계를 추가했습니다.

| 단계 | 수행 내용 | SQL 도구 |
| --- | --- | --- |
| `interpret` | 기존 조건과 새 질문을 해석하고 확인 질문/조건 반환 | 없음 |
| `document_plan` | 실제로 읽은 문서·열·FK·확정 조건을 모델 메시지에 전달 | 없음 |
| `execute_data` | 승인된 요청 ID로 기존 Lambda를 한 번 호출하고 같은 호출의 결과 반환 | 기존 `execute_approved_sql` 1회 |
| `insights` | 원본 결과·계산 통계·검증·차트 manifest 근거로 관측 설명 선택 | 없음 |
| 기존 `execute` | 기존 웹의 조회 후 설명 생성 경로 유지 | 기존 방식 유지 |

모델·리전·역할의 책임·SQS·DynamoDB·Lambda 대기 구조·예산 차단 설정은 유지합니다. Agent 역할의 S3 읽기 대상은 새 runtime 패키지 키로 함께 갱신해야 하므로 기존 CloudFormation의 `AgentKey` 변경으로 배포합니다. SQL 요청 60초 만료와 Lambda 한 번의 동기 응답을 유지합니다. PNG는 Windows 별도 프로세스에서 생성하며 클라우드에 Python 시각화 실행기를 추가하지 않습니다.

v12의 문서 계획은 단일 호출 90초를 적용하되 계획 누적 180초를 유지합니다. 로컬 호스트는 원본 문서 전체 해시와 투영 컨텍스트 해시를 검증하고, 중복 표시만 제거한 실제 근거를 최종 모델에 전달합니다. 단위·차원·복합 라벨 검증과 미확정 단위의 통계 설명 제한은 로컬 호스트·가시화 패키지의 책임입니다. 승인 전 차트를 정규화하고 재사용 결과의 표시가 달라지면 새 턴·PNG를 생성하며 SQL을 자동 재실행하지 않습니다. 128KiB·후보 12개·상세 32개·2홉 한도는 유지합니다. 최종 로컬 보완 후 Python661개(29.58초)가 통과했습니다. 변경 없는 가시화61개(9.86초), Vue10개(1.25초), Laravel10개/71 assertions 및 TypeScript·Vite 빌드 결과는 재실행 없이 유지합니다. v13 실제 full10의 수치9/10·수동 전체4/10은 자동 시험과 구분합니다. 실제 평가 시작의 비밀 제외36파일 지문·소스 ZIP·health·PID·역할·runtime 확인은 `.local/analysis-chatbot/verification/preflight-v13-20261103-001-implementation.json`, 사후 최종97파일과 시험·브라우저 복원 증거는 `.local/analysis-chatbot/evaluation/final-local-v13b-20261104-001/`에 기록했습니다.

v13은 `plan`·`document_plan`의 출력 상한만4096토큰으로 늘리고 다른 단계는2048을 유지합니다. 4096은 실제 출력량이나 청구 토큰 수가 아닙니다. max_tokens는 JSON 파싱 전에 MODEL_OUTPUT_TRUNCATED로 명시 거부하고 자동 재호출하지 않습니다. 로컬 승인 전 초안 보완은 기존6호출/180초 안에서 최대1회이며 첫 거부·공개 plan_attempts·최종 digest를 보존합니다. 승인 후 SQL 자동 재실행을 추가하지 않습니다.

## 패키지와 보존 대상

실행: `.\.venv\Scripts\python.exe aws/scripts/package_runtime.py`

| 대상 | SHA-256 / 보존 기준 |
| --- | --- |
| 현재 배포한 Agent v13 ZIP | `9d89ee85f30546a7b94ba0e33485df10cfaf5e13dba958dbd982c7dd710e02bf` |
| v13의 `aws/runtime/main.py` 소스 | `eacd4dbb97d8bb65f38f69e26cff795976396f57ca4c8b56899d1c87f8e371e4` |
| 이전 Agent v12 ZIP | `4a28ae2c554ef8e5349b6aa0f61a017ad954e3bb483f35d658ff17381f7a7273` |
| v12의 `aws/runtime/main.py` 소스 | `77d7a5ed6c7a3029f0fd8f0ad8172b96d79c6bcdf6de34cef19c8657441087a5` |
| 이전 Agent v11 ZIP | `2e8e354cf31ce30d23718c32bc7a0588c086d9aeb356bdf7e36b3b508f41aa26` |
| v11의 `aws/runtime/main.py` 소스 | `21a383c60bce88a337fe28eefdce7959979c800513c8e0802ddb4a711a4211dc` |
| 이전 Agent v9 ZIP | `af6f4d779ad1269b9c81c72c9ff098365cda9fd369e221cb457fc994ec36d200` |
| 이전 실패 증거를 보존한 Agent v8 ZIP | `2837c9234206863eb2b685710ec4f37659f3db97ca639608e2c2d23c9dbd361b` |
| 현재 배포된 Lambda ZIP — 유지 | `6270ab07ea5d57f91b18b600a13dc0ffff32f22e2b1979a40659ca83a3fbe093` |

ARM64·Python 3.13 패키지이며 manifest는 `.local/aws-deploy/packages.json`입니다. 패키징은 `.local/aws-deploy/agent.zip`과 `sql-tool.zip`을 모두 만들지만 **이번 배포에서는 Agent ZIP만 업로드합니다. manifest의 `LambdaKey`는 사용하지 않습니다.** v13 배포 전후 실제 Lambda CodeSha256은 `YnCrB+pdV/kbGLYAoT3A//8y8i4rGXmkBlnKg6P74JM=`로 같았습니다. 현재 배포된 Lambda에는 Windows/Mac 요청 라우팅 확장이 있으므로 로컬에서 생성한 다른 Lambda ZIP으로 바꾸면 해당 확장을 덮어쓸 수 있습니다. 버전별 해시는 해당 배포 당시의 기록이며, 추가 수정 후 생성하는 ZIP의 현재 해시를 대신하지 않습니다.

## 승인된 Agent 전용 실행 순서

기존 `Deploy-PocAws.ps1 -SkipPackage`는 이 절차에 사용하지 않습니다. 해당 스크립트는 Agent와 Lambda를 모두 업로드하고 로컬 템플릿·`LambdaKey`까지 반영하므로, 현재 Lambda의 라우팅 확장을 보존하는 Agent 전용 배포와 범위가 다릅니다.

1. `poc-practice` 인증의 실제 계정과 도쿄 `ap-northeast-1`을 확인합니다. 현재 `poc-practice-app`의 전체 stack 응답·템플릿·모든 파라미터·출력, runtime과 DEFAULT 엔드포인트, Lambda 코드 키·설정, 예산 차단 상태를 배포 기록 폴더에 보존합니다. 실제 계정 ID·ARN은 보호된 로컬 기록에서 확인하고 공개 예시에 복사하지 않습니다.
2. 프로젝트 루트에서 패키징하고 Agent ZIP 해시와 manifest의 `AgentKey`를 대조합니다. ZIP 안의 `main.py`·`contract.py`가 배포할 소스와 일치하는지 확인합니다.

   ```powershell
   .\.venv\Scripts\python.exe aws/scripts/package_runtime.py
   if ($LASTEXITCODE -ne 0) { throw 'Agent 패키징 실패' }
   $packages = Get-Content .local/aws-deploy/packages.json -Raw | ConvertFrom-Json
   $agentHash = (Get-FileHash .local/aws-deploy/agent.zip -Algorithm SHA256).Hash.ToLowerInvariant()
   if ($packages.AgentKey -ne "runtime/$agentHash/agent.zip") { throw 'Agent 패키지 해시 불일치' }
   ```

3. **현재 stack의 `ArtifactBucket`에 Agent ZIP만** `s3api put-object`로 업로드합니다. 새 키는 `runtime/<확인한 SHA-256>/agent.zip`이며 서버 측 암호화 `AES256`을 지정합니다. 업로드 응답과 ZIP을 보존합니다. `sql-tool.zip`은 업로드하지 않습니다.
4. 보존한 stack의 **모든 기존 파라미터**로 변경 세트 입력을 만듭니다. `AgentKey`에만 새 키를 지정하고 나머지는 모두 `UsePreviousValue=true`로 둡니다. 특히 `LambdaKey`는 `runtime/6270ab07ea5d57f91b18b600a13dc0ffff32f22e2b1979a40659ca83a3fbe093/sql-tool.zip`에서 바뀌지 않아야 합니다. 아래의 `$stackBefore`는 방금 조회·보존한 `describe-stacks` 응답의 `Stacks[0]`이며 `$parameterFile`은 배포 기록 폴더의 JSON 경로입니다.

   ```powershell
   $parameters = @($stackBefore.Parameters | ForEach-Object {
       if ($_.ParameterKey -eq 'AgentKey') {
           @{ ParameterKey = $_.ParameterKey; ParameterValue = $packages.AgentKey }
       } else {
           @{ ParameterKey = $_.ParameterKey; UsePreviousValue = $true }
       }
   })
   [IO.File]::WriteAllText($parameterFile, ($parameters | ConvertTo-Json -Depth 5), [Text.UTF8Encoding]::new($false))
   ```

5. 고유한 변경 세트 이름으로 `cloudformation create-change-set`을 호출합니다. `--stack-name poc-practice-app --change-set-type UPDATE --use-previous-template --parameters file://<위 JSON 경로> --capabilities CAPABILITY_NAMED_IAM`을 사용하고 `--profile poc-practice --region ap-northeast-1`을 명시합니다. **현재 CloudFormation 템플릿을 재사용하며 로컬 `application.json`을 배포하지 않습니다.** 변경 세트 생성 완료를 기다린 뒤 `describe-change-set --include-property-values` 결과를 저장합니다.
6. 속성의 변경 전·후 값을 대조합니다. 허용 변경은 `AgentRole`의 S3 읽기 권한에 있는 **단일 Agent 패키지 키**와 `AgentRuntime`의 Agent 패키지 경로뿐입니다. 두 리소스 모두 `Action=Modify`, `Replacement=False`인지 확인하고, Lambda·라우팅·SQS·DynamoDB·예산 및 다른 역할 설정에 변경이 없는지 확인합니다. 추가 변경이나 리소스 교체가 있으면 실행하지 않고 변경 세트를 수정합니다.
7. 위 대조가 승인된 Agent 변경 범위와 일치하면 해당 변경 세트만 `execute-change-set`으로 실행합니다. `stack-update-complete`를 기다리고 stack `UPDATE_COMPLETE`, `get-agent-runtime`의 새 버전과 `READY`, `get-agent-runtime-endpoint --endpoint-name DEFAULT`의 `liveVersion` 일치와 `READY`를 각각 확인·보존합니다. 배포 후에도 `LambdaKey`와 실제 Lambda 코드가 이전 기록과 동일한지 다시 대조합니다.
8. 기존 로컬 ARN·큐·결과 테이블 설정을 확인합니다. 앱은 `poc-chatbot`, 수신기는 `poc-worker` 일반 역할을 사용하며 root 인증을 실행환경에 사용하지 않습니다. API와 단일 수신기를 확인하고 필요할 때만 `analysis-chatbot/scripts/Start.ps1 -Receiver`로 시작합니다. 웹 서버는 localhost에 유지합니다.
9. 브라우저에서 자연어 질문 → 문서 이벤트 → 계획 승인 → 실제 Lambda/SQS/Windows/PostgreSQL 왕복 → PNG → 시사점 → 기간 변경 후속 질문 → 저장 결과 재사용을 확인합니다. `evaluation/README.md`의 10개 질문을 한 번씩 실행하고 독립 SQL·원본 응답·차트 값·사람 검토를 보존합니다. 실패를 자동 재시도로 숨기지 않으며, 수정 후 재평가는 이전 실패와 분리해 기록합니다.

## 완료 판단과 복구

배포 성공, 모델 응답 성공, Lambda 한 번의 왕복 성공, 실제 DB 값 일치, PNG 생성, 후속 대화 유지 성공을 각각 기록해야 신규 AWS 연동 완료입니다. 현재의 로컬·모의 시험은 이 완료 판단을 대신하지 않습니다.

문제 발생 시 새 질문을 중단하고 진행 작업의 SQL 상태를 확인합니다. 불확정 요청을 자동 재실행하지 않습니다. 이전 runtime 패키지 키와 CloudFormation 설정으로 복구할 수 있도록 배포 전 값을 보존합니다. 데이터·볼륨·버킷·승인 원장을 삭제하지 않습니다. 월 25 USD 차단과 10 USD 알림도 변경하지 않습니다.

새 단계가 추가되므로 기존 Nova Lite 기반 견적을 현재 비용으로 사용하지 않습니다. 실제 평가 시 DeepSeek 모델 사용량·AgentCore 실행·Lambda 대기·로그/전달 비용을 구분해 수집합니다. 실제 v13에서 완료 model_usage48회·입력614,338·출력20,695토큰을 수집했습니다. 이는 Codex 대화/워커 토큰과 별개이며 실패한 보완의 사용량과 실제 청구 금액은 미확정입니다.
