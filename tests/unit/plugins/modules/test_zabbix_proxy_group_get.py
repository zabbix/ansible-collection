#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy_group
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of API is returned.
    """
    return '6.0.18'


def mock_api_version_70(self):
    """
    Mock function to get Zabbix API version 7.0.0.
    """
    return '7.0.0'


class TestGetZabbixProxy(TestModules):
    module = zabbix_proxy_group

    def test_get_zabbix_proxy_group_70(self):
        """
        Testing function of getting data via proxy group from Zabbix.
        Test for Zabbix version 7.0 +

        Expected result: all executions of function returned
        empty inventory data.
        """

        def mock_send_request(self, method, params):
            proxy_group_data = {
                'proxy_groupid': '4',
                'name': 'test_proxy_group',
                'failover_delay': '1m',
                'min_online': '2'
            }

            return [proxy_group_data]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request):

            # Check simple get proxy data
            self.mock_module_functions.params = {}
            proxy_group = self.module.Proxy_group(self.mock_module_functions)

            result = proxy_group.get_zabbix_proxy_group('4')
            self.assertEqual(result.get('min_online'), '2')
            self.assertEqual(result.get('failover_delay'), '1m')

    def test_get_zabbix_proxy_group_error(self):
        """
        Testing function of getting data via proxy group from Zabbix
        with error during request.

        Expected result: Exception.
        """

        def mock_send_request(self, method, params):
            raise Exception

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request):

            proxy_group = self.module.Proxy_group(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy_group.get_zabbix_proxy_group('4')
            self.assertIn(
                'Failed to get existing proxy group:',
                ansible_result.exception.args[0]['msg'])

    def test_get_zabbix_proxy_group_60(self):
        """
        Testing function of getting data via proxy group from Zabbix
        version 6.0 with error during request.

        Expected result: Exception.
        """

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.Proxy_group(self.mock_module_functions)
            self.assertIn(
                'Proxy groups are not supported in Zabbix versions',
                ansible_result.exception.args[0]['msg'])
