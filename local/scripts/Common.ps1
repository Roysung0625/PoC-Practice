$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (!(Get-Variable Instance -ErrorAction SilentlyContinue)) { $Instance = 'default' }
if ($Instance -notmatch '^[a-zA-Z0-9-]{1,40}$') { throw '잘못된 인스턴스 이름입니다.' }
$StateDirectory = if ($Instance -eq 'default') { Join-Path $ProjectRoot '.local' } else { Join-Path $ProjectRoot ".local/instances/$Instance" }
$RunFile = Join-Path $StateDirectory 'services.json'
$LogDirectory = Join-Path $StateDirectory 'logs'

function Read-Processes {
    if (Test-Path -LiteralPath $RunFile) { return @(Get-Content -LiteralPath $RunFile -Raw | ConvertFrom-Json) }
    return @()
}

function Test-OwnedProcess($Record) {
    $process = Get-Process -Id $Record.pid -ErrorAction SilentlyContinue
    return $process -and $process.Path -eq $Record.path -and $process.StartTime.ToUniversalTime().Ticks -eq ([datetime]$Record.started).ToUniversalTime().Ticks
}

function Save-Processes($Records) {
    ConvertTo-Json -InputObject @($Records) -Depth 4 | Set-Content -LiteralPath $RunFile -Encoding utf8
}

function Process-Record($Process, $Role) {
    $fresh = $null
    for ($attempt=0; $attempt -lt 20; $attempt++) {
        $fresh = Get-Process -Id $Process.Id -ErrorAction Stop
        if ($fresh.Path) { break }
        Start-Sleep -Milliseconds 50
    }
    if (!$fresh.Path) { throw '프로세스 실행 경로를 확인하지 못했습니다.' }
    return [PSCustomObject]@{role=$Role; pid=$fresh.Id; path=$fresh.Path; started=$fresh.StartTime.ToUniversalTime().ToString('o')}
}
