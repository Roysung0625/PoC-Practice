$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$AppRoot = Join-Path $ProjectRoot 'analysis-chatbot'
$StateDirectory = Join-Path $ProjectRoot '.local/analysis-chatbot'
$LogDirectory = Join-Path $StateDirectory 'logs'
$RunFile = Join-Path $StateDirectory 'services.json'
$PhpDirectory = Join-Path $ProjectRoot '.local/runtime/php-8.5.12'
$Php = Join-Path $PhpDirectory 'php.exe'
$Python = Join-Path $ProjectRoot '.venv/Scripts/python.exe'
$NodeDirectory = Join-Path $ProjectRoot '.local/runtime/node-v24.20.0-win-x64'
$VisualizationPython = Join-Path $AppRoot 'visualization/.venv/Scripts/python.exe'

function Read-Processes {
    if (Test-Path -LiteralPath $RunFile) { return @(Get-Content -LiteralPath $RunFile -Raw | ConvertFrom-Json) }
    return @()
}

function Test-OwnedProcess($Record) {
    $process = Get-Process -Id $Record.pid -ErrorAction SilentlyContinue
    return $process -and $process.Path -eq $Record.path -and $process.StartTime.ToUniversalTime().Ticks -eq ([datetime]$Record.started).ToUniversalTime().Ticks
}

function Save-Processes($Records) {
    New-Item -ItemType Directory -Force $StateDirectory | Out-Null
    ConvertTo-Json -InputObject @($Records) -Depth 5 | Set-Content -LiteralPath $RunFile -Encoding utf8
}

function Process-Record($Process, $Role) {
    for ($attempt=0; $attempt -lt 20; $attempt++) {
        $fresh = Get-Process -Id $Process.Id -ErrorAction Stop
        if ($fresh.Path) { return [PSCustomObject]@{role=$Role; pid=$fresh.Id; path=$fresh.Path; started=$fresh.StartTime.ToUniversalTime().ToString('o')} }
        Start-Sleep -Milliseconds 50
    }
    throw '프로세스 소유권을 확인하지 못했습니다.'
}

function Read-LocalJson($Url, [switch]$StatusOnly) {
    $handler = [System.Net.Http.HttpClientHandler]::new()
    $handler.UseProxy = $false
    $client = [System.Net.Http.HttpClient]::new($handler)
    $client.Timeout = [TimeSpan]::FromSeconds(3)
    try {
        $response = $client.GetAsync($Url).GetAwaiter().GetResult()
        try {
            if (!$response.IsSuccessStatusCode) { return $null }
            if ($StatusOnly) { return $true }
            return ($response.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json)
        } finally { $response.Dispose() }
    } catch { return $null } finally { $client.Dispose(); $handler.Dispose() }
}

function Test-ListeningPort([int]$Port) {
    return @([System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | Where-Object Port -eq $Port).Count -gt 0
}

function Find-SharedReceiver {
    # 기존 실행 스크립트의 소유권 기록을 먼저 조회한다. PID만 일치하는 다른 프로세스는 재사용하지 않는다.
    $legacyFile = Join-Path $ProjectRoot '.local/services.json'
    $found = @()
    if (Test-Path -LiteralPath $legacyFile) {
        $found += @(Get-Content -LiteralPath $legacyFile -Raw | ConvertFrom-Json | Where-Object { $_.role -eq 'receiver' -and (Test-OwnedProcess $_) })
    }
    $found += @(Read-Processes | Where-Object { $_.role -eq 'receiver' -and (Test-OwnedProcess $_) })
    return @($found)
}

function Invoke-Checked($Executable, [string[]]$Arguments) {
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "명령 실패: $Executable (exit $LASTEXITCODE)" }
}
