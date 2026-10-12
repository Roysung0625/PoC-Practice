import unittest
from unittest.mock import Mock, patch
from guard import AWS, Guard, exceeds_limit, protected_role


class MemoryState:
    def __init__(self):
        self.objects = {}

    def get(self, key):
        return self.objects.get(key)

    def once(self, key, value):
        self.objects.setdefault(key, value)

    def put(self, key, value):
        self.objects[key] = value


class GuardTests(unittest.TestCase):
    def setUp(self):
        quiet = patch('builtins.print')
        quiet.start()
        self.addCleanup(quiet.stop)

    def build(self, amount='0.02'):
        state = MemoryState()
        aws = Mock()
        aws.cost.return_value = {'Amount': amount, 'Unit': 'USD'}
        aws.discover.return_value = iter([])
        return Guard(aws, state), aws, state

    def test_threshold_is_strictly_greater_than_25(self):
        for amount, expected in [('0.02', False), ('25', False), ('25.00001', True)]:
            self.assertEqual(exceeds_limit({'Amount': amount, 'Unit': 'USD'}), expected)

    def test_invalid_cost_does_not_silently_allow_or_cut_off(self):
        for value in [{}, {'Amount': 'NaN', 'Unit': 'USD'}, {'Amount': '26', 'Unit': 'JPY'},
                      {'Amount': '-1', 'Unit': 'USD'}, {'Amount': 'Infinity', 'Unit': 'USD'}]:
            with self.assertRaises(ValueError):
                exceeds_limit(value)

    def test_protected_roles_use_exact_arn_and_service_path(self):
        own = 'arn:aws:iam::123:role/guard'
        self.assertTrue(protected_role({'Arn': own, 'Path': '/'}, own))
        self.assertTrue(protected_role({'Arn': 'other', 'Path': '/aws-service-role/rds.amazonaws.com/'}, own))
        self.assertFalse(protected_role({'Arn': own + '-other', 'Path': '/service-role/'}, own))

    def test_below_limit_performs_no_discovery_or_writes(self):
        guard, aws, state = self.build('25')
        self.assertEqual(guard.run({})['status'], 'below_limit')
        aws.discover.assert_not_called()
        aws.apply.assert_not_called()
        self.assertEqual(state.objects, {})

    def test_breach_persists_latch_before_action_and_remains_next_month(self):
        guard, aws, state = self.build('25.01')
        action = {'id': 'role:x', 'before': {'attached': False}}
        aws.discover.return_value = iter([action])
        aws.apply.side_effect = lambda _: self.assertIn('latch.json', state.objects)
        self.assertEqual(guard.run({})['status'], 'cutoff_applied')
        aws.cost.return_value = {'Amount': '0', 'Unit': 'USD'}
        aws.discover.return_value = iter([])
        self.assertEqual(guard.run({})['status'], 'cutoff_applied')

    def test_dry_run_above_threshold_does_not_write_or_mutate(self):
        guard, aws, state = self.build('100')
        aws.discover.return_value = iter([{'id': 'test', 'before': {}}])
        result = guard.run({'dry_run': True})
        self.assertEqual(result['status'], 'dry_run')
        self.assertEqual(len(result['planned']), 1)
        self.assertEqual(state.objects, {})
        aws.apply.assert_not_called()

    def test_inventory_below_limit_is_read_only(self):
        guard, aws, state = self.build()
        self.assertEqual(guard.run({'dry_run': True})['status'], 'dry_run')
        self.assertEqual(state.objects, {})

    def test_failures_do_not_prevent_other_actions_and_are_reported(self):
        guard, aws, state = self.build('30')
        aws.discover.return_value = iter([{'id': 'one'}, {'id': 'two'}])
        aws.apply.side_effect = [RuntimeError('denied'), None]
        with self.assertRaisesRegex(RuntimeError, 'cutoff_incomplete'):
            guard.run({})
        self.assertEqual(aws.apply.call_count, 2)
        self.assertEqual(state.objects['latest.json']['applied'], ['two'])

    def test_discovery_errors_fail_loudly_after_other_actions(self):
        guard, aws, state = self.build('30')
        aws.discover.return_value = iter([{'error': 'RDS permission denied'}, {'id': 'role'}])
        with self.assertRaisesRegex(RuntimeError, 'cutoff_incomplete'):
            guard.run({})
        self.assertEqual(state.objects['latest.json']['applied'], ['role'])

    def test_original_settings_survive_repeated_cutoff(self):
        guard, aws, state = self.build('30')
        aws.discover.return_value = iter([{'id': 'ecs:a', 'before': {'desired': 2}}])
        guard.run({})
        aws.discover.return_value = iter([{'id': 'ecs:a', 'before': {'desired': 1}}])
        guard.run({})
        records = [v for k, v in state.objects.items() if k.startswith('snapshots/')]
        self.assertEqual(records[0]['before']['desired'], 2)

    def test_new_cutoff_episode_keeps_new_restore_settings(self):
        guard, aws, state = self.build('30')
        aws.discover.return_value = iter([{'id': 'ecs:a', 'before': {'desired': 2}}])
        guard.run({})
        del state.objects['latch.json']
        aws.discover.return_value = iter([{'id': 'ecs:a', 'before': {'desired': 3}}])
        guard.run({})
        records = [v for k, v in state.objects.items() if k.startswith('snapshots/')]
        self.assertEqual(sorted(r['before']['desired'] for r in records), [2, 3])

    def test_failed_snapshot_prevents_unsafely_unrecorded_change(self):
        guard, aws, state = self.build('30')
        aws.discover.return_value = iter([{'id': 'ecs:a'}])
        original = state.once
        def fail_snapshot(key, value):
            if key.startswith('snapshots/'):
                raise RuntimeError('S3 unavailable')
            original(key, value)
        state.once = fail_snapshot
        with self.assertRaisesRegex(RuntimeError, 'cutoff_incomplete'):
            guard.run({})
        aws.apply.assert_not_called()

    def test_latched_cutoff_continues_when_budget_lookup_fails(self):
        guard, aws, state = self.build()
        state.objects['latch.json'] = {'actual': {'Amount': '26', 'Unit': 'USD'}}
        aws.cost.side_effect = RuntimeError('Budgets unavailable')
        aws.discover.return_value = iter([{'id': 'role'}])
        with self.assertRaisesRegex(RuntimeError, 'cutoff_incomplete'):
            guard.run({})
        self.assertEqual(state.objects['latest.json']['applied'], ['role'])

    def test_asg_suspends_processes_without_terminating_instances(self):
        aws = AWS.__new__(AWS)
        aws.items = lambda *args, **kwargs: iter([{'AutoScalingGroupName': 'app',
            'MinSize': 1, 'MaxSize': 3, 'DesiredCapacity': 2, 'SuspendedProcesses': []}])
        aws.client = Mock()
        aws.client.return_value.describe_scaling_process_types.return_value = {
            'Processes': [{'ProcessName': 'Launch'}, {'ProcessName': 'Terminate'}]}
        actions = list(aws.asg_actions('ap-northeast-1'))
        self.assertEqual([a['operation'] for a in actions], ['suspend_processes'])
        self.assertEqual(actions[0]['params'], {'AutoScalingGroupName': 'app'})

    def test_paused_controller_makes_no_calls(self):
        guard, aws, state = self.build('30')
        state.objects['pause.json'] = {'time': 'now'}
        self.assertEqual(guard.run({})['status'], 'paused')
        aws.cost.assert_not_called()
        aws.discover.assert_not_called()

    def test_pause_during_run_prevents_next_mutation(self):
        guard, aws, state = self.build('30')
        aws.discover.return_value = iter([{'id': 'one'}, {'id': 'two'}])
        aws.apply.side_effect = lambda _: state.put('pause.json', {'time': 'now'})
        self.assertEqual(guard.run({})['status'], 'paused')
        self.assertEqual(aws.apply.call_count, 1)

    def test_iam_discovery_skips_guard_service_roles_and_already_blocked(self):
        aws = AWS.__new__(AWS)
        aws.role, aws.policy = 'own-role', 'deny-policy'
        def items(service, region, operation, key, **params):
            data = {'list_roles': [
                {'Arn': 'own-role', 'Path': '/', 'RoleName': 'guard'},
                {'Arn': 'slr', 'Path': '/aws-service-role/service/', 'RoleName': 'slr'},
                {'Arn': 'app', 'Path': '/', 'RoleName': 'app'},
                {'Arn': 'old', 'Path': '/', 'RoleName': 'old'}],
                'list_users': [{'Arn': 'human', 'UserName': 'human'}]}
            if operation == 'list_attached_role_policies' and params['RoleName'] == 'old':
                return iter([{'PolicyArn': 'deny-policy'}])
            return iter(data.get(operation, []))
        aws.items = items
        actions = list(aws.iam_actions())
        self.assertEqual([a['params'] for a in actions], [
            {'RoleName': 'app', 'PolicyArn': 'deny-policy'},
            {'UserName': 'human', 'PolicyArn': 'deny-policy'}])

    def test_rds_cluster_members_are_not_stopped_as_standalone(self):
        aws = AWS.__new__(AWS)
        def items(service, region, operation, key, **params):
            return iter({'describe_db_instances': [
                {'DBInstanceIdentifier': 'member', 'DBClusterIdentifier': 'cluster', 'DBInstanceStatus': 'available'},
                {'DBInstanceIdentifier': 'stopped', 'DBInstanceStatus': 'stopped'},
                {'DBInstanceIdentifier': 'db', 'DBInstanceStatus': 'available'}],
                'describe_db_clusters': [{'DBClusterIdentifier': 'cluster', 'Status': 'available'}]}[operation])
        aws.items = items
        self.assertEqual([a['params'] for a in aws.rds_actions('region')], [
            {'DBInstanceIdentifier': 'db'}, {'DBClusterIdentifier': 'cluster'}])

    def test_ec2_instance_store_is_reported_without_termination(self):
        aws = AWS.__new__(AWS)
        aws.items = lambda *args, **kwargs: iter([{'Instances': [
            {'InstanceId': 'safe', 'RootDeviceType': 'ebs', 'State': {'Name': 'running'}},
            {'InstanceId': 'unsafe', 'RootDeviceType': 'instance-store', 'State': {'Name': 'running'}}]}])
        actions = list(aws.ec2_actions('region'))
        self.assertEqual(actions[0]['operation'], 'stop_instances')
        self.assertEqual(actions[0]['params'], {'InstanceIds': ['safe']})
        self.assertIn('error', actions[1])


if __name__ == '__main__':
    unittest.main()
