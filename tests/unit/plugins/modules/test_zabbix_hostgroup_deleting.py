#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_hostgroup
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleExitJson, AnsibleFailJson, TestModules, set_module_args, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. For this module,
    it doesn't matter which version of API is returned.
    """
    return '6.0.18'


class TestDeleting(TestModules):
    """Class for testing the removing of host groups"""
    module = zabbix_hostgroup

    def test_delete_one_hostgroup(self):
        """
        Testing the deletion of one host group.

        Expected result: the task has been changed and the host group
        has been deleted successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return {'1000': {'groupid': '1000', 'name': 'Test group'}}
            if method == 'hostgroup.delete':
                return {'groupids': ['1000']}

        zabbix_hostgroup_name = ['Test group']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully deleted host group(s): {0}'.format(', '.join(zabbix_hostgroup_name)))

    def test_delete_non_existent_hostgroup(self):
        """
        Testing the deletion of a host group in case it has already
        been deleted.

        Expected result: the task has not been changed and host group
        has not been deleted.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return {}
            if method == 'hostgroup.delete':
                return {}

        zabbix_hostgroup_name = ['Test group']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No host group(s) to delete')

    def test_delete_two_hostgroup(self):
        """
        Testing the deletion of two host groups. The test checks the
        possibility of passing the list of host groups for deletion.

        Expected result: the task has been changed and host groups
        have been deleted successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return {'1000': {'groupid': '1000', 'name': 'Test group'},
                        '1001': {'groupid': '1001', 'name': 'Test group 2'}}
            if method == 'hostgroup.delete':
                return {'groupids': ['1000', '1001']}

        zabbix_hostgroup_name = ['Test group', 'Test group 2']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertIn(
                'Successfully deleted host group(s):',
                ansible_result.exception.args[0]['result'])

            parse_response = ansible_result.exception.args[0]['result'].split(':')[1]
            groups_form_response = [g.strip() for g in parse_response.split(',')]
            self.assertEqual(groups_form_response.sort(), zabbix_hostgroup_name.sort())

    def test_delete_two_hostgroup_one_exist(self):
        """
        Testing the deletion of two host groups. The test checks the
        possibility of passing the list of host groups for deletion
        and verifies if the function works correctly when one of the groups
        has already been deleted.

        Expected result: the task has been changed and only one host group
        has been deleted successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return {'1000': {'groupid': '1000', 'name': 'Test group'}}
            if method == 'hostgroup.delete':
                return {'groupids': ['1000']}

        zabbix_hostgroup_name = ['Test group', 'Test group 2']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully deleted host group(s): Test group')

    def test_delete_two_deleted_hostgroup(self):
        """
        Testing the deletion of two host groups. The test checks the
        possibility of passing the list of host groups for deletion
        and verifies if the function works correctly when both host groups
        have already been deleted.

        Expected result: the task has not been changed and host groups
        have not been deleted.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return {}
            if method == 'hostgroup.delete':
                return {}

        zabbix_hostgroup_name = ['Test group', 'Test group 2']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No host group(s) to delete')

    def test_create_empty_hostgroup_list(self):
        """
        Testing the deletion of a host group in case of passing an empty
        list for removal in different ways.

        Expected result: the task has not been changed and host group
        has not been deleted.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return []
            if method == 'hostgroup.create':
                {'groupids': ['1000', '1001']}

        # the first way
        zabbix_hostgroup_name = ['']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No host group(s) to delete')

        # the second way
        zabbix_hostgroup_name = ['   ']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No host group(s) to delete')

        # the third way
        zabbix_hostgroup_name = ['   ', '']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No host group(s) to delete')

        # the fourth way
        zabbix_hostgroup_name = ['   ', '', 'Test group']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No host group(s) to delete')

    def test_failed_to_get_hostgroups(self):
        """
        Testing the deletion of host groups in case of an error while
        querying existing host groups in Zabbix.

        Expected result: the task has failed and host group
        has not been deleted.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                raise Exception
            if method == 'hostgroup.delete':
                {'groupids': ['1000', '1001']}

        zabbix_hostgroup_name = ['Test group']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Failed to get existing host group(s):',
                ansible_result.exception.args[0]['msg'])

    def test_failed_to_create_hostgroups(self):
        """
        Testing the deletion of host groups in case of an error while
        querying to delete host groups in Zabbix.

        Expected result: the task has failed and host group
        has not been deleted.
        """
        def mock_send_request(self, method, params):
            if method == 'hostgroup.get':
                return {'1000': {'groupid': '1000', 'name': 'Test group'}}
            if method == 'hostgroup.delete':
                raise Exception

        zabbix_hostgroup_name = ['Test group']
        set_module_args({'state': 'absent', 'name': zabbix_hostgroup_name})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Failed to delete host group(s):',
                ansible_result.exception.args[0]['msg'])
