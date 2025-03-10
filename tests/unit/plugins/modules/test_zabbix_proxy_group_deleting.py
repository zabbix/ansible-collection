#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy_group
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleExitJson, AnsibleFailJson, TestModules, set_module_args, patch)


def mock_api_version_70(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of API is returned.
    """
    return '7.0.0'


class TestDeleting(TestModules):
    """Class for testing deletion of proxy group"""
    module = zabbix_proxy_group

    def test_delete_not_exist_proxy_group(self):
        """
        Testing proxy deletion function in case specified proxy group
        does not exist.

        Expected result: task has not been changed and proxy group
        has not been deleted.
        """

        def find_zabbix_proxy_groups_by_names(self, proxy_name):
            return []

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'absent',
            'name': zabbix_proxy_group})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No need to delete proxy group: {0}'.format(zabbix_proxy_group))

    def test_deleting_proxy_group(self):
        """
        Testing proxy group deletion function if specified proxy group exists.

        Expected result: task has been changed and proxy group
        has been updated successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return [{'name': proxy_group_name, 'proxy_groupid': '4'}]

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'absent',
            'name': zabbix_proxy_group})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully delete proxy group: {0}'.format(zabbix_proxy_group))

    def test_deleting_proxy_group_error(self):
        """
        Testing proxy group deletion function in case of encountering error
        during deletion.

        Expected result: task has been failed.
        """

        def mock_send_request(self, method, params):
            raise Exception

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return [{'name': proxy_group_name, 'proxy_groupid': '4'}]

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'absent',
            'name': zabbix_proxy_group})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                ansible_result.exception.args[0]['msg'],
                'Failed to delete proxy group: {0}'.format(zabbix_proxy_group))
