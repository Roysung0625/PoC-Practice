. "$PSScriptRoot/Common.ps1"
foreach ($record in @(Read-OwnedProcesses)) {
    [PSCustomObject]@{Role=$record.role; Pid=$record.pid; OwnedAndRunning=(Test-OwnedProcess $record)}
}
foreach ($url in @('http://127.0.0.1:9200/_cluster/health','http://127.0.0.1:9200/poc-product/_count','http://127.0.0.1:9200/poc-promotion/_count','http://127.0.0.1:5601/api/status')) {
    try { $response = Read-LocalHttp $url; Write-Output "$url : 응답 정상"; if ($null -ne $response.count) { Write-Output "문서 수: $($response.count)" } }
    catch { Write-Output "$url : 응답 실패" }
}
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 9200,9300,5601 } | Select-Object LocalAddress,LocalPort,OwningProcess
