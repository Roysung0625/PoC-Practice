# Windows SQL 왕복 배포와 운영

AWS CLI 프로필 `poc-practice`는 배포와 복구, `poc-local-login`은 브라우저 로그인, `poc-chatbot`·`poc-worker`는 앱 실행에 사용한다. 장기 액세스 키를 만들지 않는다. 앱은 다른 계정, root, 지정 역할 이외의 인증을 거부한다.

## 배포

프로젝트 루트 PowerShell에서 실행한다. 최초 부트스트랩 이후 재배포는 `Deploy-PocAws.ps1`과 `Configure-PocLocal.ps1`을 사용한다. 실행 중인 앱은 AWS 설정 변경 후 재시작한다.

```powershell
.\aws\scripts\Initialize-PocAws.ps1 -ExpectedAccountId 551013419462
.\aws\scripts\Prepare-PocLogin.ps1 -ExpectedAccountId 551013419462
# 보호된 .local/secrets/aws-login/FIRST-LOGIN.txt로 IAM 콘솔에 로그인하고 암호 변경
aws login --profile poc-local-login
.\aws\scripts\Deploy-PocAws.ps1 -ExpectedAccountId 551013419462
.\aws\scripts\Configure-PocLocal.ps1 -ExpectedAccountId 551013419462
.\local\scripts\Start.ps1 -Receiver
```

AWS CLI가 PATH에 없으면 `C:\Users\roy06\AppData\Local\Programs\Amazon\AWSCLIV2\aws.exe`를 사용한다. Python은 `.venv\Scripts\python.exe`다. ARM64용 의존성은 고정한 boto3 버전의 wheel을 내려받아 ZIP으로 만든다. Docker·EC2·NAT Gateway는 사용하지 않는다. AgentCore가 생성한 로그 그룹의 보존 기간은 배포 스크립트가 CLI로 7일을 설정한다.

`Configure-PocLocal.ps1`은 기존 `.local/app.env`에서 AWS 출력값만 갱신하며 DB DSN과 API 토큰을 보존한다. AWS 로그인은 사용자 홈 캐시에만 저장된다. 최초 암호 파일은 제한된 ACL로 보관하며 최초 암호 변경 이후의 암호는 저장하지 않는다.

## 상태와 실제 시험

```powershell
.\aws\scripts\Status-PocAws.ps1 -ExpectedAccountId 551013419462
.\local\scripts\Check.ps1
.\.venv\Scripts\python.exe aws\scripts\verify_live.py embedding
.\.venv\Scripts\python.exe aws\scripts\verify_live.py lambda
.\.venv\Scripts\python.exe aws\scripts\verify_live.py native
# 챗봇에서 자연어 질문 → 계획 검토 → 승인 → 답변 표시 후
.\.venv\Scripts\python.exe aws\scripts\verify_chatbot.py
```

시험은 실제 AWS 호출 비용이 발생한다. `embedding`은 Titan V2의 1,024차원·단위 벡터를 검사한다. `lambda`는 로컬 저널에서 승인한 3행 nation 조회를 AgentCore의 전송 시험 경로로 전달하고 동일 Lambda 응답을 PostgreSQL 기준값과 대조한다. 같은 요청의 재전송도 확인한다. 모델의 실제 도구 선택과 최종 설명은 별도로 챗봇에서 자연어 계획 → 승인 → 실행 순서로 검증한다. 성공 증거는 `.local/aws-deploy/verification/`에 저장한다.

`native`는 DeepSeek의 실제 도구 요청과 최종 설명까지 검사한다. `verify_chatbot.py`는 가장 최근 AWS 승인 작업이 완료되었는지, 원본 행이 직접 조회한 PostgreSQL 값과 일치하는지, Agent 답변과 그래프가 저장되었는지 확인한다.

수신기 중지 시험은 진행 중인 사용자 작업이 없을 때 아래처럼 실행한다. `expired`는 만료 승인이 SQL을 실행하지 않는지 확인한다. 앱 전체 중지는 `local/scripts/Stop.ps1`, 다시 시작은 `Start.ps1 -Receiver`를 사용한다. 인증 만료 시 `aws login --profile poc-local-login` 후 수신기를 다시 시작한다. 앱은 같은 계획을 자동 재실행하지 않는다.

```powershell
.\local\scripts\Stop.ps1 -Role receiver
try { .\.venv\Scripts\python.exe aws\scripts\verify_live.py offline }
finally { .\local\scripts\Start.ps1 -Receiver }
```

## 승인과 실패 처리

- 계획에는 SQL 도구가 제공되지 않는다. 로컬이 계획을 검증·해시하고 승인을 저장한다. 실행 모델의 도구 인수에는 승인 요청 ID만 허용한다.
- SQL API가 승인 ID·digest·revision·만료를 확인한다. 60초 실행 기한, SQL 20초, 최대 500행·256KiB를 적용한다.
- Lambda가 DynamoDB에 조건부 등록 후 SQS 전송과 결과 대기를 담당한다. 전송 완료 표시 전에 중단되면 같은 요청을 재전송할 수 있다. 실제 중복 SQL 실행은 로컬 SQLite claim이 방지한다.
- SQL 결과와 outbox는 같은 로컬 트랜잭션에 저장된다. 전달·설명 실패 후에도 원본 행을 보존하며 Agent가 DynamoDB를 읽지 않는다.
- API 시작 시 한 번만 미확정 실행을 복구한다. 수신기 재시작은 실행 중 SQL을 취소하지 않는다. 불명인 작업은 자동 재실행하지 않는다.
- Lambda는 승인 만료+5초 또는 65초 중 이른 시점까지 기다린다. 이후 결과는 로컬 증빙으로 남고 AWS 종료 상태를 덮어쓰지 않는다.
- 로그에는 요청 ID·시간·오류 유형·토큰 사용량만 기록한다. SQL 본문, 결과 행, 비밀번호와 토큰을 기록하지 않는다.

## 정리와 비용 제한

```powershell
.\local\scripts\Stop.ps1
.\aws\scripts\Remove-PocAws.ps1 -ExpectedAccountId 551013419462
```

애플리케이션 스택을 삭제해도 기존 계정 전체 $25 초과 차단 스택, $10 알림, 로컬 PostgreSQL, 로컬 승인/결과 증빙은 유지한다. 부트스트랩 아티팩트와 로그인 사용자도 보존한다. AgentCore 자동 로그 그룹은 7일 후 내용이 정리된다.

비용 정책은 `aws/config/budget-policy.json`과 `aws/budget_guard/README.md`를 따른다. 집계·감지 지연과 남는 저장 비용 때문에 정확한 $25 청구 상한은 보장하지 않는다. 계정 전체 강제 차단 시험은 수행하지 않는다.
