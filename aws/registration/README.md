# 상품 등록 AI·S3 규칙 운영

이 구성은 기존 Agent/Lambda/SQS/DynamoDB 스택을 수정하지 않습니다. 로컬 상품 등록 서버가 `poc-registration` 일반 IAM 역할로 DeepSeek V3.2, Titan V2와 S3의 단일 규칙 객체를 사용합니다. 웹은 로컬에서 실행하며 검색은 기존 `127.0.0.1:9200` OpenSearch 3.9.0 클러스터의 별도 `poc-registration-product-v1` 인덱스를 사용합니다.

## 배포 전 확인

`template.json`은 비공개·암호화·버전 관리 S3 버킷, 런타임 역할, 별도 규칙 발행 역할을 생성합니다. 버킷은 스택 삭제 시에도 보존합니다. 런타임은 지정 객체 읽기와 도쿄의 두 모델 호출만 허용하며, 발행 역할도 지정 객체만 읽고 쓸 수 있습니다. 삭제 권한은 없습니다. 기존 예산 차단 역할·정책은 변경하지 않습니다.

최신 승인에 따라 같은 템플릿의 `ExistingLoginProjectAccess`는 이미 존재하는 정확한 IAM 사용자 `poc-local-login`에 프로젝트 한정 인라인 정책을 추가합니다. 이 정책은 **현재 등록 전용 스택 ARN 한 개**에 대한 `cloudformation:DescribeStacks`, `DescribeStackEvents`, `ListStackResources`와 **이 스택의 두 역할 ARN**에 대한 `sts:AssumeRole`만 허용합니다. 다른 스택 조회, CloudFormation 생성·수정·삭제, 사용자/역할 관리, 계정 전체 관리자 권한은 포함하지 않습니다. 이 사용자에게 직접 Bedrock/S3 권한을 추가하지 않고 검증된 역할 전환으로 두 모델 실행과 단일 규칙 객체 발행을 수행합니다. 최초 인프라 배포는 별도 관리 인증으로 실행합니다. 기존에 관측된 등록 스택 `DescribeStacks` 권한 거부는 이 범위 안에서 해소하며, 사용자 이름이 다르면 배포 전에 실제 사용자를 다시 확인해야 합니다.

프로젝트 루트에서 실제 계정과 현재 인증 주체를 확인합니다. 결과의 ARN이 root라면 앱 실행에 사용하지 않습니다. 템플릿의 신뢰 대상은 실제 일반 IAM 사용자 또는 역할 ARN이어야 하며 `arn:aws:sts::...:assumed-role/...` 세션 ARN을 그대로 넣지 않습니다. 배포 권한과 런타임 권한을 구분합니다.

```powershell
aws sts get-caller-identity --profile poc-local-login
aws configure get region --profile poc-local-login
aws cloudformation validate-template --template-body file://aws/registration/template.json --region ap-northeast-1 --profile poc-local-login
```

계정·신뢰 주체를 확인한 관리자가 `TrustedPrincipalArn` 및 `TrustedPublisherPrincipalArn`을 지정하여 별도 스택으로 배포합니다. 두 역할 이름이 이미 존재하면 소유자를 확인하며 기존 역할을 덮어쓰지 않습니다. `CAPABILITY_NAMED_IAM`이 필요합니다. 스택 출력의 버킷과 역할 ARN은 로컬 설정에 기록하며 공개 저장소에는 실제 환경설정이나 인증정보를 게시하지 않습니다.

## 기존 로그인 프로필과 연결

사용자 AWS 설정 파일에서 기존 `poc-local-login`을 source_profile로 참조합니다. 이번 구성에서 원본 주체는 비루트 `poc-local-login` IAM 사용자이며, 런타임 역할과 게시 전용 역할은 동일한 사용자를 신뢰합니다. 원본 인증정보는 하나를 사용하고 assume한 역할·권한·프로필을 분리합니다. 이 사용자는 두 역할을 `sts:AssumeRole`할 권한도 필요합니다. 관리자 배포 프로필은 `poc-practice`입니다. 관리자 인증이 만료되어도 원본 로그인과 런타임 역할의 인증 상태는 따로 확인합니다. 만료된 프로필만 기존 로그인 절차로 갱신하고 액세스 키를 앱 `.env`나 소스에 복사하지 않습니다.

```ini
[profile poc-registration]
role_arn = arn:aws:iam::<ACCOUNT_ID>:role/poc-registration
source_profile = poc-local-login
region = ap-northeast-1

[profile poc-registration-rules-publisher]
role_arn = arn:aws:iam::<ACCOUNT_ID>:role/poc-registration-rules-publisher
source_profile = poc-local-login
region = ap-northeast-1
```

역할 전환의 실제 결과를 확인합니다. 런타임 코드는 계정 번호와 `assumed-role/poc-registration/` ARN을 검증한 뒤에만 세션을 재사용합니다. 인증 실패를 정상 응답으로 대체하지 않습니다.

```powershell
aws sts get-caller-identity --profile poc-registration
aws sts get-caller-identity --profile poc-registration-rules-publisher
```

로컬 앱 환경에 다음을 지정합니다. 등록 모듈은 첫 AWS 요청 전에 `.local/registration.env`를 읽으며 실제 값은 Git에서 제외합니다. 기존 프로세스 환경 변수가 있으면 그 값을 우선합니다. 기존 SQL 앱의 `.local/app.env`는 공통 설정만 제공하며 등록 전용 값은 한 곳에서 관리합니다.

```dotenv
POC_AWS_ACCOUNT_ID=<ACCOUNT_ID>
POC_REGISTRATION_PROFILE=poc-registration
POC_REGISTRATION_RULES_BUCKET=<STACK_RULES_BUCKET>
POC_REGISTRATION_RULES_KEY=rules/product-registration-ja.json
POC_REGISTRATION_OPENSEARCH_URL=http://127.0.0.1:9200
```

다음은 프로젝트 루트에서 실행하는 실제 배포·프로필 설정 예시입니다. 계정과 ARN은 로그인한 현재 주체에서 조회하고 버킷은 배포 출력에서 읽습니다. 비루트 IAM 사용자 `poc-local-login`을 런타임과 발행 역할의 신뢰 주체로 동일하게 사용합니다. 관리 프로필에는 CloudFormation·IAM·S3 배포 권한이 필요하며 새 역할을 assume할 원본 사용자에게도 `sts:AssumeRole` 권한이 필요합니다.

```powershell
$DeploymentProfile = 'poc-practice'
$LoginProfile = 'poc-local-login'
$Region = 'ap-northeast-1'
$StackName = 'poc-registration'
$LoginIdentity = aws sts get-caller-identity --profile $LoginProfile --output json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw '기존 로그인 인증을 먼저 갱신하세요.' }
$AccountId = $LoginIdentity.Account
$DeployIdentity = aws sts get-caller-identity --profile $DeploymentProfile --output json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or $DeployIdentity.Account -ne $AccountId) { throw '배포와 로그인 계정이 다릅니다.' }
if ($LoginIdentity.Arn -notmatch '^arn:aws:iam::[0-9]{12}:user/') { throw '비루트 poc-local-login IAM 사용자가 필요합니다.' }
$RuntimePrincipalArn = $LoginIdentity.Arn
$PublisherPrincipalArn = $RuntimePrincipalArn
aws cloudformation deploy --template-file aws/registration/template.json --stack-name $StackName --capabilities CAPABILITY_NAMED_IAM --parameter-overrides "TrustedPrincipalArn=$RuntimePrincipalArn" "TrustedPublisherPrincipalArn=$PublisherPrincipalArn" --no-fail-on-empty-changeset --region $Region --profile $DeploymentProfile
if ($LASTEXITCODE -ne 0) { throw '스택 배포 실패' }
$Outputs = (aws cloudformation describe-stacks --stack-name $StackName --region $Region --profile $DeploymentProfile --output json | ConvertFrom-Json).Stacks[0].Outputs
if ($LASTEXITCODE -ne 0) { throw '스택 출력 조회 실패' }
$RulesBucket = ($Outputs | Where-Object OutputKey -eq 'RulesBucket').OutputValue
$RuntimeRoleArn = ($Outputs | Where-Object OutputKey -eq 'RuntimeRoleArn').OutputValue
$PublisherRoleArn = ($Outputs | Where-Object OutputKey -eq 'PublisherRoleArn').OutputValue
aws configure set role_arn $RuntimeRoleArn --profile poc-registration
aws configure set source_profile $LoginProfile --profile poc-registration
aws configure set region $Region --profile poc-registration
aws configure set role_arn $PublisherRoleArn --profile poc-registration-rules-publisher
aws configure set source_profile $LoginProfile --profile poc-registration-rules-publisher
aws configure set region $Region --profile poc-registration-rules-publisher
aws sts get-caller-identity --profile poc-registration
if ($LASTEXITCODE -ne 0) { throw '런타임 역할 전환 실패' }
aws sts get-caller-identity --profile poc-registration-rules-publisher
if ($LASTEXITCODE -ne 0) { throw '발행 역할 전환 실패' }
$env:POC_AWS_ACCOUNT_ID = $AccountId
$env:POC_REGISTRATION_RULES_BUCKET = $RulesBucket
```

## 일본어 규칙 발행

`product-registration-ja.json`은 검토 가능한 정본의 소스입니다. 운영 서버는 이 파일을 자동 대체 자료로 사용하지 않고 S3의 최신 객체를 읽습니다. 모든 편집 항목·신규 마스터의 하위 항목·4단계 안내가 포함되어야 합니다. 조건은 `required`, `max_length`, `min_length`, `gw_code`, `min`, `max`, `positive`, `integer`만 허용합니다. 임의 코드·정규식은 실행하지 않습니다. 상품 코드의 고정 정규식은 `^GW-[A-Z0-9]{4,12}$`입니다. 문구와 함께 저장된 조건이 실제 서버 검증에 적용됩니다. DB 고유 제약, 테넌트·활성·참조 무결성 등은 별도로 유지합니다.

아래 명령은 `.venv` Python을 사용하는 예시입니다. 기본 동작은 읽기 전용 검토입니다. 실제 게시에는 `--apply`를 추가합니다. 최초 객체에만 `--initial`을 사용합니다.

```powershell
.venv/Scripts/python.exe aws/registration/publish_rules.py --bucket <BUCKET> --account-id <ACCOUNT_ID> --initial
.venv/Scripts/python.exe aws/registration/publish_rules.py --bucket <BUCKET> --account-id <ACCOUNT_ID> --initial --apply
```

바로 위 배포 예시의 검증된 변수를 유지한 PowerShell 세션에서는 다음 명령을 그대로 실행할 수 있습니다.

```powershell
.venv/Scripts/python.exe aws/registration/publish_rules.py --bucket $RulesBucket --account-id $AccountId --initial
if ($LASTEXITCODE -ne 0) { throw '규칙 검토 실패' }
.venv/Scripts/python.exe aws/registration/publish_rules.py --bucket $RulesBucket --account-id $AccountId --initial --apply
if ($LASTEXITCODE -ne 0) { throw '최초 규칙 발행 실패' }
```

변경 시 JSON의 `version`을 갱신하고 현재 S3 `VersionId`를 확인한 후 `--expected-version <VERSION_ID>`로 검토·발행합니다. 발행기는 버킷 버전 관리와 모든 공개 차단 설정을 확인하고, 최초 `IfNoneMatch` 또는 현재 내용의 ETag `IfMatch` 조건을 사용합니다. 최초 발행은 없는 객체를 HEAD/GET하지 않으므로 `ListBucket` 없이도 가능하며, 읽기 전용 최초 검토는 객체 존재 여부를 단정하지 않습니다. 이미 있으면 조건부 쓰기가 실패합니다. 동시 변경으로 내용이 달라지면 실패합니다. 같은 내용의 동시 재발행은 동일 ETag일 수 있으므로, 승인 서버는 규칙 이름뿐 아니라 S3 VersionId와 SHA256 전체를 묶은 `bundle.version`을 비교합니다. 발행 후 해당 VersionId를 다시 읽어 SHA256을 검증합니다. 이전 판은 삭제하지 않습니다.

## 초기 색인과 요청

초기 전체 동기화는 웹과 outbox worker를 시작하기 전에 별도 CLI에서 `RegistrationIntelligence().sync_index(store)`를 호출합니다. 웹 검색 요청에서 전체 임베딩을 생성하지 않습니다. 동기화가 완료되어 `_meta.ready=true`가 되기 전에는 검색이 `REGISTRATION_INDEX_NOT_READY`로 실패합니다. 일부 색인만으로 정상 검색을 시작하지 않습니다. 동기화가 중간에 실패하면 동일 명령으로 재시도하며, 이미 같은 SHA256인 문서는 임베딩을 다시 생성하지 않습니다. 상품 등록 이후 증분 갱신은 `index_product(row)`를 사용하고, 전체 동기화는 수정·비활성·삭제된 원본도 재반영합니다. 동기화 잠금은 같은 Python 프로세스 안에서만 적용되므로 초기 전체 동기화와 별도 프로세스의 증분 worker를 동시에 실행하지 않습니다.

검색은 일본어 Kuromoji 전문 검색과 실제 Titan V2 1024차원 정규화 벡터 검색을 각각 수행하고 RRF로 결합합니다. 순위는 확률·정확도 점수로 표시하지 않습니다. 마지막에 DB의 현재 유효 후보를 다시 조회하여 비활성·다른 테넌트·허용하지 않은 상품이 오래된 인덱스로부터 노출되지 않게 합니다. 최대 10건이며 실제 이름·용도 문자열 일치와 입수·무게의 입력/후보 값을 일본어 이유로 반환합니다.

## 실패·재시도와 비용

앱의 일반 IAM 역할은 기존 월 25 USD 실제 집계 비용 초과 차단 대상입니다. 집계 지연에 따른 초과와 S3 저장 비용은 남을 수 있습니다. 정확한 청구 상한은 아닙니다. 초기 임베딩은 상품별 호출과 질의별 호출을 발생시키며 신규 유료 AWS 검색 서비스를 만들지 않습니다. 인증·S3·모델·검색 실패는 명시적 오류로 반환하며 다른 모델, 가짜 결과, 로컬 규칙으로 대체하지 않습니다. 모델 호출 자동 재시도는 비활성화되어 있습니다. 로그인 갱신이나 서비스 복구 후 사용자가 요청을 다시 실행합니다.

서비스 시작·중지·상태 확인 및 outbox 재시도 명령은 [상품 등록 운영 안내](../../docs/product-registration/README.md)를 따릅니다. 본 모듈은 별도 상주 프로세스를 시작하지 않습니다. 인증정보·상품 원문·모델 응답을 로그에 자동 기록하지 않습니다. 템플릿 검증·오프라인 테스트와 실제 배포·모델 왕복은 [검증 기록](../../docs/product-registration/verification.md)에서 구분합니다.
