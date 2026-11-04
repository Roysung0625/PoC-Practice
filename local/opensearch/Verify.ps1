param([switch]$Faults)
. "$PSScriptRoot/Common.ps1"
$arguments = @("$PSScriptRoot/verify.py")
if ($Faults) { $arguments += '--faults' }
& "$ProjectRoot/.venv/Scripts/python.exe" @arguments
if ($LASTEXITCODE) { throw 'OpenSearch 검증 실패' }
$listeners = @(Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 9200,9300,5601 })
if (@($listeners | Where-Object { $_.LocalAddress -ne '127.0.0.1' }).Count) { throw '루프백 이외 주소에서 수신 중입니다.' }
if (@($listeners.LocalPort | Sort-Object -Unique).Count -ne 3) { throw '예상 포트가 모두 열리지 않았습니다.' }
$listeners | Select-Object LocalAddress,LocalPort,OwningProcess | ConvertTo-Json | Set-Content "$StateDirectory/listeners.json" -Encoding utf8
Write-Output '9200/9300/5601: 모두 127.0.0.1 전용'
