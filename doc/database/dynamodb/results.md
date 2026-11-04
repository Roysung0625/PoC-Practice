# SQL 요청·결과 전달 — DynamoDB Results

<!-- table-id: dynamodb:ap-northeast-1:poc-practice-app-Results-DEFYQ79N6FC -->

[전체 일람](../index.md) · [운영 저장소](../operational-stores.md)

물리명: `poc-practice-app-Results-DEFYQ79N6FC`. 리전: `ap-northeast-1`. 관계형 DB의 schema는 없습니다. CloudFormation 논리 ID는 `Results`이며 한국어 이름은 소스 흐름을 설명한 추론명입니다.

근거는 기존 배포 스냅샷(스택 갱신 2026-11-03T14:02:44.860000+00:00)과 현재 소스입니다. 이번 작업에서는 AWS API·DescribeTable·업무 item 조회를 수행하지 않았습니다. 따라서 실제 현재 테이블 존재·TTL 활성 상태·배포 후 변경은 확인 필요입니다.

[CloudFormation](../../../aws/infra/application.json) · [Lambda item 생성·대기](../../../aws/runtime/sql_tool.py) · [Windows 수신기](../../../local/python/poc/receiver.py) · [정제한 근거](../metadata-evidence.json)

## 물리 키와 저장소 정의

- Partition key: `request_id` (`S`), sort key 없음. 정의된 보조 인덱스 없음.
- CFN 정의: PAY_PER_REQUEST, 서버 측 암호화, TTL 속성 `cleanup_at`.
- `AttributeDefinitions`는 키 속성 정의입니다. 아래 item 계약을 고정 SQL 컬럼 목록으로 해석하지 않습니다. PK 외 속성은 요청 상태에 따라 없을 수 있고 SQL의 NULL/default/unique/FK 제약이 적용되지 않습니다.

## 소스의 item 계약

한 item은 승인 SQL 요청 한 건의 전달 상태입니다. Lambda가 등록→SQS 전송→Windows lease 획득·로컬 SQL→결과 기록→같은 Lambda 호출의 응답 순서로 사용합니다.

| 속성 | 소스 타입 | 의미·생성 조건 |
|---|---|---|
| `request_id` | S | 물리 PK, 요청 등록 시 필수 |
| `approval_id` | S | 승인 ID, 등록 시 필수 |
| `plan_digest` | S | 봉인 계획 digest, 등록 시 필수 |
| `contract_json` | S(JSON) | 요청 envelope; 같은 ID의 다른 계약 거부 |
| `status` | S | QUEUED/RUNNING/SUCCEEDED/FAILED/EXPIRED/TIMED_OUT |
| `expires_at` | N | 실행·도구 대기의 기한 |
| `cleanup_at` | N | 등록 시각+86400초의 정리용 TTL; 실행 기한과 별개 |
| `enqueued_at` | N | SQS 전송 후 설정; 최초에는 없음 |
| `worker_token` | S | 수신기가 lease를 잡을 때 설정 |
| `lease_until` | N | 수신기 lease 만료 Unix 시각 |
| `result_json` | S(JSON) | 정상·실패·만료·시간 초과 결과; 등록 때는 없음 |

## 조건·논리 연결·보존

`attribute_not_exists(request_id)`로 중복 등록을 제어하고 기존 contract_json을 비교합니다. 수신기는 approval_id·plan_digest·상태·lease 조건을 만족해야 갱신하며, 결과 갱신에는 worker_token을 검사합니다. 실패 상태를 빈 정상 결과로 취급하지 않습니다.

`request_id`는 SQS envelope 및 SQLite jobs/outbox와 논리 연결됩니다. 물리 FK와 삭제/갱신 전파는 없습니다. Lambda가 일관된 읽기로 대기하며 Agent가 직접 폴링하지 않습니다. TTL은 로컬 승인·결과 원장 보존을 대신하지 않습니다. 임의 item 삭제·조회 결과 공개는 이번 문서 작업에 포함되지 않습니다.
