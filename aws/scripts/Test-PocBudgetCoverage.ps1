param([string]$Profile='poc-practice', [string]$Region='ap-northeast-1', [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId)
. "$PSScriptRoot\Aws-Common.ps1"
$null = Assert-PocAccount
$guard = Get-PocOutputs 'poc-account-budget-guard'
$directory = Join-Path $script:ProjectRoot '.local\aws-deploy\verification'
$null = New-Item -ItemType Directory -Force -Path $directory
$payload = Join-Path $directory 'budget-dry-run-input.json'
$resultPath = Join-Path $directory 'budget-dry-run.json'
Write-PocJson $payload @{dry_run=$true}
$response = Invoke-PocAws @('lambda','invoke','--function-name',$guard.FunctionName,'--cli-binary-format','raw-in-base64-out','--payload',"file://$payload",'--cli-read-timeout','900',$resultPath)
if ($response.FunctionError) { throw 'Budget dry-run Lambda failed. Inspect the local verification file.' }
$report = Get-Content -Raw -LiteralPath $resultPath | ConvertFrom-Json
if ($report.status -ne 'dry_run' -or $report.errors.Count -gt 0) { throw 'Budget dry-run is incomplete' }
$planned = $report.planned | ConvertTo-Json -Depth 20
foreach ($name in @('poc-local-login','poc-chatbot','poc-worker','poc-agent-runtime','poc-sql-tool')) {
    if (-not $planned.Contains($name)) { throw "Missing cutoff target: $name" }
}
if (-not ($report.planned | Where-Object { $_.service -eq 'lambda' -and $_.params.FunctionName -eq 'poc-sql-tool' })) { throw 'SQL Lambda cutoff action is missing' }
[ordered]@{Status=$report.status; Applied=$report.applied.Count; ActualSpend=$report.actual; PocTargets=@($report.planned | Where-Object { $_.id -match 'poc-' })} | ConvertTo-Json -Depth 12
