# AWS 배포·SQL 왕복 진행 기록

승인된 계획: 도쿄 AgentCore/DeepSeek → Lambda → SQS → Windows SQL API/PostgreSQL → DynamoDB → 동일 Lambda → Agent → 챗봇. Titan은 호출 검증만, 기존 비용 차단 유지. PoC 전용 브라우저 로그인과 앱/수신기 역할 사용.

- [x] 공유 계약·승인·outbox·결과 상태 보완 및 테스트
- [x] Bootstrap S3·로그인 사용자 배포, 사용자 브라우저 로그인
- [x] SQL Lambda·큐·결과 테이블·AgentCore·역할 배포
- [x] 모델·Titan·Lambda 실제 SQL 왕복 검증
- [x] 챗봇 Agent 계획/승인/실행/설명·표·그래프 검증
- [x] 실패 시나리오·비용 차단 대상 검증·운영 문서

실제 챗봇 요청 `974faf92-e532-4430-a032-bb5b03e9d176`의 12행과 PostgreSQL 기준값이 일치하며 SQL·전달·Agent 설명 모두 성공했다. 수신기 중지 실험은 `LOCAL_RESULT_TIMEOUT`을 확인했고 수신기를 재시작했다. 인증 만료·전송 실패·요약 실패 등 주입 시험과 실환경 시험의 구분은 [검증 기록](../verification-2026-10-12.md)을 따른다. 운영 절차는 [DEPLOYMENT.md](../DEPLOYMENT.md)에 있다.

현재 폴더는 Git 저장소가 아니며 로컬 앱 코드가 함께 추가되고 있다. 변경 전 최신 파일을 확인하고 AWS 전용 파일을 먼저 구현한다. 별도 스킬·구현 서브에이전트를 자동 호출하지 않는다.
