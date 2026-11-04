. "$PSScriptRoot/Common.ps1"
$records = @(Read-Processes)
$state = [ordered]@{}
foreach ($role in @('api','web','receiver')) {
    $owned = @($records | Where-Object { $_.role -eq $role -and (Test-OwnedProcess $_) })
    $state[$role] = @{owned_running=($owned.Count -gt 0); owned_pids=@($owned | ForEach-Object pid)}
}
$state['engine'] = Read-LocalJson 'http://127.0.0.1:8001/health'
$state['web_listening'] = Test-ListeningPort 8010
$state['shared_receiver_pids'] = @(Find-SharedReceiver | ForEach-Object pid)
$state['postgresql'] = [string](Get-Service -Name poc-postgresql-18 -ErrorAction SilentlyContinue).Status
$state['url'] = 'http://127.0.0.1:8010'
$state['logs'] = $LogDirectory
$state | ConvertTo-Json -Depth 8
