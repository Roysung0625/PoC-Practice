. "$PSScriptRoot/Common.ps1"
# 공식 Windows PHP 8.5.12-1 NTS x64 재빌드. 글로벌 PHP/PATH를 바꾸지 않는다.
$fileName = 'php-8.5.12-1-nts-Win32-vs17-x64.zip'
$expectedHash = '2a36a2edcb7a5b9252f638fd5e4cf84d7f6e066092654220dc0b63e5cf4e9723'
$downloadDirectory = Join-Path $ProjectRoot '.local/downloads'
$archive = Join-Path $downloadDirectory $fileName
if (!(Test-Path -LiteralPath $Php)) {
    New-Item -ItemType Directory -Force $downloadDirectory, $PhpDirectory | Out-Null
    if (!(Test-Path -LiteralPath $archive)) {
        Invoke-WebRequest -Uri "https://downloads.php.net/~windows/releases/$fileName" -OutFile $archive
    }
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedHash) { throw 'PHP 설치 파일 SHA-256 불일치' }
    Expand-Archive -LiteralPath $archive -DestinationPath $PhpDirectory -Force
}
$ini = @"
[PHP]
extension_dir="$($PhpDirectory.Replace('\','/'))/ext"
extension=curl
extension=fileinfo
extension=mbstring
extension=openssl
extension=pdo_sqlite
extension=sqlite3
extension=zip
memory_limit=512M
max_execution_time=30
date.timezone=Asia/Tokyo
display_errors=Off
log_errors=On
expose_php=Off
"@
[System.IO.File]::WriteAllText((Join-Path $PhpDirectory 'php.ini'), $ini, [System.Text.UTF8Encoding]::new($false))
Invoke-Checked $Php @('-v')
