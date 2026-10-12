param(
    [string]$Profile = 'poc-practice',
    [string]$Region = 'ap-northeast-1',
    [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId
)
. "$PSScriptRoot\Aws-Common.ps1"
$null = Assert-PocAccount
$outputs = Get-PocOutputs 'poc-practice-app'
foreach ($pair in @(@('poc-chatbot',$outputs.ChatbotRoleArn), @('poc-worker',$outputs.WorkerRoleArn))) {
    foreach ($setting in @(@('role_arn',$pair[1]), @('source_profile','poc-local-login'), @('region',$Region), @('output','json'), @('role_session_name',$pair[0]))) {
        & $script:AwsExe configure set $setting[0] $setting[1] --profile $pair[0]
        if ($LASTEXITCODE -ne 0) { throw 'Role profile configuration failed' }
    }
}
$envPath = Join-Path $script:ProjectRoot '.local\app.env'
if (-not (Test-Path -LiteralPath $envPath)) { throw 'Run local Setup.ps1 first; DB credentials will not be generated or replaced here.' }
$lines = [Collections.Generic.List[string]]::new()
foreach ($line in [IO.File]::ReadAllLines($envPath)) { $lines.Add($line) }
$settings = @{POC_AGENT_ARN=$outputs.AgentArn; POC_QUEUE_URL=$outputs.QueueUrl; POC_RESULT_TABLE=$outputs.ResultTable; POC_AWS_ACCOUNT_ID=$ExpectedAccountId; POC_CHATBOT_PROFILE='poc-chatbot'; POC_WORKER_PROFILE='poc-worker'}
foreach ($key in $settings.Keys) {
    for ($i=$lines.Count-1; $i -ge 0; $i--) { if ($lines[$i] -match "^$key=") { $lines.RemoveAt($i) } }
    $lines.Add("$key=$($settings[$key])")
}
[IO.File]::WriteAllLines($envPath, $lines, [Text.UTF8Encoding]::new($false))
Write-PocJson (Join-Path $script:ProjectRoot '.local\aws-deploy\app-outputs.json') $outputs
foreach ($localProfile in @('poc-local-login','poc-chatbot','poc-worker')) {
    $identity = & $script:AwsExe sts get-caller-identity --profile $localProfile --region $Region --output json --no-cli-pager | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0 -or $identity.Account -ne $ExpectedAccountId -or $identity.Arn.EndsWith(':root')) { throw "Invalid local identity: $localProfile" }
    Write-Output "$localProfile -> $($identity.Arn)"
}
Write-Output 'Local AWS configuration updated. Existing DB connection and server token were preserved.'
