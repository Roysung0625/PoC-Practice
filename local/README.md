# Windows 로컬 분석 앱

새 Mac에는 [Mac 최초 설치 지침서](../docs/MACOS_SETUP.md)를 사용하세요. 현재 GardenWorld DB 복원, Mac용 런타임, AWS 인증·SQS 일괄 설정, 실행·재접속·검증 절차를 설명합니다.

> **현재 기본 데이터(2026-10-12): iDempiere 13 GardenWorld.** 912개 테이블·161개 뷰를 별도 `poc_idempiere` DB에 설치하고 챗봇을 전환했다. [설치·사용·복구 안내](IDEMPIERE_GUIDE.md) · [전체 테이블 목록](IDEMPIERE_TABLES.md). 아래 TPC-H 항목은 보존한 이전 데이터셋의 설명이다.

Vue + Laravel + Python(FastAPI) + PostgreSQL로 구성했습니다. **질문 → 계획 검토 → 사용자 승인 → 실제 PostgreSQL 조회 → 표·그래프** 흐름을 사용합니다. 고정 샘플은 AI가 생성한 응답이 아니며 화면에 출처를 표시합니다. 그래프는 계획에 포함된 경우 표시합니다.

## 실행

프로젝트 루트의 **PowerShell 7**에서 실행합니다. 설치·운영 스크립트는 PowerShell 7에서 검증했으며, 다른 작업 폴더에서도 전체 경로로 실행할 수 있습니다.

```powershell
cd D:\Projects\PoC-Practice
.\local\scripts\Start.ps1
.\local\scripts\Status.ps1
.\local\scripts\Check.ps1
# 앱 종료: 프로젝트가 기록한 PID·시작 시각·실행 경로가 모두 일치하는 프로세스만 종료
.\local\scripts\Stop.ps1
```

앱 주소: **http://127.0.0.1:8000**. `고정 샘플 계획 열기`를 누르고 정의·가정·SQL을 검토한 뒤 승인합니다. 현재 샘플은 GardenWorld의 월별·통화별 확정 판매 청구액입니다. DB 및 SQL API는 127.0.0.1:5432/8001, 웹은 127.0.0.1:8000으로 제한합니다.

PostgreSQL은 `poc-postgresql-18` Windows 서비스입니다. 앱 중지는 이 DB 서비스를 유지합니다. DB 서비스를 수동으로 중지했다면 관리자 PowerShell에서 `Start-Service poc-postgresql-18`로 복구한 뒤 연결을 점검합니다. 방화벽 인바운드 개방은 필요하지 않습니다.

다른 작업이 같은 프로젝트의 API를 이미 실행 중이라면 그 프로세스를 중지하거나 소유권을 가져오지 않습니다. 이 경우 `Start.ps1 -Components web`으로 웹만 시작할 수 있습니다. 시작 스크립트가 관리하지 않는 프로세스는 Stop으로 종료하지 않습니다.

## 설치와 재구성

설치한 런타임: Python 3.13.15 사용자 설치, PostgreSQL 18.6 Windows 서비스, PHP 8.4.25, Node 24.20.0. 기존 Python 3.8/Node 20은 보존합니다. PHP와 Node는 `.local/runtime`, Python 의존성은 루트 `.venv`에 있습니다. 시스템 PATH를 바꾸지 않습니다.

새 환경에서 Python 3.13 사용자 설치가 없다면 먼저 실행합니다.

```powershell
winget install --id Python.Python.3.13 --exact --scope user --silent --accept-package-agreements --accept-source-agreements --override '/quiet InstallAllUsers=0 PrependPath=0 Include_launcher=0 Include_test=0'
.\local\scripts\Setup.ps1 -InstallRuntimes
```

PostgreSQL 설치·로컬 수신 설정 적용에는 Windows 관리자 승격이 필요합니다. 이미 다른 PostgreSQL이 5432 포트를 사용하거나 PostgreSQL 18 폴더를 소유한다면 기존 설치를 덮어쓰지 말고 구성 대상을 분리해야 합니다.

이미 설치된 환경에서는 `Setup.ps1`로 잠금 파일의 의존성, 웹 빌드, 마이그레이션, 데이터 행 수를 다시 점검합니다. 적재한 스케일과 다른 데이터는 자동 덮어쓰지 않습니다. SF1 생성·적재에는 수 분과 수 GB의 디스크 공간이 필요합니다. 설치 파일과 중간 CSV/DuckDB는 `.local/downloads`, `.local/data`에 남습니다.

## 데이터와 지표

각 테이블의 역할, 전체 컬럼, 연결 관계와 SQL 예제는 [연습용 데이터베이스 테이블 설명서](DATABASE_GUIDE.md)를 참고하세요.

| 테이블 | SF1 행 수 |
|---|---:|
| region | 5 |
| nation | 25 |
| supplier | 10,000 |
| customer | 150,000 |
| part | 200,000 |
| partsupp | 800,000 |
| orders | 1,500,000 |
| lineitem | 6,001,215 |

생성 manifest와 적재 행 수를 대조합니다. PK/FK, 조회 인덱스, ANALYZE를 적용했습니다. `.local/catalog.json`에는 테이블·열·관계·날짜 범위·제품군·누락 지표 정보가 있습니다. 테스트용 SF0.01 데이터는 무작위 이름의 별도 DB에서 검증 후 정리합니다. SF0.001은 생성 특성상 공급원가 복합 키가 중복될 수 있어 관계 제약을 포함한 적재 시험에 사용하지 않습니다.

샘플은 할인 후 매출, 공급원가 차감액, 고유 공급업체 수를 보여줍니다. 판매관리비·세금·금융비용이 없어 **실제 순이익을 계산할 수 없습니다**. 공급업체 수는 실제 판매자 계정 수와 다르고 월별 수를 합산하면 중복됩니다. 원본 Decimal 값은 문자열로 보존하고 그래프에서만 숫자로 변환합니다. TPC-H의 금액을 원화로 가정하지 않습니다.

## 승인·작업·오류

- Laravel SQLite는 대화·계획 revision·승인·조회 이력을 보관합니다. Python SQLite는 승인 사본·작업·중복 방지·전송 outbox를 보관합니다.
- SQL·바인딩 값·조건·가정·스키마 버전을 포함한 계획 해시가 승인 이후 달라지면 실행을 거부합니다. 자연어 수정이나 SQL 오류 수정은 새 계획을 검토하고 재승인합니다.
- 한 계획에 한 SELECT만 허용합니다. SQLGlot AST 검사와 DB 읽기 전용 계정을 함께 사용합니다. 시스템 객체·임의 함수·변경 CTE·다중 SQL·잠금·SELECT INTO는 거부합니다.
- SQL 최대 20초, 반환 최대 500행/256KiB, DB 동시 실행 2개입니다. 500행 초과는 잘림을 표시하며 크기 초과는 명시적 실패입니다. 빈 결과와 실패를 구분합니다.
- 요청 만료는 승인 직후부터 60초입니다. 재시작 당시 실행 중이던 작업은 `OUTCOME_UNKNOWN`으로 처리하고 SQL을 자동 재실행하지 않습니다. `새 분석`에서 새 계획을 검토하세요.
- 전송 실패는 저장된 결과만 재전송합니다. SQL 성공, AWS 전달, Agent 설명의 상태는 분리합니다. 동일 요청의 반복 승인·수신으로 SQL을 다시 실행하지 않습니다.

| 오류 | 조치 |
|---|---|
| DB_UNAVAILABLE | PostgreSQL 서비스와 5432 로컬 수신 확인 |
| LOCAL_API_UNAVAILABLE | Start/Status/로그 확인, 기존 요청 상태부터 확인 |
| SQL_TIMEOUT / RESULT_TOO_LARGE | 기간·제품군·집계 범위를 줄인 새 계획 검토 |
| REQUEST_EXPIRED | PC/수신기 연결을 복구한 뒤 새 계획 승인 |
| PLAN_MISMATCH / PLAN_SUPERSEDED | 최신 계획을 다시 검토 |
| AWS_NOT_CONFIGURED | AWS 연결 전에는 고정 샘플 사용 |
| AWS_ROOT_FORBIDDEN / AWS_ROLE_MISMATCH | 지정된 일반 IAM 역할 프로필 사용 |
| AWS_AUTH_ERROR | AWS 가이드에 따라 해당 역할 프로필 인증 갱신 |
| COST_POLICY_BLOCKED | 공통 비용 정책 확인. 앱에서 정책을 임의로 해제하지 않음 |

로그는 `.local/logs`와 `local/web/storage/logs/laravel.log`, 실행 식별 기록은 `.local/services.json`입니다. 강제 종료 후에는 `Stop.ps1` → `Start.ps1` → `Check.ps1` 순으로 복구합니다. 로그에 DB DSN·토큰을 출력하지 않습니다. Python API는 서버 전용 Bearer 토큰, Laravel은 세션/CSRF/로컬 Host 검사를 사용합니다.

## AWS 연결 경계

일반 흐름은 **Windows → AgentCore/Bedrock → Lambda → SQS → Windows 수신기 → FastAPI/PostgreSQL → DynamoDB → 동일 Lambda 호출 응답 → Agent → Windows**입니다. Agent가 DynamoDB를 직접 폴링하지 않습니다.

로컬 구성 시험과 별도로 2026-10-12 AWS 배포·실연결 시험을 완료했습니다. DeepSeek가 만든 계획을 챗봇에서 승인해 PostgreSQL 월별 12행을 조회하고, 같은 Lambda 응답을 거쳐 Agent 설명·표·그래프가 표시되는 것을 확인했습니다. [AWS 검증 기록](../aws/verification-2026-10-12.md)에서 실제 호출과 모의 장애 시험의 범위를 구분합니다.

설정 예시는 [app.env.example](app.env.example)입니다. 실제 값은 `.local/app.env`에 저장하고 인증은 사용자 홈 AWS 설정·캐시를 사용합니다. `poc-practice`는 관리 연결 프로필이며 앱과 수신기는 각각 `poc-chatbot`, `poc-worker` 일반 역할을 사용합니다. ARN·계정 ID·큐·결과 테이블 설정과 역할 인증을 검증한 후에만 수신기를 `Start.ps1 -Receiver`로 시작합니다. 기본 `Start.ps1`은 수신기를 시작하지 않습니다.

모델은 공통 `aws/config/models.json`을 읽으며 DeepSeek V3.2를 다른 모델로 대체하지 않습니다. Titan 임베딩 설정은 보존하지만 이번 로컬 앱은 벡터 검색을 구현하지 않습니다. 최신 예산 정책은 지연된 25 USD 초과 자동 차단이며 절대 청구 상한이 아닙니다. `strict_hard_cut_required=true`인데 미보장인 정책은 앱이 차단합니다.

## 시험

```powershell
# 프로젝트 루트. 운영 시험은 별도 인스턴스/포트(18000,18001)를 사용합니다.
.\.venv\Scripts\python.exe -m pytest local/python/tests -q --basetemp=.local/pytest-run
# 별도 AWS 변경을 포함한 전체 시험
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.local/pytest-all
```

PHP와 Node는 `.local/runtime`의 실행 파일을 사용합니다. `local/web` 폴더에서 `php artisan test`, `npm test -- --run`, `npm run build`를 실행합니다. 종단 시험은 `local/scripts/Verify-Browser.ps1`을 사용합니다. 별도 포트 18002/18003, Python 작업 SQLite, Laravel 이력 SQLite를 만들어 기존 앱·AWS 작업에 영향을 주지 않고 시험 후 해당 프로세스만 중지합니다. 처음에는 `PLAYWRIGHT_BROWSERS_PATH`를 프로젝트 `.local/playwright-browsers`로 지정한 뒤 `npx playwright install chromium`이 필요합니다.

Windows PHP 개발 서버는 요청을 순차 처리합니다. 자연어 계획 생성 요청은 동기식이고 SQL 실행은 Python 백그라운드 작업입니다. `Start.ps1`은 PHP 제한을 195초로 설정해 Agent 180초와 HTTP 185초 대기를 수용합니다. 여러 사용자의 동시 이용을 지원하는 운영 서버 구성과 비동기 계획 생성은 별도 확장 범위입니다.

[구현 계획](../docs/superpowers/plans/2026-10-12-local-chatbot.md) · [검증 기록](../docs/verification/2026-10-12-local.md)

현재 검증 범위는 Windows 로그인 세션입니다. 재부팅·무인 실행·자동 인증 갱신·실제 네트워크 장애와 AWS 비용 차단 실발동은 이 로컬 시험의 완료 범위에 포함하지 않습니다.
