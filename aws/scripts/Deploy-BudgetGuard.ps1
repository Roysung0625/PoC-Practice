[CmdletBinding()]
param(
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
$identity = Invoke-AwsJson @('sts', 'get-caller-identity')
if ($identity.Account -ne $ExpectedAccountId) { throw 'AWS account does not match ExpectedAccountId.' }
$budget = (Invoke-AwsJson @('budgets', 'describe-budget', '--account-id', $identity.Account, '--budget-name', $BudgetName)).Budget
if ($budget.TimeUnit -ne 'MONTHLY' -or $budget.BudgetLimit.Amount -ne '25.0' -and [decimal]$budget.BudgetLimit.Amount -ne 25 -or $budget.BudgetLimit.Unit -ne 'USD' -or $budget.CostFilters.PSObject.Properties.Count -gt 0 -or $budget.FilterExpression) {
    throw 'Expected an unfiltered account-wide monthly USD25 budget.'
}
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$outputDir = Join-Path $root '.local\budget-control'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$template = Get-Content (Join-Path $PSScriptRoot '..\budget_guard\template.json') -Raw | ConvertFrom-Json
$template.Resources.GuardFunction.Properties.Code.ZipFile = Get-Content (Join-Path $PSScriptRoot '..\budget_guard\guard.py') -Raw
$templatePath = Join-Path $outputDir 'guard-template.json'
[IO.File]::WriteAllText($templatePath, ($template | ConvertTo-Json -Depth 100), [Text.UTF8Encoding]::new($false))
$null = Invoke-AwsJson @('cloudformation', 'validate-template', '--template-body', "file://$templatePath")
& $awsExe cloudformation deploy --profile $Profile --region $Region --stack-name $StackName --template-file $templatePath --capabilities CAPABILITY_NAMED_IAM --parameter-overrides "BudgetName=$BudgetName" --no-fail-on-empty-changeset --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw 'CloudFormation deployment failed.' }
$stack = (Invoke-AwsJson @('cloudformation', 'describe-stacks', '--stack-name', $StackName)).Stacks[0]
$outputs = @{}
foreach ($item in $stack.Outputs) { $outputs[$item.OutputKey] = $item.OutputValue }
$outputs | ConvertTo-Json | Set-Content (Join-Path $outputDir 'stack-outputs.json') -Encoding utf8
$notifications = (Invoke-AwsJson @('budgets', 'describe-notifications-for-budget', '--account-id', $identity.Account, '--budget-name', $BudgetName)).Notifications
$notifications | ConvertTo-Json -Depth 15 | Set-Content (Join-Path $outputDir 'notifications-before.json') -Encoding utf8
$notification = @{NotificationType='ACTUAL';ComparisonOperator='GREATER_THAN';Threshold=25;ThresholdType='ABSOLUTE_VALUE'}
$existing = $notifications | Where-Object { $_.NotificationType -eq 'ACTUAL' -and $_.ComparisonOperator -eq 'GREATER_THAN' -and $_.Threshold -eq 25 -and $_.ThresholdType -eq 'ABSOLUTE_VALUE' }
$request = @{AccountId=$identity.Account;BudgetName=$BudgetName;Notification=$notification}
if ($existing) {
    $requestPath = Join-Path $outputDir 'subscriber-request.json'
    $queryPath = Join-Path $outputDir 'notification-query.json'
    [IO.File]::WriteAllText($queryPath, ($request | ConvertTo-Json -Depth 10))
    $subscribers = (Invoke-AwsJson @('budgets', 'describe-subscribers-for-notification', '--cli-input-json', "file://$queryPath")).Subscribers
    if (-not ($subscribers | Where-Object { $_.Address -eq $outputs.TopicArn })) {
        $request.Subscriber = @{SubscriptionType='SNS';Address=$outputs.TopicArn}
        [IO.File]::WriteAllText($requestPath, ($request | ConvertTo-Json -Depth 10))
        $null = Invoke-AwsJson @('budgets', 'create-subscriber', '--cli-input-json', "file://$requestPath")
    }
} else {
    $request.Subscribers = @(@{SubscriptionType='SNS';Address=$outputs.TopicArn})
    $requestPath = Join-Path $outputDir 'notification-request.json'
    [IO.File]::WriteAllText($requestPath, ($request | ConvertTo-Json -Depth 10))
    $null = Invoke-AwsJson @('budgets', 'create-notification', '--cli-input-json', "file://$requestPath")
}
Write-Output ($outputs | ConvertTo-Json)
