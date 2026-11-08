# AWS·Windows SQL 전달

[전체 일람](../index.md)

분류 근거: CFN + Lambda/수신기 item 계약. 물리적 연결과 업무 의미의 확정은 구분합니다.

| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |
|---|---|---|---|---|---|---|---|---|
| AWS DynamoDB ap-northeast-1 | 해당 없음(KV) | poc-practice-app-Results-DEFYQ79N6FC | SQL 요청·결과 전달 저장소 (사전: CloudFormation logical ID: Results) | 해당 없음(신규 운영 문서) | AWS·Windows SQL 전달 | request_id별 요청 상태와 결과 JSON을 연결하여 같은 Lambda 호출에서 결과 반환 | [문서](../dynamodb/results.md) | 기존 배포 스냅샷·코드 근거 / 최신 describe 확인 필요 | <!-- table-id: dynamodb:ap-northeast-1:poc-practice-app-Results-DEFYQ79N6FC -->
