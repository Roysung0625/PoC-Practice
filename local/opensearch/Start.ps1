. "$PSScriptRoot/Common.ps1"
if (!(Test-Path "$StateDirectory/installation.json")) { throw '먼저 Install.ps1을 실행하세요.' }
New-Item -ItemType Directory -Force -Path $LogDirectory | Out-Null
$env:OPENSEARCH_JAVA_HOME = Join-Path $ProjectRoot '.local/os/jdk'
$env:OSD_NODE_HOME = Join-Path $ProjectRoot '.local/osd/node'
$records = @(Read-OwnedProcesses | Where-Object { Test-OwnedProcess $_ })
$specs = @(
    @{role='opensearch'; directory="$ProjectRoot/.local/os"; batch='opensearch.bat'; port=9200; url='http://127.0.0.1:9200'},
    @{role='dashboards'; directory="$ProjectRoot/.local/osd"; batch='opensearch-dashboards.bat'; port=5601; url='http://127.0.0.1:5601/api/status'}
)
foreach ($spec in $specs) {
    if (@($records | Where-Object { $_.role -eq $spec.role }).Count) {
        $null = Read-LocalHttp $spec.url
        Write-Output "$($spec.role): 이미 실행 중"
        continue
    }
    $listeners = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
    if (@($listeners | Where-Object { $_.Port -eq $spec.port }).Count) { throw "다른 프로세스가 포트 $($spec.port)를 사용 중입니다." }
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $batch = Join-Path $spec.directory "bin/$($spec.batch)"
    $arguments = '/d /s /c ""' + $batch + '""'
    $process = Start-Process -FilePath $env:ComSpec -ArgumentList $arguments -WorkingDirectory $spec.directory -WindowStyle Hidden -PassThru -RedirectStandardOutput "$LogDirectory/$($spec.role)-$stamp.out.log" -RedirectStandardError "$LogDirectory/$($spec.role)-$stamp.err.log"
    $records += Get-ProcessRecord $process "$($spec.role)-launcher"
    Save-OwnedProcesses $records
    $until = [DateTime]::UtcNow.AddSeconds(240)
    $nextReport = [DateTime]::UtcNow.AddSeconds(25)
    $ready = $false
    while ([DateTime]::UtcNow -lt $until) {
        try { $null = Read-LocalHttp $spec.url; $ready = $true; break } catch { }
        if ($process.HasExited) { break }
        if ([DateTime]::UtcNow -gt $nextReport) {
            Write-Output "$($spec.role): 시작 대기 중 (로그: $LogDirectory)"
            $nextReport = [DateTime]::UtcNow.AddSeconds(25)
        }
        Start-Sleep -Milliseconds 750
    }
    if (!$ready) { throw "$($spec.role) 준비 실패. 로그 확인 후 Stop.ps1로 정리하세요." }
    $connection = Get-NetTCPConnection -LocalPort $spec.port -State Listen | Select-Object -First 1
    $server = Get-Process -Id $connection.OwningProcess
    if (!$server.Path.StartsWith([IO.Path]::GetFullPath($spec.directory), [StringComparison]::OrdinalIgnoreCase)) { throw '실행 프로세스 경로가 예상과 다릅니다.' }
    $records += Get-ProcessRecord $server $spec.role
    Save-OwnedProcesses $records
    Write-Output "$($spec.role): 준비 완료 $($spec.url)"
}
