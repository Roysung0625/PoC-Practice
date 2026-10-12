param([switch]$Receiver, [string]$Instance='default', [int]$ApiPort=8001, [int]$WebPort=8000, [ValidateSet('all','api','web')][string]$Components='all')
. "$PSScriptRoot/Common.ps1"
New-Item -ItemType Directory -Force $LogDirectory | Out-Null
if (!(Test-Path "$ProjectRoot/.local/app.env")) { throw '먼저 Setup.ps1로 데이터와 환경을 구성하세요.' }
if (!(Test-Path "$ProjectRoot/local/web/public/build/manifest.json")) { throw '웹 빌드가 필요합니다. Setup.ps1을 실행하세요.' }
$records = @(Read-Processes)
$env:PYTHONUTF8 = '1'
if ($Instance -ne 'default') {
    $env:POC_JOURNAL_PATH = Join-Path $StateDirectory 'jobs.sqlite'
    $env:DB_DATABASE = Join-Path $StateDirectory 'web.sqlite'
    if (!(Test-Path -LiteralPath $env:DB_DATABASE)) {
        New-Item -ItemType File -Path $env:DB_DATABASE | Out-Null
        & "$ProjectRoot/.local/runtime/php/php.exe" "$ProjectRoot/local/web/artisan" migrate --force --no-interaction
        if ($LASTEXITCODE) { throw '격리된 웹 상태 DB 구성 실패' }
    }
}
$env:POC_API_URL = "http://127.0.0.1:$ApiPort"
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$web = Join-Path $ProjectRoot 'local/web'
$specs = @(
    @{role='api'; port=$ApiPort; executable="$ProjectRoot/.venv/Scripts/python.exe"; arguments="-m uvicorn poc.api:create_app --factory --host 127.0.0.1 --port $ApiPort --workers 1"; directory=$ProjectRoot; url="http://127.0.0.1:$ApiPort/docs"},
    @{role='web'; port=$WebPort; executable="$ProjectRoot/.local/runtime/php/php.exe"; arguments="-d max_execution_time=195 -S 127.0.0.1:$WebPort -t `"$web/public`" `"$web/vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php`""; directory="$web/public"; url="http://127.0.0.1:$WebPort/up"}
)
if ($Components -ne 'all') { $specs = @($specs | Where-Object { $_.role -eq $Components }) }
if ($Receiver) {
    $specs += @{role='receiver'; port=0; executable="$ProjectRoot/.venv/Scripts/python.exe"; arguments='-m poc.receiver'; directory=$ProjectRoot; url=$null}
}
foreach ($spec in $specs) {
    if (@($records | Where-Object { $_.role -eq $spec.role -and (Test-OwnedProcess $_) }).Count) { continue }
    $listeners = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
    if ($spec.port -and @($listeners | Where-Object { $_.Port -eq $spec.port }).Count) { throw "포트 $($spec.port)가 다른 프로세스에서 사용 중입니다." }
    $records = @($records | Where-Object { $_.role -ne $spec.role })
    $process = Start-Process -FilePath $spec.executable -ArgumentList $spec.arguments -WorkingDirectory $spec.directory -WindowStyle Hidden -PassThru -RedirectStandardOutput "$LogDirectory/$($spec.role)-$stamp.out.log" -RedirectStandardError "$LogDirectory/$($spec.role)-$stamp.err.log"
    try { $records += Process-Record $process $spec.role }
    catch { $process.Kill(); throw }
    Save-Processes $records
    if ($spec.port) {
        $ready = $false
        $handler = [System.Net.Http.HttpClientHandler]::new()
        $handler.UseProxy = $false
        $client = [System.Net.Http.HttpClient]::new($handler)
        $client.Timeout = [TimeSpan]::FromSeconds(2)
        $until = [DateTime]::UtcNow.AddSeconds(25)
        try {
            while ([DateTime]::UtcNow -lt $until) {
                try {
                    $response = $client.GetAsync($spec.url).GetAwaiter().GetResult()
                    $ready = $response.IsSuccessStatusCode
                    $response.Dispose()
                    if ($ready) { break }
                } catch { }
                if ($process.HasExited) { break }
                Start-Sleep -Milliseconds 250
            }
        } finally { $client.Dispose(); $handler.Dispose() }
        if (!$ready) { throw "$($spec.role) 시작 실패. $LogDirectory 로그를 확인하세요." }
        Write-Output "$($spec.role) 준비 완료"
    } else {
        Start-Sleep -Milliseconds 800
        if ($process.HasExited) { throw '수신기가 종료되었습니다. AWS 설정·인증 로그를 확인하세요.' }
    }
}
Write-Output "로컬 앱: http://127.0.0.1:$WebPort"
