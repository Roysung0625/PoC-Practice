$ErrorActionPreference = 'Stop'
$script:AwsExe = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
if (-not (Test-Path -LiteralPath $script:AwsExe)) { $script:AwsExe = (Get-Command aws -ErrorAction Stop).Source }
$script:ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
function Invoke-PocAws([string[]]$Arguments) {
    $output = & $script:AwsExe @Arguments --profile $Profile --region $Region --output json --no-cli-pager
    if ($LASTEXITCODE -ne 0) { throw "AWS CLI failed: $($Arguments[0..1] -join ' ')" }
    if ($output) { return ($output | ConvertFrom-Json) }
}
function Assert-PocAccount {
    $identity = Invoke-PocAws @('sts','get-caller-identity')
    if ($identity.Account -ne $ExpectedAccountId) { throw 'AWS account mismatch.' }
    return $identity
}
function Get-PocOutputs([string]$Name) {
    $stack = (Invoke-PocAws @('cloudformation','describe-stacks','--stack-name',$Name)).Stacks[0]
    if ($stack.StackStatus -notin @('CREATE_COMPLETE','UPDATE_COMPLETE')) { throw "Stack is not ready: $($stack.StackStatus)" }
    $values = @{}
    foreach ($item in $stack.Outputs) { $values[$item.OutputKey] = $item.OutputValue }
    return $values
}
function Write-PocJson([string]$Path, $Value) {
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 100), [Text.UTF8Encoding]::new($false))
}
