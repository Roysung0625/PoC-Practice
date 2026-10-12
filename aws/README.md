# AWS 구축·연결 가이드

이 폴더는 PoC-Practice의 AWS 구축 코드, 배포 스크립트, CLI 연결 안내를 관리합니다.
전체 프로젝트 개요는 [루트 README](../README.md), 공통 작업 지침은 [AGENTS.md](../AGENTS.md)를 따릅니다.
`AgentCore + Bedrock + Lambda SQL Tool + SQS + DynamoDB + Windows 로컬 수신 프로그램` 구성을 기준으로 합니다.
AWS CLI로 부트스트랩과 애플리케이션 스택을 배포했습니다. 전용 IAM 로그인, AgentCore·DeepSeek·Lambda·SQS·DynamoDB와 Windows PostgreSQL의 실제 연결을 확인했습니다. 배포·실행 방법은 [운영 가이드](DEPLOYMENT.md), 시험별 증거와 한계는 [검증 기록](verification-2026-10-12.md)을 확인하세요.

## 폴더 구성

```text
aws/
├── README.md                # AWS 구축·연결 안내
├── config/
│   ├── models.json          # 생성·임베딩 모델 기본값
│   └── budget-policy.json  # 계정 전체 예산 요구와 적용 상태
├── costs/                   # Calculator 비용 가정·결과와 화면 증빙
├── budget_guard/            # 비용 차단 Lambda, CloudFormation, 시험·복구 안내
├── infra/                   # 비공개 아티팩트·IAM 부트스트랩과 앱 CloudFormation
├── runtime/                 # Agent HTTP 런타임·SQL Lambda·승인 계약
├── tests/                   # 승인·전달·실패 처리 시험
├── plans/                   # AWS 작업 계획
└── scripts/
    ├── Connect-Aws.ps1      # 프로필 설정, 브라우저 로그인, 연결 확인
    ├── Deploy-BudgetGuard.ps1 # 비용 차단 배포·예산 알림 연결
    └── Manage-BudgetGuard.ps1 # 상태 조회·일시 정지·수동 복구
```

AWS 인프라 정의, Lambda SQL Tool, Agent 배포 코드는 이 폴더에서 관리합니다.
사용자 홈의 `.aws` 설정과 인증 캐시는 기존 위치에서 관리하며 프로젝트에 복사하지 않습니다.

## 적용 모델

공통 기본값은 [config/models.json](config/models.json)에서 관리합니다.

| 용도 | 모델 | 모델 ID | 기본 설정 |
| --- | --- | --- | --- |
| 질문 해석·SQL 생성·결과 설명 | DeepSeek V3.2 | `deepseek.v3.2` | 도쿄, 온디맨드 |
| 텍스트 임베딩 | Amazon Titan Text Embeddings V2 | `amazon.titan-embed-text-v2:0` | 도쿄, 온디맨드, 1,024차원, `normalize=true` |

2026-10-12에 `poc-practice` 프로필로 두 모델의 `GetFoundationModel`을 조회해 도쿄 리전의 `ACTIVE` 상태와 `ON_DEMAND` 지원을 확인했습니다.
같은 날 실제 DeepSeek 추론·native tool_use·SQL 결과 설명과 Titan 임베딩 1,024차원·정규화를 추가 검증했습니다. 모델을 자동 대체하지 않습니다.

Amazon Titan Embeddings는 Text Embeddings V2를 기본으로 선택했습니다. Titan 호출은 텍스트를 벡터로 변환하며, 벡터 저장과 유사도 검색 기능은 별도 구현 대상입니다.
앱은 공통 모델 설정을 읽습니다. 벡터 저장·검색 인덱스와 검색 품질 검증은 이번 범위에서 제외했습니다.

## 구축 흐름과 Windows 연결 계획

사용자 요청 흐름은 다음과 같습니다. Agent는 앞선 설계의 AgentCore + Bedrock을 기준으로 합니다.

```text
Windows 로컬 챗봇 -> AWS Agent -> Lambda SQL Tool -> Windows 로컬 SQL 실행
Windows 로컬 SQL 결과 -> Lambda Tool 응답 -> Agent -> Windows 로컬 챗봇
```

Lambda Tool이 로컬 SQL 실행 결과를 받아 Agent에 반환합니다. Agent는 SQL 도구를 호출하고 그 결과로 답변을 만듭니다.
결과 조회는 Lambda가 담당하며, Agent는 Lambda의 도구 응답으로 결과를 받습니다.

Windows와 AWS의 연결은 다음 두 경로로 구축합니다.

1. **로컬 챗봇 -> AWS Agent:** 로컬 Python 백엔드가 AWS SDK와 임시 인증으로 AgentCore를 호출하고 응답을 챗봇 화면에 전달합니다. AWS 인증정보는 브라우저에 전달하지 않습니다.
2. **Lambda Tool <-> 로컬 SQL:** Lambda가 SQS에 요청을 넣으면 Windows 수신 프로그램이 HTTPS long polling으로 받아 로컬 FastAPI와 PostgreSQL을 호출합니다. 수신 프로그램은 DynamoDB에 결과를 기록하고 Lambda가 이를 읽어 같은 도구 호출의 응답으로 반환합니다.

SQS/DynamoDB는 Lambda와 Windows 사이의 요청과 결과를 전달하는 내부 구성입니다.
이 방식은 Lambda가 로컬 IP로 직접 HTTP 접속하는 네트워크 터널이 아닙니다. Windows에서 AWS로 HTTPS 연결을 시작합니다.

Windows에는 Python 가상환경, 로컬 PostgreSQL, FastAPI, 작업 수신 프로그램, 챗봇을 구성합니다.
PowerShell 시작·중지·상태 확인 스크립트, 프로젝트 로그, 연결 점검, 네트워크 복구 후 재접속을 포함합니다.
기존 설치와 기존 DB/API의 위치를 확인한 후 실제 설치·연결 대상을 정합니다.
초기 PoC는 사용자가 로그인한 Windows 세션에서 실행하며, 재부팅 후 무인 실행용 인증은 별도 단계로 구분합니다.

SQL 실행 시간, 작업 만료 시간, Lambda의 결과 대기 시간, Agent의 도구 호출 시간 제한을 함께 설정합니다.
제한 시간 안에 결과가 없으면 Lambda가 오류 상태를 반환하고, Agent가 성공한 조회처럼 답변하지 않도록 합니다.
Lambda의 결과 대기 시간도 실행 과금에 반영합니다. [2026-10-12 Calculator 견적](costs/estimate-2026-10-12.md)의 **월 2.21 USD는 이전 Nova Lite 구성의 기록**입니다. 현재 DeepSeek V3.2 + Titan Text Embeddings V2 구성에는 적용하지 않습니다. 생성 토큰, 최초 임베딩·재색인·질의 임베딩 사용량을 포함해 새 비용을 산정해야 합니다.

## 계정 전체 비용 제한

사용자는 **AWS 계정 전체의 실제 집계 비용이 월 25 USD를 초과하면 자동 차단하고, 감지 지연에 따른 초과 과금은 허용**하는 방식을 선택했습니다. 요구와 적용 상태는 [budget-policy.json](config/budget-policy.json), 실행 코드·운영 절차는 [budget_guard](budget_guard/README.md)에서 관리합니다.

2026-10-12에 실제 AWS 설정을 변경·조회한 결과입니다.

| 항목 | 상태 |
| --- | --- |
| 기존 예산 이름 | `My Zero-Spend Budget` |
| 적용 범위 | 계정 전체, 서비스·리전 필터 없음 |
| 월 비용 예산 | 50 USD에서 **25 USD**로 변경 |
| 비용 산정 옵션 | 세금·지원·구독 포함, 크레딧·환불 제외 등 기존 옵션 유지 |
| 기존 알림 | 실제 반영 비용 **10 USD 초과** 알림 유지 |
| 자동 차단 | **Budgets → SNS → Lambda 배포 완료**, 15분 주기 재점검 |
| 차단 주체·실행 | 일반 IAM 사용자·역할의 전체 API 거부, 활성 리전의 지원 실행 자원 중단 |
| 다음 달 재개 | 자동 재개 안 함, 기록을 확인한 후 수동 복구 |
| 확인 당시 예산 집계 | 실제 반영 비용 0.02 USD. 실시간 청구액이나 확정 청구액을 뜻하지 않음 |
| 조직 상태 | AWS Organizations에 속하지 않은 독립 계정 |
| 청구액 절대 상한 | 보장하지 않음. 사용자가 감지 지연과 초과 가능성을 허용 |

AWS Budgets는 과금 정보가 지연 반영되므로 알림이나 Budget Actions만으로 실제 청구액이 정확히 25 USD 이하라고 보장할 수 없습니다. [AWS Budgets 설명](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
IAM 정책으로 root를 제한할 수 없고, EC2 등을 중지해도 저장 비용이 계속 발생할 수 있습니다. [AWS 인증·권한](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html), [EC2 상태별 과금](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)

초과 시 EC2 Auto Scaling 프로세스 중지, EC2·RDS 중지, ECS 실행 축소·태스크 중지, Lambda 동시 실행 0을 적용합니다. 제어 역할과 AWS 서비스 연결 역할은 IAM 차단에서 제외하며 root도 제한할 수 없습니다. **애플리케이션에는 일반 IAM 역할을 사용해야 합니다.** 중단 전에 복구 설정을 S3에 저장하며 영구 데이터를 삭제하지 않습니다.

현재 집계액은 임계값 미만이어서 기존 사용자·역할에는 차단 정책을 연결하지 않았습니다. AWS 읽기 전용 dry-run과 IAM 정책 시뮬레이션으로 검증했으며, 실제 계정 전체 강제 중단은 시험하지 않았습니다. [검증 기록](budget_guard/verification-2026-10-12.md)

변경 전 설정과 실제 변경 요청은 Git 제외 대상인 `.local/budget-control/`에 보관했습니다. 계정 예산의 실제 값과 자동 중단 유무는 AWS 조회 결과를 기준으로 확인해야 합니다.

## 연결 설정

| 항목 | 설정 |
| --- | --- |
| CLI | AWS CLI v2, `aws login`을 지원하는 2.32.0 이상 |
| 인증 | AWS 웹 콘솔 계정으로 브라우저 로그인 |
| 배포·복구 프로필 | `poc-practice` |
| 전용 로그인·앱 프로필 | `poc-local-login` → `poc-chatbot` / `poc-worker` |
| 리전 | 도쿄 `ap-northeast-1` |
| 출력 | JSON |
| 설정 파일 | 기본값 `%USERPROFILE%\.aws\config` |
| 임시 인증 캐시 | 기본값 `%USERPROFILE%\.aws\login\cache` |

Access Key와 Secret Key를 입력하거나 저장소에 넣을 필요가 없습니다.
브라우저에서 로그인과 MFA를 직접 완료합니다.
IAM 사용자나 역할로 로그인한다면 해당 주체에 AWS 관리형 정책 `SignInLocalDevelopmentAccess`가 필요합니다.
이 정책은 CLI 로그인용이며 SQS, DynamoDB 등 리소스 생성 권한을 대신하지 않습니다.

## 사용 순서

프로젝트 폴더에서 PowerShell로 실행합니다.

```powershell
Set-Location 'D:\Projects\PoC-Practice'

# 프로필 설정 -> 브라우저 로그인 -> STS 계정 확인
.\aws\scripts\Connect-Aws.ps1

# 이후 인증 상태만 확인: 설정 변경이나 리소스 생성 없음
.\aws\scripts\Connect-Aws.ps1 -Mode Check
```

스크립트는 현재 사용자 설치 경로도 확인하므로, 설치 직후 기존 터미널의 PATH가 갱신되지 않았어도 사용할 수 있습니다.
`aws`를 직접 실행하려면 새 PowerShell 창을 열거나 아래 실행 파일 경로를 사용합니다.

```powershell
$awsExe = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
& $awsExe sts get-caller-identity --profile poc-practice --region ap-northeast-1 --no-cli-pager
```

로그인 전 설정만 만들거나, 이후 예상 계정을 확인하는 명령입니다.

```powershell
.\aws\scripts\Connect-Aws.ps1 -Mode Configure
.\aws\scripts\Connect-Aws.ps1 -Mode Check -ExpectedAccountId 123456789012
```

`123456789012`는 예시이므로 실제 계정 ID로 바꿉니다. 실제 계정 ID를 스크립트에 저장하지 않습니다.
`-Mode Check`는 STS 응답의 계정과 ARN을 표시합니다. 연결 성공은 실제 STS 응답으로 확인하며, 서비스별 배포 권한까지 검증한 것은 아닙니다.

## 다른 PC에서 CLI 설치

[AWS 공식 현재 사용자용 MSI](https://awscli.amazonaws.com/AWSCLIV2-User.msi)를 설치한 뒤 위 연결 스크립트를 실행합니다.
Windows 현재 사용자용 설치는 관리자 권한 없이 사용할 수 있습니다.
이 프로젝트에서는 설치 파일의 Authenticode 서명이 유효하고 게시자가 `Amazon Web Services, Inc.`인지 확인합니다.

## 로그인 문제 해결

- 브라우저가 열리지 않으면 `aws login`이 출력한 링크를 같은 PC의 브라우저에서 엽니다.
- IAM 사용자나 역할의 로그인 권한 오류는 `SignInLocalDevelopmentAccess` 부여 여부를 콘솔에서 확인합니다.
- 세션이 만료되면 연결 스크립트를 다시 실행합니다. CLI가 자동 갱신하는 로그인 세션은 최대 12시간입니다.
- PowerShell이 스크립트 실행을 차단하면 해당 PC의 실행 정책을 확인합니다. 직접 CLI 명령을 실행할 수도 있습니다.

```powershell
$awsExe = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
& $awsExe configure set region ap-northeast-1 --profile poc-practice
& $awsExe configure set output json --profile poc-practice
& $awsExe login --profile poc-practice --region ap-northeast-1
& $awsExe sts get-caller-identity --profile poc-practice --region ap-northeast-1 --no-cli-pager
```

## 구축 단계에서 이어서 할 일

1. Windows Python·PostgreSQL·FastAPI 실행환경과 로컬 조회 확인.
2. SQS 작업 큐·DLQ, DynamoDB 결과 테이블, Lambda SQL Tool과 실행 역할을 IaC로 정의.
3. 로컬 수신 프로그램의 임시 인증과 대상 큐 수신·메시지 삭제·결과 저장 권한 구성.
4. Lambda Tool 호출 -> Windows의 실제 SQL 실행 -> 같은 Lambda 호출의 결과 반환을 검증.
5. Agent의 Lambda 도구 등록과 로컬 챗봇의 Agent 호출을 연결.
6. PC 중지·인증 만료·통신 단절·요청 중복·시간 초과를 검증하고 실행·복구·정리 절차를 제공.

이 스크립트는 AWS 리소스를 생성하지 않습니다. 로컬 수신 프로그램의 상시 실행용 인증은 개발자용 브라우저 로그인과 별도로 설계해야 합니다.
원문에 적힌 비용은 이전 설계 추정치이며, 실제 구축 시 현재 요금과 사용량으로 다시 확인합니다.

## 공식 문서

- [Windows AWS CLI 설치](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [콘솔 계정을 이용한 CLI 로그인](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html)
- [aws login 명령](https://docs.aws.amazon.com/cli/latest/reference/login/)
- [STS get-caller-identity](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html)
- [DeepSeek V3.2](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-deepseek-deepseek-v3-2.html)
- [Amazon Titan Text Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
- [Titan 임베딩 차원과 정규화](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-embed-text.html)
