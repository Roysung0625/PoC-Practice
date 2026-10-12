param([switch]$Activate)
. "$PSScriptRoot/Common.ps1"
$env:PYTHONUTF8 = '1'
$arguments = @('-m', 'poc.idempiere')
if ($Activate) { $arguments += '--activate' }
& "$ProjectRoot/.venv/Scripts/python.exe" @arguments
if ($LASTEXITCODE) { throw 'iDempiere 설치 실패. .local/datasets/idempiere/restore.log를 확인하세요.' }
