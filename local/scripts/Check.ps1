. "$PSScriptRoot/Common.ps1"
& "$PSScriptRoot/Status.ps1"
try {
    Invoke-RestMethod 'http://127.0.0.1:8001/health' -TimeoutSec 5 | ConvertTo-Json -Depth 5
    $response = Invoke-WebRequest 'http://127.0.0.1:8000/' -UseBasicParsing -TimeoutSec 5
    Write-Output "웹 HTTP 상태: $($response.StatusCode)"
} catch { throw '로컬 앱 연결 실패. Start.ps1과 로그를 확인하세요.' }
