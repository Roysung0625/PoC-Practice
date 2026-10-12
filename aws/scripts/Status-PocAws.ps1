param([string]$Profile='poc-practice', [string]$Region='ap-northeast-1', [Parameter(Mandatory)][string]$ExpectedAccountId)
. "$PSScriptRoot\Aws-Common.ps1"
$null = Assert-PocAccount
$values = Get-PocOutputs 'poc-practice-app'
$runtime = Invoke-PocAws @('bedrock-agentcore-control','get-agent-runtime','--agent-runtime-id',$values.AgentId)
$queue = Invoke-PocAws @('sqs','get-queue-attributes','--queue-url',$values.QueueUrl,'--attribute-names','ApproximateNumberOfMessages','ApproximateNumberOfMessagesNotVisible','VisibilityTimeout','MessageRetentionPeriod')
$limits = Invoke-PocAws @('lambda','get-account-settings')
$function = Invoke-PocAws @('lambda','get-function-configuration','--function-name',$values.SqlFunction)
[ordered]@{AgentStatus=$runtime.status; AgentArn=$values.AgentArn; LambdaState=$function.State; LambdaTimeout=$function.Timeout; Queue=$queue.Attributes; LambdaConcurrency=$limits.AccountLimit.ConcurrentExecutions; Outputs=$values} | ConvertTo-Json -Depth 8
