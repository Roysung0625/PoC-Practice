"""Account-wide post-detection cutoff. No application inference or data deletion."""
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation


def now():
    return datetime.now(timezone.utc).isoformat()


def exceeds_limit(cost):
    try:
        amount = Decimal(str(cost['Amount']))
        if cost['Unit'] != 'USD' or not amount.is_finite() or amount < 0:
            raise ValueError('Invalid USD actual cost')
    except (KeyError, TypeError, InvalidOperation) as exc:
        raise ValueError('Missing or invalid actual cost') from exc
    return amount > Decimal('25')


def protected_role(role, own_arn):
    return role['Arn'] == own_arn or role.get('Path', '').startswith('/aws-service-role/')


class Guard:
    def __init__(self, aws, state):
        self.aws, self.state = aws, state

    def run(self, event):
        dry_run = event.get('dry_run') is True
        if self.state.get('pause.json'):
            return {'status': 'paused', 'time': now()}
        latch = self.state.get('latch.json')
        budget_errors = []
        try:
            cost = self.aws.cost()
            breached = exceeds_limit(cost)
        except Exception as exc:
            if not latch:
                raise
            cost, breached = None, False
            budget_errors.append({'error': 'Budget lookup: ' + str(exc)})
        result = {'time': now(), 'actual': cost, 'latched': bool(latch),
                  'threshold_usd': 25, 'applied': [], 'errors': budget_errors, 'planned': []}
        if not dry_run and not breached and not latch:
            result['status'] = 'below_limit'
            print(json.dumps(result))
            return result
        if not dry_run:
            self.state.once('latch.json', {'time': now(), 'actual': cost, 'episode': uuid.uuid4().hex})
            latch = self.state.get('latch.json')
            result['latched'] = True
        paused = False
        for action in self.aws.discover():
            if 'error' in action:
                result['errors'].append(action)
                continue
            if dry_run:
                result['planned'].append(action)
                continue
            try:
                if self.state.get('pause.json'):
                    paused = True
                    break
                key = hashlib.sha256(action['id'].encode()).hexdigest()
                self.state.once('snapshots/' + latch.get('episode', 'legacy') + '/' + key + '.json',
                                dict(action, time=now()))
                self.aws.apply(action)
                result['applied'].append(action['id'])
            except Exception as exc:
                result['errors'].append({'id': action['id'], 'error': str(exc)})
        result['status'] = 'paused' if paused else ('dry_run' if dry_run else 'cutoff_applied')
        if result['errors']:
            result['status'] = 'cutoff_incomplete' if not dry_run else 'dry_run_incomplete'
        if not dry_run:
            self.state.put('latest.json', result)
        print(json.dumps(result, default=str))
        if result['errors']:
            raise RuntimeError(json.dumps(result, default=str))
        return result


class S3State:
    def __init__(self, client, bucket):
        self.client, self.bucket = client, bucket

    def get(self, key):
        try:
            return json.loads(self.client.get_object(Bucket=self.bucket, Key=key)['Body'].read())
        except self.client.exceptions.ClientError as exc:
            if exc.response['Error']['Code'] in ('NoSuchKey', '404'):
                return None
            raise

    def once(self, key, value):
        try:
            self.client.put_object(Bucket=self.bucket, Key=key, IfNoneMatch='*',
                                   Body=json.dumps(value, default=str).encode(), ContentType='application/json')
        except self.client.exceptions.ClientError as exc:
            if exc.response['Error']['Code'] != 'PreconditionFailed':
                raise

    def put(self, key, value):
        self.client.put_object(Bucket=self.bucket, Key=key, Body=json.dumps(value, default=str).encode(),
                               ContentType='application/json')


class AWS:
    def __init__(self):
        import boto3
        from botocore.config import Config
        self.session = boto3.Session()
        self.config = Config(retries={'mode': 'standard', 'total_max_attempts': 3},
                             connect_timeout=5, read_timeout=15)
        self.clients = {}
        self.account = os.environ['ACCOUNT_ID']
        self.budget = os.environ['BUDGET_NAME']
        self.policy = os.environ['DENY_POLICY_ARN']
        self.role = os.environ['GUARD_ROLE_ARN']
        self.function = os.environ['AWS_LAMBDA_FUNCTION_NAME']
        self.region = os.environ['AWS_REGION']

    def client(self, service, region=None):
        key = (service, region or self.region)
        if key not in self.clients:
            self.clients[key] = self.session.client(service, region_name=key[1], config=self.config)
        return self.clients[key]

    def cost(self):
        budget = self.client('budgets', 'us-east-1').describe_budget(
            AccountId=self.account, BudgetName=self.budget)['Budget']
        if budget.get('CostFilters') or budget.get('FilterExpression') or budget['TimeUnit'] != 'MONTHLY':
            raise ValueError('Budget scope changed: account-wide monthly budget required')
        if budget['BudgetLimit']['Unit'] != 'USD' or Decimal(budget['BudgetLimit']['Amount']) != 25:
            raise ValueError('Budget amount changed: expected 25 USD')
        return budget['CalculatedSpend']['ActualSpend']

    def items(self, service, region, operation, key, **params):
        client = self.client(service, region)
        if client.can_paginate(operation):
            for page in client.get_paginator(operation).paginate(**params):
                yield from page.get(key, [])
        else:
            yield from getattr(client, operation)(**params).get(key, [])

    @staticmethod
    def action(service, region, operation, resource, params, before=None):
        return {'id': ':'.join([service, region or 'global', resource, operation]),
                'service': service, 'region': region, 'operation': operation,
                'params': params, 'before': before or {}}

    def iam_actions(self):
        for kind, plural in [('role', 'Roles'), ('user', 'Users')]:
            for entity in self.items('iam', None, 'list_' + plural.lower(), plural):
                if kind == 'role' and protected_role(entity, self.role):
                    continue
                name_key = kind.title() + 'Name'
                name = entity[name_key]
                attached = self.items('iam', None, 'list_attached_' + kind + '_policies',
                                      'AttachedPolicies', **{name_key: name})
                if any(p['PolicyArn'] == self.policy for p in attached):
                    continue
                yield self.action('iam', None, 'attach_' + kind + '_policy', name,
                                  {name_key: name, 'PolicyArn': self.policy}, {'attached': False})

    def asg_actions(self, region):
        processes = {p['ProcessName'] for p in self.client('autoscaling', region).describe_scaling_process_types()['Processes']}
        for group in self.items('autoscaling', region, 'describe_auto_scaling_groups', 'AutoScalingGroups'):
            name = group['AutoScalingGroupName']
            suspended = [p['ProcessName'] for p in group.get('SuspendedProcesses', [])]
            if not processes.issubset(suspended):
                yield self.action('autoscaling', region, 'suspend_processes', name,
                                  {'AutoScalingGroupName': name},
                                  {'SuspendedProcesses': suspended})

    def ecs_actions(self, region):
        client = self.client('ecs', region)
        for cluster in self.items('ecs', region, 'list_clusters', 'clusterArns'):
            for arn in self.items('ecs', region, 'list_services', 'serviceArns', cluster=cluster):
                response = client.describe_services(cluster=cluster, services=[arn])
                if response.get('failures'):
                    raise RuntimeError(str(response['failures']))
                service = response['services'][0]
                if service['schedulingStrategy'] == 'DAEMON':
                    yield {'error': 'ECS DAEMON service needs manual review: ' + arn}
                elif service['desiredCount']:
                    yield self.action('ecs', region, 'update_service', arn,
                                      {'cluster': cluster, 'service': arn, 'desiredCount': 0},
                                      {'desiredCount': service['desiredCount']})
            for task in self.items('ecs', region, 'list_tasks', 'taskArns', cluster=cluster, desiredStatus='RUNNING'):
                yield self.action('ecs', region, 'stop_task', task,
                                  {'cluster': cluster, 'task': task, 'reason': 'Monthly account budget exceeded'})

    def ec2_actions(self, region):
        for reservation in self.items('ec2', region, 'describe_instances', 'Reservations',
                                      Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}]):
            for instance in reservation['Instances']:
                if instance.get('RootDeviceType') != 'ebs':
                    yield {'error': 'Cannot stop instance-store EC2: ' + instance['InstanceId']}
                    continue
                yield self.action('ec2', region, 'stop_instances', instance['InstanceId'],
                                  {'InstanceIds': [instance['InstanceId']]}, {'state': instance['State']['Name']})

    def rds_actions(self, region):
        for db in self.items('rds', region, 'describe_db_instances', 'DBInstances'):
            if db.get('DBClusterIdentifier') or db['DBInstanceStatus'] == 'stopped':
                continue
            if db['DBInstanceStatus'] != 'available':
                if db['DBInstanceStatus'] != 'stopping':
                    yield {'error': 'RDS not stoppable yet: ' + db['DBInstanceIdentifier'] + ':' + db['DBInstanceStatus']}
                continue
            yield self.action('rds', region, 'stop_db_instance', db['DBInstanceIdentifier'],
                              {'DBInstanceIdentifier': db['DBInstanceIdentifier']}, {'status': 'available'})
        for cluster in self.items('rds', region, 'describe_db_clusters', 'DBClusters'):
            if cluster['Status'] in ('stopped', 'stopping'):
                continue
            if cluster['Status'] != 'available':
                yield {'error': 'RDS cluster not stoppable yet: ' + cluster['DBClusterIdentifier']}
                continue
            yield self.action('rds', region, 'stop_db_cluster', cluster['DBClusterIdentifier'],
                              {'DBClusterIdentifier': cluster['DBClusterIdentifier']}, {'status': 'available'})

    def lambda_actions(self, region):
        client = self.client('lambda', region)
        for function in self.items('lambda', region, 'list_functions', 'Functions'):
            name = function['FunctionName']
            if region == self.region and name == self.function:
                continue
            concurrency = client.get_function_concurrency(FunctionName=name)
            previous = concurrency.get('ReservedConcurrentExecutions')
            # Provisioned concurrency must be removed before reducing the reservation.
            for config in self.items('lambda', region, 'list_provisioned_concurrency_configs',
                                     'ProvisionedConcurrencyConfigs', FunctionName=name):
                qualifier = config['FunctionArn'].rsplit(':', 1)[1]
                yield self.action('lambda', region, 'delete_provisioned_concurrency_config', name + ':' + qualifier,
                                  {'FunctionName': name, 'Qualifier': qualifier},
                                  {'ProvisionedConcurrentExecutions': config['RequestedProvisionedConcurrentExecutions']})
            if previous != 0:
                yield self.action('lambda', region, 'put_function_concurrency', name,
                                  {'FunctionName': name, 'ReservedConcurrentExecutions': 0},
                                  {'ReservedConcurrentExecutions': previous})

    def discover(self):
        try:
            yield from self.iam_actions()
        except Exception as exc:
            yield {'error': 'IAM discovery: ' + str(exc)}
        regions = self.client('ec2').describe_regions()['Regions']
        for entry in regions:
            region = entry['RegionName']
            for service, discover in [('autoscaling', self.asg_actions), ('ecs', self.ecs_actions),
                                      ('ec2', self.ec2_actions), ('rds', self.rds_actions),
                                      ('lambda', self.lambda_actions)]:
                try:
                    yield from discover(region)
                except Exception as exc:
                    yield {'error': service + '/' + region + ': ' + str(exc)}

    def apply(self, action):
        return getattr(self.client(action['service'], action['region']), action['operation'])(**action['params'])


def handler(event, context):
    aws = AWS()
    state = S3State(aws.client('s3'), os.environ['STATE_BUCKET'])
    return Guard(aws, state).run(event)
