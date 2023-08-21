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
else:
    try:
        import unittest2 as unittest
    except ImportError:
        print("Error import unittest library for Python 2")

from ansible.errors import AnsibleParserError
from ansible.parsing.yaml.objects import AnsibleUnicode


class TestValidation(unittest.TestCase):

    def test_query_validation(self):
        """
        This test checks validation of query.

        Test cases:
            1. Query wrote in lower case.
            2. Query parameter in upper case.
            3. Query parameters as string
            4. Query parameters as list with 'name' and 'extend'
            5. Query parameters as string with value 'extend'
            6. Empty query parameters

        Expected result: all cases run success
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
            1. Invalid query options

        Expected result: all cases run success
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
            1. Output as a list
            2. Output as a list in upper case
            3. Empty value

        Expected result: all cases run success
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
            1. Filter option in upper case and value as a string
            2. Filter option in upper case and value as a list
            3. Filter option in upper case and value in upper case as a list
            4. Filter option in upper case and two value as a list
            5. Filter option 'status' with value 'enabled'
            6. Filter option 'status' with value 'disabled'
            7. Filter option 'status' with empty value
            8. Filter option 'tags_behavior' with value 'and/or'
            9. Filter option 'tags_behavior' with value 'or'
            10. Filter option 'tags_behavior' with empty value
            11. Filter option 'tags' with empty value
            12. Filter option 'tags' with upper case and value in upper case
            13. Filter option 'tags' with operator in lower case
            14. Filter option 'tags' with operator in upper case

        Expected result: all cases run success
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

    def test_filter_validation_error(self):
        """
        This test checks filter validation only with error cases.

        Test cases:
            1. Filter option 'status' with not 'AnsibleUnicode' type
            2. Filter option 'status' with invalid value
            3. Filter option 'tags_behavior' with not 'AnsibleUnicode' type
            4. Filter option 'tags_behavior' with invalid value
            5. Filter option 'tags' without tag name
            6. Filter option 'tags' with invalid 'operator' value

        Expected result: all cases run success
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
