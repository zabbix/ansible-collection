#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.inventory.zabbix_inventory import InventoryModule

import sys

if sys.version_info[0] > 2:
    import unittest
    from unittest.mock import patch
else:
    try:
        import unittest2 as unittest
        from mock import patch
    except ImportError:
        print("Error import unittest library for Python 2")


class TestParserResolving(unittest.TestCase):

    def test_resolve_ids_proxy(self):
        """
        This test checks 'self.ids' in case of resolving proxyid -> proxy_name.

        Test cases:
            1. 'self.ids' is absent.
            2. 'self.ids' is empty.
            3. 'self.ids' contains one proxyid. Need to request another one.
            4. 'self.ids' contains required proxyid.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if method == 'proxy.get':
                if params['proxyids'] == ['2']:
                    return [{'proxyid': '2', 'host': 'Linux proxy'}]
                if params['proxyids'] == ['3']:
                    return [{'proxyid': '3', 'host': 'Windows proxy'}]
                else:
                    return []
            if method == 'proxygroup.get':
                return []

        test_cases = [
            # case #1
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'zabbix_hosts': [{'host': 'test', 'proxy_hostid': '2'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxy_hostid': '2', 'proxy_name': 'Linux proxy'}}},
            # case #2
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxy_hostid': '2'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxy_hostid': '2', 'proxy_name': 'Linux proxy'}}},
            # case #3
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxy_hostid': '3'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy', '3': 'Windows proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxy_hostid': '3', 'proxy_name': 'Windows proxy'}}},
            # case #4
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxy_hostid': '2'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxy_hostid': '2', 'proxy_name': 'Linux proxy'}}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '6.0.18'
                inventory.zabbix_hosts = each['zabbix_hosts']
                if 'ids' in each:
                    inventory.ids = each['ids']
                inventory.resolve_id_to_names()
                self.assertEqual(inventory.ids.keys(), each['expected']['ids'].keys(),
                                 'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.zabbix_hosts[0].items())),
                    dict(sorted(each['expected']['zabbix_hosts'].items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy').items())),
                    dict(sorted(each['expected']['ids'].get('proxy').items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy_group').items())),
                    dict(sorted(each['expected']['ids'].get('proxy_group').items())),
                    'error with input data: {0}'.format(each['input']))

    def test_resolve_ids_proxy_in_diff_output(self):
        """
        This test checks 'self.ids' in case of different 'output' params.

        Test cases:
            1. Output == extend. 'proxyid' and 'proxy_groupid' must be present.
            2. Output == proxyid. 'proxyid' must be present.
            3. Output == status. 'proxyid' and 'proxy_groupid' must NOT be present.
            4. Output == extend. zabbix_hosts is empty. Result empty.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if method == 'proxy.get':
                if params['proxyids'] == ['2']:
                    return [{'proxyid': '2', 'host': 'Linux proxy'}]
                else:
                    return []
            if method == 'proxygroup.get':
                return []

        test_cases = [
            # case #1
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'zabbix_hosts': [{'host': 'test', 'proxy_hostid': '2', 'proxy_groupid': '0'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxy_hostid': '2', 'proxy_name': 'Linux proxy',
                                 'proxy_groupid': '0', 'proxy_group_name': ''}}},
            # case #2
            {'input': {'filter': {'status': 'enabled'}, 'output': 'proxy_hostid'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxy_hostid': '2'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxy_hostid': '2', 'proxy_name': 'Linux proxy'}}},
            # case #3
            {'input': {'filter': {'status': 'enabled'}, 'output': 'status'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'status': 'enabled'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'status': 'enabled'}}},
            # case #4
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {}},
                'zabbix_hosts': {}}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '6.0.18'
                inventory.zabbix_hosts = each['zabbix_hosts']
                if 'ids' in each:
                    inventory.ids = each['ids']
                inventory.resolve_id_to_names()
                self.assertEqual(inventory.ids.keys(), each['expected']['ids'].keys(),
                                 'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.zabbix_hosts[0].items())),
                    dict(sorted(each['expected']['zabbix_hosts'].items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy').items())),
                    dict(sorted(each['expected']['ids'].get('proxy').items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy_group').items())),
                    dict(sorted(each['expected']['ids'].get('proxy_group').items())),
                    'error with input data: {0}'.format(each['input']))

    def test_resolve_ids_proxy_70(self):
        """
        This test checks 'self.ids' in case of resolving proxyid -> proxy_name.
        Only for Zabbix version above 7.0.0

        Test cases:
            1. 'self.ids' is absent.
            2. 'self.ids' is empty.
            3. 'self.ids' contains one proxyid. Need to request another one.
            4. 'self.ids' contains required proxyid.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if method == 'proxy.get':
                if params['proxyids'] == ['2']:
                    return [{'proxyid': '2', 'name': 'Linux proxy'}]
                if params['proxyids'] == ['3']:
                    return [{'proxyid': '3', 'name': 'Windows proxy'}]
                else:
                    return []
            if method == 'proxygroup.get':
                return []

        test_cases = [
            # case #1
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '2', 'proxy_groupid': '0'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '2', 'proxy_name': 'Linux proxy',
                                 'proxy_groupid': '0', 'proxy_group_name': ''}}},
            # case #2
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '2', 'proxy_groupid': '0'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '2', 'proxy_name': 'Linux proxy',
                                 'proxy_groupid': '0', 'proxy_group_name': ''}}},
            # case #3
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '3', 'proxy_groupid': '0'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy', '3': 'Windows proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '3', 'proxy_name': 'Windows proxy',
                                 'proxy_groupid': '0', 'proxy_group_name': ''}}},
            # case #4
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '2', 'proxy_groupid': '0'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '2', 'proxy_name': 'Linux proxy',
                                 'proxy_groupid': '0', 'proxy_group_name': ''}}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.zabbix_hosts = each['zabbix_hosts']
                if 'ids' in each:
                    inventory.ids = each['ids']
                inventory.resolve_id_to_names()
                self.assertEqual(inventory.ids.keys(), each['expected']['ids'].keys(),
                                 'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.zabbix_hosts[0].items())),
                    dict(sorted(each['expected']['zabbix_hosts'].items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy').items())),
                    dict(sorted(each['expected']['ids'].get('proxy').items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy_group').items())),
                    dict(sorted(each['expected']['ids'].get('proxy_group').items())),
                    'error with input data: {0}'.format(each['input']))

    def test_resolve_ids_proxy_in_diff_output_70(self):
        """
        This test checks 'self.ids' in case of different 'output' params.

        Test cases:
            1. Output == extend. 'proxyid' and 'proxy_groupid' must be present.
            2. Output == proxyid. 'proxyid' must be present.
            3. Output == status. 'proxyid' and 'proxy_groupid' must NOT be present.
            4. Output == extend. zabbix_hosts is empty. Result empty.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if method == 'proxy.get':
                if params['proxyids'] == ['2']:
                    return [{'proxyid': '2', 'name': 'Linux proxy'}]
                else:
                    return []
            if method == 'proxygroup.get':
                return []

        test_cases = [
            # case #1
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '2', 'proxy_groupid': '0'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '2', 'proxy_name': 'Linux proxy',
                                 'proxy_groupid': '0', 'proxy_group_name': ''}}},
            # case #2
            {'input': {'filter': {'status': 'enabled'}, 'output': 'proxyid'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '2'}],
             'expected': {
                'ids': {'proxy': {'2': 'Linux proxy'}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '2', 'proxy_name': 'Linux proxy'}}},
            # case #3
            {'input': {'filter': {'status': 'enabled'}, 'output': 'status'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'status': 'enabled'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'status': 'enabled'}}},
            # case #4
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {}},
                'zabbix_hosts': {}}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.zabbix_hosts = each['zabbix_hosts']
                if 'ids' in each:
                    inventory.ids = each['ids']
                inventory.resolve_id_to_names()
                self.assertEqual(inventory.ids.keys(), each['expected']['ids'].keys(),
                                 'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.zabbix_hosts[0].items())),
                    dict(sorted(each['expected']['zabbix_hosts'].items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy').items())),
                    dict(sorted(each['expected']['ids'].get('proxy').items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy_group').items())),
                    dict(sorted(each['expected']['ids'].get('proxy_group').items())),
                    'error with input data: {0}'.format(each['input']))

    def test_resolve_ids_proxy_group(self):
        """
        This test checks 'self.ids' in case of resolving proxy_groupid -> proxy_group_name.
        Only for Zabbix version above 7.0.0

        Test cases:
            1. 'self.ids' is absent.
            2. 'self.ids' is empty.
            3. 'self.ids' contains one proxy_groupid. Need to request another one.
            4. 'self.ids' contains required proxy_groupid.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if method == 'proxy.get':
                return []
            if method == 'proxygroup.get':
                if params['proxy_groupids'] == ['2']:
                    return [{'proxy_groupid': '2', 'name': 'Linux proxy group'}]
                if params['proxy_groupids'] == ['3']:
                    return [{'proxy_groupid': '3', 'name': 'Windows proxy group'}]
                else:
                    return []

        test_cases = [
            # case #1
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '0', 'proxy_groupid': '2'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '0', 'proxy_name': '',
                                 'proxy_groupid': '2', 'proxy_group_name': 'Linux proxy group'}}},
            # case #2
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '0', 'proxy_groupid': '2'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '0', 'proxy_name': '',
                                 'proxy_groupid': '2', 'proxy_group_name': 'Linux proxy group'}}},
            # case #3
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '0', 'proxy_groupid': '3'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group', '3': 'Windows proxy group'}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '0', 'proxy_name': '',
                                 'proxy_groupid': '3', 'proxy_group_name': 'Windows proxy group'}}},
            # case #4
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '0', 'proxy_groupid': '2'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '0', 'proxy_name': '',
                                 'proxy_groupid': '2', 'proxy_group_name': 'Linux proxy group'}}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.zabbix_hosts = each['zabbix_hosts']
                if 'ids' in each:
                    inventory.ids = each['ids']
                inventory.resolve_id_to_names()
                self.assertEqual(inventory.ids.keys(), each['expected']['ids'].keys(),
                                 'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.zabbix_hosts[0].items())),
                    dict(sorted(each['expected']['zabbix_hosts'].items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy').items())),
                    dict(sorted(each['expected']['ids'].get('proxy').items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy_group').items())),
                    dict(sorted(each['expected']['ids'].get('proxy_group').items())),
                    'error with input data: {0}'.format(each['input']))

    def test_resolve_ids_proxy_group_in_diff_output(self):
        """
        This test checks 'self.ids' in case of different 'output' params.

        Test cases:
            1. Output == extend. 'proxyid' and 'proxy_groupid' must be present.
            2. Output == proxy_group. 'proxy_group' must be present.
            3. Output == status. 'proxyid' and 'proxy_groupid' must NOT be present.
            4. Output == extend. zabbix_hosts is empty. Result empty.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if method == 'proxy.get':
                return []
            if method == 'proxygroup.get':
                if params['proxy_groupids'] == ['2']:
                    return [{'proxy_groupid': '2', 'name': 'Linux proxy group'}]
                else:
                    return []

        test_cases = [
            # case #1
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'zabbix_hosts': [{'host': 'test', 'proxyid': '0', 'proxy_groupid': '2'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
                'zabbix_hosts': {'host': 'test', 'proxyid': '0', 'proxy_name': '',
                                 'proxy_groupid': '2', 'proxy_group_name': 'Linux proxy group'}}},
            # case #2
            {'input': {'filter': {'status': 'enabled'}, 'output': 'proxy_groupid'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'proxy_groupid': '2'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {'2': 'Linux proxy group'}},
                'zabbix_hosts': {'host': 'test', 'proxy_groupid': '2', 'proxy_group_name': 'Linux proxy group'}}},
            # case #3
            {'input': {'filter': {'status': 'enabled'}, 'output': 'status'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{'host': 'test', 'status': 'enabled'}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {}},
                'zabbix_hosts': {'host': 'test', 'status': 'enabled'}}},
            # case #4
            {'input': {'filter': {'status': 'enabled'}, 'output': 'extend'},
             'ids': {'proxy': {}, 'proxy_group': {}},
             'zabbix_hosts': [{}],
             'expected': {
                'ids': {'proxy': {}, 'proxy_group': {}},
                'zabbix_hosts': {}}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.zabbix_hosts = each['zabbix_hosts']
                if 'ids' in each:
                    inventory.ids = each['ids']
                inventory.resolve_id_to_names()
                self.assertEqual(inventory.ids.keys(), each['expected']['ids'].keys(),
                                 'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.zabbix_hosts[0].items())),
                    dict(sorted(each['expected']['zabbix_hosts'].items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy').items())),
                    dict(sorted(each['expected']['ids'].get('proxy').items())),
                    'error with input data: {0}'.format(each['input']))
                self.assertEqual(
                    dict(sorted(inventory.ids.get('proxy_group').items())),
                    dict(sorted(each['expected']['ids'].get('proxy_group').items())),
                    'error with input data: {0}'.format(each['input']))
