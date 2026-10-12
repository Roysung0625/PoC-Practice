# 2026-10-12 검증 기록

## 실제 AWS 설정

- CloudFormation `poc-account-budget-guard`: `UPDATE_COMPLETE`.
- CloudFormation에 저장된 Lambda 소스와 로컬 `guard.py` 내용 일치 확인.
- 월 25 USD / 계정 전체 예산 유지. 실제 비용 10 USD 초과 알림 보존.
- ACTUAL / GREATER_THAN / ABSOLUTE_VALUE / 25 SNS 알림과 Lambda 구독 생성·조회 확인.
- EventBridge `rate(15 minutes)` 활성화, 오류 경보 `OK`.
- 당시 집계액 0.02 USD. 실시간 또는 확정 청구액은 아니다.
- 차단 정책이 연결된 사용자·역할·그룹은 0개. `latch.json`, `pause.json` 없음.
- 관리 스크립트 `-Mode Status` 실제 실행 성공.

## 검증한 동작

- 로컬 Python unittest **19개 통과**: 25 USD 경계, 잘못된 금액, dry-run 비변경, 차단 유지, 비용 조회 실패 시 기존 차단 유지, 개별 실패 후 계속 처리, 원래 설정 보존, 회차 분리, 복구 일시 정지, 보호 역할 제외, EC2/RDS/ASG 처리.
- PowerShell 스크립트 3개의 구문 분석 통과.
- 실제 Lambda `dry_run=true`: 함수 오류 없이 성공, `errors=[]`. 활성 17개 리전 조회 완료.
- 초과 시 차단 대상: 현재 일반 IAM 사용자 1개·역할 3개. 제어 역할·서비스 연결 역할은 대상에서 제외.
- 배포 전 17개 리전에서 조회한 EC2, RDS 인스턴스·클러스터, Lambda, ECS 클러스터, Auto Scaling 그룹은 비어 있었다. 모든 AWS 서비스·저장소가 없다는 뜻은 아니다.
- IAM 시뮬레이션: Bedrock 일반·스트리밍, AgentCore 호출, EC2 생성, SQS 전송, IAM 차단 정책 해제 작업 모두 `explicitDeny`.
- 제어 역할 시뮬레이션: 일반 역할에 지정한 차단 정책 연결 `allowed`; 제어 역할·서비스 연결 역할에 연결 `explicitDeny`.
- SNS 검증 메시지 전송 후 Lambda 실행 로그에서 `below_limit`, `applied=[]`, `errors=[]` 확인. Lambda 요청 ID `b472b425-6600-4d1b-9eb0-cb917264b6de`, 2026-10-12 07:50 UTC.

## 검증하지 않은 동작

실제 계정 비용을 25 USD 넘게 만들거나 예산을 낮추는 시험, 실제 계정 전체 IAM 차단·자원 중지, 실제 차단 후 복구는 실행하지 않았다. 초과 분기는 로컬 모의 시험, 권한은 IAM 시뮬레이션으로 확인했다. AWS 청구 반영과 Budgets 초과 알림 자체의 실시간 종단 시험은 수행하지 않았다.

원본 AWS 응답과 생성 템플릿은 `.local/budget-control/`에 저장하며 버전 관리 대상에서 제외한다. 이후 운영 상태는 저장 문서가 아니라 실제 AWS 조회를 기준으로 판단한다.
