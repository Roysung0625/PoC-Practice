# 새 Mac 설치 지침서 — iDempiere DB와 기존 AWS 연결

작성 기준: 2026-10-12의 프로젝트 소스, 2026-10-13 비공개 저장소 이전 절차 반영. **현재 기본 DB인 iDempiere 13 GardenWorld**를 새 Mac에 설치하고, 기존 AWS의 AgentCore·Lambda·SQS·DynamoDB에 연결하는 절차다. TPC-H를 먼저 설치할 필요가 없다.

이 문서는 **Mac에는 아무것도 없고, 현재 프로젝트의 AWS 배포는 있는 경우**를 기본으로 한다. 새 AWS 계정에 인프라까지 처음 만드는 경우는 [15절](#15-aws도-아무것도-없는-경우)을 먼저 확인한다. 기존 AWS 리소스를 조회해 설정값을 한 번에 채우므로 큐 URL이나 역할 ARN을 각각 추측해서 입력하지 않는다.

**검증 경계:** 기존 Windows의 GardenWorld 설치·AWS 왕복 기록은 [기존 검증 보고서](verification/2026-10-12-idempiere.md)에 있다. 이 문서는 소스와 공식 설치 문서를 대조해 작성했다. Mac 실기기의 패키지 설치, DB 복원, 브라우저 및 실제 AWS 왕복은 Mac에서 아래 완료 기준으로 검증해야 한다. Windows용 `.ps1` 운영 스크립트는 Mac에서 실행하지 않는다.

## 목차

1. [설치할 구성과 준비물](#1-설치할-구성과-준비물)
2. [현재 프로젝트 소스 가져오기](#2-현재-프로젝트-소스-가져오기)
3. [Mac 개발 도구 설치](#3-mac-개발-도구-설치)
4. [Python·PHP·웹 의존성 설치](#4-pythonphp웹-의존성-설치)
5. [Mac 전용 PostgreSQL과 비밀값 생성](#5-mac-전용-postgresql과-비밀값-생성)
6. [GardenWorld 복원과 DB 연결](#6-gardenworld-복원과-db-연결)
7. [AWS 로그인과 배포 출력값 준비](#7-aws-로그인과-배포-출력값-준비)
8. [SQS·DynamoDB·Agent·역할 한 번에 연결](#8-sqsdynamodbagent역할-한-번에-연결)
9. [SQS 설정과 권한 확인](#9-sqs-설정과-권한-확인)
10. [앱과 수신기 실행](#10-앱과-수신기-실행)
11. [로컬 조회 → Lambda 왕복 → 자연어 분석 검증](#11-로컬-조회--lambda-왕복--자연어-분석-검증)
12. [종료·재시작·인증 갱신](#12-종료재시작인증-갱신)
13. [문제 해결](#13-문제-해결)
14. [설정·로그·완료 체크리스트](#14-설정로그완료-체크리스트)
15. [AWS도 아무것도 없는 경우](#15-aws도-아무것도-없는-경우)

## 1. 설치할 구성과 준비물

### 1.1 최종 구성

```text
Mac 브라우저 → Laravel(127.0.0.1:8000) → Python API(127.0.0.1:8001)
 → AWS AgentCore / Bedrock → Lambda SQL Tool → SQS
 → Mac 수신기 → 같은 Mac의 Python API → PostgreSQL(127.0.0.1:5432)
 → Mac 수신기 → DynamoDB → 대기 중인 동일 Lambda 호출의 응답
 → AWS Agent → Python API → Laravel → 브라우저
```

Mac이 AWS로 HTTPS 연결을 시작한다. 공유기 포트 포워딩, 공인 DB 주소, SSH 터널, Mac 인바운드 방화벽 개방은 이 구성에 필요하지 않다. Lambda의 SQS 요청 전송과 DynamoDB 결과 대기를 유지한다.

| 항목 | 설치·설정 기준 |
| --- | --- |
| Mac | Apple Silicon을 기본 경로로 설명. Intel은 아래 지원 제한 확인 |
| Python | 3.13, 프로젝트 `.venv` |
| PostgreSQL | 18, 프로젝트 전용 데이터 디렉터리 |
| PHP / Node | 8.4 / 24 |
| Composer / AWS CLI | Composer 2 / AWS CLI v2, `aws login` 지원 버전 |
| 분석 DB / 스키마 | `poc_idempiere` / `adempiere` |
| DB 읽기 계정 | `poc_idempiere_reader` |
| DB 소유자 | `poc_idempiere_owner`, NOLOGIN |
| 데이터 | 공식 GardenWorld 시드, 물리 테이블 912개·뷰 161개가 기존 검증 기준 |
| 웹 이력 / 작업 저널 | Laravel SQLite / Python SQLite, Mac에서 새로 생성 |
| AWS 리전 | `ap-northeast-1` |
| 앱 / 수신기 역할 | `poc-chatbot` / `poc-worker` |
| 생성 모델 | `deepseek.v3.2` |
| 임베딩 모델 | `amazon.titan-embed-text-v2:0`, 1,024차원, 정규화 |

모델은 [공통 설정](../aws/config/models.json)을 읽는다. 이 설치는 벡터 검색이나 Java iDempiere ERP 서버를 설치하지 않는다. 디스크는 패키지·DB·다운로드를 위해 **여유 10GB 이상을 준비하는 운영상 권장값**으로 잡는다. 정확한 설치 용량을 실측한 값은 아니다.

### 1.2 미리 확보할 것

- 현재 프로젝트 전체 소스와 잠금 파일 3개: `local/python/requirements.lock`, `local/web/composer.lock`, `local/web/package-lock.json`.
- 기존 AWS 계정의 12자리 ID와 IAM 사용자 **`poc-local-login`**의 콘솔 로그인 수단. Windows의 기존 비밀번호를 사용하되 Mac에서 새로 로그인한다.
- AWS 배포 출력값. 7절에서 Mac의 관리 프로필로 읽거나 기존 Windows에서 JSON만 내보낼 수 있다.
- 인터넷 연결. Homebrew, Python 패키지, Composer, npm, 공식 DB 시드, AWS에 접근할 수 있어야 한다.

**동일 SQS 큐에는 Windows와 Mac 수신기를 동시에 실행하지 않는다.** 현재 메시지에는 대상 PC를 선택하는 라우팅이 없고, 승인은 각 PC의 `.local/jobs.sqlite`에 있다. 다른 PC가 요청을 받으면 `NOT_APPROVED` 등으로 실패 처리할 수 있다. Mac으로 전환하기 전에 Windows의 진행 중 작업을 끝내고 Windows 앱·수신기를 중지한다. 소스 준비와 Mac의 로컬 DB 설치는 그 전에 진행해도 된다.

## 2. 현재 프로젝트 소스 가져오기

### 2.1 비공개 GitHub 저장소에서 받기 — 기본 방법

저장소는 [Roysung0625/PoC-Practice](https://github.com/Roysung0625/PoC-Practice)다. **아직 Homebrew가 없는 새 Mac이면 3.1절의 Command Line Tools·Homebrew·런타임 설치를 먼저 완료하고 이곳으로 돌아온다.** 3.2절은 clone 후 진행한다.

```bash
brew install gh
gh auth login --hostname github.com --git-protocol https --web
gh auth status --hostname github.com
mkdir -p "$HOME/Projects"
gh repo clone Roysung0625/PoC-Practice "$HOME/Projects/PoC-Practice"
cd "$HOME/Projects/PoC-Practice"
```

로그인 브라우저에서 저장소 소유 계정 또는 접근 권한이 있는 계정을 사용한다. 비공개 저장소이므로 로그인하지 않은 `git clone`이나 ZIP 다운로드는 실패할 수 있다. GitHub 계정 비밀번호를 Git HTTPS 비밀번호로 입력하지 않는다. 위 명령은 GitHub CLI의 브라우저 인증을 사용한다. [공식 로그인 안내](https://cli.github.com/manual/gh_auth_login) · [공식 clone 안내](https://cli.github.com/manual/gh_repo_clone)

소스만 내려받으며 큰 설치 파일·DB 시드는 [다운로드·재생성 안내](SOURCE_DOWNLOADS.md)에 따라 설치 중 공식 출처에서 받는다. clone 완료 후 3.2절로 이동한다. 이미 같은 폴더가 있다면 기존 환경을 덮어쓰지 말고 새 경로를 사용한다. 이후 갱신은 로컬 변경을 먼저 확인하고 `git pull --ff-only`로 진행한다.

### 2.2 GitHub 대신 소스 ZIP으로 옮기기 — 선택 사항

Windows PowerShell에서 아래를 실행하면 프로젝트의 소스용 ZIP을 만든다. `.local`, `.venv`, 인증·실제 환경설정, DB 파일, 의존성과 캐시는 제외한다. 결과 경로만 출력하며 비밀값을 읽어 출력하지 않는다.

```powershell
cd D:\Projects\PoC-Practice
@'
import os
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path.cwd()
destination = root / '.local/exports/PoC-Practice-macos-source.zip'
destination.parent.mkdir(parents=True, exist_ok=True)
excluded = {'.local', '.venv', '.aws', '.git', '.pytest_cache', '__pycache__',
            'node_modules', 'vendor', '.idea', '.phpunit.cache',
            'test-results', 'playwright-report'}
with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
    for directory, directories, files in os.walk(root):
        directories[:] = [n for n in directories if n not in excluded and not n.endswith('.egg-info')]
        for name in files:
            path = Path(directory) / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                continue
            if rel.startswith(('local/web/storage/', 'local/web/bootstrap/cache/', 'local/web/public/build/')):
                continue
            if name.startswith('.env') and name != '.env.example':
                continue
            if name.endswith(('.sqlite', '.sqlite-wal', '.sqlite-shm', '.sqlite-journal', '.pyc', '.log', '.pem', '.key')):
                continue
            if rel == 'local/web/public/hot':
                continue
            archive.write(path, 'PoC-Practice/' + rel)
print(destination)
'@ | .\.venv\Scripts\python.exe -
```

ZIP을 AirDrop·USB 등으로 Mac의 Downloads에 옮긴 뒤, Mac 터미널에서 실행한다. `~/Projects/PoC-Practice`가 이미 있다면 다른 폴더에 풀어 비교하고 기존 설정 위에 덮어쓰지 않는다.

```bash
mkdir -p "$HOME/Projects"
unzip "$HOME/Downloads/PoC-Practice-macos-source.zip" -d "$HOME/Projects"
cd "$HOME/Projects/PoC-Practice"
ls local/python/poc/idempiere.py local/web/composer.lock aws/infra/application.json
```

Windows의 PostgreSQL 데이터 디렉터리, Python 가상환경, `.local/app.env`, AWS 캐시, 승인·작업 SQLite를 복사하지 않는다. Mac에서 DB 시드를 다시 복원하고 연결값과 승인을 새로 만든다. 공식 시드 복원은 Windows에서 별도로 수정한 업무 데이터를 이관하는 절차와는 다르다.

## 3. Mac 개발 도구 설치

### 3.1 기기와 Homebrew 확인

```bash
uname -m
sw_vers
xcode-select --install
```

Command Line Tools 설치 창이 나타나면 완료할 때까지 기다린다. 이미 설치되었다는 메시지는 오류로 처리할 필요가 없다. `uname -m`이 Apple Silicon에서 `arm64`인지 확인한다. Rosetta 터미널에서 시작했다면 기본 터미널로 다시 시작한다.

2026-10-12 조회한 Homebrew 공식 문서는 Apple Silicon과 macOS 15 이상을 지원 경로로 안내하며 Intel은 Tier 3로 분류한다. Intel에서는 아래 수식의 바이너리 제공·소스 빌드 성공을 보장하지 않는다. 설치 오류를 다른 런타임 버전으로 자동 우회하지 말고 해당 기기의 지원 상태를 확인한다. [Homebrew 설치 요구사항](https://docs.brew.sh/Installation)

Homebrew가 없다면 공식 설치 명령을 실행하고 화면의 안내를 따른다.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

이후 이 문서의 명령은 **Bash**에서 실행한다. 새 터미널에서도 `/bin/bash`로 들어간다. 설치 도중 오류가 발생하면 해당 단계에서 중단하고 원인을 해결한 뒤 재개한다.

```bash
/bin/bash
set -euo pipefail
umask 077
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
else
  echo 'Homebrew 설치 후 표시되는 PATH 설정을 먼저 완료하세요.'
  exit 1
fi
brew --version
brew install python@3.13 postgresql@18 php@8.4 node@24 awscli
```

수식은 같은 메이저 계열의 최신 패치 버전을 설치한다. Windows에서 사용한 패치 번호와 완전히 같다고 가정하지 않는다. 공식 수식: [Python 3.13](https://formulae.brew.sh/formula/python@3.13), [PostgreSQL 18](https://formulae.brew.sh/formula/postgresql@18), [PHP 8.4](https://formulae.brew.sh/formula/php@8.4), [Node 24](https://formulae.brew.sh/formula/node@24).

### 3.2 프로젝트용 터미널 설정

아래 파일은 이 프로젝트의 터미널에서만 필요한 경로를 설정한다. `brew services start postgresql@18`은 실행하지 않는다. 5절에서 프로젝트 전용 DB 클러스터를 직접 시작한다.

```bash
cd "$HOME/Projects/PoC-Practice"
mkdir -p .local/logs .local/secrets .local/runtime .local/aws-deploy
cat > .local/macos-shell.sh <<'SH'
export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi
export PATH="$(brew --prefix php@8.4)/bin:$(brew --prefix node@24)/bin:$(brew --prefix postgresql@18)/bin:$PATH"
export POC_PGDATA="$PROJECT_ROOT/.local/postgres/data"
export PYTHONUTF8=1
export AWS_PAGER=""
export NO_PROXY="127.0.0.1,localhost${NO_PROXY:+,$NO_PROXY}"
umask 077
cd "$PROJECT_ROOT"
SH
source .local/macos-shell.sh
python3.13 --version
php --version
node --version
psql --version
aws --version
```

확인 기준은 Python 3.13, PHP 8.4, Node 24, PostgreSQL 18이다. AWS CLI는 `aws login`을 위해 **v2.32.0 이상**이어야 한다. [AWS 공식 로그인 안내](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html)

## 4. Python·PHP·웹 의존성 설치

### 4.1 Python

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r local/python/requirements.lock
.venv/bin/python -m pip install --no-deps -e local/python
.venv/bin/python -m pip check
.venv/bin/python -c 'import psycopg, duckdb, boto3, awscrt, fastapi; print("Python imports OK")'
```

`awscrt`도 설치되어야 한다. 프로젝트는 `boto3[crt]` 계열 인증 사용을 전제로 하며 잠금 파일에 CRT가 포함되어 있다. 패키지가 없거나 Mac용 wheel 설치가 실패하면 Python 버전·CPU와 패키지 배포 상태를 확인한다. 이때 잠금 파일을 삭제하거나 다른 모델·인증 방식으로 자동 변경하지 않는다.

### 4.2 Composer와 웹

Composer는 프로젝트 `.local/runtime/composer.phar`에 설치한다. 공식 설치 파일의 현재 SHA-384를 대조한 후 실행한다. [Composer 공식 다운로드·검증 안내](https://getcomposer.org/download/)

```bash
curl -fsSL https://getcomposer.org/installer -o .local/runtime/composer-setup.php
curl -fsSL https://composer.github.io/installer.sig -o .local/runtime/composer-installer.sig
php -r '$expected=trim(file_get_contents(".local/runtime/composer-installer.sig")); if (!hash_equals($expected, hash_file("sha384", ".local/runtime/composer-setup.php"))) { fwrite(STDERR, "Composer checksum mismatch\n"); exit(1); }'
php .local/runtime/composer-setup.php --2 --install-dir=.local/runtime --filename=composer.phar
php .local/runtime/composer.phar --version
```

실행 중인 기존 환경을 갱신하는 명령이 아니라 **새 Mac 최초 구성**이다. `.env`가 이미 있으면 복사하지 않는다.

```bash
cd "$PROJECT_ROOT/local/web"
mkdir -p bootstrap/cache storage/framework/cache/data storage/framework/sessions \
  storage/framework/views storage/logs storage/app/private storage/app/public
if [ ! -f .env ]; then cp .env.example .env; fi
php "$PROJECT_ROOT/.local/runtime/composer.phar" install --no-interaction
php "$PROJECT_ROOT/.local/runtime/composer.phar" check-platform-reqs
npm ci
npm run build
cd "$PROJECT_ROOT"
```

PHP는 SQLite·mbstring·XML 등 Composer가 요구하는 확장을 만족해야 한다. `check-platform-reqs` 오류를 `--ignore-platform-reqs`로 건너뛰지 않는다. 빌드가 끝나면 `local/web/public/build/manifest.json`이 있어야 한다.

## 5. Mac 전용 PostgreSQL과 비밀값 생성

### 5.1 포트 확인

```bash
for port in 5432 8000 8001; do
  if lsof -nP -iTCP:"$port" -sTCP:LISTEN; then
    echo "포트 $port 사용 중: 기존 프로세스를 확인한 뒤 진행하세요."
    exit 1
  fi
done
```

아무 출력 없이 통과하는 것이 새 환경의 기대 상태다. 아래 설치 코드와 수신기는 기본 주소·포트를 사용하므로 포트 충돌을 임의로 다른 번호로 바꾸어 회피하지 않는다. 기존 서비스를 먼저 확인한다.

### 5.2 클러스터·환경 파일을 한 번에 초기화

다음 블록은 새 비밀번호와 API 토큰을 생성하고 `initdb`를 실행한다. 비밀번호를 터미널에 출력하거나 명령행 인수로 전달하지 않는다. 기존 `.local/app.env`, DB 디렉터리 또는 PostgreSQL 비밀 파일이 있으면 중단한다. 재시작은 12절을 사용한다.

```bash
.venv/bin/python - <<'PY'
import json
from pathlib import Path
import secrets
import shutil
import subprocess
import tempfile
from dotenv import set_key
from poc.config import ROOT

data = ROOT / '.local/postgres/data'
secret_file = ROOT / '.local/secrets/postgres.json'
app_env = ROOT / '.local/app.env'
web_env = ROOT / 'local/web/.env'
for target in (data, secret_file, app_env):
    if target.exists():
        raise SystemExit(f'이미 존재합니다. 최초 설치를 반복하지 마세요: {target}')
if not web_env.exists():
    raise SystemExit('4절의 웹 .env 준비를 먼저 완료하세요.')
initdb = shutil.which('initdb')
if not initdb:
    raise SystemExit('PostgreSQL 18 bin 경로가 필요합니다.')
data.parent.mkdir(parents=True, exist_ok=True)
password = secrets.token_hex(32)
token = secrets.token_hex(32)
secret_file.write_text(json.dumps({'password': password}), encoding='utf-8')
secret_file.chmod(0o600)
with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=secret_file.parent, delete=False) as file:
    file.write(password + '\n')
    temporary = Path(file.name)
try:
    temporary.chmod(0o600)
    subprocess.run([initdb, '-D', str(data), '-U', 'postgres',
                    '--encoding=UTF8', '--locale=C', '--auth=scram-sha-256',
                    '--pwfile=' + str(temporary)], check=True)
finally:
    temporary.unlink(missing_ok=True)
with (data / 'postgresql.conf').open('a', encoding='utf-8') as file:
    file.write("\n# PoC-Practice macOS\nlisten_addresses = '127.0.0.1'\nport = 5432\nunix_socket_directories = ''\n")
app_env.touch(mode=0o600)
for key, value in {
    'POC_INTERNAL_TOKEN': token, 'POC_CHATBOT_PROFILE': 'poc-chatbot',
    'POC_WORKER_PROFILE': 'poc-worker', 'POC_AGENT_ARN': '',
    'POC_QUEUE_URL': '', 'POC_RESULT_TABLE': '', 'POC_AWS_ACCOUNT_ID': '',
}.items():
    set_key(str(app_env), key, value)
for key, value in {
    'APP_NAME': '로컬 데이터 랩', 'APP_ENV': 'local', 'APP_DEBUG': 'false',
    'APP_URL': 'http://127.0.0.1:8000', 'DB_CONNECTION': 'sqlite',
    'DB_DATABASE': str(ROOT / 'local/web/database/database.sqlite'),
    'POC_API_URL': 'http://127.0.0.1:8001', 'POC_INTERNAL_TOKEN': token,
    'SESSION_DRIVER': 'file', 'CACHE_STORE': 'file', 'QUEUE_CONNECTION': 'sync',
    'SESSION_SAME_SITE': 'strict', 'LOG_LEVEL': 'info',
}.items():
    set_key(str(web_env), key, value)
web_env.chmod(0o600)
print('DB 클러스터·비밀 파일·API 토큰 생성 완료. 비밀값은 출력하지 않았습니다.')
PY
pg_ctl -D "$POC_PGDATA" -l "$PROJECT_ROOT/.local/logs/postgres.log" -w start
pg_isready -h 127.0.0.1 -p 5432 -U postgres -d postgres
```

이 클러스터의 관리자 이름을 `postgres`로 지정하는 이유는 현재 iDempiere 설치 코드가 그 이름을 사용하기 때문이다. 앱은 이후 생성하는 별도의 읽기 계정으로 접속한다. PostgreSQL을 `sudo`로 실행하지 않는다. `initdb`의 비밀번호 파일·인증 옵션은 [PostgreSQL 18 공식 문서](https://www.postgresql.org/docs/18/app-initdb.html)를 따른다.

초기화가 실패해 일부 파일만 생겼다면 파일을 무조건 삭제해 재실행하지 않는다. `.local/logs/postgres.log`와 `PG_VERSION` 유무를 확인한다. 비밀 파일은 해당 클러스터 관리자 암호의 유일한 로컬 기록이다.

## 6. GardenWorld 복원과 DB 연결

### 6.1 현재 데이터셋 설치

```bash
cd "$PROJECT_ROOT"
psql --version
.venv/bin/python -m poc.idempiere --activate
```

이 명령이 수행하는 일:

1. 고정 커밋의 iDempiere 13 공식 시드를 다운로드하고 SHA-256 확인.
2. `poc_idempiere_owner`와 `poc_idempiere_reader`, `poc_idempiere` 생성.
3. `adempiere` 스키마를 단일 트랜잭션으로 복원하고 PG18 호환 처리 적용.
4. 읽기 전용 권한, 20초 쿼리 제한, 카탈로그와 manifest 생성.
5. `.local/app.env`의 **`POC_DB_DSN`과 `POC_CATALOG_PATH`를 함께 설정**.

현재 소스의 `psql_executable()`은 Windows 설치 경로를 우선 유지하고 Mac에서는 PATH의 `psql`을 찾는다. 이 함수가 없는 이전 소스를 받았다면 최신 소스로 갱신한다. Mac에 PowerShell만 설치해서 기존 설치 스크립트를 실행하는 것으로 대체할 수 없다.

| 연결 항목 | Mac에서 생성되는 값 |
| --- | --- |
| 호스트 / 포트 | `127.0.0.1` / `5432` |
| DB / 스키마 | `poc_idempiere` / `adempiere` |
| 사용자 | `poc_idempiere_reader` |
| DSN | `.local/app.env`에 새 읽기 계정 비밀번호 포함 |
| 카탈로그 | `<Mac 프로젝트 절대경로>/.local/datasets/idempiere/catalog.json` |
| 관리자 암호 / 읽기 암호 | `.local/secrets/postgres.json` / `.local/secrets/idempiere.json` |

**처음부터 `python -m poc.bootstrap`을 실행하지 않는다.** 활성 카탈로그가 없는 새 환경에서는 이전 TPC-H 설치로 들어갈 수 있다. GardenWorld는 위 명령으로 직접 설치한다. 시드 상세·업무 해석은 [iDempiere 안내](../local/IDEMPIERE_GUIDE.md)를 참고한다.

### 6.2 웹 이력 DB 구성

```bash
cd "$PROJECT_ROOT/local/web"
touch database/database.sqlite
php artisan key:generate --force
php artisan config:clear
php artisan migrate --force
cd "$PROJECT_ROOT"
```

`key:generate`는 최초 설치에만 실행한다. Laravel의 `DB_CONNECTION=sqlite`는 대화·승인 이력을 저장하는 DB다. 분석용 PostgreSQL 연결은 `.local/app.env`의 `POC_DB_DSN`에 있으므로 Laravel DB를 PostgreSQL로 바꾸지 않는다.

### 6.3 비밀값을 출력하지 않고 연결 검증

```bash
.venv/bin/python - <<'PY'
import json
import psycopg
from psycopg.conninfo import conninfo_to_dict
from poc.config import environment

cfg = environment()
catalog = json.loads(cfg['catalog'].read_text(encoding='utf-8'))
dsn = conninfo_to_dict(cfg['dsn'])
assert dsn['host'] == '127.0.0.1' and dsn['dbname'] == 'poc_idempiere'
assert dsn['user'] == 'poc_idempiere_reader'
assert catalog['dataset_id'] == 'idempiere' and catalog['schema'] == 'adempiere'
with psycopg.connect(cfg['dsn']) as db:
    identity = db.execute('SELECT current_database(), current_user').fetchone()
    readonly = db.execute('SHOW default_transaction_read_only').fetchone()[0]
    invoices = db.execute('SELECT count(*) FROM adempiere.c_invoice').fetchone()[0]
assert readonly == 'on'
assert len(catalog['tables']) == 912 and catalog['view_count'] == 161
print({'database': identity[0], 'user': identity[1], 'read_only': readonly,
       'tables': len(catalog['tables']), 'views': catalog['view_count'], 'invoice_rows': invoices})
PY
```

공식 시드 기준 청구서 전체 행 수는 8건이다. 데모 청구일은 2002~2003년이며 현재 연도 조회가 비어 있어도 DB 장애는 아니다. 기존 Windows의 DB에 변경을 가했다면 Mac의 새 공식 시드와 동일한 데이터라고 가정하지 않는다.

## 7. AWS 로그인과 배포 출력값 준비

### 7.1 Mac에서 일반 IAM 사용자로 로그인

AWS 콘솔에서 사용할 **실제 계정 ID**를 확인한 뒤 아래 자리표시자를 바꾼다. 계정 ID는 비밀번호가 아니며 잘못된 계정 연결을 차단하는 비교값이다.

```bash
export POC_EXPECTED_ACCOUNT_ID='YOUR_12_DIGIT_ACCOUNT_ID'
export POC_REGION='ap-northeast-1'
aws configure set region "$POC_REGION" --profile poc-local-login
aws configure set output json --profile poc-local-login
aws login --profile poc-local-login
aws sts get-caller-identity --profile poc-local-login --region "$POC_REGION"
```

브라우저에서는 **`poc-local-login` IAM 사용자**를 선택한다. root나 관리 역할을 앱의 로그인 사용자로 선택하지 않는다. 로그인 후 ARN은 `arn:aws:iam::<계정>:user/poc-local-login`이어야 한다. 이 사용자는 기존 부트스트랩의 `SignInLocalDevelopmentAccess`와 앱의 역할 AssumeRole 권한을 사용한다.

로그인 세션은 Mac 사용자 홈의 `~/.aws/config`, `~/.aws/login/cache`에서 관리한다. 장기 액세스 키를 생성하거나 Windows 인증 캐시를 복사하지 않는다. CLI 로그인은 최대 세션 시간 이후 다시 필요하다. [AWS 로그인·캐시 안내](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html)

### 7.2 기존 AWS 출력값 받기: A 또는 B 중 하나

`poc-local-login`, `poc-chatbot`, `poc-worker`는 배포 관리자가 아니다. 이들에게 `cloudformation:DescribeStacks`가 없다는 이유로 관리자 권한을 추가하지 않는다.

**A. Mac에서 관리 프로필로 읽기**

이미 승인된 관리용 일반 IAM 사용자·역할로 `poc-practice`에 로그인한다. 관리 조직이 IAM Identity Center를 사용한다면 해당 관리 프로필은 조직 안내에 따라 `aws configure sso`·`aws sso login`으로 준비한다. 앱 역할의 `source_profile`은 아래에서도 계속 `poc-local-login`이다.

```bash
aws configure set region "$POC_REGION" --profile poc-practice
aws configure set output json --profile poc-practice
aws login --profile poc-practice
.venv/bin/python - <<'PY'
import json
import os
import re
import subprocess
from poc.config import ROOT

account = os.environ['POC_EXPECTED_ACCOUNT_ID']
assert re.fullmatch(r'\d{12}', account), '계정 ID 자리표시자를 바꾸세요.'
def aws(*args):
    return json.loads(subprocess.check_output(['aws', *args, '--profile', 'poc-practice',
        '--region', 'ap-northeast-1', '--output', 'json', '--no-cli-pager'], text=True))
identity = aws('sts', 'get-caller-identity')
assert identity['Account'] == account, '관리 프로필 계정 불일치'
stack = aws('cloudformation', 'describe-stacks', '--stack-name', 'poc-practice-app')['Stacks'][0]
assert stack['StackStatus'] in ('CREATE_COMPLETE', 'UPDATE_COMPLETE'), stack['StackStatus']
values = {item['OutputKey']: item['OutputValue'] for item in stack['Outputs']}
path = ROOT / '.local/aws-deploy/app-outputs.json'
path.write_text(json.dumps(values, indent=2), encoding='utf-8')
print('현재 스택 출력값 저장 완료:', path)
PY
```

**B. Mac에 관리 인증을 추가하지 않고 Windows에서 가져오기**

기존 Windows에서 계정·리전을 확인한 관리 프로필로 다음 명령을 실행한다. 생성한 JSON만 Mac의 `.local/aws-deploy/app-outputs.json`으로 옮긴다. 인증 캐시·환경설정 전체를 옮기지 않는다.

```powershell
cd D:\Projects\PoC-Practice
aws sts get-caller-identity --profile poc-practice --region ap-northeast-1
$stackJson = aws cloudformation describe-stacks --stack-name poc-practice-app --profile poc-practice --region ap-northeast-1 --output json --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw '스택 조회 실패' }
$stack = ($stackJson | ConvertFrom-Json).Stacks[0]
if ($stack.StackStatus -notin @('CREATE_COMPLETE','UPDATE_COMPLETE')) { throw '스택이 준비되지 않았습니다.' }
$values = @{}
foreach ($item in $stack.Outputs) { $values[$item.OutputKey] = $item.OutputValue }
[IO.File]::WriteAllText((Join-Path (Get-Location) '.local/aws-deploy/app-outputs.json'), ($values | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
```

이 JSON에는 큐 URL·테이블 이름·역할/Agent ARN이 있고 비밀번호·액세스 키는 없다. 배포가 바뀌면 다시 내보낸다. `aws`가 Windows PATH에 없다면 [기존 AWS 가이드](../aws/README.md)의 CLI 경로를 사용한다.

## 8. SQS·DynamoDB·Agent·역할 한 번에 연결

아래 블록을 Mac 프로젝트 루트에서 실행한다. 앞 절의 `POC_EXPECTED_ACCOUNT_ID`와 `app-outputs.json`이 필요하다. AWS 리소스를 새로 만들지 않고 **Mac의 AWS 역할 프로필 2개와 앱의 AWS 설정 6개**를 작성한다. 기존 DB DSN·카탈로그·API 토큰은 보존한다.

```bash
.venv/bin/python - <<'PY'
import json
import os
import re
import subprocess
from urllib.parse import urlparse
import boto3
from dotenv import set_key
from poc.config import ROOT, validate_aws_identity

account = os.environ['POC_EXPECTED_ACCOUNT_ID']
region = 'ap-northeast-1'
assert re.fullmatch(r'\d{12}', account), '12자리 계정 ID를 입력하세요.'
values = json.loads((ROOT / '.local/aws-deploy/app-outputs.json').read_text(encoding='utf-8-sig'))
required = ('AgentArn', 'QueueUrl', 'ResultTable', 'ChatbotRoleArn', 'WorkerRoleArn')
assert all(values.get(key) for key in required), 'CloudFormation 출력값이 부족합니다.'
assert values['AgentArn'].startswith(f'arn:aws:bedrock-agentcore:{region}:{account}:runtime/')
url = urlparse(values['QueueUrl'])
assert url.scheme == 'https' and url.netloc == f'sqs.{region}.amazonaws.com'
assert url.path.startswith(f'/{account}/'), 'SQS 계정 불일치'
for profile, output in [('poc-chatbot', 'ChatbotRoleArn'), ('poc-worker', 'WorkerRoleArn')]:
    assert values[output] == f'arn:aws:iam::{account}:role/{profile}', '실행 역할 불일치'
app_env = ROOT / '.local/app.env'
assert app_env.exists(), 'DB와 API 토큰을 먼저 생성하세요.'
login = boto3.Session(profile_name='poc-local-login', region_name=region).client('sts').get_caller_identity()
assert login['Account'] == account
assert login['Arn'] == f'arn:aws:iam::{account}:user/poc-local-login', '전용 IAM 사용자로 다시 로그인하세요.'
for profile, output in [('poc-chatbot', 'ChatbotRoleArn'), ('poc-worker', 'WorkerRoleArn')]:
    settings = {'role_arn': values[output], 'source_profile': 'poc-local-login',
                'region': region, 'output': 'json', 'role_session_name': profile + '-mac'}
    for key, value in settings.items():
        subprocess.run(['aws', 'configure', 'set', key, value, '--profile', profile], check=True)
    session = boto3.Session(profile_name=profile, region_name=region)
    identity = validate_aws_identity(session, account, profile)
    print(profile, '->', identity['Arn'])
settings = {'POC_AGENT_ARN': values['AgentArn'], 'POC_QUEUE_URL': values['QueueUrl'],
            'POC_RESULT_TABLE': values['ResultTable'], 'POC_AWS_ACCOUNT_ID': account,
            'POC_CHATBOT_PROFILE': 'poc-chatbot', 'POC_WORKER_PROFILE': 'poc-worker'}
for key, value in settings.items():
    set_key(str(app_env), key, value)
app_env.chmod(0o600)
print('AWS 연결 설정 완료. DB 연결과 내부 토큰은 유지했습니다.')
PY
```

구성 후 `~/.aws/config`의 역할 설정은 개념적으로 다음과 같다. 직접 이 내용을 덮어쓸 필요는 없다. 실제 `login_session`은 `aws login`이 관리한다.

```ini
[profile poc-chatbot]
role_arn = arn:aws:iam::<ACCOUNT_ID>:role/poc-chatbot
source_profile = poc-local-login
region = ap-northeast-1

[profile poc-worker]
role_arn = arn:aws:iam::<ACCOUNT_ID>:role/poc-worker
source_profile = poc-local-login
region = ap-northeast-1
```

설정이 바뀌면 실행 중인 Python API와 수신기를 재시작한다. 셸에 이전 `POC_DB_DSN` 등이 `export`되어 있으면 `.env`보다 우선할 수 있으므로 새 터미널에서 실행하는 편이 명확하다. `.local/app.env`를 `source`로 읽지 않아도 Python 코드가 자동으로 로드한다.

## 9. SQS 설정과 권한 확인

### 9.1 SQS는 기존 CloudFormation 설정을 사용

프로젝트의 [애플리케이션 템플릿](../aws/infra/application.json)에 다음이 정의되어 있다. Mac 설치를 위해 SQS 콘솔에서 별도 큐를 만들거나 Lambda 트리거를 추가할 필요가 없다.

| 항목 | 현재 템플릿 값 / 이유 |
| --- | --- |
| 큐 유형 | Standard. 중복 실행 방지는 승인 ID·작업 저널에서 처리 |
| Long polling | 20초, 수신기가 HTTPS로 요청 |
| Visibility timeout | 90초 |
| 메시지 보존 | 86,400초, 1일 |
| 암호화 | SQS 관리형 SSE |
| DLQ 이동 | 최대 수신 횟수 3회 |
| DLQ 보존 | 345,600초, 4일 |
| 결과 테이블 | DynamoDB, 파티션 키 `request_id` (String) |
| 과금 / TTL | PAY_PER_REQUEST / `cleanup_at` |
| Lambda | 75초 제한, 결과를 직접 대기·조회 |
| 요청 / SQL 제한 | 승인 후 최대 60초 / SQL 최대 20초 |

**SQS → Lambda 이벤트 소스 매핑을 추가하지 않는다.** 여기서 SQS 소비자는 Mac 수신기이고 Lambda는 송신자다. 큐의 보존 기간과 작업 실행 기한도 별개다. 메시지가 남아 있어도 만료된 승인은 실행할 수 없다.

### 9.2 실제 일반 역할로 비파괴 조회

아래는 큐 속성과 존재하지 않는 임의 결과 키를 읽는다. 작업 메시지를 가져오거나 삭제하지 않는다. SQS 콘솔의 “메시지 폴링”도 실행 중에는 다른 소비자처럼 메시지를 잠시 숨길 수 있으므로 상태 확인에는 속성 조회를 사용한다.

```bash
.venv/bin/python - <<'PY'
import json
import uuid
import boto3
from poc.config import environment, validate_aws_identity

cfg = environment()
session = boto3.Session(profile_name=cfg['worker_profile'], region_name='ap-northeast-1')
validate_aws_identity(session, cfg['account_id'], 'poc-worker')
attributes = session.client('sqs').get_queue_attributes(
    QueueUrl=cfg['queue_url'], AttributeNames=['All'])['Attributes']
expected = {'VisibilityTimeout': '90', 'ReceiveMessageWaitTimeSeconds': '20',
            'MessageRetentionPeriod': '86400', 'SqsManagedSseEnabled': 'true'}
for name, value in expected.items():
    assert attributes.get(name) == value, (name, attributes.get(name))
redrive = json.loads(attributes['RedrivePolicy'])
assert int(redrive['maxReceiveCount']) == 3
result = session.resource('dynamodb').Table(cfg['result_table']).get_item(
    Key={'request_id': 'setup-check-' + uuid.uuid4().hex}, ConsistentRead=True)
assert 'Item' not in result
print({'queue_settings': 'OK', 'dynamodb_get_item': 'OK',
       'visible': attributes.get('ApproximateNumberOfMessages'),
       'in_flight': attributes.get('ApproximateNumberOfMessagesNotVisible')})
PY
```

이 검사는 DynamoDB 결과 **쓰기**와 Lambda 왕복의 성공을 의미하지 않는다. 그것은 11절에서 실제로 확인한다. 일반 수신기에는 `DescribeTable`, `ListQueues`, DLQ 읽기 권한이 없을 수 있고 정상이다.

권한 구조는 다음과 같다.

| 주체 | 필요한 권한 |
| --- | --- |
| `poc-local-login` | 브라우저 로그인, 지정된 앱·수신기 역할 AssumeRole |
| `poc-chatbot` | 지정된 AgentRuntime 호출·세션 중지 |
| `poc-worker` | 지정 큐 Receive/Delete/ChangeVisibility/GetAttributes, 결과 테이블 Get/Update |
| Lambda 역할 | 지정 큐 SendMessage, 결과 테이블 Put/Get/Update |
| Agent 역할 | 지정 Bedrock 모델 추론, SQL Lambda 호출 |

### 9.3 비용 차단 상태

기존 계정은 **계정 전체 실제 집계 비용 월 25 USD 초과 시 자동 차단**, 기존 10 USD 알림 유지 정책이다. 집계·감지 지연을 허용하며 정확한 청구 상한이 아니다. 다음 달에도 수동 복구 전까지 차단이 유지된다. [예산 정책](../aws/config/budget-policy.json) · [운영·복구](../aws/budget_guard/README.md)

관리 프로필이 있는 장비에서 `poc-account-budget-guard` 스택 상태와 운영 문서의 상태 조회 절차를 확인한다. 로컬 JSON에 `automatic_shutdown_configured=true`라고 적혀 있다는 사실만으로 새 AWS 계정의 실제 배포를 증명할 수 없다. 비용 차단으로 호출이 거부되면 root 인증이나 정책 변경으로 우회하지 않는다.

## 10. 앱과 수신기 실행

### 10.1 먼저 Windows에서 전환 준비

진행 중인 작업을 끝내고 Windows PowerShell에서 실행한다. Windows 웹도 중지해 새 요청이 만들어지지 않게 한다. PostgreSQL 서비스는 유지된다.

```powershell
cd D:\Projects\PoC-Practice
.\local\scripts\Stop.ps1
.\local\scripts\Status.ps1
```

같은 큐를 사용하는 다른 PC도 없는지 확인한다. 큐에 이전 작업이 남아 있다면 기존 장비에서 상태를 확인하고 정리한다. Mac의 정상 동작을 확인하기 위해 큐를 통째로 purge하지 않는다.

### 10.2 Mac 터미널 3개 열기

각 터미널에서 먼저 아래 세 줄을 실행한다. 전경 실행으로 시작·오류·종료를 직접 확인하며 최초 구성에서는 로그인 시 자동 실행을 등록하지 않는다.

```bash
/bin/bash
cd "$HOME/Projects/PoC-Practice"
source .local/macos-shell.sh
```

**터미널 A — SQL API**

```bash
set -o pipefail
.venv/bin/python -m uvicorn poc.api:create_app --factory \
  --host 127.0.0.1 --port 8001 --workers 1 \
  2>&1 | tee -a .local/logs/api-mac.log
```

`--workers 1`을 유지한다. API는 시작 시 작업 저널 복구를 수행한다. 같은 작업 저널을 사용한 API를 여러 개 띄우지 않는다.

**터미널 B — Laravel 웹**

```bash
set -o pipefail
cd "$PROJECT_ROOT/local/web/public"
php -d max_execution_time=195 -S 127.0.0.1:8000 \
  -t "$PROJECT_ROOT/local/web/public" \
  "$PROJECT_ROOT/local/web/vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php" \
  2>&1 | tee -a "$PROJECT_ROOT/.local/logs/web-mac.log"
```

**터미널 C — SQS 수신기**

API가 준비된 다음 실행한다. 로컬 고정 샘플 검증만 먼저 할 때는 이 명령을 나중에 실행해도 된다.

```bash
set -o pipefail
.venv/bin/python -u -m poc.receiver 2>&1 | tee -a .local/logs/receiver-mac.log
```

수신기는 메시지가 없을 때 조용히 기다리는 것이 정상이다. 성공 시작 메시지가 매번 출력되는 구조가 아니므로 프로세스가 남아 있는지와 11절 왕복으로 판단한다.

**점검용 터미널 D**에서도 공통 세 줄을 실행한 다음:

```bash
pg_ctl -D "$POC_PGDATA" status
curl --fail --silent --show-error http://127.0.0.1:8001/health | .venv/bin/python -m json.tool
curl --fail --silent --show-error http://127.0.0.1:8000/up
open http://127.0.0.1:8000
```

`health`에서 `db_connected=true`, `dataset_ready=true`, `dataset_id=idempiere`, `table_count=912`를 확인한다. AWS 설정 후에는 `aws_configured=true`가 기대값이지만 이 값은 **ARN이 채워졌다는 뜻**이며 인증·실제 모델 호출 성공 표시가 아니다. `aws_cost_policy=allowed`도 로컬 정책 검사 결과다.

## 11. 로컬 조회 → Lambda 왕복 → 자연어 분석 검증

### 11.1 AWS를 호출하지 않는 로컬 고정 샘플

1. 브라우저에서 `iDempiere 13 · GardenWorld 데모` 연결 표시 확인.
2. `고정 샘플 계획 열기` 선택.
3. GardenWorld 테넌트, 확정 판매 문서, 월별·통화별 집계, 대변전표 차감 조건 검토.
4. 승인 후 `succeeded`와 실제 표 확인.

이 샘플은 서로 다른 통화를 한 그래프로 섞지 않도록 기본적으로 표를 반환한다. 그래프가 없다는 이유만으로 실패라고 판단하지 않는다. 여기까지 성공하면 **Mac 웹 → SQL API → 실제 PostgreSQL**을 확인한 것이고 AWS 왕복은 아직 별도다.

### 11.2 GardenWorld로 동일 Lambda 호출 왕복 검증

기존 `aws/scripts/verify_live.py`의 `lambda`·`native`·`offline`·`expired` 경로에는 TPC-H `nation` 조회가 남아 있다. GardenWorld 설치 후 그 명령을 그대로 사용하지 않는다. 아래 검증은 현재 GardenWorld 샘플을 사용하며 **실제 AWS 호출 비용이 발생한다**. API와 수신기가 실행 중이고 다른 승인 작업이 없을 때 점검용 터미널에서 실행한다.

```bash
.venv/bin/python - <<'PY'
import json
import time
import uuid
from poc.agent import AgentPlanner, sample_plan
from poc.config import environment, load_shared
from poc.contracts import seal_plan
from poc.db import execute_query
from poc.journal import Journal

cfg = environment()
shared = load_shared()
catalog = json.loads(cfg['catalog'].read_text(encoding='utf-8'))
assert catalog['dataset_id'] == 'idempiere'
plan = seal_plan({**sample_plan(catalog), 'plan_id': str(uuid.uuid4()), 'provenance': 'aws_agent'})
baseline = execute_query(cfg['dsn'], plan['sql'], plan['params'], catalog=catalog)
assert baseline['status'] == 'succeeded'
store = Journal(cfg['journal'])
store.save_plan(plan)
approval = store.approve(plan['plan_id'], plan['digest'])
store.dispatch(approval['request_id'])
planner = AgentPlanner(cfg['agent_arn'], shared['budget'], shared['models'],
                       profile=cfg['profile'], account_id=cfg['account_id'])
try:
    payload = {'phase': 'tool_probe', 'plan': plan, 'approval': approval}
    result = planner.invoke(payload)
    assert result['status'] == 'succeeded', result.get('error')
    assert result['rows'] == baseline['rows'] and result['columns'] == baseline['columns']
    repeated = planner.invoke(payload)
    assert repeated['status'] == 'succeeded' and repeated['rows'] == result['rows']
    report = {'status': 'succeeded', 'dataset': 'idempiere', 'request_id': approval['request_id'],
              'same_lambda_response': True, 'postgres_baseline_equal': True,
              'duplicate_result_equal': True, 'row_count': result['row_count'],
              'verified_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    destination = cfg['root'] / '.local/aws-deploy/verification/macos-idempiere-lambda.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
finally:
    store.finish_agent(approval['request_id'], {'status': 'failed', 'error': {
        'code': 'INTEGRATION_PROBE', 'message': '전송 검증 전용이며 모델 설명을 요청하지 않았습니다.'}})
PY
```

전송 검증 전용 작업은 마지막에 `INTEGRATION_PROBE`로 닫는다. 검증 성공 여부는 생성한 보고서의 `status`로 판단한다. 중복 응답 일치는 재전송 결과 검증이며 모든 장애 상황에서의 중복 방지를 실증한 것은 아니다. `tool_probe`는 모델의 자연스러운 도구 선택을 검증하지 않으므로 다음 단계를 수행한다.

### 11.3 실제 DeepSeek 질문·도구 호출·그래프

브라우저에서 새 분석을 만들고 다음과 같이 질문한다.

> GardenWorld의 USD 확정 판매 청구액을 월별로 집계하고 막대그래프로 보여줘.

테넌트 `ad_client_id=11`, 판매 `issotrx='Y'`, 완료·마감 `docstatus IN ('CO','CL')`, USD, 세전 청구액 `totallines`, 판매 대변전표 차감을 검토한 뒤 승인한다. SQL 성공·AWS 결과 전달·Agent 설명이 각각 성공인지 확인한다. 공식 시드와 위 정의 기준 기존 Windows 검증값은 2002-02의 142.5 USD, 2002-08의 152 USD이며 **Mac에서는 직접 대조해야 한다**.

그래프까지 성공한 직후, 중간에 다른 AWS 테스트를 실행하지 않고 다음 명령으로 최신 승인 작업을 직접 SQL과 대조한다.

```bash
.venv/bin/python aws/scripts/verify_chatbot.py
```

이 검증기는 최신 AWS 작업과 **그래프 존재**를 검사한다. 표 전용 질문의 정상 성공에는 사용하지 않는다. 결과 파일은 `.local/aws-deploy/verification/chatbot.json`이다. 모델 설명의 모든 수치·업무 해석 정확성을 이 검사 하나로 보장하지 않는다.

선택적으로 Titan 실제 추론을 별도 확인한다. 이는 벡터 검색 구축을 의미하지 않는다.

```bash
.venv/bin/python aws/scripts/verify_live.py embedding
```

## 12. 종료·재시작·인증 갱신

### 12.1 정상 종료

진행 중인 요청의 완료 또는 명시적인 시간 초과를 먼저 확인한다. 터미널 C(수신기) → B(웹) → A(API)에서 각각 **Ctrl+C**로 종료한다. PostgreSQL도 중지하려면 점검용 터미널에서:

```bash
pg_ctl -D "$POC_PGDATA" -m fast -w stop
```

`fast` 종료는 남은 DB 트랜잭션을 중단하므로 사용자 작업이 끝난 다음 사용한다. `killall python`, 포트 소유자 확인 없는 `kill -9`, DB 디렉터리 삭제로 종료하지 않는다.

### 12.2 다음 날 또는 재부팅 후

```bash
/bin/bash
cd "$HOME/Projects/PoC-Practice"
source .local/macos-shell.sh
if ! pg_ctl -D "$POC_PGDATA" status; then
  pg_ctl -D "$POC_PGDATA" -l "$PROJECT_ROOT/.local/logs/postgres.log" -w start
fi
aws sts get-caller-identity --profile poc-worker --region ap-northeast-1
aws sts get-caller-identity --profile poc-chatbot --region ap-northeast-1
```

STS가 인증 만료로 실패하면 `aws login --profile poc-local-login`으로 다시 로그인하고 위 두 역할을 재확인한다. 이후 10절의 API·웹·수신기를 시작한다. 설치, `initdb`, `key:generate`, DB 복원은 반복할 필요가 없다.

수신기가 인증 오류를 반복하는 중이라면 Ctrl+C → 로그인 갱신 → 수신기 재시작 순서로 처리한다. API에도 오래된 설정이 남아 있으면 진행 중 작업을 정리한 뒤 재시작한다. 만료·실패·불명 작업은 자동 재실행하지 말고 새 계획을 승인한다.

### 12.3 Mac 절전과 통신 복구

절전·네트워크 끊김 동안 로컬 작업을 처리할 수 없다. 점검 세션에서만 별도 터미널의 `caffeinate -i`로 유휴 절전을 방지할 수 있으며 끝나면 Ctrl+C로 해제한다. 이 명령이 덮개 닫힘이나 모든 절전 상황을 막는 것은 아니다.

수신기는 통신 예외 시 5초 간격으로 재접속을 시도한다. 이미 만료된 승인을 새 SQL 실행으로 바꾸지 않는다. 연결 복구 후 `/health`, 역할 STS, 새 분석 순서로 점검한다. 무인 실행은 재부팅·프로세스 복구·로그인 갱신까지 검증하기 전에는 완료로 보지 않는다.

### 12.4 Windows로 다시 전환

Mac의 진행 중 작업을 끝내고 Mac 수신기와 앱을 중지한 뒤 Windows에서 인증과 DB 상태를 확인하고 `Start.ps1 -Receiver`를 실행한다. 장비마다 계획·승인이 독립적이므로 Mac에서 승인한 작업을 Windows에서 이어 실행하지 않는다. 두 장비의 동시 AWS 분석이 필요하면 대상 장비 라우팅 또는 전체 독립 환경 설계가 추가로 필요하다.

## 13. 문제 해결

| 증상 | 확인·조치 |
| --- | --- |
| `brew`·`php`·`psql` 없음 | Bash에서 `.local/macos-shell.sh`를 source하고 `command -v`와 버전 확인 |
| Intel Mac 패키지 설치 실패 | Homebrew Tier 3 및 해당 수식의 제공 여부 확인. Apple Silicon 설치 성공으로 간주하지 않음 |
| Python wheel 없음 / 아키텍처 오류 | `uname -m`, Python 3.13 확인. Windows `.venv`를 복사하지 않았는지 확인 |
| `psql.exe` 경로 오류 | 최신 `poc/idempiere.py`의 `psql_executable()` 포함 여부와 Mac PATH 확인 |
| `postgres.json` 없음 | 5절 초기화 누락. Windows 비밀번호 파일을 복사하는 대신 Mac 클러스터 생성 |
| 5432 사용 중 | `lsof -nP -iTCP:5432 -sTCP:LISTEN`으로 소유자 확인. 다른 DB를 중지·덮어쓰지 않고 구성 재검토 |
| DB 암호 불일치 | 프로젝트 PGDATA가 실행 중인지, 해당 클러스터의 비밀 파일인지 확인. `trust`로 완화하지 않음 |
| 공식 시드 체크섬 불일치 | 설치 중단. 다운로드 오류와 고정 소스 확인. 기대 해시를 받은 파일에 맞춰 바꾸지 않음 |
| 복원 실패 / `uuid-ossp` 없음 | PostgreSQL 18 패키지 확인, `.local/datasets/idempiere/restore.log` 확인. 소유자·스키마 검사 유지 |
| 화면이 TPC-H 또는 `SCHEMA_CHANGED` | `POC_DB_DSN`과 `POC_CATALOG_PATH`를 함께 확인, API 재시작, 새 분석 생성 |
| `DB_UNAVAILABLE` | `pg_ctl status`, 5432 수신, 6.3절 실제 읽기 연결 확인 |
| 웹 500 / SQLite 없음 | storage 디렉터리, SQLite 파일, `APP_KEY`, `php artisan migrate`, Laravel 로그 확인 |
| API 401 | 웹과 Python의 `POC_INTERNAL_TOKEN` 일치 여부를 값 출력 없이 확인. `config:clear` 후 재시작 |
| `aws login` 명령 없음 | AWS CLI v2.32.0 이상인지와 다른 `aws` 실행 파일이 PATH 앞에 있는지 확인 |
| `poc-local-login` 로그인 거부 | 계정·IAM 사용자·콘솔 암호·로그인 권한 확인. 기존 최초 암호 변경이 필요하면 관리자에게 확인 |
| `AssumeRole` AccessDenied | 로그인 ARN이 전용 사용자인지, `PocAssumeLocalRoles`와 역할 신뢰 정책·계정 ID 확인 |
| CloudFormation 조회 거부 | 일반 앱 역할로 조회한 것은 아닌지 확인. 7.2절 B의 출력값 전달 방식 사용 |
| SQS `NonExistentQueue` | 동일 배포의 QueueUrl·계정·도쿄 리전인지 확인하고 출력값 다시 취득 |
| DynamoDB `ResourceNotFoundException` | 동일 스택의 ResultTable과 리전 확인 |
| SQS 속성 조회는 성공하지만 처리 실패 | API 실행·토큰·DynamoDB Update 권한·승인 저널과 11.2절 왕복 확인 |
| `NOT_APPROVED` / `APPROVAL_MISMATCH` | Windows나 다른 Mac이 같은 큐를 소비하는지, API·수신기가 같은 프로젝트 저널인지 확인 |
| `LOCAL_RESULT_TIMEOUT` | 수신기·네트워크·Mac 절전 상태와 인증 확인. 승인 60초와 SQL 20초 제한을 함께 고려 |
| `AWS_ROOT_FORBIDDEN` / `AWS_ROLE_MISMATCH` | 앱에는 지정된 일반 역할 사용. 역할 프로필에 직접 `aws login`하지 말고 source profile 로그인 |
| `AWS_AUTH_ERROR` / 반복 ExpiredToken | `poc-local-login` 재로그인, STS 역할 확인, API·수신기 재시작 |
| `COST_POLICY_BLOCKED` / 계정 전체 AccessDenied | 예산 차단 상태 확인. 승인된 운영·복구 절차 사용 |
| 모델 AccessDenied / 모델 없음 | 실제 배포 리전·권한·모델 접근 상태 점검. 모델 카탈로그 조회 성공과 추론 성공 구분 |
| 표 전용 결과인데 `verify_chatbot.py` 실패 | 해당 검증기는 그래프를 요구함. 11.3절의 명시적 막대그래프 질문으로 검증 |
| `AGENT_RESPONSE_INVALID` / `SQL_REJECTED` | 허용 SQL·테이블과 질문을 검토해 새 계획 요청. 검사 비활성화 금지 |
| 날짜 조건 결과 0행 | 데모는 2002~2003년. 현재 연도 데이터가 있는지 확인하고 기간을 명시 |

내부 토큰 일치 여부만 확인하는 명령:

```bash
.venv/bin/python - <<'PY'
from dotenv import dotenv_values
from poc.config import ROOT
a = dotenv_values(ROOT / '.local/app.env').get('POC_INTERNAL_TOKEN')
b = dotenv_values(ROOT / 'local/web/.env').get('POC_INTERNAL_TOKEN')
print('token_match =', bool(a and a == b))
PY
```

## 14. 설정·로그·완료 체크리스트

| 위치 | 용도 |
| --- | --- |
| `.local/macos-shell.sh` | Mac 터미널 PATH와 프로젝트 경로 |
| `.local/app.env` | 분석 DB·카탈로그·내부 토큰·AWS 리소스 |
| `local/web/.env` | Laravel 이력 DB·앱 키·내부 API 연결 |
| `.local/secrets/postgres.json` | Mac PostgreSQL 관리자 암호 |
| `.local/secrets/idempiere.json` | GardenWorld 읽기 계정 암호 |
| `.local/postgres/data/` | Mac PostgreSQL 클러스터 |
| `.local/datasets/idempiere/` | 카탈로그·manifest·복원 로그·전환 전 설정 백업 |
| `.local/jobs.sqlite` | 승인·실행 상태·중복 방지·전송 outbox |
| `local/web/database/database.sqlite` | 대화·계획·승인 이력 |
| `.local/aws-deploy/app-outputs.json` | 배포 출력값 |
| `.local/aws-deploy/verification/` | Mac에서 직접 수행한 검증 결과 |
| `.local/logs/*-mac.log`, `postgres.log` | 이번 문서의 실행 로그 |
| `local/web/storage/logs/laravel.log` | Laravel 오류 |
| `~/.aws/config`, `~/.aws/login/cache/` | Mac 사용자 AWS 프로필·임시 로그인 |

로그를 공유할 때 DSN·토큰·인증정보·원본 조회 데이터가 포함되어 있지 않은지 확인한다. `.local/datasets/idempiere/app-before-idempiere.env`도 비밀값이 있는 설정 백업이다. Windows의 `.local/services.json`은 이 문서의 Mac 전경 프로세스를 관리하지 않는다.

완료 여부를 아래 순서로 기록한다.

- [ ] Mac의 런타임 버전과 잠금 파일 의존성 설치 성공.
- [ ] PostgreSQL·웹·API가 `127.0.0.1`에서만 수신.
- [ ] GardenWorld DB의 912개 물리 테이블·161개 뷰와 읽기 계정 확인.
- [ ] 활성 DSN과 카탈로그 모두 iDempiere, 로컬 고정 샘플 조회 성공.
- [ ] 지정 계정의 `poc-local-login` → `poc-chatbot`·`poc-worker` AssumeRole 성공.
- [ ] SQS 속성과 DynamoDB 읽기 확인, 동시 소비 중인 다른 PC 없음.
- [ ] GardenWorld Lambda 왕복·원본 SQL 대조 보고서 생성.
- [ ] DeepSeek의 자연어 계획·승인·도구 호출·설명·표·막대그래프 확인.
- [ ] 그래프 포함 최신 요청을 `verify_chatbot.py`로 PostgreSQL과 대조.
- [ ] 종료·재시작·인증 갱신 후 새 분석 성공.

마지막 단계까지 직접 확인하기 전에는 “Mac AWS 연동 완료”라고 기록하지 않는다. 무인 운영·실제 네트워크 장애·계정 비용 차단의 실발동 검증은 이 체크리스트와 별도의 운영 시험이다.

### 문서 작성 시 수행한 점검

- 실제 활성 설정을 비밀번호·토큰 출력 없이 읽어 `127.0.0.1:5432`, `poc_idempiere`, `poc_idempiere_reader`, iDempiere 카탈로그 경로 확인.
- `psql` 경로 선택 3개와 기존 iDempiere 정책·테이블 선택·계획 단위 시험 3개: **6 passed**. 실제 DB를 사용하는 시험 1개는 이 실행에서 제외.
- 문서에 포함된 Python 블록 8개의 구문 검사, 상대 파일 링크 12개 및 목차 연결 16개 검사 통과.
- Mac의 Bash 실행, Homebrew 설치, 새 DB 복원, AWS 실호출은 수행하지 않음. 위 단위·정적 점검은 Mac 설치 성공 증거를 대신하지 않음.

## 15. AWS도 아무것도 없는 경우

새 Mac 설치와 새 AWS 계정 구축은 필요한 권한·영향이 다르다. 이 문서의 기본 경로는 기존 배포를 재사용하므로, 새 계정에서 `poc-practice-app`이 없다는 오류가 나오면 SQS만 임의 생성해 진행하지 않는다.

프로젝트는 다음 순서의 CloudFormation 배포를 사용한다. 실제 새 계정·리전을 먼저 확인하고, 계정 전체 차단 범위와 관리 권한을 승인된 구성으로 준비한다.

| 순서 | 템플릿 / 작업 | 생성·확인할 내용 |
| --- | --- | --- |
| 1 | [예산 차단 운영 가이드](../aws/budget_guard/README.md) | 실제 계정의 월 25 USD 초과 차단, 기존 10 USD 알림 보존, 제어 역할·복구 절차 |
| 2 | [bootstrap.json](../aws/infra/bootstrap.json) | 아티팩트 S3, `poc-local-login` IAM 사용자 |
| 3 | 로그인 준비 | 전용 사용자의 콘솔 암호·최초 변경, Mac 브라우저 로그인 |
| 4 | [package_runtime.py](../aws/scripts/package_runtime.py) | AWS용 Python 3.13 Linux ARM64 ZIP, Mac 네이티브 라이브러리와 구분 |
| 5 | [application.json](../aws/infra/application.json) | SQS·DLQ·DynamoDB·Lambda·AgentCore·IAM 역할 |
| 6 | 출력값·로그·모델 검증 | 스택 성공 상태, 로그 보존 7일, 현재 모델의 실제 추론·도구 호출 |
| 7 | 이 문서 7~11절 | Mac 프로필·설정·수신기·왕복 연결 |

배포 운영 명령은 [AWS 배포 가이드](../aws/DEPLOYMENT.md)에 있다. **현재 `Aws-Common.ps1`, `Prepare-PocLogin.ps1`, `Deploy-PocAws.ps1` 등은 Windows 경로·ACL·실행 파일에 의존한다.** 새 AWS 환경은 기존 Windows 관리 환경에서 그 가이드대로 구축하고 출력값을 Mac에 넘기는 경로를 사용한다. Mac만으로 AWS 전체를 최초 배포하는 자동화까지 완료되었다고 보지 않는다.

독립 스택을 만들더라도 현재 템플릿은 `poc-sql-tool`, `poc-agent-runtime`, `poc-chatbot`, `poc-worker`, `poc_sql_agent` 등의 이름이 고정되어 있다. 같은 계정에서 스택 이름만 바꾸면 별도 환경이 되는 구조가 아니다. Windows와 Mac의 동시 독립 실행은 이름·역할 검증·큐 라우팅을 함께 설계한 뒤 적용해야 한다.
