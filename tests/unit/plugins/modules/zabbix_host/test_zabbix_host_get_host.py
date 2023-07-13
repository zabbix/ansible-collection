#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_host
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of the API is returned.
    """
    return '6.0.18'


class TestGetZabbixHost(TestModules):
    module = zabbix_host

    def test_get_zabbix_host_only_host(self):
        """
        Testing the function of getting data by host from Zabbix.

        Expected result: all executions of the function returned
        empty inventory data.
        """
        def mock_send_request(self, method, params):
            host_data = {
                'hostid': '10582',
                'proxy_hostid': '0',
                'host': 'test',
                'status': '0'}
            if 'selectItems' in params:
                host_data['items'] = [{
                    'name': 'test',
                    'inventory_link': '0'}]
                host_data['inventory'] = {
                    'type': '',
                    'type_full': ''}
            return [host_data]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            # Check simple get host data
            self.mock_module_functions.params = {}
            host = self.module.Host(self.mock_module_functions)

            result = host.get_zabbix_host('10582')
            self.assertEqual(result.get('items'), None)
            self.assertEqual(result.get('inventory'), None)

            # Check get host data with empty inventory
            self.mock_module_functions.params = {'inventory': True}
            host = self.module.Host(self.mock_module_functions)

            result = host.get_zabbix_host('10582')
            self.assertNotEqual(result.get('items'), None)
            self.assertNotEqual(result.get('inventory'), None)
            self.assertEqual(host.inventory_links, {})

    def test_get_zabbix_host_w_inventory(self):
        """
        Testing the function of getting data by host from Zabbix
        with inventory data.

        Expected result: the execution of the function returns
        inventory data.
        """
        def mock_send_request(self, method, params):
            host_data = {
                'hostid': '10582',
                'proxy_hostid': '0',
                'host': 'test',
                'status': '0'}
            if 'selectItems' in params:
                host_data['items'] = [{
                    'name': 'test',
                    'inventory_link': '1'}]
                host_data['inventory'] = {
                    'type': '',
                    'type_full': ''}
            return [host_data]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            self.mock_module_functions.params = {'inventory': True}
            host = self.module.Host(self.mock_module_functions)

            result = host.get_zabbix_host('10582')
            self.assertEqual(
                result.get('items'),
                [{'name': 'test', 'inventory_link': '1'}])
            self.assertEqual(
                result.get('inventory'),
                {'type': '', 'type_full': ''})
            self.assertEqual(host.inventory_links['type'], 'test')

    def test_get_zabbix_host_error(self):
        """
        Testing the function of getting data by host from Zabbix
        with error during request.

        Expected result: Exception.
        """
        def mock_send_request(self, method, params):
            raise Exception

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            host = self.module.Host(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                host.get_zabbix_host('10582')
            self.assertIn(
                'Failed to get existing host:',
                ansible_result.exception.args[0]['msg'])
