param([string]$Instance='default')
. "$PSScriptRoot/Common.ps1"
$records = @(Read-Processes)
$state = [ordered]@{}
foreach ($role in @('api','web','receiver')) {
    $owned = @($records | Where-Object { $_.role -eq $role -and (Test-OwnedProcess $_) })
    $state[$role] = @{running=($owned.Count -gt 0); pids=@($owned | ForEach-Object { $_.pid })}
}
$service = Get-Service -Name poc-postgresql-18 -ErrorAction SilentlyContinue
$state['postgresql'] = if ($service) { [string]$service.Status } else { 'unknown' }
$state['url'] = 'http://127.0.0.1:8000'
$state['logs'] = $LogDirectory
$state | ConvertTo-Json -Depth 5
