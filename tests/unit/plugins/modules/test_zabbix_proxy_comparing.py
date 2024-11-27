#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    TestModules, patch)


def mock_api_version_70(self):
    """
    Mock function to get Zabbix API version 7.0.
    """
    return '7.0.0'


class TestWOProcessing(TestModules):
    """Class for testing comparing parameters without processing"""
    module = zabbix_proxy

    def test_params_wo_processing(self):
        """
        Testing proxy name. Result depends on the Zabbix API version.

        Expected result: name parameter will be added to the correct output field.

        Test for Zabbix version 7.0 +
        """
        exist_proxy = {
            'tls_accept': '1',
            'tls_issuer': '123',
            'tls_subject': '123',
            'tls_issuer': '123',
            'tls_subject': '123',
            'tls_connect': '2',
            'custom_timeouts': '1',
            'timeout_zabbix_agent': '3s',
            'timeout_simple_check': '3s',
            'timeout_snmp_agent': '3s',
            'timeout_external_check': '3s',
            'timeout_db_monitor': '3s',
            'timeout_http_agent': '3s',
            'timeout_ssh_agent': '3s',
            'timeout_telnet_agent': '3s',
            'timeout_script': '3s',
            'timeout_browser': '3s',
            'status': '5',
            'operating_mode': '1',
            'proxy_groupid': '1',
            'local_address': '127.0.0.1',
            'local_port': '10051',
            'address': '127.0.0.1',
            'port': '10051',
            'allowed_addresses': '127.0.0.1',
            'proxy_address': '127.0.0.1',
            'description': 'proxy_description'}

        test_cases = [
            {
                'number': 1,
                'input': {'tls_accept': '1', 'tls_issuer': '456', 'tls_subject': ''},
                'exist_proxy': exist_proxy,
                'expected': {'tls_issuer': '456', 'tls_subject': ''}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param = {**input_param, **case['input']}
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.compare_zabbix_proxy(exist_proxy=case['exist_proxy'], new_proxy=case['input'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_params_interface(self):
        """
        Testing comparing proxy interface.

        Expected result: interface parameter will be added to the correct output field.

        Test for Zabbix version 6.0

        Test cases:
        1. Input empty interface
        2. Exist empty interface
        3. Input and exist has empty interface
        4. Equals interface
        5. Input has different ip address
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'exist_proxy': {'interface': []},
                'expected': {'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}}
            },
            {
                'number': 2,
                'input': {'interface': []},
                'exist_proxy': {'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'interface': []}
            },
            {
                'number': 3,
                'input': {'interface': []},
                'exist_proxy': {'interface': []},
                'expected': {}
            },
            {
                'number': 4,
                'input': {'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'exist_proxy': {'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {}
            },
            {
                'number': 5,
                'input': {'interface': {'ip': '192.168.0.11', 'dns': '', 'port': '10051', 'useip': '1'}},
                'exist_proxy': {'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'interface': {'ip': '192.168.0.11', 'dns': '', 'port': '10051', 'useip': '1'}}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param = {**input_param, **case['input']}
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.compare_zabbix_proxy(exist_proxy=case['exist_proxy'], new_proxy=case['input'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))
