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


class TestCompareCachedInputArgs(unittest.TestCase):

    def test_compare_input_args_simple_params(self):
        """
        This test checks function of comparing simple arguments in input parameters.

        Test cases:
            1. Old and new values are the same.
            2. Old and new values are different.
            3. Old and new values are different, but the old one includes a part of the new value.
            4. Old value is empty.
            5. New value is empty.
            6. Old value is None.
            7. New value is None.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': 'test', 'old': 'test', 'expected': True},
            {'input': 'test', 'old': 'value', 'expected': False},
            {'input': 'test', 'old': 'test2', 'expected': False},
            {'input': 'test', 'old': '', 'expected': False},
            {'input': '', 'old': 'test', 'expected': False},
            {'input': 'test', 'old': None, 'expected': False},
            {'input': None, 'old': 'test', 'expected': False}]

        params = ['zabbix_user', 'zabbix_password', 'zabbix_api_token', 'zabbix_api_url']
        for param in params:
            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = {param: each['input']}
                result = inventory.compare_cached_input_args({param: each['old']})
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each))

    def test_compare_input_args_output(self):
        """
        This test checks function of comparing output arguments in input parameters.

        Test cases:
            1. Old and new values are the same.
            2. Old and new values are the same but set as a list.
            3. Old and new values are the same but set as a list in a different order.
            4. Old value has one more element in the list.
            5. New value has one more element in the list.
            6. New value is empty.
            7. Old value is empty.
            8. Old and new values are empty at the same time.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': ['test'], 'old': ['test'], 'expected': True},
            {'input': ['test', 'name'], 'old': ['test', 'name'], 'expected': True},
            {'input': ['name', 'test'], 'old': ['test', 'name'], 'expected': True},
            {'input': ['name', 'test'], 'old': ['test', 'name', 'host'], 'expected': False},
            {'input': ['name', 'test', 'host'], 'old': ['test', 'name'], 'expected': False},
            {'input': [], 'old': ['test', 'name'], 'expected': False},
            {'input': ['test', 'name'], 'old': [], 'expected': False},
            {'input': [], 'old': [], 'expected': True}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = {'output': each['input']}
            result = inventory.compare_cached_input_args({'output': each['old']})
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each))

    def test_compare_input_args_query(self):
        """
        This test checks function of comparing query arguments in input parameters.

        Test cases:
            1. Old and new values are the same.
            2. Old and new values are the same but set as a list.
            3. Old and new values are the same but set as a list and with two values.
            4. Old and new values are the same but set as a list in a different order.
            5. New value has one more element in the list.
            6. Old value has one more element in the list.
            7. New value has one more query.
            8. Old value has one more query.
            9. Different values.
            10. New value is empty.
            11. Old value is empty.
            12. New and old values are empty at the same time.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'selectItems': 'extend'},
             'old': {'selectItems': 'extend'}, 'expected': True},
            {'input': {'selectItems': ['extend']},
             'old': {'selectItems': ['extend']}, 'expected': True},
            {'input': {'selectItems': ['name', 'status']},
             'old': {'selectItems': ['name', 'status']}, 'expected': True},
            {'input': {'selectItems': ['name', 'status']},
             'old': {'selectItems': ['status', 'name']}, 'expected': True},
            {'input': {'selectItems': ['name', 'status', 'lastvalue']},
             'old': {'selectItems': ['status', 'name']}, 'expected': False},
            {'input': {'selectItems': ['name', 'status']},
             'old': {'selectItems': ['status', 'name', 'lastvalue']}, 'expected': False},
            {'input': {'selectItems': ['name', 'status'], 'selectTags': 'extend'},
             'old': {'selectItems': ['status', 'name']}, 'expected': False},
            {'input': {'selectItems': ['name', 'status']},
             'old': {'selectItems': ['status', 'name'], 'selectTags': 'extend'}, 'expected': False},
            {'input': {'selectItems': ['name', 'status']},
             'old': {'selectTags': 'extend'}, 'expected': False},
            {'input': {}, 'old': {'selectTags': 'extend'}, 'expected': False},
            {'input': {'selectItems': ['name', 'status']}, 'old': {}, 'expected': False},
            {'input': {}, 'old': {}, 'expected': True}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = {'query': each['input']}
            result = inventory.compare_cached_input_args({'query': each['old']})
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each))

    def test_compare_input_args_filter(self):
        """
        This test checks function of comparing input arguments.

        Test cases:
            1. Old and new values are the same.
            2. Old value has one more element in the list.
            3. New value has one more element in the list.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'hostgroups': 'Linux*'},
             'old': {'templates': 'Linux*'}, 'expected': False},
            {'input': {'hostgroups': 'Linux*'},
             'old': {'hostgroups': 'Linux*', 'templates': 'Linux*'}, 'expected': False},
            {'input': {'hostgroups': 'Linux*', 'templates': 'Linux*'},
             'old': {'hostgroups': 'Linux*'}, 'expected': False}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = {'filter': each['input']}
            result = inventory.compare_cached_input_args({'filter': each['old']})
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each))

    def test_compare_input_args_filter_simple(self):
        """
        This test checks function of comparing simple input arguments.

        Test cases:
            1. Old and new values are the same.
            2. Old and new values are different.
            3. Old and new values are the same but set as a list.
            4. Old and new values are the same but set as a list with two values each.
            5. Same as previous but in a different order.
            6. Old value has one more element.
            7. New value has one more element.
            8. Old value is empty.
            9. New value is empty.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': 'Linux*', 'old': 'Linux*', 'expected': True},
            {'input': 'Linux*', 'old': 'Windows*', 'expected': False},
            {'input': ['Linux*'], 'old': ['Linux*'], 'expected': True},
            {'input': ['Linux*', 'Windows*'], 'old': ['Linux*', 'Windows*'], 'expected': True},
            {'input': ['Linux*', 'Windows*'], 'old': ['Windows*', 'Linux*'], 'expected': True},
            {'input': ['Linux*'], 'old': ['Linux*', 'Windows*'], 'expected': False},
            {'input': ['Linux*', 'Windows*'], 'old': ['Windows*'], 'expected': False},
            {'input': ['Linux*', 'Windows*'], 'old': '', 'expected': False},
            {'input': '', 'old': ['Windows*', 'Linux*'], 'expected': False}]

        params = ['hostgroups', 'templates', 'proxy', 'name', 'host']
        for param in params:
            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = {'filter': {param: each['input']}}
                result = inventory.compare_cached_input_args({'filter': {param: each['old']}})
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each))

    def test_compare_input_args_filter_status_and_tags_behavior(self):
        """
        This test checks function of comparing input arguments.

        Test cases:
            1. Status value is the same, i.e., 'enabled'.
            2. Status value is the same, i.e., 'disabled'.
            3. Status values are different.
            4. Same as previous but in a different order.
            5. tags_behavior value is the same, i.e., 'or'.
            6. tags_behavior value is the same, i.e., 'and/or'.
            7. tags_behavior values are different.
            8. Same as previous but in a different order.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'status': 'enabled'}, 'old': {'status': 'enabled'}, 'expected': True},
            {'input': {'status': 'disabled'}, 'old': {'status': 'disabled'}, 'expected': True},
            {'input': {'status': 'enabled'}, 'old': {'status': 'disabled'}, 'expected': False},
            {'input': {'status': 'disabled'}, 'old': {'status': 'enabled'}, 'expected': False},
            {'input': {'tags_behavior': 'or'}, 'old': {'tags_behavior': 'or'}, 'expected': True},
            {'input': {'tags_behavior': 'and/or'}, 'old': {'tags_behavior': 'and/or'}, 'expected': True},
            {'input': {'tags_behavior': 'and/or'}, 'old': {'tags_behavior': 'or'}, 'expected': False},
            {'input': {'tags_behavior': 'or'}, 'old': {'tags_behavior': 'and/or'}, 'expected': False}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = {'filter': each['input']}
            result = inventory.compare_cached_input_args({'filter': each['old']})
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each))

    def test_compare_input_args_filter_tags(self):
        """
        This test checks function of comparing input arguments.

        Test cases:
            1. The same value.
            2. Two equal values.
            3. Same as previous but in a different order.
            4. New value has one more tag.
            5. Old value has one more tag.
            6. Different count of elements in the first tag in new value.
            7. Different count of elements in the first tag in old value.
            8. The same values but in a different order.

        Expected result: all cases run successfully.
        """

        test_cases = [
            {'input': {'tags': [{'tag': 'test'}]},
             'old': {'tags': [{'tag': 'test'}]}, 'expected': True},
            {'input': {'tags': [{'tag': 'test'}, {'tag': 'test2'}]},
             'old': {'tags': [{'tag': 'test'}, {'tag': 'test2'}]}, 'expected': True},
            {'input': {'tags': [{'tag': 'test2'}, {'tag': 'test'}]},
             'old': {'tags': [{'tag': 'test'}, {'tag': 'test2'}]}, 'expected': True},
            {'input': {'tags': [{'tag': 'test', 'value': 'test'}]},
             'old': {'tags': [{'tag': 'test'}]}, 'expected': False},
            {'input': {'tags': [{'tag': 'test'}]},
             'old': {'tags': [{'tag': 'test', 'value': 'test'}]}, 'expected': False},
            {'input': {'tags': [{'tag': 'test2'}, {'tag': 'test', 'value': 'test'}]},
             'old': {'tags': [{'tag': 'test'}, {'tag': 'test2'}]}, 'expected': False},
            {'input': {'tags': [{'tag': 'test2'}, {'tag': 'test'}]},
             'old': {'tags': [{'tag': 'test', 'value': 'test'}, {'tag': 'test2'}]}, 'expected': False},
            {'input': {'tags': [{'tag': 'test2'}, {'tag': 'test', 'value': 'test'}]},
             'old': {'tags': [{'tag': 'test', 'value': 'test'}, {'tag': 'test2'}]}, 'expected': True}]

        for each in test_cases:
            inventory = InventoryModule()
            inventory.args = {'filter': each['input']}
            result = inventory.compare_cached_input_args({'filter': each['old']})
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each))
