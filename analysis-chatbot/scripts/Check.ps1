. "$PSScriptRoot/Common.ps1"
$health = Read-LocalJson 'http://127.0.0.1:8001/health'
if (!$health) { throw 'Python API에 연결할 수 없습니다.' }
if (!$health.db_connected) { throw 'PostgreSQL 읽기 연결 실패' }
if ($health.analysis_contract_version -ne 1) { throw '분석 API 계약 버전 불일치' }
if (!(Test-ListeningPort 8010)) { throw '챗봇 웹이 실행 중이지 않습니다.' }
Invoke-Checked $Php @('-r', 'echo PHP_VERSION, PHP_EOL;')
Invoke-Checked $VisualizationPython @('-c', 'import matplotlib; print("Matplotlib " + matplotlib.__version__)')
Write-Output '로컬 API·DB·웹·가시화 실행환경 확인 완료. AWS 왕복 성공을 뜻하지 않습니다.'
