param(
    [string]$Profile = 'poc-practice',
    [string]$Region = 'ap-northeast-1',
    [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId,
    [switch]$SkipPackage
)
. "$PSScriptRoot\Aws-Common.ps1"
$null = Assert-PocAccount
$bootstrap = Get-PocOutputs 'poc-practice-bootstrap'
if (-not $SkipPackage) {
    & "$script:ProjectRoot\.venv\Scripts\python.exe" "$PSScriptRoot\package_runtime.py"
    if ($LASTEXITCODE -ne 0) { throw 'ARM64 packaging failed' }
}
$build = Join-Path $script:ProjectRoot '.local\aws-deploy'
$packages = Get-Content -Raw -LiteralPath "$build\packages.json" | ConvertFrom-Json
foreach ($artifact in @(@('agent.zip',$packages.AgentKey), @('sql-tool.zip',$packages.LambdaKey))) {
    $null = Invoke-PocAws @('s3api','put-object','--bucket',$bootstrap.ArtifactBucket,'--key',$artifact[1],'--body',(Join-Path $build $artifact[0]),'--server-side-encryption','AES256')
}
$template = Join-Path $script:ProjectRoot 'aws\infra\application.json'
$null = Invoke-PocAws @('cloudformation','validate-template','--template-body',"file://$template")
& $script:AwsExe cloudformation deploy --stack-name poc-practice-app --template-file $template --capabilities CAPABILITY_NAMED_IAM --disable-rollback --no-fail-on-empty-changeset --parameter-overrides "ArtifactBucket=$($bootstrap.ArtifactBucket)" "AgentKey=$($packages.AgentKey)" "LambdaKey=$($packages.LambdaKey)" "LoginUserArn=$($bootstrap.LoginUserArn)" --profile $Profile --region $Region --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw 'Application CloudFormation deployment failed' }
$outputs = Get-PocOutputs 'poc-practice-app'
Write-PocJson "$build\app-outputs.json" $outputs
# AgentCore creates its log group during provisioning; setting retention avoids a CFN name collision.
$null = Invoke-PocAws @('logs','put-retention-policy','--log-group-name',$outputs.AgentLogGroup,'--retention-in-days','7')
$groups = Invoke-PocAws @('logs','describe-log-groups','--log-group-name-prefix','/aws/bedrock-agentcore/runtimes/poc_sql_agent-')
foreach ($group in $groups.logGroups) {
    if ($group.retentionInDays -ne 7) {
        $null = Invoke-PocAws @('logs','put-retention-policy','--log-group-name',$group.logGroupName,'--retention-in-days','7')
    }
}
$outputs | ConvertTo-Json
