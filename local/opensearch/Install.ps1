$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$env:PYTHONUTF8 = '1'
& "$ProjectRoot/.venv/Scripts/python.exe" "$PSScriptRoot/install.py"
if ($LASTEXITCODE) { throw 'OpenSearch 설치 실패' }
