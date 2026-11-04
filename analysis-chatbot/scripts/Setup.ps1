param([switch]$SkipInstall)
. "$PSScriptRoot/Common.ps1"
if (!(Test-Path "$ProjectRoot/.local/app.env")) { throw '기존 local/scripts/Setup.ps1과 iDempiere 구성을 먼저 완료하세요. 기존 설정은 재생성하지 않습니다.' }
if (!(Test-Path -LiteralPath $Python)) { throw '프로젝트 Python 가상환경이 필요합니다.' }
New-Item -ItemType Directory -Force $StateDirectory, $LogDirectory | Out-Null
if (!$SkipInstall) { & "$PSScriptRoot/Install-Php.ps1" }
if (!(Test-Path -LiteralPath $Php)) { throw 'Install-Php.ps1 실행이 필요합니다.' }
$previousPath = $env:PATH
$previousTemp = $env:TEMP
$previousTmp = $env:TMP
$previousDatabase = $env:DB_DATABASE
try {
    $env:PATH = "$PhpDirectory;$NodeDirectory;$previousPath"
    $env:TEMP = Join-Path $StateDirectory 'tmp'
    $env:TMP = $env:TEMP
    $env:DB_DATABASE = Join-Path $StateDirectory 'conversations.sqlite'
    New-Item -ItemType Directory -Force $env:TEMP | Out-Null
    Push-Location $AppRoot
    try {
        if (!$SkipInstall) {
            Invoke-Checked $Php @("$ProjectRoot/.local/runtime/composer.phar", 'install', '--no-interaction', '--prefer-dist')
            Invoke-Checked "$NodeDirectory/npm.cmd" @('ci', '--ignore-scripts')
        }
        if (!(Test-Path -LiteralPath "$AppRoot/.env")) { Copy-Item -LiteralPath "$AppRoot/.env.example" -Destination "$AppRoot/.env" }
        $appSettings = Get-Content -LiteralPath "$AppRoot/.env"
        if (!($appSettings | Where-Object { $_ -match '^APP_KEY=.+$' })) { Invoke-Checked $Php @('artisan', 'key:generate', '--no-interaction', '--force') }
        if (!(Test-Path -LiteralPath "$StateDirectory/conversations.sqlite")) { New-Item -ItemType File -Path "$StateDirectory/conversations.sqlite" | Out-Null }
        Invoke-Checked $Php @('artisan', 'migrate', '--force', '--no-interaction')
        Invoke-Checked "$NodeDirectory/npm.cmd" @('run', 'build')
    } finally { Pop-Location }
    if (!(Test-Path -LiteralPath $VisualizationPython)) { Invoke-Checked $Python @('-m', 'venv', "$AppRoot/visualization/.venv") }
    if (!$SkipInstall) {
        Invoke-Checked $VisualizationPython @('-m', 'pip', 'install', '-r', "$AppRoot/visualization/requirements.lock")
        Invoke-Checked $VisualizationPython @('-m', 'pip', 'install', '--no-deps', '--no-build-isolation', '-e', "$AppRoot/visualization")
    }
} finally { $env:PATH = $previousPath; $env:TEMP = $previousTemp; $env:TMP = $previousTmp; $env:DB_DATABASE = $previousDatabase }
Write-Output '설치 완료. Start.ps1로 로컬 웹과 분석 API를 시작하세요. AWS 배포·DB 데이터 변경은 수행하지 않았습니다.'
