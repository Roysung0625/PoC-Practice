# AWS CLI 배포와 Windows SQL 왕복 검증

2026-10-12 도쿄 리전 `ap-northeast-1`, 계정 `551013419462`에서 검증했다. 아래 전체 흐름의 실제 성공과 챗봇 화면 표시를 확인했다.

```text
Windows 챗봇 → AgentCore / DeepSeek V3.2 → SQL Lambda
→ SQS → Windows 수신기 → localhost FastAPI → PostgreSQL
→ DynamoDB → 같은 Lambda 호출 응답 → Agent 설명 → 챗봇 표·그래프
```

## 실제 호출 증거

| 항목 | 확인 결과 | 로컬 증거 |
|---|---|---|
| Titan V2 | 1,024차원, norm `0.9999999846146388`, 입력 10토큰 | `.local/aws-deploy/verification/embedding.json` |
| Lambda 왕복 | nation 3행, PostgreSQL 기준값 일치, 같은 요청 재전송 결과 일치 | `lambda.json`, 요청 `4d712606-0c50-4b08-af31-c1fcbf953d66` |
| DeepSeek 도구 호출 | 실제 native tool_use, 3행 조회와 446자 설명 | `native.json`, 요청 `24be1e3a-434d-41d3-9dc0-7e3b600cbabf` |
| 전체 챗봇 | 자연어 계획·승인·도구 호출·SQL·852자 Agent 답변·표·막대그래프 | `chatbot.json`, 요청 `974faf92-e532-4430-a032-bb5b03e9d176` |
| 승인 만료 | SQL 실행 없이 `REQUEST_EXPIRED` | `expired.json` |
| 수신기 중지 | 17.76초 후 `LOCAL_RESULT_TIMEOUT`, 이후 수신기 재시작 | `offline.json`, 요청 `31601a06-ebd3-4bc7-9f86-fcd71d64b01f` |
| 비용 차단 | 새 사용자·4개 역할·SQL Lambda 포함, applied/errors 빈 배열 | `budget-dry-run.json` |

위 증거 JSON의 기본 폴더는 모두 `.local/aws-deploy/verification/`이며 Git 제외 대상이다. 모델 자동 대체 없이 `deepseek.v3.2`, `amazon.titan-embed-text-v2:0`만 호출했다.

챗봇 검증 질문은 “1995년 주문일 기준 STANDARD 제품군(p_type이 STANDARD로 시작하는 전체 유형)의 월별 할인 적용 매출을 조회하고 막대그래프로 보여줘. 월을 오름차순으로 정렬해줘.”였다. 계획의 `STANDARD%` 바인딩과 날짜 조건을 검토하고 승인했다. 12개월 원본 행·열이 별도 읽기 전용 PostgreSQL 조회와 정확히 일치했고, 그래프의 점 수도 12개였다. 원본 Decimal 값은 문자열로 보존했다.

- 원본 행 SHA256: `ff5a72e71421186774a8354155b4a237125bb15012098a5e30f8882c7cca0376`
- SQL 실행 814ms, SQL `succeeded`, AWS `delivered`, Agent `succeeded`
- 검증 시각: `2026-10-12T09:15:29Z`
- AgentCore: `poc_sql_agent-OkSxdVEslY`; SQL Lambda: `poc-sql-tool`

브라우저 새로고침 후 분석 이력에서 같은 결과를 다시 열어 Agent 설명·원본 표·그래프의 보존도 확인했다. 실제 화면은 `.local/aws-deploy/verification/chatbot-result.jpg`에 저장했다.

## 배포와 인증

- AWS CLI CloudFormation으로 `poc-practice-bootstrap`, `poc-practice-app` 배포. 비공개 암호화 S3와 앱 스택을 분리했다.
- AgentCore Python 3.13/Linux ARM64 ZIP. Docker·EC2·NAT Gateway를 추가하지 않았다.
- `poc-local-login` 최초 암호 변경과 CLI 브라우저 로그인 후 실제 STS 사용자 ARN을 확인했다. `poc-chatbot`·`poc-worker` 역할 AssumeRole도 확인했다. 이 IAM 사용자의 장기 액세스 키는 0개다.
- 앱은 root·다른 계정·잘못된 역할을 거부한다. 배포 프로필 `poc-practice`를 앱에 사용하지 않는다.
- Lambda timeout 75초, 예약 동시 실행 없음, 계정 한도 10. DDB `cleanup_at` TTL 활성, 온디맨드. SQS visibility 90초·보존 1일, DLQ 4일·3회. Agent idle 60초·최대 300초, 로그 7일.
- 실제 호출 후 AgentCore 세션 종료 로그를 확인했다. 재배포 산출물 SHA와 AWS 출력은 `.local/aws-deploy/`에 저장했다.
- 최종 상태 확인에서 Agent `READY`, Lambda `Active`, 요청 큐의 대기/처리 중 메시지 각각 0, Windows API·웹·수신기 및 PostgreSQL 모두 실행 중이었다.

## 자동 시험과 보완 사항

`python -m pytest local/python/tests aws/tests -q --basetemp=.local/pytest-aws-final`: **64 passed**. Vue Vitest **5 passed**, TypeScript 검사와 Vite 빌드 성공. Plotly 청크 크기 경고는 남아 있다.

승인 누락·ID/계획 변조·revision·중복·만료, SQS 전송 전후 간격 복구, 재시작 불명 작업의 재실행 금지, SQL 결과/outbox 원자 저장, 늦은 결과의 cloud timeout 보존을 자동 시험했다. 인증 만료·DynamoDB 결과 전송 실패·Agent 요약 실패는 장애를 주입한 모의 시험으로 확인했다. 실제 사용자 인증을 만료시키거나 서비스 장애를 일으킨 시험은 아니다.

실환경에서 발견한 문제도 수정했다. DeepSeek 실행 단계는 `toolChoice.any`로 실제 도구 요청을 요구하고, 승인 요청 ID 외 인수를 거부한다. 도구 없이 설명만 반환했던 이전 작업은 SQL을 실행하지 않았다. PHP 기본 30초 제한은 실제 계획 생성에 짧아 `Start.ps1`에서 195초로 조정했다(Agent 180초, HTTP 185초).

## 비용과 남은 범위

기존 계정 전체 실제 집계액 월 **25 USD 초과 자동 차단**, **10 USD 알림**을 유지했다. dry-run은 새 `poc-local-login`, `poc-chatbot`, `poc-worker`, `poc-agent-runtime`, `poc-sql-tool` 역할과 SQL Lambda 동시 실행 0 조치를 포함했다. 실제 차단은 수행하지 않았다. dry-run 당시 집계 0.02 USD는 지연된 값이며 이번 시험의 실시간 비용이나 확정 청구액을 뜻하지 않는다.

집계·감지 지연으로 25 USD 초과 금액이 발생할 수 있고 저장 비용 등이 남을 수 있다. root·서비스 연결 역할 등 제외 범위와 복구는 [비용 차단 가이드](budget_guard/README.md)를 따른다.

벡터 검색, Windows 재부팅 후 무인 실행, 자동 브라우저 인증 갱신, 실제 계정 강제 차단은 이번 완료 범위에 포함하지 않는다. 앱 사용은 [배포·운영 가이드](DEPLOYMENT.md), 로컬 설치는 [local/README.md](../local/README.md)를 참고한다.
