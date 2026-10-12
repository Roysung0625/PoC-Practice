# 계정 월 25 USD 초과 자동 차단

**AWS Budgets의 계정 전체 실제 집계액이 25 USD를 초과하면 자동 차단한다.** 집계 지연에 따른 초과 과금은 사용자가 허용한 조건이다. 25 USD와 정확히 같을 때는 차단하지 않는다.

## 동작

```text
기존 월 25 USD 예산 (계정 전체)
  ├─ 기존 실제 10 USD 초과 알림 유지
  └─ 실제 25 USD 초과 → SNS → 제어 Lambda
                                ↑
                         15분 주기 재점검
                                ↓
       집계액 재조회 → 차단 상태 저장 → IAM 차단 + 실행 중지
```

- 스택·함수: `poc-account-budget-guard`, 도쿄 `ap-northeast-1`.
- CloudFormation 정의: [template.json](template.json), Lambda 소스: [guard.py](guard.py).
- 월 예산 이름: `My Zero-Spend Budget`. SNS 알림은 기존 예산에 배포 스크립트가 추가하며, 예산 자체는 스택 소유가 아니다.
- 메시지에 적힌 임의 금액을 믿지 않고 매번 Budgets 실제 비용을 조회한다. 비용 데이터·권한 오류는 정상으로 처리하지 않는다.
- 초과를 한 번 감지하면 S3 `latch.json`에 상태를 남긴다. 월이 바뀌거나 비용이 낮아져도 자동 재개하지 않는다.
- 각 조치 전 원래 설정을 비공개·암호화·버전 관리 S3 `snapshots/<차단 회차>/`에 저장한다. 같은 회차에서 재시도해도 원래 설정을 덮어쓰지 않는다.
- 한 조치가 실패해도 나머지 조치를 계속한다. 실패는 `latest.json`, Lambda 로그, CloudWatch 오류 경보에 남고 다음 점검에서 재시도한다. 오류 경보는 콘솔 상태용이며 별도 이메일은 설정하지 않았다.

## 차단 범위

| 대상 | 조치 |
| --- | --- |
| 모든 일반 IAM 사용자·역할 | 관리형 정책 `Deny *` 연결. Bedrock, AgentCore 등 추가 API 호출과 권한 변경 거부 |
| EC2 Auto Scaling | 모든 확장·교체 프로세스 일시 중지. 희망 개수를 0으로 바꿔 인스턴스를 종료하지 않음 |
| EC2 | 실행·시작 중인 EBS 기반 인스턴스 중지 |
| RDS | 중지 가능한 DB 인스턴스·클러스터 중지. 상태·엔진·복제 구성상 불가하면 오류 보고 |
| ECS | REPLICA 서비스 희망 개수 0, 실행 태스크 중지. DAEMON 서비스는 별도 검토 오류 보고 |
| Lambda | provisioned concurrency 해제, reserved concurrency 0. 제어 Lambda는 제외 |

제어 Lambda는 활성 리전을 매번 조회한다. 현재 존재하는 IAM 목록을 고정하지 않아 이후 생성된 일반 사용자·역할도 초과 후 점검에 포함된다. 조치는 요청 단계이며 실제 종료·중지는 비동기일 수 있다. ECS autoscaling·서비스 연결 역할 등이 다시 실행을 늘리면 다음 점검에서 다시 중지하므로 그 사이 과금은 남을 수 있다.

## 한계와 비용

- AWS Budgets는 통상 8–12시간 간격으로 갱신되며 알림도 지연될 수 있다. 15분 점검은 과금 집계 자체를 실시간으로 만들지 않는다. [AWS Budgets 공식 설명](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- root, AWS 서비스 연결 역할, 제어 역할은 IAM 차단 대상이 아니다. **프로젝트 앱은 일반 IAM 역할로 실행해야 한다.** 현재 개발자 CLI 로그인은 root이므로 앱 인증으로 재사용하지 않는다. [AWS root 권한](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html)
- 이미 실행 중인 Bedrock 호출·AgentCore 세션·Lambda 호출은 즉시 취소되지 않을 수 있다. AgentCore 세션의 강제 종료는 세션 ID가 필요하며 이 제어 코드에는 포함하지 않았다.
- EBS, RDS 저장소·스냅샷, S3, 공인 IP·로드밸런서·NAT, 지원·구독·약정 비용은 별도다. 이 코드는 데이터 자원을 삭제하지 않는다. 새 서비스에는 중지 처리 추가가 필요할 수 있다. [EC2 상태별 과금](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
- RDS는 장기 중지 후 자동 재시작될 수 있어 차단 상태가 유지되는 동안 반복 점검한다. [RDS 중지 제약](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html)
- 실행 중단은 메모리·임시 디스크·진행 중인 요청을 보존하지 않는다. 영구 DB·볼륨·버킷 삭제 API는 실행하지 않는다.
- 제어용 Lambda, SNS, EventBridge, S3, CloudWatch 로그·경보도 계정 비용에 포함된다. 무료 사용량 적용 여부에 따라 과금되며 무료라고 보장하지 않는다. 평상시 Lambda는 비용과 제어 상태만 조회하고 종료한다.

## 배포·조회

프로젝트 루트 PowerShell에서 실행한다. `$accountId`에는 실제 12자리 계정 ID를 입력한다.

```powershell
$accountId = '실제12자리계정ID'
.\aws\scripts\Deploy-BudgetGuard.ps1 -ExpectedAccountId $accountId
.\aws\scripts\Manage-BudgetGuard.ps1 -Mode Status -ExpectedAccountId $accountId
```

배포는 기존 25 USD 알림에 이미 SNS 구독이 있다면 보존한다. AWS의 알림당 SNS 구독 수 제한에 걸리면 배포가 오류로 끝나며, 기존 구독을 임의로 삭제하지 않는다. 재배포는 일시 중지·차단 복구와 구분한다.

원본 템플릿은 코드 삽입 자리표시자를 가진다. **원본을 직접 배포하지 말고 스크립트를 사용한다.** 실제 생성 템플릿, 스택 출력, 검증 응답은 Git 제외 경로 `.local/budget-control/`에 저장한다.

## 안전한 검증

```powershell
python -m unittest discover -s aws/budget_guard -v
$awsExe = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
$dryRun = Join-Path (Get-Location) '.local\budget-control\dry-run-request.json'
[IO.File]::WriteAllText($dryRun, '{"dry_run":true}')
& $awsExe lambda invoke --profile poc-practice --region ap-northeast-1 `
  --function-name poc-account-budget-guard --payload "fileb://$dryRun" `
  --cli-read-timeout 650 .local/budget-control/dry-run-response.json
Get-Content .local/budget-control/dry-run-response.json
```

`dry_run`은 현재 비용과 관계없이 대상 검색만 하고 상태 저장·권한 차단·실행 중지는 하지 않는다. 응답에 `FunctionError`가 없어야 하며 본문의 `status=dry_run`, `errors=[]`를 확인한다. 테스트하려고 실제 예산을 낮추거나 `latch.json`을 만들면 계정 전체 차단이 실행될 수 있으므로 사용하지 않는다.

## 수동 복구

차단 정책은 일반 관리자 역할의 복구 API도 막는다. root로 로그인해 복구한다. **배포 스택을 삭제하는 것으로 복구를 대신하지 않는다.** 연결된 정책이나 중지된 자원 설정은 별도다.

1. `Manage-BudgetGuard.ps1 -Mode Pause -ExpectedAccountId $accountId` 실행. 제어 상태를 일시 정지하고 스케줄을 비활성화하며 새 Lambda 실행을 막는다. 기존 실행이 끝나도록 **11분 이상** 기다린다.
2. `-Mode Export` 실행. `.local/budget-control/recovery/`에서 `latch.json`, `latest.json`, 해당 회차 `snapshots/`를 확인한다. 어떤 조치가 성공·실패했는지 먼저 판단한다.
3. `-Mode ReleaseIam` 실행. **이 제어기가 만든 차단 정책만** 사용자·역할에서 해제한다. 다른 IAM 정책은 변경하지 않는다. 이때부터 허용된 호출은 다시 과금될 수 있다.
4. 필요한 자원만 수동 복구한다. 아래 표와 각 기록의 `before`를 사용한다.
5. 집계액이 25 USD 이하이고 재개할 준비가 되었을 때 `-Mode Rearm` 실행. 차단 상태를 지우고 함수·15분 점검을 다시 활성화한다. S3 과거 버전·회차 기록은 보존한다. 아직 25 USD 초과이면 재가동을 거부한다.

| 자원 | 복구 기준 |
| --- | --- |
| EC2/RDS | 기록된 인스턴스·클러스터 중 필요한 것만 Start 실행 |
| Auto Scaling | `before.SuspendedProcesses`에 원래 없었던 프로세스만 Resume. 원래 중지된 프로세스는 유지 |
| ECS 서비스 | `before.desiredCount`로 UpdateService. 독립 태스크는 태스크 정의·네트워크를 확인하여 수동 재실행 |
| Lambda | `before.ReservedConcurrentExecutions=null`이면 DeleteFunctionConcurrency, 숫자면 그 수치로 PutFunctionConcurrency. 필요한 provisioned concurrency도 기록된 qualifier·수치로 별도 복구 |

중지·정리할 때는 먼저 위 Pause를 실행하고 필요하면 정책을 해제한다. CloudFormation을 삭제하더라도 복구용 S3는 보존된다. `My Zero-Spend Budget`의 25 USD SNS 구독은 스택 외부 설정이므로 별도로 제거해야 한다. 기존 10 USD 알림과 월 예산을 실수로 삭제하지 않는다.

## 검증 기록

검증 증빙은 [verification-2026-10-12.md](verification-2026-10-12.md)에 기록한다. 로컬 모의 시험, AWS 읽기 전용 검증, 실제 전체 중단은 구분한다.
