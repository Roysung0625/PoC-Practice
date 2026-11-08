param([string]$AdminSecret = '', [string]$Database = 'poc_idempiere')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'プロジェクトの Python 仮想環境を先に準備してください。' }
$arguments = @((Join-Path $PSScriptRoot 'setup.py'), '--database', $Database)
if ($AdminSecret) { $arguments += @('--admin-secret', $AdminSecret) }
& $python @arguments
if ($LASTEXITCODE -ne 0) { throw '登録 DB の準備に失敗しました。' }
