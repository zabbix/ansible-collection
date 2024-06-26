#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

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


class TestParserFilters(unittest.TestCase):

    def test_filter_hostgroups(self):
        """
        This test checks filtering by host groups.

        Test cases:
            1. Filter by host groups with asterisk.
            2. Certain host group.
            3. Non-existing host group.
            4. Several conditions in a list with asterisk.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if params['search']['name'] == 'Linux*':
                return [{'groupid': '2'}, {'groupid': '628'}]
            if params['search']['name'] == 'Linux servers':
                return [{'groupid': '2'}]
            if params['search']['name'] == 'Unknown':
                return {}
            if params['search']['name'] == ['Linux*', 'Windows*']:
                return [{'groupid': '2'}, {'groupid': '628'}]

        test_cases = [
            {'input': {'filter': {'hostgroups': 'Linux*'}}, 'expected': {'groupids': ['2', '628']}},
            {'input': {'filter': {'hostgroups': 'Linux servers'}}, 'expected': {'groupids': ['2']}},
            {'input': {'filter': {'hostgroups': 'Unknown'}}, 'expected': {'groupids': []}},
            {'input': {'filter': {'hostgroups': ['Linux*', 'Windows*']}}, 'expected': {'groupids': ['2', '628']}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                result = inventory.parse_filter()
                result['groupids'].sort()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_templates(self):
        """
        This test checks filtering by templates.

        Test cases:
            1. Filter by templates with asterisk.
            2. Certain templates.
            3. Non-existing templates.
            4. Several conditions in a list with asterisk.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if params['search']['name'] == 'Linux*':
                return [{'templateid': '2'}, {'templateid': '628'}]
            if params['search']['name'] == 'Linux template':
                return [{'templateid': '2'}]
            if params['search']['name'] == 'Unknown':
                return {}
            if params['search']['name'] == ['Linux*', 'Windows*']:
                return [{'templateid': '2'}, {'templateid': '628'}]

        test_cases = [
            {'input': {'filter': {'templates': 'Linux*'}}, 'expected': {'templateids': ['2', '628']}},
            {'input': {'filter': {'templates': 'Linux template'}}, 'expected': {'templateids': ['2']}},
            {'input': {'filter': {'templates': 'Unknown'}}, 'expected': {'templateids': []}},
            {'input': {'filter': {'templates': ['Linux*', 'Windows*']}}, 'expected': {'templateids': ['2', '628']}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                result = inventory.parse_filter()
                result['templateids'].sort()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_proxies(self):
        """
        This test checks filtering by proxy.

        Test cases:
            1. Filter by proxy with asterisk.
            2. Certain proxy.
            3. Non-existing proxy.
            4. Several conditions in a list with asterisk.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if params['search']['host'] == 'proxy*':
                return [{'proxyid': '2'}, {'proxyid': '628'}]
            if params['search']['host'] == 'Linux proxy':
                return [{'proxyid': '2'}]
            if params['search']['host'] == 'Unknown':
                return {}
            if params['search']['host'] == ['Linux*', 'Windows*']:
                return [{'proxyid': '2'}, {'proxyid': '628'}]

        test_cases = [
            {'input': {'filter': {'proxy': 'proxy*'}}, 'expected': {'proxyids': ['2', '628']}},
            {'input': {'filter': {'proxy': 'Linux proxy'}}, 'expected': {'proxyids': ['2']}},
            {'input': {'filter': {'proxy': 'Unknown'}}, 'expected': {'proxyids': []}},
            {'input': {'filter': {'proxy': ['Linux*', 'Windows*']}}, 'expected': {'proxyids': ['2', '628']}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '6.0.18'
                result = inventory.parse_filter()
                result['proxyids'].sort()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_host(self):
        """
        This test checks filtering by technical name of hosts.

        Test cases:
            1. Filter by technical name with asterisk.
            2. Certain host.
            3. Non-existing host.
            4. Several conditions in a list with asterisk.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if params['search']['host'] == 'host*':
                return [{'hostid': '2'}, {'hostid': '628'}]
            if params['search']['host'] == 'Linux host':
                return [{'hostid': '2'}]
            if params['search']['host'] == 'Unknown host':
                return {}
            if params['search']['host'] == ['Linux*', 'Windows*']:
                return [{'hostid': '2'}, {'hostid': '628'}]

        test_cases = [
            {'input': {'filter': {'host': 'host*'}}, 'expected': {'hostids': ['2', '628']}},
            {'input': {'filter': {'host': 'Linux host'}}, 'expected': {'hostids': ['2']}},
            {'input': {'filter': {'host': 'Unknown host'}}, 'expected': {'hostids': []}},
            {'input': {'filter': {'host': ['Linux*', 'Windows*']}}, 'expected': {'hostids': ['2', '628']}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                result = inventory.parse_filter()
                result['hostids'].sort()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_name(self):
        """
        This test checks filtering by visible name of hosts.

        Test cases:
            1. Filter by visible name with asterisk.
            2. Certain host.
            3. Non-existing host.
            4. Several conditions in a list with asterisk.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if params['search']['name'] == 'host*':
                return [{'hostid': '2'}, {'hostid': '628'}]
            if params['search']['name'] == 'Linux host':
                return [{'hostid': '2'}]
            if params['search']['name'] == 'Unknown host':
                return {}
            if params['search']['name'] == ['Linux*', 'Windows*']:
                return [{'hostid': '2'}, {'hostid': '629'}]

        test_cases = [
            {'input': {'filter': {'name': 'host*'}}, 'expected': {'hostids': ['2', '628']}},
            {'input': {'filter': {'name': 'Linux host'}}, 'expected': {'hostids': ['2']}},
            {'input': {'filter': {'name': 'Unknown host'}}, 'expected': {'hostids': []}},
            {'input': {'filter': {'name': ['Linux*', 'Windows*']}}, 'expected': {'hostids': ['2', '629']}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                result = inventory.parse_filter()
                result['hostids'].sort()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_host_and_name(self):
        """
        This test checks filtering by visible name and technical name of hosts at the same time.
        Mostly we need to check how these parameters work together and we need to check it in different cases.

        Test cases:
            1. The same value for visible and technical names.
            2. Visible name is empty. As a result, there are 0 hosts found.
            3. Same as previous case, but technical name is empty this time.
            4. Two hosts found by visible name and one host by technical name, one host is common.
            5. Same as previous case but reverse.
            6. No common hosts for the given visible and technical names.
            7. Same as previous case, but with values of visible and technical names reversed.

        Expected result: all cases run successfully.
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            if params['search'].get('name') == 'empty' or params['search'].get('host') == 'empty':
                return []
            if params['search'].get('name') == 'full' or params['search'].get('host') == 'full':
                return [{'hostid': '2'}, {'hostid': '628'}]

            hosts = []
            if 'name' in params['search'] and 'set_1' in params['search']['name']:
                hosts.append({'hostid': '2'})
            if 'host' in params['search'] and 'set_1' in params['search']['host']:
                hosts.append({'hostid': '2'})
            if 'name' in params['search'] and 'set_2' in params['search']['name']:
                hosts.append({'hostid': '628'})
            if 'host' in params['search'] and 'set_2' in params['search']['host']:
                hosts.append({'hostid': '628'})
            return hosts

        test_cases = [
            {'input': {'filter': {'name': 'full', 'host': 'full'}},
             'expected': {'hostids': ['2', '628']}},
            {'input': {'filter': {'name': 'empty', 'host': 'full'}},
             'expected': {'hostids': []}},
            {'input': {'filter': {'name': 'full', 'host': 'empty'}},
             'expected': {'hostids': []}},
            {'input': {'filter': {'name': 'full', 'host': 'set_1'}},
             'expected': {'hostids': ['2']}},
            {'input': {'filter': {'name': 'set_1', 'host': 'full'}},
             'expected': {'hostids': ['2']}},
            {'input': {'filter': {'name': 'set_1', 'host': 'set_2'}},
             'expected': {'hostids': []}},
            {'input': {'filter': {'name': 'set_2', 'host': 'set_1'}},
             'expected': {'hostids': []}}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                result = inventory.parse_filter()
                result['hostids'].sort()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_status(self):
        """
        This test checks filtering by status.

        Test cases:
            1. Status is 'enabled'.
            2. Status is 'disabled'.
            3. Status is 'enabled' in upper case.
            4. Status is 'disabled' in upper case.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'filter': {'status': 'enabled'}}, 'expected': {'filter': {'status': '0'}}},
            {'input': {'filter': {'status': 'disabled'}}, 'expected': {'filter': {'status': '1'}}},
            {'input': {'filter': {'status': 'ENABLED'}}, 'expected': {'filter': {'status': '0'}}},
            {'input': {'filter': {'status': 'DISABLED'}}, 'expected': {'filter': {'status': '1'}}}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = each['input']
            result = inventory.parse_filter()
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each['input']))

    def test_filter_tags(self):
        """
        This test checks filtering by tags.

        Test cases:
            1. Only tag name without value and operator.
            2. Tag with empty value and 'equals' operator.
            3. Tag with name, value and operator.
            4. Tag with name, value and operator (usually unknown operator doesn't work on this level, because in
            validation function this incorrect value will be raised as error.)

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'filter': {'tags': [{'tag': 'test'}]}},
             'expected': {'tags': [{'tag': 'test', 'value': '', 'operator': '0'}]}},
            {'input': {'filter': {'tags': [{'tag': 'test', 'value': 'test'}]}},
             'expected': {'tags': [{'tag': 'test', 'value': 'test', 'operator': '0'}]}},
            {'input': {'filter': {'tags': [{'tag': 'test', 'value': 'test', 'operator': 'contains'}]}},
             'expected': {'tags': [{'tag': 'test', 'value': 'test', 'operator': '0'}]}},
            {'input': {'filter': {'tags': [{'tag': 'test', 'value': 'test', 'operator': 'unknown'}]}},
             'expected': {'tags': [{'tag': 'test', 'value': 'test', 'operator': '0'}]}}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = each['input']
            result = inventory.parse_filter()
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each['input']))

    def test_filter_tags_behavior(self):
        """
        This test checks filtering by 'tags_behavior' parameter.

        Test cases:
            1. Parameter with 'and/or' value.
            2. Parameter with 'or' value.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'filter': {'tags_behavior': 'and/or'}}, 'expected': {'evaltype': '0'}},
            {'input': {'filter': {'tags_behavior': 'or'}}, 'expected': {'evaltype': '2'}}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = each['input']
            result = inventory.parse_filter()
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each['input']))
