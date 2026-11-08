param([switch]$Receiver)
. "$PSScriptRoot/Common.ps1"
New-Item -ItemType Directory -Force $LogDirectory | Out-Null
foreach ($required in @($Php, $Python, $VisualizationPython, "$AppRoot/.env", "$AppRoot/public/build/manifest.json", "$ProjectRoot/.local/app.env")) {
    if (!(Test-Path -LiteralPath $required)) { throw "설치가 필요합니다: $required" }
}
# 두 앱은 기존 journal 하나를 공유한다. 호출자의 격리 테스트 환경을 상속하지 않는다.
$previousEnvironment = @{}
foreach ($name in @('PYTHONUTF8','POC_JOURNAL_PATH','POC_API_URL','PYTHON_API_URL','DB_DATABASE')) { $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
try {
$env:PYTHONUTF8 = '1'
$env:POC_JOURNAL_PATH = Join-Path $ProjectRoot '.local/jobs.sqlite'
$env:POC_API_URL = 'http://127.0.0.1:8001'
$env:PYTHON_API_URL = 'http://127.0.0.1:8001'
$env:DB_DATABASE = Join-Path $StateDirectory 'conversations.sqlite'
$records = @(Read-Processes | Where-Object { Test-OwnedProcess $_ })
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$specs = @()
if (Test-ListeningPort 8001) {
    $health = Read-LocalJson 'http://127.0.0.1:8001/health'
    if (!$health -or $health.analysis_contract_version -ne 1 -or $health.product_registration_contract_version -ne 1) { throw '8001의 기존 API가 현재 분석·상품 등록 계약을 지원하지 않습니다. 해당 API를 소유한 실행 스크립트로 재시작하세요.' }
    Write-Output '기존 Python API를 재사용합니다.'
} else {
    $specs += @{role='api'; executable=$Python; arguments='-m uvicorn poc.api:create_app --factory --host 127.0.0.1 --port 8001 --workers 1'; directory=$ProjectRoot; url='http://127.0.0.1:8001/health'}
}
if (Test-ListeningPort 8010) {
    if (!@($records | Where-Object role -eq 'web').Count) { throw '8010을 다른 프로세스가 사용 중입니다.' }
    Write-Output '기존 분석 챗봇 웹을 재사용합니다.'
} else {
    $specs += @{role='web'; executable=$Php; arguments="-S 127.0.0.1:8010 -t `"$AppRoot/public`" `"$AppRoot/vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php`""; directory="$AppRoot/public"; url='http://127.0.0.1:8010/'}
}
if ($Receiver) {
    if (@(Find-SharedReceiver).Count) { Write-Output '기존 SQS 수신기를 재사용합니다.' }
    else {
        # 수동 실행한 수신기도 찾는다. 확인 불가 상태에서 두 번째 수신기를 시작하지 않는다.
        $manualReceivers = @(Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Where-Object { $_.CommandLine -match '(?i)-m\s+poc\.receiver(?:\s|$)' })
        if ($manualReceivers.Count) { Write-Output '수동 실행된 SQS 수신기를 재사용합니다. 중지 권한을 가져오지 않습니다.' }
        else { $specs += @{role='receiver'; executable=$Python; arguments='-m poc.receiver'; directory=$ProjectRoot; url=$null} }
    }
}
foreach ($spec in $specs) {
    $records = @($records | Where-Object role -ne $spec.role)
    $process = Start-Process -FilePath $spec.executable -ArgumentList $spec.arguments -WorkingDirectory $spec.directory -WindowStyle Hidden -PassThru -RedirectStandardOutput "$LogDirectory/$($spec.role)-$stamp.out.log" -RedirectStandardError "$LogDirectory/$($spec.role)-$stamp.err.log"
    try { $records += Process-Record $process $spec.role } catch { $process.Kill(); throw }
    Save-Processes $records
    if ($spec.url) {
        $ready = $false
        $until = [DateTime]::UtcNow.AddSeconds(25)
        while ([DateTime]::UtcNow -lt $until) {
            if (Read-LocalJson $spec.url -StatusOnly) { $ready = $true; break }
            if ($process.HasExited) { break }
            Start-Sleep -Milliseconds 250
        }
        if (!$ready) { throw "$($spec.role) 시작 실패. $LogDirectory 로그를 확인하세요." }
    } else {
        Start-Sleep -Milliseconds 800
        if ($process.HasExited) { throw '수신기 시작 실패. 인증 및 로그를 확인하세요.' }
    }
    Write-Output "$($spec.role) 시작 완료"
}
Write-Output '분석 챗봇: http://127.0.0.1:8010'
} finally {
    foreach ($name in $previousEnvironment.Keys) { [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], 'Process') }
}
