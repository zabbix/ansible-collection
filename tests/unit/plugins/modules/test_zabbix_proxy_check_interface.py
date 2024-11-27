#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)
from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    default_values)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of API is returned.
    """
    return '6.0.18'


class TestCheckInterfaceZabbixProxy(TestModules):
    module = zabbix_proxy

    def test_check_interface_param_passive_proxy(self):
        """
        Testing the function of checking interface setting for passive proxy.
        Test for both Zabbix version 6.0 and 7.0 +

        Expected result: all executions of the function returned
        expected data.

        Test cases:
        # Base cases. Must return valid value of field
        1. Valid value of address field as IP for passive proxy for Zabbix version 7.0 +
        2. Valid value of address field as IP for passive proxy for Zabbix version 6.0
        3. Valid value of address field as DNS for passive proxy for Zabbix version 7.0 +
        4. Valid value of address field as DNS for passive proxy for Zabbix version 6.0
        5. Valid value of port field for passive proxy for Zabbix version 7.0 +
        6. Valid value of port field for passive proxy for Zabbix version 6.0
        # Case of returning default values of field
        7. Empty value of address field as IP for passive proxy for Zabbix version 7.0 +
        8. Empty value of address field as IP for passive proxy for Zabbix version 6.0
        9. Empty value of address field as DNS for passive proxy for Zabbix version 7.0 +
        10. Empty value of address field as DNS for passive proxy for Zabbix version 6.0
        11. Empty value of port field for passive proxy for Zabbix version 7.0 +
        12. Empty value of port field for passive proxy for Zabbix version 6.0
        """
        test_cases = [
            {
                'number': 1,
                'input': {'address': '192.168.10.10'},
                'param': 'address',
                'proxy_mode': '1',
                'default_pname': None,
                'expected': '192.168.10.10'
            },
            {
                'number': 2,
                'input': {'address': '192.168.10.10'},
                'param': 'address',
                'proxy_mode': '6',
                'default_pname': None,
                'expected': '192.168.10.10'
            },
            {
                'number': 3,
                'input': {'address': 'dns-name.test'},
                'param': 'address',
                'proxy_mode': '1',
                'default_pname': 'proxy_dns',
                'expected': 'dns-name.test'
            },
            {
                'number': 4,
                'input': {'address': 'dns-name.test'},
                'param': 'address',
                'proxy_mode': '6',
                'default_pname': 'proxy_dns',
                'expected': 'dns-name.test'
            },
            {
                'number': 5,
                'input': {'port': '10051'},
                'param': 'port',
                'proxy_mode': '1',
                'default_pname': None,
                'expected': '10051'
            },
            {
                'number': 6,
                'input': {'port': '10051'},
                'param': 'port',
                'proxy_mode': '6',
                'default_pname': None,
                'expected': '10051'
            },
            {
                'number': 7,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '1',
                'default_pname': None,
                'expected': default_values['proxy_address']
            },
            {
                'number': 8,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '6',
                'default_pname': None,
                'expected': default_values['proxy_address']
            },
            {
                'number': 9,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '1',
                'default_pname': 'proxy_dns',
                'expected': default_values['proxy_dns']
            },
            {
                'number': 10,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '6',
                'default_pname': 'proxy_dns',
                'expected': default_values['proxy_dns']
            },
            {
                'number': 11,
                'input': {'port': ''},
                'param': 'port',
                'proxy_mode': '1',
                'default_pname': None,
                'expected': default_values['proxy_port']
            },
            {
                'number': 12,
                'input': {'port': ''},
                'param': 'port',
                'proxy_mode': '6',
                'default_pname': None,
                'expected': default_values['proxy_port']
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy',
                    'interface': case['input']}
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                # Check address param as IP
                result = proxy.check_interface_param(case['param'], case['proxy_mode'], case['default_pname'])
                self.assertEqual(result, case['expected'])

    def test_check_interface_param_active_proxy(self):
        """
        Testing the function of checking interface setting for active proxy.
        Test for both Zabbix version 6.0 and 7.0 +

        Expected result: all executions of the function returned
        expected data.

        Test cases:
        # Base cases. Must return default value of field
        1. Default value of address field as IP for active proxy for Zabbix version 7.0 +
        2. Default value of address field as IP for active proxy for Zabbix version 6.0
        3. Default value of address field as DNS for active proxy for Zabbix version 7.0 +
        4. Default value of address field as DNS for active proxy for Zabbix version 6.0
        5. Default value of port field for active proxy for Zabbix version 7.0 +
        6. Default value of port field for active proxy for Zabbix version 6.0
        # Case of returning default values of field
        7. Empty value of address field as IP for active proxy for Zabbix version 7.0 +
        8. Empty value of address field as IP for active proxy for Zabbix version 6.0
        9. Empty value of address field as DNS for active proxy for Zabbix version 7.0 +
        10. Empty value of address field as DNS for active proxy for Zabbix version 6.0
        11. Empty value of port field for active proxy for Zabbix version 7.0 +
        12. Empty value of port field for active proxy for Zabbix version 6.0
        """
        test_cases = [
            {
                'number': 1,
                'input': {'address': '127.0.0.1'},
                'param': 'address',
                'proxy_mode': '0',
                'default_pname': None,
                'expected': '127.0.0.1'
            },
            {
                'number': 2,
                'input': {'address': '127.0.0.1'},
                'param': 'address',
                'proxy_mode': '5',
                'default_pname': None,
                'expected': '127.0.0.1'
            },
            {
                'number': 3,
                'input': {'address': 'localhost'},
                'param': 'address',
                'proxy_mode': '0',
                'default_pname': 'proxy_dns',
                'expected': 'localhost'
            },
            {
                'number': 4,
                'input': {'address': 'localhost'},
                'param': 'address',
                'proxy_mode': '5',
                'default_pname': 'proxy_dns',
                'expected': 'localhost'
            },
            {
                'number': 5,
                'input': {'port': '10051'},
                'param': 'port',
                'proxy_mode': '0',
                'default_pname': None,
                'expected': '10051'
            },
            {
                'number': 6,
                'input': {'port': '10051'},
                'param': 'port',
                'proxy_mode': '5',
                'default_pname': None,
                'expected': '10051'
            },
            {
                'number': 7,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '0',
                'default_pname': None,
                'expected': default_values['proxy_address']
            },
            {
                'number': 8,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '5',
                'default_pname': None,
                'expected': default_values['proxy_address']
            },
            {
                'number': 9,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '0',
                'default_pname': 'proxy_dns',
                'expected': default_values['proxy_dns']
            },
            {
                'number': 10,
                'input': {'address': ''},
                'param': 'address',
                'proxy_mode': '5',
                'default_pname': 'proxy_dns',
                'expected': default_values['proxy_dns']
            },
            {
                'number': 11,
                'input': {'port': ''},
                'param': 'port',
                'proxy_mode': '0',
                'default_pname': None,
                'expected': default_values['proxy_port']
            },
            {
                'number': 12,
                'input': {'port': ''},
                'param': 'port',
                'proxy_mode': '5',
                'default_pname': None,
                'expected': default_values['proxy_port']
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy',
                    'interface': case['input']}
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                # Check address param as IP
                result = proxy.check_interface_param(case['param'], case['proxy_mode'], case['default_pname'])
                self.assertEqual(result, case['expected'])

    def test_check_interface_param_active_proxy_error(self):
        """
        Testing the function of checking interface setting for active proxy.
        Test for both Zabbix version 6.0 and 7.0 +

        Expected result: all executions of the function returned error.

        Test cases:
        # Non default value for active proxy. Must return Exception.
        1. Non default value of address field as IP for active proxy for Zabbix version 7.0 +
        2. Non default value of address field as IP for active proxy for Zabbix version 6.0
        3. Non default value of address field as DNS for active proxy for Zabbix version 7.0 +
        4. Non default value of address field as DNS for active proxy for Zabbix version 6.0
        5. Non default value of port field for active proxy for Zabbix version 7.0 +
        6. Non default value of port field for active proxy for Zabbix version 6.0
        """
        test_cases = [
            {
                'number': 1,
                'input': {'address': '192.168.10.10'},
                'param': 'address',
                'proxy_mode': '0',
                'default_pname': None
            },
            {
                'number': 2,
                'input': {'address': '192.168.10.10'},
                'param': 'address',
                'proxy_mode': '5',
                'default_pname': None
            },
            {
                'number': 3,
                'input': {'address': 'dns-name.test'},
                'param': 'address',
                'proxy_mode': '0',
                'default_pname': 'proxy_dns'
            },
            {
                'number': 4,
                'input': {'address': 'dns-name.test'},
                'param': 'address',
                'proxy_mode': '5',
                'default_pname': 'proxy_dns'
            },
            {
                'number': 5,
                'input': {'port': '10052'},
                'param': 'port',
                'proxy_mode': '0',
                'default_pname': None
            },
            {
                'number': 6,
                'input': {'port': '10052'},
                'param': 'port',
                'proxy_mode': '5',
                'default_pname': None
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy',
                    'interface': case['input']}
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                # Check address param as IP
                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.check_interface_param(case['param'], case['proxy_mode'], case['default_pname'])

                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    'Available only in passive proxy mode.',
                    ansible_result.exception.args[0]['msg'])
