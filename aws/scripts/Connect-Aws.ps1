<#
.SYNOPSIS
Configure, sign in to, or check the AWS profile for this PoC.
.EXAMPLE
.\aws\scripts\Connect-Aws.ps1
.EXAMPLE
.\aws\scripts\Connect-Aws.ps1 -Mode Check
.EXAMPLE
.\aws\scripts\Connect-Aws.ps1 -Mode Check -ExpectedAccountId 123456789012
#>
[CmdletBinding()]
param(
    [ValidateSet('Login', 'Configure', 'Check')]
    [string]$Mode = 'Login',

    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9_.-]*$')]
    [string]$Profile = 'poc-practice',

    [ValidatePattern('^[a-z]{2}(-[a-z]+)+-\d+$')]
    [string]$Region = 'ap-northeast-1',

    [ValidatePattern('^\d{12}$')]
    [string]$ExpectedAccountId
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false

$awsCandidates = @()
$awsCommand = Get-Command aws.exe -CommandType Application -ErrorAction SilentlyContinue
if ($awsCommand) {
    $awsCandidates += $awsCommand.Source
}
$awsCandidates += Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
$awsCandidates += Join-Path $env:ProgramFiles 'Amazon\AWSCLIV2\aws.exe'
$awsExe = $awsCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $awsExe) {
    throw 'AWS CLI v2 is not installed. See aws/README.md for the official installer.'
}

$awsVersion = (& $awsExe --version | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $awsVersion -notmatch 'aws-cli/(\d+\.\d+\.\d+)') {
    throw 'Unable to determine the AWS CLI version.'
}
if ([version]$Matches[1] -lt [version]'2.32.0') {
    throw 'AWS CLI 2.32.0 or newer is required for browser-based aws login.'
}
Write-Host $awsVersion

if ($Mode -ne 'Check') {
    & $awsExe configure set region $Region --profile $Profile
    if ($LASTEXITCODE -ne 0) { throw 'Unable to save the AWS profile region.' }
    & $awsExe configure set output json --profile $Profile
    if ($LASTEXITCODE -ne 0) { throw 'Unable to save the AWS profile output format.' }
    Write-Host "Configured profile '$Profile' in region '$Region'."
}

if ($Mode -eq 'Configure') {
    Write-Host 'Profile configured. Run this script without -Mode to sign in.'
    return
}

if ($Mode -eq 'Login') {
    Write-Host 'Complete AWS sign-in and approval in the browser. Keep passwords and MFA codes there.'
    & $awsExe login --profile $Profile --region $Region --no-cli-pager --no-cli-auto-prompt
    if ($LASTEXITCODE -ne 0) {
        throw 'AWS login did not complete. See the sign-in troubleshooting steps in aws/README.md.'
    }
}

$identityJson = & $awsExe sts get-caller-identity --profile $Profile --region $Region --output json --no-cli-pager --no-cli-auto-prompt --cli-connect-timeout 10 --cli-read-timeout 20
if ($LASTEXITCODE -ne 0) {
    throw 'AWS identity verification failed. Run this script in Login mode to authenticate again.'
}
$identity = ($identityJson -join [Environment]::NewLine) | ConvertFrom-Json
if ($ExpectedAccountId -and $identity.Account -ne $ExpectedAccountId) {
    throw "Account mismatch: expected $ExpectedAccountId but authenticated to $($identity.Account)."
}

[pscustomobject]@{
    Profile = $Profile
    Region = $Region
    Account = $identity.Account
    Arn = $identity.Arn
    Authentication = 'Verified with STS GetCallerIdentity'
}
Write-Host 'This checks authentication only. Deployment permissions and service access are not checked.'
