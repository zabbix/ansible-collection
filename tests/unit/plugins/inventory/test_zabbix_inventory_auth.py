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

from ansible.errors import AnsibleAuthenticationFailure

import uuid


class TestLogin(unittest.TestCase):

    def test_login_success(self):
        """
        This test checks login function.

        Test cases:
            1. Use only token
            2. Use token and login/password at the same time. Expect, that token will use
            3. Use only login/password

        Expected result: all cases run success
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            return '81d1d5314be37f3444bc5bc0f7d55bbf'

        test_cases = [
            {'input': {'zabbix_api_token': 12345}, 'expected': 12345},
            {'input': {'zabbix_api_token': 12345, 'zabbix_user': 'Admin', 'zabbix_password': 'zabbix'}, 'expected': 12345},
            {'input': {'zabbix_user': 'Admin', 'zabbix_password': 'zabbix'}, 'expected': '81d1d5314be37f3444bc5bc0f7d55bbf'}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                result = inventory.login()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_login_failed(self):
        """
        This test checks login function. It this function we except, that all test cases will we failed.

        Test cases:
            1. Empty credentials
            2. Only login without password
            3. Only password without login
            4. Invalid login/password (with help of mock response)

        Expected result: all cases run success
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            return ''

        test_cases = [
            {'input': {}, 'expected': 'Not found credentials'},
            {'input': {'zabbix_user': 'Admin'}, 'expected': 'Not found credentials'},
            {'input': {'zabbix_password': 'zabbix'}, 'expected': 'Not found credentials'},
            {'input': {'zabbix_user': 'Admin', 'zabbix_password': 'zabbix'}, 'expected': 'Login failed'}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']

                with self.assertRaises(AnsibleAuthenticationFailure) as ansible_result:
                    inventory.login()
                self.assertEqual(str(ansible_result.exception), each['expected'],
                                 'error with input data: {0}'.format(each['input']))


class TestLogout(unittest.TestCase):

    def test_logout_success(self):
        """
        This test checks logout function.

        Test cases:
            1. Empty token parameters. It means, that we used login and password.
            2. Random value for token for attempt to logout.

        Expected result: all cases run success
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            return True

        test_cases = [
            {'input': None, 'expected': True},
            {'input': uuid.uuid4().hex, 'expected': True}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.auth_token = each['input']
                result = inventory.logout()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))

    def test_logout_failed(self):
        """
        This test checks logout function. In this test we except False value from API.

        Test cases:
            1. Empty token parameters. It means, that we used login and password.

        Expected result: all cases run success
        """

        # mock for api_request
        def mock_api_request(self, method, params):
            return False

        test_cases = [{'input': None, 'expected': False}]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.auth_token = each['input']
                inventory.auth = uuid.uuid4().hex
                result = inventory.logout()
                self.assertEqual(result, each['expected'],
                                 'error with input data: {0}'.format(each['input']))
