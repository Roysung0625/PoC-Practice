param([string]$Instance='default', [ValidateSet('all','api','web','receiver')][string]$Role = 'all')
. "$PSScriptRoot/Common.ps1"
$records = @(Read-Processes | Where-Object { $Role -eq 'all' -or $_.role -eq $Role })
[array]::Reverse($records)
foreach ($record in $records) {
    if (Test-OwnedProcess $record) {
        # venv 실행기는 실제 Python 자식을 만든다. 확인된 시작 PID의 자식만 함께 종료한다.
        & "$env:SystemRoot/System32/taskkill.exe" /PID $record.pid /T /F 2>$null | Out-Null
        Wait-Process -Id $record.pid -Timeout 5 -ErrorAction SilentlyContinue
    }
}
Write-Output "프로젝트 프로세스 중지 범위: $Role. PostgreSQL Windows 서비스는 유지합니다."
