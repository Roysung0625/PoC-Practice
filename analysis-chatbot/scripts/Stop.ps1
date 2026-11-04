param([ValidateSet('all','api','web','receiver')][string]$Role='all')
. "$PSScriptRoot/Common.ps1"
$records = @(Read-Processes)
$selected = @($records | Where-Object { $Role -eq 'all' -or $_.role -eq $Role })
[array]::Reverse($selected)
foreach ($record in $selected) {
    if (Test-OwnedProcess $record) {
        & "$env:SystemRoot/System32/taskkill.exe" /PID $record.pid /T /F 2>$null | Out-Null
        Wait-Process -Id $record.pid -Timeout 5 -ErrorAction SilentlyContinue
    }
}
Save-Processes @($records | Where-Object { Test-OwnedProcess $_ })
Write-Output '이 실행 스크립트가 시작한 프로세스만 중지했습니다. 재사용한 API·수신기와 PostgreSQL 서비스는 유지합니다.'
