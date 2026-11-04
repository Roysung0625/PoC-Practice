# 소스 저장소에서 제외한 파일과 다운로드 방법

최초 기준일: 2026-10-13. 당시 Mac으로 옮기기 위해 비공개로 게시했으며, 2026-11-04 사용자 승인으로 GitHub 저장소를 공개로 전환했다. 현재 공개 저장소에도 실행 코드, 테스트, CloudFormation, 운영 스크립트, 설정 예시, 잠금 파일과 문서만 저장한다. 라이선스와 프로젝트에 포함된 스킬 소스도 유지한다. 실제 인증정보·DB·런타임 바이너리·설치 파일·의존성 폴더·생성 결과는 업로드하지 않는다. Git LFS나 별도 공개 파일 서버를 만들지 않고 **공식 배포처에서 다운로드하거나 소스로 재생성**한다.

## 새 Mac에서 필요한 항목

전체 설치 순서는 [Mac 설치 지침서](MACOS_SETUP.md)를 따른다. 아래 명령은 해당 지침서에서 런타임·DB·환경설정을 준비한 다음 단계에 맞춰 실행한다.

| 제외한 항목 | 다운로드·재생성 방법 | 보관 위치 |
| --- | --- | --- |
| Python 3.13·PostgreSQL 18·PHP 8.4·Node 24·AWS CLI | Mac에서는 `brew install python@3.13 postgresql@18 php@8.4 node@24 awscli` | Homebrew 관리 경로 |
| Python 가상환경·라이브러리 | `python3.13 -m venv .venv`, 잠금 파일로 pip 설치 | `.venv/` |
| Composer 실행 파일 | Mac 지침서의 공식 installer + SHA-384 검증 | `.local/runtime/composer.phar` |
| PHP 의존성 | `local/web`에서 `php ../../.local/runtime/composer.phar install --no-interaction` | `local/web/vendor/` |
| JS 의존성 | `local/web`에서 `npm ci` | `local/web/node_modules/` |
| 웹 빌드 결과 | `local/web`에서 `npm run build` | `local/web/public/build/` |
| GardenWorld 공식 시드·복원 SQL | `.venv/bin/python -m poc.idempiere --activate`가 다운로드·체크섬 검사·복원 | `.local/downloads/idempiere/` |
| PostgreSQL 실제 데이터 | Mac 지침서대로 `initdb` 후 위 시드 복원 | `.local/postgres/data/` |
| iDempiere 카탈로그·manifest | 위 iDempiere 설치 명령으로 DB에서 재생성 | `.local/datasets/idempiere/` |
| 웹 SQLite·API 작업 저널 | Laravel migrate / SQL API 시작 시 새로 생성 | `local/web/database/database.sqlite`, `.local/jobs.sqlite` |
| AWS 배포용 ZIP | 배포가 필요한 경우 `.venv/bin/python aws/scripts/package_runtime.py` | `.local/aws-deploy/` |
| Playwright 브라우저 | 선택적 브라우저 시험에만 `local/web`에서 `npx playwright install chromium` | Playwright 캐시 |

Python 의존성 설치 명령은 프로젝트 루트에서 실행한다.

```bash
.venv/bin/python -m pip install -r local/python/requirements.lock
.venv/bin/python -m pip install --no-deps -e local/python
```

`requirements.lock`, `composer.lock`, `package-lock.json`은 저장소에 포함한다. 이 파일들은 큰 의존성 폴더를 다시 구성하기 위한 소스의 일부다. Mac용 라이브러리는 Mac에서 설치하며 Windows의 `.venv`, `vendor`, `node_modules`를 복사하지 않는다.

## GardenWorld 시드를 직접 받는 경우

정상 설치에서는 다운로드를 따로 실행할 필요가 없다. 네트워크 재시도·사전 다운로드가 필요한 경우에만 아래를 사용한다. 프로젝트가 고정한 값은 [설치 코드](../local/python/poc/idempiere.py)에 있다.

- 공식 원본: [고정 커밋의 Adempiere_pg.jar](https://raw.githubusercontent.com/idempiere/binary.file/30af25e9db302a6cdefd9e6c3846f7cedc5ce4d0/database/13/Adempiere_pg.jar)
- SHA-256: `f6e5f409791c9eb576caf3c36e0bf9747d59d261ff9bdd743e55fcb125b21b9c`
- 기존 PC에서 측정한 압축 파일: 약 9.5 MiB. 추출한 SQL 덤프는 약 43.7 MiB이며 둘 다 Git에서 제외한다.

Mac 프로젝트 루트에서:

```bash
mkdir -p .local/downloads/idempiere
curl --fail --location --retry 3 \
  'https://raw.githubusercontent.com/idempiere/binary.file/30af25e9db302a6cdefd9e6c3846f7cedc5ce4d0/database/13/Adempiere_pg.jar' \
  -o .local/downloads/idempiere/Adempiere_pg-13.jar
printf '%s  %s\n' \
  'f6e5f409791c9eb576caf3c36e0bf9747d59d261ff9bdd743e55fcb125b21b9c' \
  '.local/downloads/idempiere/Adempiere_pg-13.jar' | shasum -a 256 -c -
```

체크섬이 맞지 않으면 설치를 중단한다. 공식 시드를 수정하지 않는다. 전용 NOLOGIN 소유자 매핑·PG18 호환 처리·읽기 권한은 `poc.idempiere`가 적용하므로 덤프를 임의로 바로 `psql`에 넣는 절차로 대체하지 않는다. 시드 JAR은 Python의 ZIP 처리로 읽으며 Java 서버 설치는 필요하지 않다.

## Windows 전용 큰 설치 파일

기존 PostgreSQL 설치 EXE는 약 395.7 MiB, Node ZIP은 약 35.8 MiB, PHP ZIP은 약 33.5 MiB였다. Mac에서는 사용하지 않는다. Windows 재설치가 필요하면 [Setup-Runtimes.ps1](../local/scripts/Setup-Runtimes.ps1)이 공식 배포처에서 다운로드하고 해시를 확인한다. 이 바이너리를 GitHub 저장소에 넣을 필요가 없다.

이전 TPC-H 데이터·CSV·DuckDB 파일도 업로드하지 않는다. 현재 기본 데이터는 GardenWorld이며 TPC-H는 [기존 데이터 생성 코드](../local/python/poc/dataset.py)로 따로 만들 수 있다. 새 Mac에서 TPC-H bootstrap을 먼저 실행하면 현재 기본 DB와 다른 환경을 만들 수 있으므로 Mac 지침서의 iDempiere 경로를 따른다.

## 다운로드하거나 그대로 복사하면 안 되는 설정

- `.local/app.env`, `local/web/.env`, `.local/secrets/`: Mac에서 새 DB 암호·API 토큰·앱 키 생성.
- `.aws/`, `~/.aws/` 인증 캐시: Mac에서 `aws login --profile poc-local-login`으로 새 로그인.
- Windows의 실제 PostgreSQL 데이터 디렉터리: Mac에서 공식 시드를 새로 복원.
- 기존 승인·실행 SQLite: Mac에서 새 승인과 작업 저널 생성. 같은 SQS 큐의 수신기를 두 PC에서 동시에 실행하지 않음.
- 계정별 AWS 출력값: Mac 설치 지침서 7~8절의 방법으로 권한 있는 계정에서 읽거나 출력 JSON만 전달. 저장소에 실제 배포 출력값을 고정하지 않음.

기존 증빙 스크린샷·로컬 로그는 기존 PC에 보존한다. 소스·문서의 검증 기록은 남기지만 새 Mac에서 수행한 결과로 간주하지 않는다.
