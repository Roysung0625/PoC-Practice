param([switch]$InstallPostgres)
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$cache = Join-Path $root '.local/downloads'
$runtime = Join-Path $root '.local/runtime'
New-Item -ItemType Directory -Force $cache, $runtime | Out-Null
function Get-CheckedFile($Url, $File, $Sha256) {
    if (!(Test-Path -LiteralPath $File)) { Invoke-WebRequest $Url -OutFile $File }
    if ((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash -ne $Sha256) { throw "다운로드 검증 실패: $File" }
}
$phpZip = Join-Path $cache 'php-8.4.25.zip'
Get-CheckedFile 'https://downloads.php.net/~windows/releases/archives/php-8.4.25-Win32-vs17-x64.zip' $phpZip '2cf521fb6bcb45b634c7e9a7ab2afb6d41698b987bbc73c4975d90a065e0f16c'
$phpDir = Join-Path $runtime 'php'
if (!(Test-Path "$phpDir/php.exe")) { Expand-Archive -LiteralPath $phpZip -DestinationPath $phpDir }
$ini = @"
[PHP]
extension_dir="$phpDir/ext"
extension=curl
extension=fileinfo
extension=mbstring
extension=openssl
extension=pdo_sqlite
extension=sqlite3
extension=zip
memory_limit=512M
date.timezone=Asia/Tokyo
"@
Set-Content -LiteralPath "$phpDir/php.ini" -Value $ini -Encoding utf8
$nodeVersion = '24.20.0'
$nodeName = "node-v$nodeVersion-win-x64.zip"
$sums = (Invoke-WebRequest "https://nodejs.org/dist/v$nodeVersion/SHASUMS256.txt").Content
$nodeHash = (($sums -split "`n" | Where-Object { $_ -match " $([regex]::Escape($nodeName))$" }) -split '\s+')[0]
if (!$nodeHash) { throw 'Node 해시를 확인할 수 없습니다.' }
Get-CheckedFile "https://nodejs.org/dist/v$nodeVersion/$nodeName" (Join-Path $cache $nodeName) $nodeHash
if (!(Test-Path "$runtime/node-v$nodeVersion-win-x64/node.exe")) { Expand-Archive -LiteralPath (Join-Path $cache $nodeName) -DestinationPath $runtime }
if (!(Test-Path "$runtime/composer.phar")) {
    $installer = Join-Path $cache 'composer-setup.php'
    Invoke-WebRequest 'https://getcomposer.org/installer' -OutFile $installer
    $signature = (Invoke-WebRequest 'https://composer.github.io/installer.sig').Content
    $expected = $(if ($signature -is [byte[]]) { [Text.Encoding]::UTF8.GetString($signature) } else { [string]$signature }).Trim()
    if ((Get-FileHash $installer -Algorithm SHA384).Hash -ne $expected) { throw 'Composer 해시 불일치' }
    & "$phpDir/php.exe" $installer "--install-dir=$runtime" '--filename=composer.phar'
    if ($LASTEXITCODE) { throw 'Composer 설치 실패' }
}
if ($InstallPostgres) {
    $pgExe = Join-Path $cache 'postgresql-18.6-5.exe'
    Get-CheckedFile 'https://get.enterprisedb.com/postgresql/postgresql-18.6-5-windows-x64.exe' $pgExe '227e2bc08091b4c2b8338c7d61b11d057f895711480b006f90bfcfcd2410a58a'
    $service = Get-Service -Name 'poc-postgresql-18' -ErrorAction SilentlyContinue
    if (!$service) {
        if (Test-Path 'C:/Program Files/PostgreSQL/18') { throw '기존 PostgreSQL 18 설치가 있습니다. 프로젝트 설치로 덮어쓰지 않습니다.' }
        $listeners = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
        if (@($listeners | Where-Object { $_.Port -eq 5432 }).Count) { throw '5432 포트를 기존 서비스가 사용 중입니다. 설치 대상을 먼저 분리하세요.' }
        $secrets = Join-Path $root '.local/secrets'
        New-Item -ItemType Directory -Force $secrets | Out-Null
        $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        & icacls $secrets /inheritance:r /grant:r "${identity}:(OI)(CI)F" 'SYSTEM:(OI)(CI)F' 'BUILTIN\Administrators:(OI)(CI)F' | Out-Null
        $secretPath = Join-Path $secrets 'postgres.json'
        if (!(Test-Path $secretPath)) {
            $secret = @{ password = [Convert]::ToHexString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)).ToLower() }
            $secret | ConvertTo-Json | Set-Content $secretPath -Encoding utf8
        }
        $secret = Get-Content $secretPath -Raw | ConvertFrom-Json
        $options = Join-Path $secrets 'postgres-options.txt'
        @"
mode=unattended
unattendedmodeui=none
prefix=C:\Program Files\PostgreSQL\18
datadir=$root\.local\postgres
serverport=5432
servicename=poc-postgresql-18
superpassword=$($secret.password)
disable-components=stackbuilder,pgAdmin
"@ | Set-Content $options -Encoding utf8
        try {
            $process = Start-Process -FilePath $pgExe -ArgumentList @('--optionfile', "`"$options`"") -WindowStyle Hidden -PassThru -Wait
            if ($process.ExitCode) { throw "PostgreSQL 설치 종료 코드: $($process.ExitCode)" }
        } finally { Remove-Item -LiteralPath $options -ErrorAction SilentlyContinue }
    }
    $configPath = Join-Path $root '.local/postgres/postgresql.conf'
    $content = Get-Content -LiteralPath $configPath -Raw
    $content = $content -replace "(?m)^listen_addresses\s*=.*$", "listen_addresses = '127.0.0.1'"
    Set-Content -LiteralPath $configPath -Value $content -Encoding utf8
    $restart = Start-Process powershell.exe -Verb RunAs -WindowStyle Hidden -Wait -PassThru -ArgumentList '-NoProfile -Command "Restart-Service -Name poc-postgresql-18 -ErrorAction Stop"'
    if ($restart.ExitCode) { throw 'PostgreSQL 로컬 수신 설정 재시작 실패' }
}
& "$phpDir/php.exe" --version
& "$runtime/node-v$nodeVersion-win-x64/node.exe" --version
