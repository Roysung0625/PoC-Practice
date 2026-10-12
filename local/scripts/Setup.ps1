param([switch]$InstallRuntimes)
. "$PSScriptRoot/Common.ps1"
if ($InstallRuntimes) { & "$PSScriptRoot/Setup-Runtimes.ps1" -InstallPostgres }
$python = Join-Path $env:LOCALAPPDATA 'Programs/Python/Python313/python.exe'
if (!(Test-Path $python)) { throw 'Python 3.13 사용자 설치가 필요합니다. local/README.md를 확인하세요.' }
if (!(Test-Path "$ProjectRoot/.venv/Scripts/python.exe")) { & $python -m venv "$ProjectRoot/.venv"; if ($LASTEXITCODE) { throw '가상환경 생성 실패' } }
$python = "$ProjectRoot/.venv/Scripts/python.exe"
& $python -m pip install -r "$ProjectRoot/local/python/requirements.lock"
if ($LASTEXITCODE) { throw 'Python 의존성 설치 실패' }
& $python -m pip install --no-deps -e "$ProjectRoot/local/python"
if ($LASTEXITCODE) { throw 'Python 모듈 설치 실패' }
$php = "$ProjectRoot/.local/runtime/php/php.exe"
$env:Path = "$ProjectRoot/.local/runtime/node-v24.20.0-win-x64;$env:Path"
Push-Location "$ProjectRoot/local/web"
try {
    & $php "$ProjectRoot/.local/runtime/composer.phar" install --no-interaction
    if ($LASTEXITCODE) { throw 'Composer 설치 실패' }
    if (!(Test-Path '.env')) { Copy-Item '.env.example' '.env'; & $php artisan key:generate }
    if (!(Test-Path 'database/database.sqlite')) { New-Item -ItemType File 'database/database.sqlite' | Out-Null }
    & $php artisan migrate --force
    if ($LASTEXITCODE) { throw '웹 DB 마이그레이션 실패' }
    & "$ProjectRoot/.local/runtime/node-v24.20.0-win-x64/npm.cmd" ci
    if ($LASTEXITCODE) { throw '프런트엔드 의존성 설치 실패' }
    & "$ProjectRoot/.local/runtime/node-v24.20.0-win-x64/npm.cmd" run build
    if ($LASTEXITCODE) { throw '웹 빌드 실패' }
} finally { Pop-Location }
& $python -m poc.bootstrap
if ($LASTEXITCODE) { throw '데이터 구성 실패' }
Write-Output '로컬 구성이 완료되었습니다. Start.ps1로 앱을 시작하세요.'
