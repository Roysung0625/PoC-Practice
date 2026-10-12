param([string]$Profile='poc-practice', [string]$Region='ap-northeast-1', [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId)
. "$PSScriptRoot\Aws-Common.ps1"
$null = Assert-PocAccount
$null = Invoke-PocAws @('cloudformation','delete-stack','--stack-name','poc-practice-app')
& $script:AwsExe cloudformation wait stack-delete-complete --stack-name poc-practice-app --profile $Profile --region $Region
if ($LASTEXITCODE -ne 0) { throw 'Application stack deletion is incomplete. Inspect CloudFormation events.' }
Write-Output 'Application stack removed. Budget guard, bootstrap private artifacts/login identity, local PostgreSQL and local evidence are preserved. Stop the local receiver separately.'
