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
    Mock function to get Zabbix API version 7.0.
    """
    return '7.0.0'


class TestCreating(TestModules):
    """Class for testing creation of proxy"""
    module = zabbix_proxy_group

    def test_create_proxy_wo_parameters(self):
        """
        Testing proxy group creation function without additional parameters.

        Expected result: task has been changed and proxy group
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return []

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
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
                'Successfully created proxy group: {0}'.format(zabbix_proxy_group))

    def test_create_active_proxy_w_all_parameters(self):
        """
        Testing active proxy creation function with all supported proxy options.
        Unsupported active proxy parameters must be empty.
        Test for Zabbix version 7.0 +

        Expected result: task has been changed and proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return []

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy_group,
            'failover_delay': '2m',
            'min_online': '10',
            'description': 'description of proxy group'})

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
                'Successfully created proxy group: {0}'.format(zabbix_proxy_group))

    def test_create_proxy_error(self):
        """
        Testing proxy group creation function in case of encountering error
        during creation.

        Expected result: task has been failed.
        """

        def mock_send_request(self, method, params):
            raise Exception

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return []

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
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
                'Failed to create proxy group: {0}'.format(zabbix_proxy_group))
