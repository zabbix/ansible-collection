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

from ansible.errors import AnsibleParserError
from ansible.parsing.yaml.objects import AnsibleUnicode


class TestValidation(unittest.TestCase):

    def test_getting_version(self):
        """
        This test checks validation of query.

        Test cases:
            1. Parameters are empty .
            2. Parameters with 'None' in value.
            3. Parameters with values, with not require version.
            4. Parameters with values, with not require version in upper case.
            5. Two parameters with values, with not require version.
            5. Parameters with values, with require version. Request of the version.
            6. Parameters with values, with require version in upper case. Request of the version.
            7. Two parameters and one of them, with require version. Request of the version.
            8. Two parameters and one of them, with require version in upper case
               + one in different field. Request of the version.

        Expected result: all cases run successfully.
        """

        # mock for get_api_version
        def mock_get_api_version(self):
            return '7.0.0'

        with patch.multiple(
                InventoryModule,
                get_api_version=mock_get_api_version):

            test_cases = [
                {'input': {},
                 'expected': False},
                {'input': {'query': None, 'output': None, 'filter': None},
                 'expected': False},
                {'input': {'output': ['name']},
                 'expected': False},
                {'input': {'output': ['NAME']},
                 'expected': False},
                {'input': {'filter': {'status': AnsibleUnicode('enabled'), 'tags_behavior': AnsibleUnicode('and/or')}},
                 'expected': False},
                {'input': {'filter': {'proxy_group': 'test'}},
                 'expected': True},
                {'input': {'filter': {'PROXY_GROUP': 'test'}},
                 'expected': True},
                {'input': {'filter': {'proxy_group': 'test', 'status': AnsibleUnicode('enabled')}},
                 'expected': True},
                {'input': {'filter': {'proxy_group': 'test', 'status': AnsibleUnicode('enabled')}, 'output': ['NAME']},
                 'expected': True}]

            inventory = InventoryModule()
            for each in test_cases:
                inventory.args = each['input']
                inventory.validate_params()
                self.assertEqual(hasattr(inventory, 'zabbix_version'), each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_query_validation(self):
        """
        This test checks validation of query.

        Test cases:
            1. Query written in lower case.
            2. Query parameter in upper case.
            3. Query parameters as string.
            4. Query parameters as list with 'name' and 'extend'.
            5. Query parameters as string with 'extend' value.
            6. Empty query parameters.

        Expected result: all cases run successfully.
        """
        test_cases = [
            {'input': {'query': {'selectitems': ['name']}},
             'expected': {'query': {'selectItems': ['name']}}},
            {'input': {'query': {'selectitems': ['NAME']}},
             'expected': {'query': {'selectItems': ['name']}}},
            {'input': {'query': {'selectitems': AnsibleUnicode('name')}},
             'expected': {'query': {'selectItems': ['name']}}},
            {'input': {'query': {'selectitems': ['name', 'extend']}},
             'expected': {'query': {'selectItems': 'extend'}}},
            {'input': {'query': {'selectitems': AnsibleUnicode('extend')}},
             'expected': {'query': {'selectItems': 'extend'}}},
            {'input': {'query': None},
             'expected': {'query': None}}]

        inventory = InventoryModule()
        for each in test_cases:
            inventory.args = each['input']
            inventory.validate_params()
            self.assertEqual(inventory.args, each['expected'],
                             'error with input data: {0}'.format(each['input']))

    def test_query_validation_error(self):
        """
        This test checks validation of query and only failed cases.

        Test cases:
            1. Invalid query options.

        Expected result: all cases run successfully.
        """
        test_cases = [
            {'input': {'query': {'select': ['name']}}, 'expected': 'Unknown query parameters'}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = each['input']

            with self.assertRaises(AnsibleParserError) as ansible_result:
                inventory.validate_params()
            self.assertIn(each['expected'], str(ansible_result.exception))

    def test_output_validation(self):
        """
        This test checks output validation.

        Test cases:
            1. Output as a list.
            2. Output as a list in upper case.
            3. Empty value.

        Expected result: all cases run successfully.
        """
        test_cases = [
            {'input': {'output': ['name']}, 'expected': {'output': ['name']}},
            {'input': {'output': ['NAME']}, 'expected': {'output': ['name']}},
            {'input': {'output': None}, 'expected': {'output': None}}]

        inventory = InventoryModule()
        for each in test_cases:
            inventory.args = each['input']
            inventory.validate_params()
            self.assertEqual(inventory.args, each['expected'],
                             'error with input data: {0}'.format(each['input']))

    def test_filter_validation(self):
        """
        This test checks filter validation.

        Test cases:
            1. Filter option in upper case and value as a string.
            2. Filter option in upper case and value as a list.
            3. Filter option in upper case and value in upper case as a list.
            4. Filter option in upper case and two values as a list.
            5. Filter 'status' option with 'enabled' value.
            6. Filter 'status' option with 'disabled' value.
            7. Filter 'status' option with empty value.
            8. Filter 'tags_behavior' option with 'and/or' value.
            9. Filter 'tags_behavior' option with 'or' value.
            10. Filter 'tags_behavior' option with empty value.
            11. Filter 'tags' option with empty value.
            12. Filter 'tags' option in upper case and with value in upper case.
            13. Filter 'tags' option with operator in lower case.
            14. Filter 'tags' option with operator in upper case.

        Expected result: all cases run successfully.
        """
        test_cases = [
            {'input': {'filter': {'TEMPLATES': 'test'}},
             'expected': {'filter': {'templates': 'test'}}},
            {'input': {'filter': {'TEMPLATES': ['test']}},
             'expected': {'filter': {'templates': ['test']}}},
            {'input': {'filter': {'TEMPLATES': ['TEST']}},
             'expected': {'filter': {'templates': ['TEST']}}},
            {'input': {'filter': {'TEMPLATES': ['test', 'test*']}},
             'expected': {'filter': {'templates': ['test', 'test*']}}},
            {'input': {'filter': {'status': AnsibleUnicode('enabled')}},
             'expected': {'filter': {'status': 'enabled'}}},
            {'input': {'filter': {'status': AnsibleUnicode('disabled')}},
             'expected': {'filter': {'status': 'disabled'}}},
            {'input': {'filter': {'status': None}},
             'expected': {'filter': {'status': None}}},
            {'input': {'filter': {'tags_behavior': AnsibleUnicode('and/or')}},
             'expected': {'filter': {'tags_behavior': 'and/or'}}},
            {'input': {'filter': {'tags_behavior': AnsibleUnicode('or')}},
             'expected': {'filter': {'tags_behavior': 'or'}}},
            {'input': {'filter': {'tags_behavior': None}},
             'expected': {'filter': {'tags_behavior': None}}},
            {'input': {'filter': {'tags': None}},
             'expected': {'filter': {'tags': None}}},
            {'input': {'filter': {'TAGS': [{'TAG': 'TEST'}]}},
             'expected': {'filter': {'tags': [{'tag': 'TEST'}]}}},
            {'input': {'filter': {'tags': [{'tag': 'TEST', 'operator': 'equals'}]}},
             'expected': {'filter': {'tags': [{'tag': 'TEST', 'operator': 'equals'}]}}},
            {'input': {'filter': {'tags': [{'tag': 'TEST', 'operator': 'EQUALS'}]}},
             'expected': {'filter': {'tags': [{'tag': 'TEST', 'operator': 'equals'}]}}}]

        inventory = InventoryModule()
        for each in test_cases:
            inventory.args = each['input']
            inventory.validate_params()
            self.assertEqual(inventory.args, each['expected'],
                             'error with input data: {0}'.format(each['input']))

    def test_filter_validation_proxy_group(self):
        """
        This test checks filter validation proxy_group.

        Test cases:
            1. Filter option in upper case and value as a string.
            2. Filter option in upper case and value as a list.
            3. Filter option in upper case and value in upper case as a list.
            4. Filter option in upper case and two values as a list.

        Expected result: all cases run successfully.
        """

        # mock for get_api_version
        def mock_get_api_version(self):
            return '7.0.0'

        with patch.multiple(
                InventoryModule,
                get_api_version=mock_get_api_version):

            test_cases = [
                {'input': {'filter': {'PROXY_GROUP': 'test'}},
                 'expected': {'filter': {'proxy_group': 'test'}}},
                {'input': {'filter': {'PROXY_GROUP': ['test']}},
                 'expected': {'filter': {'proxy_group': ['test']}}},
                {'input': {'filter': {'PROXY_GROUP': ['TEST']}},
                 'expected': {'filter': {'proxy_group': ['TEST']}}},
                {'input': {'filter': {'PROXY_GROUP': ['test', 'test*']}},
                 'expected': {'filter': {'proxy_group': ['test', 'test*']}}}]

            inventory = InventoryModule()
            for each in test_cases:
                inventory.args = each['input']
                inventory.validate_params()
                self.assertEqual(inventory.args, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_filter_validation_error_proxy_group(self):
        """
        This test checks filter validation of proxy group parameter
        with error in case of Zabbix varsion below 7.0.0.

        Test cases:
            1. Filter 'proxy_group' option with Zabbix version 6.0.18.

        Expected result: all cases run successfully.
        """

        # mock for get_api_version
        def mock_get_api_version(self):
            return '6.0.18'

        with patch.multiple(
                InventoryModule,
                get_api_version=mock_get_api_version):

            test_cases = [
                {'input': {'filter': {'proxy_group': 'test'}},
                 'expected': 'Unsupported filter: proxy_group. This filter is not supported in Zabbix API v.6.0.18'}]

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']

                with self.assertRaises(AnsibleParserError) as ansible_result:
                    inventory.validate_params()
                self.assertIn(each['expected'], str(ansible_result.exception))

    def test_filter_validation_error(self):
        """
        This test checks filter validation only with error cases.

        Test cases:
            1. Filter 'status' option with not 'AnsibleUnicode' type.
            2. Filter 'status' option with invalid value.
            3. Filter 'tags_behavior' option with not 'AnsibleUnicode' type.
            4. Filter 'tags_behavior' option with invalid value.
            5. Filter 'tags' option without tag name.
            6. Filter 'tags' option with invalid 'operator' value.

        Expected result: all cases run successfully.
        """
        test_cases = [
            {'input': {'filter': {'status': 'enabled'}},
             'expected': 'Unknown status filter'},
            {'input': {'filter': {'status': AnsibleUnicode('invalid status')}},
             'expected': 'Unknown status filter'},
            {'input': {'filter': {'tags_behavior': 'or'}},
             'expected': 'Unknown tags_behavior filter'},
            {'input': {'filter': {'tags_behavior': AnsibleUnicode('invalid tags_behavior')}},
             'expected': 'Unknown tags_behavior filter'},
            {'input': {'filter': {'tags': [{'value': 'TEST', 'operator': 'EQUALS'}]}},
             'expected': 'Not found tag name'},
            {'input': {'filter': {'tags': [{'tag': 'TEST', 'operator': 'INVALID'}]}},
             'expected': 'Unknown tag operator filter'}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = each['input']

            with self.assertRaises(AnsibleParserError) as ansible_result:
                inventory.validate_params()
            self.assertIn(each['expected'], str(ansible_result.exception))
