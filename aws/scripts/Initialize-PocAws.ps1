[CmdletBinding()]
param([string]$Profile='poc-practice', [string]$Region='ap-northeast-1',
      [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId)
. "$PSScriptRoot/Aws-Common.ps1"
$null = Assert-PocAccount
& $script:AwsExe cloudformation deploy --profile $Profile --region $Region --stack-name poc-practice-bootstrap --template-file "$PSScriptRoot/../infra/bootstrap.json" --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw 'Bootstrap deployment failed.' }
$outputs = Get-PocOutputs 'poc-practice-bootstrap'
$directory = Join-Path $script:ProjectRoot '.local/aws-deploy'
New-Item -ItemType Directory -Force -Path $directory | Out-Null
Write-PocJson (Join-Path $directory 'bootstrap-outputs.json') $outputs
Write-Output ($outputs | ConvertTo-Json)
