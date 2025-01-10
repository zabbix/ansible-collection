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
    Mock function to get Zabbix API version 7.0.0.
    """
    return '7.0.0'


class TestUpdating(TestModules):
    """Class for testing the update of the proxy"""
    module = zabbix_proxy_group

    def test_update_proxy_group_wo_parameters(self):
        """
        Testing the proxy group update function without additional parameters.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy group
        has been updated successfully.
        """

        def mock_send_request(self, method, params):
            if method == 'proxygroup.get':
                return [{
                    "proxy_groupid": "4",
                    "name": "test_proxy_group",
                    "failover_delay": "1m",
                    "min_online": "2",
                    "description": "description of proxy group"
                }]

            return True

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return [{'name': proxy_group_name, 'proxy_groupid': '4'}]

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy_group,
            'failover_delay': '2m'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated proxy group: {0}'.format(zabbix_proxy_group))

    def test_update_proxy_group_no_need_update(self):
        """
        Testing the proxy group update function in case nothing needs to be updated.
        Test for Zabbix version 7.0 +

        Expected result: the task has not been changed and the proxy group
        has not been updated.
        """

        def mock_send_request(self, method, params):
            return [{
                    "proxy_groupid": "4",
                    "name": "test_proxy_group",
                    "failover_delay": "1m",
                    "min_online": "2"}]

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return [{'name': proxy_group_name, 'proxy_groupid': '4'}]

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy_group,
            'failover_delay': '1m',
            'min_online': '2'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'No need to update proxy group: {0}'.format(zabbix_proxy_group))

    def test_update_proxy_group_w_all_parameters(self):
        """
        Testing the proxy group update function with all possible options.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy group
        has been updated successfully.
        """

        def mock_send_request(self, method, params):
            if method == 'proxygroup.get':
                return [{
                    "proxy_groupid": "4",
                    "name": "test_proxy_group",
                    "failover_delay": "1m",
                    "min_online": "2",
                    "description": "description of proxy group"
                }]

            return True

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return [{'name': proxy_group_name, 'proxy_groupid': '4'}]

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy_group,
            'failover_delay': '2m',
            'min_online': '10',
            'description': 'new description'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated proxy group: {0}'.format(zabbix_proxy_group))

    def test_update_proxy_error(self):
        """
        Testing the proxy update function in case of encountering an error
        during the update.
        Test for Zabbix version 7.0 +

        Expected result: the task has been failed.
        """

        def mock_send_request(self, method, params):
            if method == 'proxygroup.get':
                return [{
                    "proxy_groupid": "4",
                    "name": "test_proxy_group",
                    "failover_delay": "1m",
                    "min_online": "2",
                    "description": "description of proxy group"
                }]

            raise Exception

        def find_zabbix_proxy_groups_by_names(self, proxy_group_name):
            return [{'name': proxy_group_name, 'proxy_groupid': '4'}]

        zabbix_proxy_group = 'test_proxy_group'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy_group,
            'failover_delay': '2m',
            'min_online': '10',
            'description': 'new description'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["failed"])
            self.assertEqual(
                ansible_result.exception.args[0]["msg"],
                'Failed to update proxy group: {0}'.format(zabbix_proxy_group))
