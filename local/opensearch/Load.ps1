param([ValidateSet('load','seed','index','dashboards')][string]$Action='load')
. "$PSScriptRoot/Common.ps1"
& "$ProjectRoot/.venv/Scripts/python.exe" "$PSScriptRoot/search_lab.py" $Action
if ($LASTEXITCODE) { throw '더미 생성/색인 실패. 오류를 해결한 뒤 같은 명령으로 재실행하세요.' }
