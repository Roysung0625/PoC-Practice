. "$PSScriptRoot/Common.ps1"
$verifyInstance = 'browser-' + [guid]::NewGuid().ToString('N').Substring(0,8)
$env:Path = "$ProjectRoot/.local/runtime/node-v24.20.0-win-x64;$env:Path"
$env:PLAYWRIGHT_BROWSERS_PATH = "$ProjectRoot/.local/playwright-browsers"
$env:POC_E2E_URL = 'http://127.0.0.1:18002'
Remove-Item Env:NO_COLOR -ErrorAction SilentlyContinue
try {
    & "$PSScriptRoot/Start.ps1" -Instance $verifyInstance -ApiPort 18003 -WebPort 18002
    Push-Location "$ProjectRoot/local/web"
    try {
        & "$ProjectRoot/.local/runtime/node-v24.20.0-win-x64/npm.cmd" run e2e
        if ($LASTEXITCODE) { throw '브라우저 종단 시험 실패' }
    } finally { Pop-Location }
} finally {
    & "$PSScriptRoot/Stop.ps1" -Instance $verifyInstance
}
