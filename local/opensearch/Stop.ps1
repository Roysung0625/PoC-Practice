. "$PSScriptRoot/Common.ps1"
$records = @(Read-OwnedProcesses)
# 먼저 우리가 시작한 launcher의 자식 트리를 종료한다. PID뿐 아니라 경로와 시작 시각을 확인한다.
foreach ($record in $records) {
    if (Test-OwnedProcess $record) {
        $process = Get-Process -Id $record.pid
        $process.Kill($true)
        $process.WaitForExit(10000) | Out-Null
        Write-Output "$($record.role): 중지"
    }
}
$remaining = @($records | Where-Object { Test-OwnedProcess $_ })
Save-OwnedProcesses $remaining
if ($remaining.Count) { throw '일부 프로세스가 아직 실행 중입니다.' }
