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


def mock_api_version_70(self):
    """
    Mock function to get Zabbix API version 7.0.
    """
    return '7.0.0'


class TestProxyName(TestModules):
    """Class for testing name of the proxy depends on Zabbix version"""
    module = zabbix_proxy

    def test_proxy_name_param_70(self):
        """
        Testing proxy name. Result depends on the Zabbix API version.

        Expected result: name parameter will be added to the correct output field.

        Test for Zabbix version 7.0 +
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            input_param = {
                'state': 'present',
                'name': 'test_proxy'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            result = proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertEqual(result, {'name': 'test_proxy', 'operating_mode': '0'})

    def test_proxy_name_param_60(self):
        """
        Testing proxy name. Result depends on the Zabbix API version.

        Expected result: name parameter will be added to the correct output field.

        Test for Zabbix version 6.0
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'state': 'present',
                'name': 'test_proxy'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            result = proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertEqual(result, {'host': 'test_proxy', 'status': '5'})


class TestWOProcessing(TestModules):
    """Class for testing parameters that do not require preprocessing"""
    module = zabbix_proxy

    def test_param_wo_processing_70(self):
        """
        Testing parameters that do not require preprocessing.

        Expected result: all parameters will be added in the
        same form as in the input data.

        Test for Zabbix version 7.0 +

        Test cases:
        1. Without params and without existing proxy
        2. Without params but with existing proxy
        3. One parameter in input without existing proxy
        4. One parameter in input with existing proxy
        5. All parameters without existing proxy
        6. All parameters with existing proxy
        """
        exist_proxy = {
            "proxyid": "4",
            "name": "test_proxy",
            "proxy_groupid": "0",
            "local_address": "",
            "local_port": "10051",
            "operating_mode": "0",
            "allowed_addresses": "",
            "address": "127.0.0.1",
            "port": "10051",
            "description": "",
            "tls_connect": "1",
            "tls_accept": "1",
            "tls_issuer": "",
            "tls_subject": "",
            "custom_timeouts": "1",
            "timeout_zabbix_agent": "5s",
            "timeout_simple_check": "3s",
            "timeout_snmp_agent": "3s",
            "timeout_external_check": "3s",
            "timeout_db_monitor": "3s",
            "timeout_http_agent": "3s",
            "timeout_ssh_agent": "3s",
            "timeout_telnet_agent": "3s",
            "timeout_script": "3s",
            "timeout_browser": "60s",
            "lastaccess": "0",
            "version": "0",
            "compatibility": "0",
            "state": "1",
            "proxyGroup": []
        }

        test_cases = [
            {
                'number': 1,
                'input': {},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 2,
                'input': {},
                'exist_proxy': exist_proxy,
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 3,
                'input': {'description': 'test description'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'description': 'test description'}},
            {
                'number': 4,
                'input': {'description': 'test description'},
                'exist_proxy': exist_proxy,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'description': 'test description'}},
            {
                'number': 5,
                'input': {'description': 'test description', 'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer',
                          'tls_psk_identity': 'my_tls_psk_identity', 'tls_subject': 'my_tls_subject'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'description': 'test description',
                             'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer', 'tls_subject': 'my_tls_subject',
                             'tls_psk_identity': 'my_tls_psk_identity'}},
            {
                'number': 6,
                'input': {'description': 'test description', 'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer',
                          'tls_psk_identity': 'my_tls_psk_identity', 'tls_subject': 'my_tls_subject'},
                'exist_proxy': exist_proxy,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'description': 'test description',
                             'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer', 'tls_subject': 'my_tls_subject',
                             'tls_psk_identity': 'my_tls_psk_identity'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_wo_processing_60(self):
        """
        Testing parameters that do not require preprocessing.

        Expected result: all parameters will be added in the
        same form as in the input data.

        Test for Zabbix version 6.0

        Test cases:
        1. Without params and without existing proxy
        2. Without params but with existing proxy
        3. One parameter in input without existing proxy
        4. One parameter in input with existing proxy
        5. All parameters without existing proxy
        6. All parameters with existing proxy
        """
        exist_proxy = {
            "proxy_hostid": "0",
            "host": "test_proxy",
            "status": "5",
            "lastaccess": "0",
            "ipmi_authtype": "-1",
            "ipmi_privilege": "2",
            "ipmi_username": "",
            "ipmi_password": "",
            "maintenanceid": "0",
            "maintenance_status": "0",
            "maintenance_type": "0",
            "maintenance_from": "0",
            "name": "",
            "flags": "0",
            "templateid": "0",
            "description": "",
            "tls_connect": "1",
            "tls_accept": "1",
            "tls_issuer": "",
            "tls_subject": "",
            "proxy_address": "",
            "auto_compress": "1",
            "discover": "0",
            "custom_interfaces": "0",
            "uuid": "",
            "proxyid": "11085",
            "interface": []
        }

        test_cases = [
            {
                'number': 1,
                'input': {},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5'}},
            {
                'number': 2,
                'input': {},
                'exist_proxy': exist_proxy,
                'expected': {'host': 'test_proxy', 'status': '5'}},
            {
                'number': 3,
                'input': {'description': 'test description'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'description': 'test description'}},
            {
                'number': 4,
                'input': {'description': 'test description'},
                'exist_proxy': exist_proxy,
                'expected': {'host': 'test_proxy', 'status': '5', 'description': 'test description'}},
            {
                'number': 5,
                'input': {'description': 'test description', 'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer',
                          'tls_psk_identity': 'my_tls_psk_identity', 'tls_subject': 'my_tls_subject'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'description': 'test description',
                             'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer', 'tls_subject': 'my_tls_subject',
                             'tls_psk_identity': 'my_tls_psk_identity'}},
            {
                'number': 6,
                'input': {'description': 'test description', 'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer',
                          'tls_psk_identity': 'my_tls_psk_identity', 'tls_subject': 'my_tls_subject'},
                'exist_proxy': exist_proxy,
                'expected': {'host': 'test_proxy', 'status': '5', 'description': 'test description',
                             'tls_psk': 'my_tls_psk', 'tls_issuer': 'my_tls_issuer', 'tls_subject': 'my_tls_subject',
                             'tls_psk_identity': 'my_tls_psk_identity'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))


class TestOperatingMode(TestModules):
    """Class for testing operating mode parameter"""
    module = zabbix_proxy

    def test_param_operating_mode_70(self):
        """
        Testing operating mode parameter.

        Expected result: all parameters will be added in correct form.

        Test for Zabbix version 7.0 +

        Test cases:
        1. Set active proxy mode in input data
        2. Set passive proxy mode in input data
        3. Empty input parameters and use active proxy mode from existing proxy
        4. Empty input parameters and use passive proxy mode from existing proxy
        5. Empty input parameters, proxy doesn't exist
        6. Set active proxy mode in input data with active proxy mode on existing proxy
        7. Set passive proxy mode in input data with passive proxy mode on existing proxy
        8. Set active proxy mode in input data with passive proxy mode on existing proxy
        9. Set passive proxy mode in input data with active proxy mode on existing proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 2,
                'input': {'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1'}},
            {
                'number': 3,
                'input': {},
                'exist_proxy': {'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 4,
                'input': {},
                'exist_proxy': {'operating_mode': '1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '1'}},
            {
                'number': 5,
                'input': {},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': default_values['proxy_mode']['7']}},
            {
                'number': 6,
                'input': {'mode': 'active'},
                'exist_proxy': {'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 7,
                'input': {'mode': 'passive'},
                'exist_proxy': {'operating_mode': '1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '1'}},
            {
                'number': 8,
                'input': {'mode': 'active'},
                'exist_proxy': {'operating_mode': '1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 9,
                'input': {'mode': 'passive'},
                'exist_proxy': {'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '1'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_operating_mode_60(self):
        """
        Testing operating mode parameter.

        Expected result: all parameters will be added in correct form.

        Test for Zabbix version 6.0

        Test cases:
        1. Set active proxy mode in input data
        2. Set passive proxy mode in input data
        3. Empty input parameters and use active proxy mode from existing proxy
        4. Empty input parameters and use passive proxy mode from existing proxy
        5. Empty input parameters, proxy doesn't exist
        6. Set active proxy mode in input data with active proxy mode on existing proxy
        7. Set passive proxy mode in input data with passive proxy mode on existing proxy
        8. Set active proxy mode in input data with passive proxy mode on existing proxy
        9. Set passive proxy mode in input data with active proxy mode on existing proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5'}},
            {
                'number': 2,
                'input': {'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {
                                 'dns': 'localhost',
                                 'ip': '127.0.0.1',
                                 'port': '10051',
                                 'useip': '1'}}},
            {
                'number': 3,
                'input': {},
                'exist_proxy': {'status': '5'},
                'expected': {'host': 'test_proxy', 'status': '5'}},
            {
                'number': 4,
                'input': {},
                'exist_proxy': {'status': '6', 'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {
                                 'dns': 'localhost',
                                 'ip': '127.0.0.1',
                                 'port': '10051',
                                 'useip': '1'}}},
            {
                'number': 5,
                'input': {},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': default_values['proxy_mode']['6.0']}},
            {
                'number': 6,
                'input': {'mode': 'active'},
                'exist_proxy': {'status': '5'},
                'expected': {'host': 'test_proxy', 'status': '5'}},
            {
                'number': 7,
                'input': {'mode': 'passive'},
                'exist_proxy': {'status': '6', 'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {
                                 'dns': 'localhost',
                                 'ip': '127.0.0.1',
                                 'port': '10051',
                                 'useip': '1'}}},
            {
                'number': 8,
                'input': {'mode': 'active'},
                'exist_proxy': {'status': '6'},
                'expected': {'host': 'test_proxy', 'status': '5'}},
            {
                'number': 9,
                'input': {'mode': 'passive'},
                'exist_proxy': {'status': '5', 'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {
                                 'dns': 'localhost',
                                 'ip': '127.0.0.1',
                                 'port': '10051',
                                 'useip': '1'}}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))


class TestProxyGroup(TestModules):
    """Class for testing proxy group parameter"""
    module = zabbix_proxy

    def test_param_proxy_group(self):
        """
        Testing proxy group parameter.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Without proxy group parameter
        2. Empty proxy group to reset to default value
        3. Proxy group existed in instance
        """

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'name': proxy_group_names, 'proxy_groupid': '4'}]

        test_cases = [
            {
                'number': 1,
                'input': {},
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 2,
                'input': {'proxy_group': ''},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '0'}},
            {
                'number': 3,
                'input': {'proxy_group': 'test proxy group', 'local_address': 'test_local_address'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_address': 'test_local_address'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=None)
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_proxy_group_60(self):
        """
        Testing proxy group parameter for Zabbix version 6.0.

        Expected result: raised error.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'state': 'present',
                'name': 'test_proxy',
                'proxy_group': 'test proxy group'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Incorrect arguments for Zabbix version',
                ansible_result.exception.args[0]['msg'])

    def test_param_proxy_group_error(self):
        """
        Testing proxy group parameter for Zabbix version 6.0
        Proxy group not exist in Zabbix

        Expected result: raised error.
        """

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return []

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            input_param = {
                'state': 'present',
                'name': 'test_proxy',
                'proxy_group': 'test proxy group'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Proxy group not found in Zabbix',
                ansible_result.exception.args[0]['msg'])


class TestLocalAddress(TestModules):
    """Class for testing local address parameter"""
    module = zabbix_proxy

    def test_param_local_address(self):
        """
        Testing local address parameter.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Empty value suring creation proxy wiout proxy group
        2. Empty value during cleaning proxy group from proxy
        3. Empty value in case of not configured proxy in task and on existing proxy
        4. Correct value with configuring proxy group
        5. Correct value for already configured proxy group
        6. Change proxy group without specifying local address (already has on the exist proxy)
        """

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            if proxy_group_names == 'test_proxy_group_2':
                return [{'name': proxy_group_names, 'proxy_groupid': '5'}]
            return [{'name': proxy_group_names, 'proxy_groupid': '4'}]

        test_cases = [
            {
                'number': 1,
                'input': {'local_address': ''},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 2,
                'input': {'local_address': '', 'proxy_group': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '0'}},
            {
                'number': 3,
                'input': {'local_address': ''},
                'exist_proxy': {'proxy_groupid': '0', 'local_address': '', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0'}},
            {
                'number': 4,
                'input': {'local_address': '192.168.0.10', 'proxy_group': 'test_proxy_group'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'local_address': '192.168.0.10',
                             'proxy_groupid': '4'}},
            {
                'number': 5,
                'input': {'local_address': '192.168.0.10'},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'local_address': '192.168.0.10'}},
            {
                'number': 6,
                'input': {'proxy_group': 'test_proxy_group_2'},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '5'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_local_address_error(self):
        """
        Testing local address parameter for Zabbix version 7.0 +

        Expected result: raised error.

        Test cases:
        1. Clean proxy group with non empty local_address
        2. Set local_address without proxy group
        3. Set local_address during creation proxy
        4. Empty local_address with proxy group
        5. Empty local_address with proxy group configured on proxy
        6. Proxy group without local_address during creation proxy
        6. Proxy group without local_address during updating proxy
        """

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'name': proxy_group_names, 'proxy_groupid': '4'}]

        test_cases = [
            {
                'number': 1,
                'input': {'local_address': '192.168.0.10', 'proxy_group': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 2,
                'input': {'local_address': '192.168.0.10'},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 3,
                'input': {'local_address': '192.168.0.10'},
                'exist_proxy': None,
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 4,
                'input': {'local_address': '', 'proxy_group': 'test_proxy_group'},
                'exist_proxy': None,
                'expected': 'Can not be empty with configured proxy group.'},
            {
                'number': 5,
                'input': {'local_address': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': 'Can not be empty with configured proxy group.'},
            {
                'number': 6,
                'input': {'proxy_group': 'test_proxy_group'},
                'exist_proxy': None,
                'expected': 'Not found required argument: local_address'},
            {
                'number': 7,
                'input': {'proxy_group': 'test_proxy_group'},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': 'Not found required argument: local_address'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])

    def test_param_local_address_60(self):
        """
        Testing proxy group parameter for Zabbix version 6.0.

        Expected result: raised error.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'state': 'present',
                'name': 'test_proxy',
                'local_address': '192.168.0.10'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Incorrect arguments for Zabbix version',
                ansible_result.exception.args[0]['msg'])


class TestLocalPort(TestModules):
    """Class for testing local address parameter"""
    module = zabbix_proxy

    def test_param_local_port(self):
        """
        Testing local port parameter.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set correct value with proxy group during creation of proxy
        2. Set correct value with proxy group during updating of proxy
        3. Set default value with proxy group during creation of proxy
        4. Set default value with proxy group during updating of proxy
        5. Set empty value with proxy group during creation of proxy
        6. Set empty value with proxy group during updating of proxy
        7. Set correct value with already configured proxy group
        8. Set default value with already configured proxy group
        9. Set empty value with already configured proxy group
        10. Clean proxy group with empty value
        11. Clean proxy group with default value
        """

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'name': proxy_group_names, 'proxy_groupid': '4'}]

        test_cases = [
            {
                'number': 1,
                'input': {'local_port': '10052', 'proxy_group': 'test_proxy_group',
                          'local_address': '192.168.0.10'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_port': '10052', 'local_address': '192.168.0.10'}},
            {
                'number': 2,
                'input': {'local_port': '10052', 'proxy_group': 'test_proxy_group',
                          'local_address': '192.168.0.10'},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_port': '10052', 'local_address': '192.168.0.10'}},
            {
                'number': 3,
                'input': {'local_port': default_values['proxy_port'], 'proxy_group': 'test_proxy_group',
                          'local_address': '192.168.0.10'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_port': default_values['proxy_port'], 'local_address': '192.168.0.10'}},
            {
                'number': 4,
                'input': {'local_port': default_values['proxy_port'], 'proxy_group': 'test_proxy_group',
                          'local_address': '192.168.0.10'},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_port': default_values['proxy_port'], 'local_address': '192.168.0.10'}},
            {
                'number': 5,
                'input': {'local_port': '', 'proxy_group': 'test_proxy_group',
                          'local_address': '192.168.0.10'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_port': default_values['proxy_port'], 'local_address': '192.168.0.10'}},
            {
                'number': 6,
                'input': {'local_port': '', 'proxy_group': 'test_proxy_group',
                          'local_address': '192.168.0.10'},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '4',
                             'local_port': default_values['proxy_port'], 'local_address': '192.168.0.10'}},
            {
                'number': 7,
                'input': {'local_port': '10052'},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'local_port': '10052'}},
            {
                'number': 8,
                'input': {'local_port': default_values['proxy_port']},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'local_port': default_values['proxy_port']}},
            {
                'number': 9,
                'input': {'local_port': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'local_port': default_values['proxy_port']}},
            {
                'number': 10,
                'input': {'local_port': '', 'proxy_group': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '0',
                             'local_port': default_values['proxy_port']}},
            {
                'number': 10,
                'input': {'local_port': default_values['proxy_port'], 'proxy_group': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'proxy_groupid': '0',
                             'local_port': default_values['proxy_port']}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_local_port_error(self):
        """
        Testing local port parameter for Zabbix version 7.0 +

        Expected result: raised error.

        Test cases:
        1. Set empty value during creation of proxy
        2. Set empty value during updating of proxy without proxy group
        3. Set correct value with empty proxy group during creation of proxy
        4. Set correct value with empty proxy group during updating of proxy
        5. Set correct value with empty proxy group during cleaning proxy group
        """
        test_cases = [
            {
                'number': 1,
                'input': {'local_port': '10052'},
                'exist_proxy': None,
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 2,
                'input': {'local_port': '10052'},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 3,
                'input': {'local_port': '10052', 'proxy_group': ''},
                'exist_proxy': None,
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 4,
                'input': {'local_port': '10052', 'proxy_group': ''},
                'exist_proxy': {'proxy_groupid': '0', 'operating_mode': '0'},
                'expected': 'Can be used only with proxy group.'},
            {
                'number': 5,
                'input': {'local_port': '10052', 'proxy_group': ''},
                'exist_proxy': {'proxy_groupid': '4', 'operating_mode': '0'},
                'expected': 'Can be used only with proxy group.'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])

    def test_param_local_port_60(self):
        """
        Testing proxy group parameter for Zabbix version 6.0.

        Expected result: raised error.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'state': 'present',
                'name': 'test_proxy',
                'local_port': '10052'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Incorrect arguments for Zabbix version',
                ansible_result.exception.args[0]['msg'])


class TestInterface(TestModules):
    """Class for testing interface parameter"""
    module = zabbix_proxy

    def test_param_interface_70_independency_of_exist_proxy(self):
        """
        Testing interface parameter.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set ip address and port for new proxy
        2. Set ip address and port for updating existing proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {
                    'interface': {
                        'address': '192.168.0.10',
                        'port': '10052'},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': '192.168.0.10', 'port': '10052'}},
            {
                'number': 2,
                'input': {
                    'interface': {
                        'address': '192.168.0.10',
                        'port': '10052'}},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '1',
                                'address': '192.168.0.20', 'port': '10054'},
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': '192.168.0.10', 'port': '10052'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_70_passive_proxy_mode(self):
        """
        Testing interface parameter with passive proxy mode.

        Expected result: all parameters will be added in correct form.

        Test cases for passive proxy mode:
        1. Set only ip address in address field
        2. Set only dns name in address field
        3. Set only port
        4. Set ip address and port
        5. Set dns name and port
        6. Set empty value of address field
        7. Set empty value of port field
        8. Set empty value of both address and port field
        9. Set default value of address field
        10. Set default value of port field
        11. Set default value of both address and port field

        useip - must be ignored in any cases for Zabbix version 7.0 +
        12. Set ip address and set the value of useip to True
        13. Set dns name and set the value of useip to True
        14. Set ip address and set the value of useip to False
        15. Set dns name and set the value of useip to False
        """
        test_cases = [
            {
                'number': 1,
                'input': {
                    'interface': {
                        'address': '192.168.0.10'},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': '192.168.0.10'}},
            {
                'number': 2,
                'input': {
                    'interface': {
                        'address': 'integration-test.com'},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': 'integration-test.com'}},
            {
                'number': 3,
                'input': {
                    'interface': {
                        'port': '10052'},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'port': '10052'}},
            {
                'number': 4,
                'input': {
                    'interface': {
                        'address': '192.168.0.10',
                        'port': '10052'},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': '192.168.0.10', 'port': '10052'}},
            {
                'number': 5,
                'input': {
                    'interface': {
                        'address': 'integration-test.com',
                        'port': '10052'},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': 'integration-test.com', 'port': '10052'}},
            {
                'number': 6,
                'input': {
                    'interface': {
                        'address': ''},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': default_values['proxy_address']}},
            {
                'number': 7,
                'input': {
                    'interface': {
                        'port': ''},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'port': default_values['proxy_port']}},
            {
                'number': 8,
                'input': {
                    'interface': {
                        'address': '',
                        'port': ''},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': default_values['proxy_address'], 'port': default_values['proxy_port']}},
            {
                'number': 9,
                'input': {
                    'interface': {
                        'address': default_values['proxy_address']},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': default_values['proxy_address']}},
            {
                'number': 10,
                'input': {
                    'interface': {
                        'port': default_values['proxy_port']},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'port': default_values['proxy_port']}},
            {
                'number': 11,
                'input': {
                    'interface': {
                        'address': default_values['proxy_address'],
                        'port': default_values['proxy_port']},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': default_values['proxy_address'], 'port': default_values['proxy_port']}},
            {
                'number': 12,
                'input': {
                    'interface': {
                        'address': '192.168.0.10',
                        'useip': True},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': '192.168.0.10'}},
            {
                'number': 13,
                'input': {
                    'interface': {
                        'address': 'integration-test.com',
                        'useip': True},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': 'integration-test.com'}},
            {
                'number': 14,
                'input': {
                    'interface': {
                        'address': '192.168.0.10',
                        'useip': False},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': '192.168.0.10'}},
            {
                'number': 15,
                'input': {
                    'interface': {
                        'address': 'integration-test.com',
                        'useip': False},
                    'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1',
                             'address': 'integration-test.com'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_70_active_proxy_mode(self):
        """
        Testing interface parameter with active proxy mode.

        Expected result: all parameters will be added in correct form.

        Test cases for active proxy mode:
        1. Set empty address field
        2. Set empty port field
        3. Set empty both address and port field
        1. Set default address field
        2. Set default port field
        3. Set default both address and port field
        """
        test_cases = [
            {
                'number': 1,
                'input': {
                    'interface': {'address': ''},
                    'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'address': default_values['proxy_address']}},
            {
                'number': 2,
                'input': {
                    'interface': {'port': ''},
                    'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'port': default_values['proxy_port']}},
            {
                'number': 3,
                'input': {
                    'interface': {'address': '', 'port': ''},
                    'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'address': default_values['proxy_address'], 'port': default_values['proxy_port']}},
            {
                'number': 4,
                'input': {
                    'interface': {'address': default_values['proxy_address']},
                    'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'address': default_values['proxy_address']}},
            {
                'number': 5,
                'input': {
                    'interface': {'port': default_values['proxy_port']},
                    'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'port': default_values['proxy_port']}},
            {
                'number': 6,
                'input': {
                    'interface': {
                        'address': default_values['proxy_address'],
                        'port': default_values['proxy_port']},
                    'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0',
                             'address': default_values['proxy_address'], 'port': default_values['proxy_port']}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_error(self):
        """
        Testing interface parameter for Zabbix version 7.0 +

        Expected result: raised error.

        Test cases:
        1. Set correct address with active proxy mode
        2. Set correct port with active proxy mode
        3. Set correct address and port with active proxy mode
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'address': '192.168.0.10'}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode.'},
            {
                'number': 2,
                'input': {'interface': {'port': '10052'}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode.'},
            {
                'number': 2,
                'input': {'interface': {'address': '192.168.0.10', 'port': '10052'}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode.'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])

    def test_param_interface_60_useip(self):
        """
        Testing interface useip parameter. For 6.0 interface parameters DEPENDS ON
        existing proxy.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set useip=True for new proxy
        2. Set useip=False for new proxy
        3. Set useip=True for updating existing proxy (no need to update)
        4. Set useip=False for updating existing proxy (no need to update)
        5. Use value from the existing proxy (True)
        6. Use value from the existing proxy (False)
        7. Use default value (set only one different paramater, e.g. address)
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'useip': True}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '127.0.0.1', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 2,
                'input': {'interface': {'useip': False}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'localhost', 'port': '10051', 'useip': '0'}}},
            {
                'number': 3,
                'input': {'interface': {'useip': True}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '127.0.0.1', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '127.0.0.1', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 4,
                'input': {'interface': {'useip': False}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'localhost', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'localhost', 'port': '10051', 'useip': '0'}}},
            {
                'number': 5,
                'input': {'interface': {}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '127.0.0.1', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '127.0.0.1', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 6,
                'input': {'interface': {}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'localhost', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'localhost', 'port': '10051', 'useip': '0'}}},
            {
                'number': 7,
                'input': {'interface': {'port': '10052'}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '127.0.0.1', 'dns': '', 'port': '10052', 'useip': '1'}}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_60_address(self):
        """
        Testing interface address parameter. For 6.0 interface parameters DEPENDS ON
        existing proxy.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set ip address for the value of address field for new proxy
        2. Set ip address for the value of address field for updating existing proxy
        3. Set ip address for the value of address field and set useip=True for new proxy
        4. Set ip address for the value of address field and set useip=True for updating existing proxy
        5. Set dns for the value of address field and set useip=False for new proxy
        6. Set dns for the value of address field and set useip=False for updating existing proxy
        7. Change from the ip to dns for updating exising proxy
        8. Change from the dns to ip for updating exising proxy
        9. Use the correct value (ip) from existing proxy
        10. Use the correct value (dns) from existing proxy
        11. Try to use the correct value (ip) from existing proxy (empty interface) (use default)
        12. Use the correct value (ip) from existing proxy + set useip=True
        13. Use the correct value (dns) from existing proxy + set useip=False
        14. Use the correct value (ip) from existing proxy (exist only dns) + set useip=True
        15. Use the correct value (dns) from existing proxy (exist only ip) + set useip=False
        16. Try to use the correct value (ip) from existing proxy (empty interface) (use default) + set useip=True
        17. Try to use the correct value (dns) from existing proxy (empty interface) (use default) + set useip=True
        18. Set empty address for new proxy
        19. Set empty address for existing proxy (exist ip)
        20. Set empty address for existing proxy (exist dns)
        21. Set empty address and useip=True for new proxy
        22. Set empty address and useip=False for new proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'address': '192.168.0.10'}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 2,
                'input': {'interface': {'address': '192.168.0.11'}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.11', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 3,
                'input': {'interface': {'address': '192.168.0.11', 'useip': True}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.11', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 4,
                'input': {'interface': {'address': '192.168.0.11', 'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.11', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 5,
                'input': {'interface': {'address': 'test.com', 'useip': False}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}}},
            {
                'number': 6,
                'input': {'interface': {'address': 'test1.com', 'useip': False}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'test1.com', 'port': '10051', 'useip': '0'}}},
            {
                'number': 7,
                'input': {'interface': {'address': '192.168.0.10', 'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 8,
                'input': {'interface': {'address': 'test.com', 'useip': False}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}}},
            {
                'number': 9,
                'input': {'interface': {}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 10,
                'input': {'interface': {}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}}},
            {
                'number': 11,
                'input': {'interface': {}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': default_values['proxy_port'], 'useip': '1'}}},
            {
                'number': 12,
                'input': {'interface': {'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}}},
            {
                'number': 13,
                'input': {'interface': {'useip': False}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}}},
            {
                'number': 14,
                'input': {'interface': {'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': '10051',
                                           'useip': '1'}}},
            {
                'number': 15,
                'input': {'interface': {'useip': False}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': default_values['proxy_dns'], 'port': '10051',
                                           'useip': '0'}}},
            {
                'number': 16,
                'input': {'interface': {'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': '10051',
                                           'useip': '1'}}},
            {
                'number': 17,
                'input': {'interface': {'useip': False}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': default_values['proxy_dns'], 'port': '10051',
                                           'useip': '0'}}},
            {
                'number': 18,
                'input': {'interface': {'address': ''}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': '10051',
                                           'useip': '1'}}},
            {
                'number': 19,
                'input': {'interface': {'address': ''}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10051', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': '10051',
                                           'useip': '1'}}},
            {
                'number': 20,
                'input': {'interface': {'address': ''}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10051', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': default_values['proxy_dns'], 'port': '10051',
                                           'useip': '0'}}},
            {
                'number': 21,
                'input': {'interface': {'address': '', 'useip': True}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': '10051',
                                           'useip': '1'}}},
            {
                'number': 22,
                'input': {'interface': {'address': '', 'useip': False}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '', 'dns': default_values['proxy_dns'], 'port': '10051',
                                           'useip': '0'}}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_60_port(self):
        """
        Testing interface port parameter. For 6.0 interface parameters DEPENDS ON
        existing proxy.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set port for new proxy
        2. Set port for updating exist proxy (no need to update)
        3. Set port for updating exist proxy (need to update)
        4. Set empty for new proxy
        5. Set empty for updating exist proxy
        6. Use the value from existing proxy
        7. Use the value from existing proxy (empty interface)
        8. Use default value (Set any other parameter) for new proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'port': '10052'}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '', 'port': '10052',
                                           'useip': '1'}}},
            {
                'number': 2,
                'input': {'interface': {'port': '10052'}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10052', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10052',
                                           'useip': '1'}}},
            {
                'number': 3,
                'input': {'interface': {'port': '10053'}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10052', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10053',
                                           'useip': '1'}}},
            {
                'number': 4,
                'input': {'interface': {'port': ''}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                           'port': default_values['proxy_port'], 'useip': '1'}}},
            {
                'number': 5,
                'input': {'interface': {'port': ''}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10052', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '',
                                           'port': default_values['proxy_port'], 'useip': '1'}}},
            {
                'number': 6,
                'input': {'interface': {'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10053', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': '192.168.0.10', 'dns': '',
                                           'port': '10053', 'useip': '1'}}},
            {
                'number': 6,
                'input': {'interface': {'useip': True}},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                           'port': default_values['proxy_port'], 'useip': '1'}}},
            {
                'number': 7,
                'input': {'interface': {'useip': True}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6',
                             'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                           'port': default_values['proxy_port'], 'useip': '1'}}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_60_active_mode(self):
        """
        Testing interface parameters in case of active mode. For 6.0 interface parameters DEPENDS ON
        existing proxy.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set empty for new proxy
        2. Set empty for updating exist proxy from active mode
        3. Set empty for updating exist proxy from passive mode
        4. Set empty for new proxy + useip=True
        5. Set empty for updating exist proxy from active mode + useip=True
        6. Set empty for updating exist proxy from passive mode + useip=True
        7. Set empty for new proxy + useip=False
        8. Set empty for updating exist proxy from active mode + useip=False
        9. Set empty for updating exist proxy from passive mode + useip=False
        10. Set default for new proxy
        11. Set default for updating exist proxy from active mode
        12. Set default for updating exist proxy from passive mode
        13. Set default for new proxy + useip=True
        14. Set default for updating exist proxy from active mode + useip=True
        15. Set default for updating exist proxy from passive mode + useip=True
        16. Set default for new proxy + useip=False
        17. Set default for updating exist proxy from active mode + useip=False
        18. Set default for updating exist proxy from passive mode + useip=False
        19. Set empty interface ({}) for new proxy
        20. Set empty interface ({}) for updating existing proxy with existing interface
        21. Set empty interface ({}) for updating existing proxy with empty interface
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'port': '', 'address': ''}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 2,
                'input': {'interface': {'port': '', 'address': ''}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 2,
                'input': {'interface': {'port': '', 'address': ''}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10053', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 4,
                'input': {'interface': {'port': '', 'address': '', 'useip': True}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 5,
                'input': {'interface': {'port': '', 'address': '', 'useip': True}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 6,
                'input': {'interface': {'port': '', 'address': '', 'useip': True}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10053', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 7,
                'input': {'interface': {'port': '', 'address': '', 'useip': False}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 8,
                'input': {'interface': {'port': '', 'address': '', 'useip': False}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 9,
                'input': {'interface': {'port': '', 'address': '', 'useip': False}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '192.168.0.10', 'dns': '', 'port': '10053', 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 10,
                'input': {'interface': {'port': default_values['proxy_port'],
                                        'address': default_values['proxy_address']}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 11,
                'input': {'interface': {'port': default_values['proxy_port'],
                                        'address': default_values['proxy_address']}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5',
                                'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                              'port': default_values['proxy_port'], 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 12,
                'input': {'interface': {'port': default_values['proxy_port'],
                                        'address': default_values['proxy_address']}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                              'port': default_values['proxy_port'], 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 13,
                'input': {'interface': {'port': default_values['proxy_port'], 'address': default_values['proxy_address'],
                                        'useip': True}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 14,
                'input': {'interface': {'port': default_values['proxy_port'], 'address': default_values['proxy_address'],
                                        'useip': True}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5',
                                'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                              'port': default_values['proxy_port'], 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 15,
                'input': {'interface': {'port': default_values['proxy_port'], 'address': default_values['proxy_address'],
                                        'useip': True}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': default_values['proxy_address'], 'dns': '',
                                              'port': default_values['proxy_port'], 'useip': '1'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 16,
                'input': {'interface': {'port': default_values['proxy_port'], 'address': default_values['proxy_dns'],
                                        'useip': False}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 17,
                'input': {'interface': {'port': default_values['proxy_port'], 'address': default_values['proxy_dns'],
                                        'useip': False}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5',
                                'interface': {'ip': '', 'dns': default_values['proxy_dns'],
                                              'port': default_values['proxy_port'], 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 18,
                'input': {'interface': {'port': default_values['proxy_port'], 'address': default_values['proxy_dns'],
                                        'useip': False}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': default_values['proxy_dns'],
                                              'port': default_values['proxy_port'], 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 19,
                'input': {'interface': {}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 20,
                'input': {'interface': {}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': default_values['proxy_dns'],
                                              'port': default_values['proxy_port'], 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}},
            {
                'number': 21,
                'input': {'interface': {}, 'mode': 'active'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '5', 'interface': []}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_60_empty_interface(self):
        """
        Testing interface parameters in case of passive mode and empty interface.
        For 6.0 interface parameters DEPENDS ON existing proxy.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Set empty interface ({}) for new proxy
        2. Set empty interface ({}) for updating existing proxy with existing interface
        3. Set empty interface ({}) for updating existing proxy with empty interface
        4. Set empty interface ({}) for updating existing proxy with existing interface (no need to update)
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {}, 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6', 'interface': {
                    'ip': default_values['proxy_address'], 'dns': '', 'port': default_values['proxy_port'],
                    'useip': '1'}}},
            {
                'number': 2,
                'input': {'interface': {}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': default_values['proxy_dns'],
                                              'port': default_values['proxy_port'], 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6', 'interface': {
                    'ip': '', 'dns': default_values['proxy_dns'], 'port': default_values['proxy_port'],
                    'useip': '0'}}},
            {
                'number': 3,
                'input': {'interface': {}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6', 'interface': {
                    'ip': default_values['proxy_address'], 'dns': '', 'port': default_values['proxy_port'],
                    'useip': '1'}}},
            {
                'number': 4,
                'input': {'interface': {}, 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10052', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6', 'interface': {
                    'ip': '', 'dns': 'test.com', 'port': '10052', 'useip': '0'}}
            },
            {
                'number': 5,
                'input': {'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6',
                                'interface': {'ip': '', 'dns': 'test.com', 'port': '10052', 'useip': '0'}},
                'expected': {'host': 'test_proxy', 'status': '6', 'interface': {
                    'ip': '', 'dns': 'test.com', 'port': '10052', 'useip': '0'}}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_interface_60_error(self):
        """
        Testing interface parameter for Zabbix version 6.0

        Expected result: raised error.

        Test cases:
        1. Set correct address with active proxy mode
        2. Set correct port with active proxy mode
        3. Set correct address and port with active proxy mode
        """
        test_cases = [
            {
                'number': 1,
                'input': {'interface': {'address': '192.168.0.10'}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode.'},
            {
                'number': 2,
                'input': {'interface': {'port': '10052'}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode.'},
            {
                'number': 2,
                'input': {'interface': {'address': '192.168.0.10', 'port': '10052'}, 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode.'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])


class TestAllowedAddresses(TestModules):
    """Class for testing allowed_addresses parameter"""
    module = zabbix_proxy

    def test_param_allowed_addresses_70(self):
        """
        Testing allowed_addresses parameter. Test for Zabbix version 7.0 +

        Expected result: all parameters will be added in correct form.

        Test cases
        1. Set value for new proxy
        2. Set value for updating existing proxy (no need update)
        3. Set value for updating existing proxy (need update)
        4. Set empty value for new proxy
        5. Set empty value for updating existing proxy (no need update)
        6. Set empty value for updating existing proxy (need update)
        7. Set empty value for new proxy with passive mode
        8. Set empty value for updating existing proxy with passive mode
        """
        test_cases = [
            {
                'number': 1,
                'input': {'allowed_addresses': '192.168.0.10'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.10'}},
            {
                'number': 2,
                'input': {'allowed_addresses': '192.168.0.10'},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.10'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.10'}},
            {
                'number': 3,
                'input': {'allowed_addresses': '192.168.0.10'},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.10'}},
            {
                'number': 4,
                'input': {'allowed_addresses': ''},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': ''}},
            {
                'number': 5,
                'input': {'allowed_addresses': ''},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': ''},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': ''}},
            {
                'number': 6,
                'input': {'allowed_addresses': ''},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': ''}},
            {
                'number': 7,
                'input': {'allowed_addresses': '', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'allowed_addresses': ''}},
            {
                'number': 8,
                'input': {'allowed_addresses': '', 'mode': 'passive'},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '1', 'allowed_addresses': '192.168.0.1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'allowed_addresses': ''}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_allowed_addresses_60(self):
        """
        Testing allowed_addresses parameter. Test for Zabbix version 6.0

        Expected result: all parameters will be added in correct form.

        Test cases
        1. Set value for new proxy
        2. Set value for updating existing proxy (no need update)
        3. Set value for updating existing proxy (need update)
        4. Set empty value for new proxy
        5. Set empty value for updating existing proxy (no need update)
        6. Set empty value for updating existing proxy (need update)
        7. Set empty value for new proxy with passive mode
        8. Set empty value for updating existing proxy with passive mode
        """
        test_cases = [
            {
                'number': 1,
                'input': {'allowed_addresses': '192.168.0.10'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.10'}},
            {
                'number': 2,
                'input': {'allowed_addresses': '192.168.0.10'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.10'},
                'expected': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.10'}},
            {
                'number': 3,
                'input': {'allowed_addresses': '192.168.0.10'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.1'},
                'expected': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.10'}},
            {
                'number': 4,
                'input': {'allowed_addresses': ''},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '5', 'proxy_address': ''}},
            {
                'number': 5,
                'input': {'allowed_addresses': ''},
                'exist_proxy': {'host': 'test_proxy', 'status': '5', 'proxy_address': ''},
                'expected': {'host': 'test_proxy', 'status': '5', 'proxy_address': ''}},
            {
                'number': 6,
                'input': {'allowed_addresses': ''},
                'exist_proxy': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.1'},
                'expected': {'host': 'test_proxy', 'status': '5', 'proxy_address': ''}},
            {
                'number': 7,
                'input': {'allowed_addresses': '', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'host': 'test_proxy', 'status': '6', 'proxy_address': '',
                             'interface': {
                                 'dns': 'localhost',
                                 'ip': '127.0.0.1',
                                 'port': '10051',
                                 'useip': '1'
                             }}},
            {
                'number': 8,
                'input': {'allowed_addresses': '', 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '6', 'proxy_address': '192.168.0.1',
                                'interface': []},
                'expected': {'host': 'test_proxy', 'status': '6', 'proxy_address': '',
                             'interface': {
                                 'dns': 'localhost',
                                 'ip': '127.0.0.1',
                                 'port': '10051',
                                 'useip': '1'
                             }}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_allowed_addresses_error_70(self):
        """
        Testing allowed_addresses parameter for Zabbix version 7.0 + in case of error

        Expected result: raised error.

        Test cases:
        1. Set value with passive mode for new proxy
        2. Set value with passive mode for updating existing proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'allowed_addresses': '192.168.0.10', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 2,
                'input': {'allowed_addresses': '192.168.0.10', 'mode': 'passive'},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'allowed_addresses': '192.168.0.10'},
                'expected': 'Available only in active proxy mode'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])

    def test_param_allowed_addresses_error_60(self):
        """
        Testing allowed_addresses parameter for Zabbix version 7.0 + in case of error

        Expected result: raised error.

        Test cases:
        1. Set value with passive mode for new proxy
        2. Set value with passive mode for updating existing proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'allowed_addresses': '192.168.0.10', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 2,
                'input': {'allowed_addresses': '192.168.0.10', 'mode': 'passive'},
                'exist_proxy': {'host': 'test_proxy', 'status': '5', 'proxy_address': '192.168.0.10',
                                'interface': []},
                'expected': 'Available only in active proxy mode'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])


class TestEncryption(TestModules):
    """Class for testing encryption parameters"""
    module = zabbix_proxy

    def test_param_tls_accept(self):
        """
        Testing tls_accept parameter. Test for both Zabbix version.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Unencrypted for new proxy
        2. PSK for new proxy
        3. Unencrypted + PSK for new proxy
        4. Cert for new proxy
        5. Unencrypted + Cert for new proxy
        6. PSK + Cert for new proxy
        7. Unencrypted + PSK + Cert for new proxy

        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_accept': ['unencrypted']},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '1'}},
            {
                'number': 2,
                'input': {'tls_accept': ['psk'], 'tls_psk_identity': '123', 'tls_psk': '123'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '2',
                             'tls_psk_identity': '123', 'tls_psk': '123'}},
            {
                'number': 3,
                'input': {'tls_accept': ['unencrypted', 'psk'], 'tls_psk_identity': '123', 'tls_psk': '123'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '3',
                             'tls_psk_identity': '123', 'tls_psk': '123'}},
            {
                'number': 4,
                'input': {'tls_accept': ['cert']},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '4'}},
            {
                'number': 5,
                'input': {'tls_accept': ['unencrypted', 'cert']},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '5'}},
            {
                'number': 6,
                'input': {'tls_accept': ['psk', 'cert'], 'tls_psk_identity': '123', 'tls_psk': '123'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '6',
                             'tls_psk_identity': '123', 'tls_psk': '123'}},
            {
                'number': 7,
                'input': {'tls_accept': ['unencrypted', 'psk', 'cert'], 'tls_psk_identity': '123', 'tls_psk': '123'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '7',
                             'tls_psk_identity': '123', 'tls_psk': '123'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_tls_accept_with_passive_mode(self):
        """
        Testing tls_accept parameter with passive proxy mode. Test for both Zabbix version.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Empty with passive mode
        2. Unecrypted with passive mode
        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_accept': ['unencrypted'], 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'tls_accept': '1'}},
            {
                'number': 2,
                'input': {'tls_accept': [], 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'tls_accept': '1'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_tls_accept_error(self):
        """
        Testing tls_accept parameter for both Zabbix version in case of error

        Expected result: raised error.

        Test cases:
        1. PSK without tls_psk_identity
        2. PSK without tls_psk
        3. PSK without tls_psk_identity and tls_psk
        Passive proxy mode:
        4. PSK for new proxy
        5. Unencrypted + PSK for new proxy
        6. Cert for new proxy
        7. Unencrypted + Cert for new proxy
        8. PSK + Cert for new proxy
        9. Unencrypted + PSK + Cert for new proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_accept': ['psk'], 'tls_psk': '123'},
                'exist_proxy': None,
                'expected': 'Missing TLS PSK params'},
            {
                'number': 2,
                'input': {'tls_accept': ['psk'], 'tls_psk_identity': '123'},
                'exist_proxy': None,
                'expected': 'Missing TLS PSK params'},
            {
                'number': 3,
                'input': {'tls_accept': ['psk']},
                'exist_proxy': None,
                'expected': 'Missing TLS PSK params'},
            {
                'number': 4,
                'input': {'tls_accept': ['psk'], 'tls_psk_identity': '123', 'tls_psk': '123', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 5,
                'input': {'tls_accept': ['unencrypted', 'psk'], 'tls_psk_identity': '123', 'tls_psk': '123',
                          'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 6,
                'input': {'tls_accept': ['cert'], 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 7,
                'input': {'tls_accept': ['unencrypted', 'cert'], 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 8,
                'input': {'tls_accept': ['psk', 'cert'], 'tls_psk_identity': '123', 'tls_psk': '123',
                          'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'},
            {
                'number': 9,
                'input': {'tls_accept': ['unencrypted', 'psk', 'cert'], 'tls_psk_identity': '123', 'tls_psk': '123',
                          'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Available only in active proxy mode'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])

    def test_param_tls_connect(self):
        """
        Testing tls_connect parameter. Test for both Zabbix version.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Unencrypted for new proxy
        2. PSK for new proxy
        3. Cert for new proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_connect': 'unencrypted', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'tls_connect': '1'}},
            {
                'number': 2,
                'input': {'tls_connect': 'psk', 'tls_psk_identity': '123', 'tls_psk': '123', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'tls_connect': '2',
                             'tls_psk_identity': '123', 'tls_psk': '123'}},
            {
                'number': 3,
                'input': {'tls_connect': 'cert', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'tls_connect': '4'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_tls_connect_with_active_mode(self):
        """
        Testing tls_connect parameter with passive proxy mode. Test for both Zabbix version.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Empty with passive mode
        2. Unecrypted with passive mode
        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_connect': 'unencrypted', 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_connect': '1'}},
            {
                'number': 2,
                'input': {'tls_connect': '', 'mode': 'active'},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_connect': '1'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_tls_connect_error(self):
        """
        Testing tls_connect parameter for both Zabbix version in case of error

        Expected result: raised error.

        Test cases:
        1. PSK without tls_psk_identity
        2. PSK without tls_psk
        3. PSK without tls_psk_identity and tls_psk
        Active proxy mode:
        4. PSK for new proxy
        5. Cert for new proxy
        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_connect': 'psk', 'tls_psk': '123', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Missing TLS PSK params'},
            {
                'number': 2,
                'input': {'tls_connect': 'psk', 'tls_psk_identity': '123', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Missing TLS PSK params'},
            {
                'number': 3,
                'input': {'tls_connect': 'psk', 'mode': 'passive'},
                'exist_proxy': None,
                'expected': 'Missing TLS PSK params'},
            {
                'number': 4,
                'input': {'tls_connect': 'psk', 'tls_psk_identity': '123', 'tls_psk': '123', 'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode'},
            {
                'number': 5,
                'input': {'tls_connect': 'cert', 'tls_psk_identity': '123', 'tls_psk': '123',
                          'mode': 'active'},
                'exist_proxy': None,
                'expected': 'Available only in passive proxy mode'}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}

                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    case['expected'],
                    ansible_result.exception.args[0]['msg'])

    def test_param_psk_updating(self):
        """
        Testing parameter in case of updating psk. Test for both Zabbix version.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. tls_accept: Exist psk, update psk + unencrypted (active mode)
        2. tls_accept: Exist psk, update psk + cert  (active mode)
        3. tls_accept: Exist psk, tls_connect: psk (passive mode)
        4. tls_connect: Exist psk, tls_accept: psk (active mode)
        """
        test_cases = [
            {
                'number': 1,
                'input': {'tls_accept': ['unencrypted', 'psk']},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '2'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '3'}},
            {
                'number': 2,
                'input': {'tls_accept': ['psk', 'cert']},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '2'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '6'}},
            {
                'number': 3,
                'input': {'tls_connect': 'psk', 'mode': 'passive'},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '2'},
                'expected': {'name': 'test_proxy', 'operating_mode': '1', 'tls_connect': '2'}},
            {
                'number': 4,
                'input': {'tls_accept': ['psk'], 'mode': 'active'},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '1', 'tls_connect': '2', 'tls_accept': '1'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'tls_accept': '2'}}
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))


class TestCustomTimeouts(TestModules):
    """Class for testing custom_timeouts parameters"""
    module = zabbix_proxy

    def test_param_custom_timeouts(self):
        """
        Testing custom_timeouts parameter. Test for Zabbix version 7.0 +.

        Expected result: all parameters will be added in correct form.

        Test cases:
        1. Unencrypted for new proxy
        2. PSK for new proxy
        3. Unencrypted + PSK for new proxy
        4. Cert for new proxy
        5. Unencrypted + Cert for new proxy
        6. PSK + Cert for new proxy
        7. Unencrypted + PSK + Cert for new proxy
        """

        def get_global_setting(self):
            return {
                'timeout_zabbix_agent': '3s',
                'timeout_simple_check': '3s',
                'timeout_snmp_agent': '3s',
                'timeout_external_check': '3s',
                'timeout_db_monitor': '3s',
                'timeout_http_agent': '3s',
                'timeout_ssh_agent': '3s',
                'timeout_telnet_agent': '3s',
                'timeout_script': '3s',
                'timeout_browser': '3s'
            }

        test_cases = [
            {
                'number': 1,
                'input': {'custom_timeouts': {'timeout_zabbix_agent': '10s'}},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                             'timeout_zabbix_agent': '10s', 'timeout_simple_check': '3s',
                             'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                             'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                             'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                             'timeout_script': '3s', 'timeout_browser': '3s'}},
            {
                'number': 2,
                'input': {'custom_timeouts': {'timeout_zabbix_agent': '10s', 'timeout_simple_check': '10s'}},
                'exist_proxy': None,
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                             'timeout_zabbix_agent': '10s', 'timeout_simple_check': '10s',
                             'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                             'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                             'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                             'timeout_script': '3s', 'timeout_browser': '3s'}},
            {
                'number': 3,
                'input': {'custom_timeouts': {'timeout_simple_check': '10s'}},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                                'timeout_zabbix_agent': '10s', 'timeout_simple_check': '3s',
                                'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                                'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                                'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                                'timeout_script': '3s', 'timeout_browser': '3s'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                             'timeout_zabbix_agent': '10s', 'timeout_simple_check': '10s',
                             'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                             'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                             'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                             'timeout_script': '3s', 'timeout_browser': '3s'}},
            {
                'number': 4,
                'input': {'custom_timeouts': {}},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                                'timeout_zabbix_agent': '10s', 'timeout_simple_check': '3s',
                                'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                                'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                                'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                                'timeout_script': '3s', 'timeout_browser': '3s'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '0'}},
            {
                'number': 5,
                'input': {'custom_timeouts': {'timeout_zabbix_agent': ''}},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                                'timeout_zabbix_agent': '10s', 'timeout_simple_check': '10s',
                                'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                                'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                                'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                                'timeout_script': '3s', 'timeout_browser': '3s'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                             'timeout_zabbix_agent': '3s', 'timeout_simple_check': '10s',
                             'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                             'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                             'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                             'timeout_script': '3s', 'timeout_browser': '3s'}},
            {
                'number': 6,
                'input': {'custom_timeouts': {'timeout_zabbix_agent': '', 'timeout_simple_check': '10s'}},
                'exist_proxy': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                                'timeout_zabbix_agent': '10s', 'timeout_simple_check': '3s',
                                'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                                'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                                'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                                'timeout_script': '3s', 'timeout_browser': '3s'},
                'expected': {'name': 'test_proxy', 'operating_mode': '0', 'custom_timeouts': '1',
                             'timeout_zabbix_agent': '3s', 'timeout_simple_check': '10s',
                             'timeout_snmp_agent': '3s', 'timeout_external_check': '3s',
                             'timeout_db_monitor': '3s', 'timeout_http_agent': '3s',
                             'timeout_ssh_agent': '3s', 'timeout_telnet_agent': '3s',
                             'timeout_script': '3s', 'timeout_browser': '3s'}}

        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                get_global_setting=get_global_setting):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy = self.module.Proxy(self.mock_module_functions)

                result = proxy.generate_zabbix_proxy(exist_proxy=case['exist_proxy'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))

    def test_param_custom_timeouts_error(self):
        """
        Testing custom_timeouts parameter for Zabbix version 6.0 in case of error

        Expected result: raised error.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'state': 'present',
                'name': 'test_proxy',
                'custom_timeouts': {'timeout_simple_check': '10s'}}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy.generate_zabbix_proxy(exist_proxy=None)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Incorrect arguments for Zabbix version',
                ansible_result.exception.args[0]['msg'])
