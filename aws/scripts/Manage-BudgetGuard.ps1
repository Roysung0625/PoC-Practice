[CmdletBinding()]
param(
    [ValidateSet('Status','Pause','Export','ReleaseIam','Rearm')][string]$Mode = 'Status',
    [string]$Profile = 'poc-practice',
    [string]$Region = 'ap-northeast-1',
    [string]$StackName = 'poc-account-budget-guard',
    [string]$BudgetName = 'My Zero-Spend Budget',
    [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId
)
$ErrorActionPreference = 'Stop'
$awsExe = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
if (-not (Test-Path -LiteralPath $awsExe)) { $awsExe = (Get-Command aws -ErrorAction Stop).Source }
function Invoke-AwsJson([string[]]$Arguments) {
    $result = & $awsExe @Arguments --profile $Profile --region $Region --output json --no-cli-pager
    if ($LASTEXITCODE -ne 0) { throw "AWS CLI failed: $($Arguments[0..1] -join ' ')" }
    if ($result) { return ($result | ConvertFrom-Json) }
}
$identity = Invoke-AwsJson @('sts','get-caller-identity')
if ($identity.Account -ne $ExpectedAccountId) { throw 'Wrong AWS account.' }
$stack = (Invoke-AwsJson @('cloudformation','describe-stacks','--stack-name',$StackName)).Stacks[0]
$outputs = @{}
foreach ($item in $stack.Outputs) { $outputs[$item.OutputKey] = $item.OutputValue }
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$outputDir = Join-Path $root '.local\budget-control\recovery'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
function Get-ControlObject([string]$Key) {
    $listing = Invoke-AwsJson @('s3api','list-objects-v2','--bucket',$outputs.StateBucket,'--prefix',$Key)
    if (-not ($listing.Contents | Where-Object { $_.Key -eq $Key })) { return $null }
    $path = Join-Path $outputDir $Key
    $null = Invoke-AwsJson @('s3api','get-object','--bucket',$outputs.StateBucket,'--key',$Key,$path)
    return (Get-Content -LiteralPath $path -Raw | ConvertFrom-Json)
}
if ($Mode -eq 'Status') {
    $budget = (Invoke-AwsJson @('budgets','describe-budget','--account-id',$identity.Account,'--budget-name',$BudgetName)).Budget
    $schedule = Invoke-AwsJson @('events','describe-rule','--name',$outputs.ScheduleName)
    $function = Invoke-AwsJson @('lambda','get-function-concurrency','--function-name',$outputs.FunctionName)
    $alarm = Invoke-AwsJson @('cloudwatch','describe-alarms','--alarm-names',$outputs.FailureAlarm)
    [ordered]@{Account=$identity.Account;ActualSpend=$budget.CalculatedSpend.ActualSpend;Schedule=$schedule.State;
        FunctionConcurrency=$function;Latch=(Get-ControlObject 'latch.json');Pause=(Get-ControlObject 'pause.json');
        Latest=(Get-ControlObject 'latest.json');FailureAlarm=$alarm.MetricAlarms[0].StateValue} | ConvertTo-Json -Depth 20
    return
}
if ($Mode -eq 'Pause') {
    $pausePath = Join-Path $outputDir 'pause.json'
    [IO.File]::WriteAllText($pausePath, (@{time=[DateTimeOffset]::UtcNow.ToString('o')} | ConvertTo-Json))
    $null = Invoke-AwsJson @('s3api','put-object','--bucket',$outputs.StateBucket,'--key','pause.json','--body',$pausePath)
    $null = Invoke-AwsJson @('events','disable-rule','--name',$outputs.ScheduleName)
    $null = Invoke-AwsJson @('lambda','put-function-concurrency','--function-name',$outputs.FunctionName,'--reserved-concurrent-executions','0')
    Write-Output 'Paused. Wait at least 11 minutes for existing invocations before ReleaseIam or Rearm.'
    return
}
if ($Mode -eq 'Export') {
    & $awsExe s3 sync "s3://$($outputs.StateBucket)/" $outputDir --profile $Profile --region $Region --only-show-errors --no-cli-pager
    if ($LASTEXITCODE -ne 0) { throw 'State export failed.' }
    Write-Output "Recovery records: $outputDir"
    return
}
$pause = Get-ControlObject 'pause.json'
if (-not $pause -or ([DateTimeOffset]::UtcNow - [DateTimeOffset]::Parse($pause.time)).TotalSeconds -lt 660) {
    throw 'Pause the guard and wait at least 11 minutes before changing cutoff or restoring service.'
}
$entities = Invoke-AwsJson @('iam','list-entities-for-policy','--policy-arn',$outputs.DenyPolicyArn)
if ($Mode -eq 'ReleaseIam') {
    foreach ($role in $entities.PolicyRoles) {
        $null = Invoke-AwsJson @('iam','detach-role-policy','--role-name',$role.RoleName,'--policy-arn',$outputs.DenyPolicyArn)
    }
    foreach ($user in $entities.PolicyUsers) {
        $null = Invoke-AwsJson @('iam','detach-user-policy','--user-name',$user.UserName,'--policy-arn',$outputs.DenyPolicyArn)
    }
    Write-Output 'Only the budget guard policy was detached. Restore selected resources from snapshots; guard remains paused.'
    return
}
if ($entities.PolicyRoles -or $entities.PolicyUsers -or $entities.PolicyGroups) { throw 'Release the guard IAM policy before rearming.' }
$budget = (Invoke-AwsJson @('budgets','describe-budget','--account-id',$identity.Account,'--budget-name',$BudgetName)).Budget
if ($budget.CalculatedSpend.ActualSpend.Unit -ne 'USD' -or [decimal]$budget.CalculatedSpend.ActualSpend.Amount -gt 25) {
    throw 'Actual budget spend remains above USD25. Rearming would immediately cut off again.'
}
$null = Invoke-AwsJson @('s3api','delete-object','--bucket',$outputs.StateBucket,'--key','latch.json')
$null = Invoke-AwsJson @('s3api','delete-object','--bucket',$outputs.StateBucket,'--key','pause.json')
$null = Invoke-AwsJson @('lambda','delete-function-concurrency','--function-name',$outputs.FunctionName)
$null = Invoke-AwsJson @('events','enable-rule','--name',$outputs.ScheduleName)
Write-Output 'Guard rearmed. Historical recovery records remain in the versioned S3 bucket.'
