param(
    [string]$Profile = 'poc-practice',
    [string]$Region = 'ap-northeast-1',
    [Parameter(Mandatory)][ValidatePattern('^\d{12}$')][string]$ExpectedAccountId
)
. "$PSScriptRoot\Aws-Common.ps1"
$null = Assert-PocAccount
$null = Get-PocOutputs 'poc-practice-bootstrap'
$secretDir = Join-Path $script:ProjectRoot '.local\secrets\aws-login'
$null = New-Item -ItemType Directory -Force -Path $secretDir
$sid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$acl = [Security.AccessControl.DirectorySecurity]::new()
$acl.SetAccessRuleProtection($true, $false)
foreach ($principal in @($sid, 'S-1-5-18', 'S-1-5-32-544')) {
    $rule = [Security.AccessControl.FileSystemAccessRule]::new([Security.Principal.SecurityIdentifier]::new($principal), 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
    $acl.AddAccessRule($rule)
}
Set-Acl -LiteralPath $secretDir -AclObject $acl
$existing = & $script:AwsExe iam get-login-profile --user-name poc-local-login --profile $Profile --region $Region --output json --no-cli-pager 2>&1
if ($LASTEXITCODE -ne 0) {
    if (($existing -join '') -notmatch 'NoSuchEntity') { throw 'Unable to inspect login profile; no password was changed.' }
    $password = 'Aa1!' + [Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(30))
    $requestPath = Join-Path $secretDir 'create-login-profile.json'
    $instructionPath = Join-Path $secretDir 'FIRST-LOGIN.txt'
    Write-PocJson $requestPath @{UserName='poc-local-login'; Password=$password; PasswordResetRequired=$true}
    try {
        $null = Invoke-PocAws @('iam','create-login-profile','--cli-input-json',"file://$requestPath")
        [IO.File]::WriteAllText($instructionPath, "AWS PoC first login`nConsole: https://$ExpectedAccountId.signin.aws.amazon.com/console/`nIAM user: poc-local-login`nTemporary password: $password`n`nChange the password in the AWS browser. Do not share it in chat. Then approve AWS CLI login as poc-local-login.`n", [Text.UTF8Encoding]::new($false))
    } finally {
        Remove-Item -LiteralPath $requestPath -Force -ErrorAction SilentlyContinue
        $password = $null
    }
}
& $script:AwsExe configure set region $Region --profile poc-local-login
if ($LASTEXITCODE -ne 0) { throw 'Profile configuration failed' }
& $script:AwsExe configure set output json --profile poc-local-login
if ($LASTEXITCODE -ne 0) { throw 'Profile configuration failed' }
Write-Output "Protected first-login instructions: $secretDir\FIRST-LOGIN.txt"
Write-Output 'Existing passwords are never reset by this script. No access keys were created.'
