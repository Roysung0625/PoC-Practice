#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$StateDirectory = Join-Path $ProjectRoot '.local/opensearch'
$RunFile = Join-Path $StateDirectory 'processes.json'
$LogDirectory = Join-Path $StateDirectory 'logs'
$env:PYTHONUTF8 = '1'

function Read-OwnedProcesses {
    if (Test-Path -LiteralPath $RunFile) { return @(Get-Content -LiteralPath $RunFile -Raw | ConvertFrom-Json) }
    return @()
}
function Test-OwnedProcess($Record) {
    $process = Get-Process -Id $Record.pid -ErrorAction SilentlyContinue
    return $process -and $process.Path -eq $Record.path -and $process.StartTime.ToUniversalTime().Ticks -eq ([datetime]$Record.started).ToUniversalTime().Ticks
}
function Get-ProcessRecord($Process, $Role) {
    return [PSCustomObject]@{role=$Role; pid=$Process.Id; path=$Process.Path; started=$Process.StartTime.ToUniversalTime().ToString('o')}
}
function Save-OwnedProcesses($Records) {
    ConvertTo-Json -InputObject @($Records) -Depth 5 | Set-Content -LiteralPath $RunFile -Encoding utf8
}
function Read-LocalHttp($Url) {
    $handler = [System.Net.Http.HttpClientHandler]::new()
    $handler.UseProxy = $false
    $client = [System.Net.Http.HttpClient]::new($handler)
    $client.Timeout = [TimeSpan]::FromSeconds(4)
    try {
        $response = $client.GetAsync($Url).GetAwaiter().GetResult()
        if (!$response.IsSuccessStatusCode) { throw "HTTP $($response.StatusCode)" }
        return $response.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json
    } finally { $client.Dispose(); $handler.Dispose() }
}
