#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_host
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)
from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    inventory_mode_types, snmp_authprotocol_types, snmp_privprotocol_types)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of API is returned.
    """
    return '6.0.18'


class TestWOProcessing(TestModules):
    """Class for testing parameters that do not require preprocessing"""
    module = zabbix_host

    def test_param_wo_processing(self):
        """
        Testing parameters that do not require preprocessing.

        Expected result: all parameters will be added in the
        same form as in the input data.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        test_data_1 = {
            'host': 'test_host',
            'description': 'test'}
        test_data_2 = {
            'host': 'test_host',
            'description': 'test',
            'name': 'Test name',
            'tags': [{
                'tag': 'test',
                'value': 'test'}],
            'ipmi_username': 'ipmi_username',
            'ipmi_password': 'ipmi_password',
            'tls_psk': 'tls_psk',
            'tls_psk_identity': 'tls_psk_identity',
            'tls_issuer': 'tls_issuer',
            'tls_subject': 'tls_subject'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            # Check test_data_1
            self.mock_module_functions.params = test_data_1
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, test_data_1)

            # Check test_data_2
            self.mock_module_functions.params = test_data_2
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, test_data_2)


class TestHostgroups(TestModules):
    """Class for testing the operation of the module with host groups"""
    module = zabbix_host

    def test_hostgroups_in_param(self):
        """
        Testing the processing of the host group parameter.
        In this case, input parameters must be processed successfully.

        Expected result: the resulting data equals the expected result.
        """
        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{'groupid': '2', 'name': 'Linux servers'}]

        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                find_zabbix_hostgroups_by_names=mock_find_zabbix_hostgroups_by_names):

            input_param = {
                'host': 'test_host',
                'hostgroups': ['Linux servers']}
            expected_result = {
                'host': 'test_host',
                'groups': [{'groupid': '2'}]}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_empty_hostgroups(self):
        """
        Testing the processing with an empty host group parameter.
        In this case, the host group parameter must not be empty.

        Expected result: an exception with an error message.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'hostgroups': []}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                host.generate_zabbix_host()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                'Cannot remove all host groups from a host',
                ansible_result.exception.args[0]['msg'])

    def test_wo_hostgroups_wo_exist_host(self):
        """
        Testing the processing without the host group parameter
        for creating a new host. In this case, host groups are required.

        Expected result: an exception with an error message.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                host.generate_zabbix_host()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                'Required parameter not found: hostgroups',
                ansible_result.exception.args[0]['msg'])

    def test_wo_hostgroups_w_exist_host(self):
        """
        Testing the processing of a case without the host group parameter, but with
        an existing host. In this case, the host group parameter is not required.

        Expected result: the resulting data equals the expected result, and in the resulting
        data, only the host parameter is present.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            exist_host = {'host': 'exist host', 'inventory_mode': '1'}
            input_param = {'host': 'test_host'}
            expected_result = {'host': 'test_host'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)


class TestTemplates(TestModules):
    """Class for testing the operation of the module with templates"""
    module = zabbix_host

    def test_removing_templates(self):
        """
        Testing the processing of the templates parameter.
        In this case we can clear template from host.

        Expected result: result data equals expected result and the templates
        parameter is empty.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'templates': []}
            expected_result = {
                'host': 'test_host',
                'templates': []}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_processing_templates(self):
        """
        Testing the processing of the templates parameter.
        In this case, input parameters must be processed successfully.

        Expected result: the resulting data equals the expected result.
        """
        def mock_find_zabbix_templates_by_names(self, hostgroup_names):
            return [{'templateid': '2', 'name': 'Basic Linux'}]

        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                find_zabbix_templates_by_names=mock_find_zabbix_templates_by_names):

            input_param = {
                'host': 'test_host',
                'templates': ['Basic Linux']}
            expected_result = {
                'host': 'test_host',
                'templates': [{'templateid': '2'}]}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)


class TestProxy(TestModules):
    """Class for testing the operation of the module with proxy"""
    module = zabbix_host

    def test_removing_proxy(self):
        """
        Testing the processing of the proxy parameter.
        In this case, we can clear the proxy from the host.

        Expected result: the resulting data equals the expected result, and
        the proxy parameter is set to '0'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'proxy': ''}
            expected_result = {
                'host': 'test_host',
                'proxy_hostid': '0'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_processing_proxy(self):
        """
        Testing the processing of the proxy parameter.
        In this case, input parameters must be processed successfully.

        Expected result: the resulting data equals the expected result.
        """
        def mock_find_zabbix_proxy_by_names(self, hostgroup_names):
            return [{'proxyid': '2', 'name': 'Test Proxy'}]

        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                find_zabbix_proxy_by_names=mock_find_zabbix_proxy_by_names):

            input_param = {
                'host': 'test_host',
                'proxy': 'Test Proxy'}
            expected_result = {
                'host': 'test_host',
                'proxy_hostid': '2'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_processing_proxy_error(self):
        """
        Testing the processing of the proxy parameter.
        In this case, the proxy was not found in Zabbix, resulting in an error.

        Expected result: an exception.
        """
        def mock_find_zabbix_proxy_by_names(self, hostgroup_names):
            return []

        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                find_zabbix_proxy_by_names=mock_find_zabbix_proxy_by_names):

            input_param = {
                'host': 'test_host',
                'proxy': 'Test Proxy'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                host.generate_zabbix_host(exist_host)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                'Proxy not found in Zabbix: Test Proxy',
                ansible_result.exception.args[0]['msg'])


class TestStatus(TestModules):
    """Class for testing the operation of the module with status"""
    module = zabbix_host

    def test_status_enable(self):
        """
        Testing the processing of the status parameter. In this case,
        we are testing sending a value to enable the host.

        Expected result: the resulting data equals the expected result.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'status': 'enabled'}
            expected_result = {
                'host': 'test_host',
                'status': '0'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_status_disable(self):
        """
        Testing the processing of the status parameter. In this case,
        we are testing sending a value to disable the host.

        Expected result: the resulting data equals the expected result.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'status': 'disable'}
            expected_result = {
                'host': 'test_host',
                'status': '1'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)


class TestMacro(TestModules):
    """Class for testing the operation of the module with macros"""
    module = zabbix_host

    def test_macros_removing(self):
        """
        Testing the deletion of macros from the host.
        To delete, you need to pass an empty value to the 'macros' field.

        Expected result: the 'macros' field is empty.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'macros': []}
            expected_result = {
                'host': 'test_host',
                'macros': []}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_macros_processing(self):
        """
        Testing the processing of various combinations
        of macros. The test includes checking all fields for macros.

        Expected result: the resulting data equals the expected result.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'macros': [
                    {
                        'macro': 'test1',
                        'value': '',
                        'type': 'text',
                        'description': ''
                    },
                    {
                        'macro': 'test2',
                        'value': 'macro_value_2',
                        'type': 'text',
                        'description': ''
                    },
                    {
                        'macro': 'test3',
                        'value': '',
                        'type': 'secret',
                        'description': ''
                    },
                    {
                        'macro': 'test4',
                        'value': '',
                        'type': 'vault_secret',
                        'description': ''
                    },
                    {
                        'macro': 'test5',
                        'value': '',
                        'type': 'text',
                        'description': 'test description'
                    }
                ]}
            expected_result = {
                'host': 'test_host',
                'macros': [
                    {
                        'macro': '{$TEST1}',
                        'value': '',
                        'type': '0',
                        'description': ''
                    },
                    {
                        'macro': '{$TEST2}',
                        'value': 'macro_value_2',
                        'type': '0',
                        'description': ''
                    },
                    {
                        'macro': '{$TEST3}',
                        'value': '',
                        'type': '1',
                        'description': ''
                    },
                    {
                        'macro': '{$TEST4}',
                        'value': '',
                        'type': '2',
                        'description': ''
                    },
                    {
                        'macro': '{$TEST5}',
                        'value': '',
                        'type': '0',
                        'description': 'test description'
                    }
                ]}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)


class TestIPMI(TestModules):
    """Class for testing the operation of the module with IPMI parameters"""
    module = zabbix_host

    def test_ipmi_authtype(self):
        """
        Testing IPMI authorization type parameter. The test includes
        all possible authorization types.

        Expected result: All possible authorization types can
        be applied and match the expected values after transformations.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        ipmi_authtype_test_cases = {
            'default': '-1',
            'none': '0',
            'md2': '1',
            'md5': '2',
            'straight': '4',
            'oem': '5',
            'rmcp+': '6'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for each in ipmi_authtype_test_cases:
                input_param = {
                    'host': 'test_host',
                    'ipmi_authtype': each}
                expected_result = {
                    'host': 'test_host',
                    'ipmi_authtype': ipmi_authtype_test_cases[each]}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

    def test_ipmi_privilege(self):
        """
        Testing IPMI privilege parameter. The test includes
        all possible privilege types.

        Expected result: All possible privilege types can
        be applied and match the expected values after transformations.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1'}
        ipmi_privilege_test_cases = {
            'callback': '1',
            'user': '2',
            'operator': '3',
            'admin': '4',
            'oem': '5'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for each in ipmi_privilege_test_cases:
                input_param = {
                    'host': 'test_host',
                    'ipmi_privilege': each}
                expected_result = {
                    'host': 'test_host',
                    'ipmi_privilege': ipmi_privilege_test_cases[each]}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)


class TestTLS(TestModules):
    """
    Class for testing the operation of the module with
    encryption parameters.
    """
    module = zabbix_host

    def test_unencrypted_accept(self):
        """
        Testing the non-encrypted mode for acceptance.

        Expected result: the encryption parameter value is set to '1'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1',
                      'tls_accept': '1', 'tls_connect': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host', 'tls_accept': ['unencrypted']}
            expected_result = {'host': 'test_host', 'tls_accept': '1'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_unencrypted_connect(self):
        """
        Testing the non-encrypted mode for connection.

        Expected result: the encryption parameter value is set to '1'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1',
                      'tls_accept': '1', 'tls_connect': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host', 'tls_connect': 'unencrypted'}
            expected_result = {'host': 'test_host', 'tls_connect': '1'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_cert_accept(self):
        """
        Testing encryption mode using a certificate for acceptance.

        Expected result: the encryption parameter value is set to '4'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1',
                      'tls_accept': '1', 'tls_connect': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host', 'tls_accept': ['cert']}
            expected_result = {'host': 'test_host', 'tls_accept': '4'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_cert_connect(self):
        """
        Testing encryption mode using a certificate for connection.

        Expected result: the encryption parameter value is set to '4'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1',
                      'tls_accept': '1', 'tls_connect': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host', 'tls_connect': 'cert'}
            expected_result = {'host': 'test_host', 'tls_connect': '4'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_empty_accept(self):
        """
        Testing the encryption mode reset for acceptance. To reset encryption to
        the default value, you must specify an empty value.

        Expected result: the encryption parameter value is set to '1'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1',
                      'tls_accept': '1', 'tls_connect': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host', 'tls_accept': []}
            expected_result = {'host': 'test_host', 'tls_accept': '1'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_empty_connect(self):
        """
        Testing the encryption mode reset for connection. To reset encryption
        to the default value, you must specify an empty value.

        Expected result: the encryption parameter value is set to '1'.
        """
        exist_host = {'host': 'exist host', 'inventory_mode': '1',
                      'tls_accept': '1', 'tls_connect': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {'host': 'test_host', 'tls_connect': ''}
            expected_result = {'host': 'test_host', 'tls_connect': '1'}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            result = host.generate_zabbix_host(exist_host)
            self.assertEqual(result, expected_result)

    def test_psk_accept(self):
        """
        Testing the PSK encryption mode for acceptance.
        This test checks if the host already has PSK encryption
        configured, then the `tls_psk` and `tls_psk_identity` parameters
        are not required.

        Expected result: all test cases run successfully,
        and additional PSK parameters are not required.
        """
        input_param = {'host': 'test_host', 'tls_accept': ['psk']}
        expected_result = {'host': 'test_host', 'tls_accept': '2'}
        test_cases_accept_exist = ['2', '3', '6', '7']
        test_cases_connect_exist = ['2']
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for each in test_cases_accept_exist:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': each,
                    'tls_connect': '1'}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

            for each in test_cases_connect_exist:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': '1',
                    'tls_connect': each}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

    def test_psk_connect(self):
        """
        Testing the PSK encryption mode for connection.
        This test checks if the host already has PSK encryption
        configured, then the `tls_psk` and `tls_psk_identity` parameters
        are not required.

        Expected result: all test cases run successfully,
        and additional PSK parameters are not required.
        """
        input_param = {'host': 'test_host', 'tls_connect': 'psk'}
        expected_result = {'host': 'test_host', 'tls_connect': '2'}
        test_cases_accept_exist = ['2', '3', '6', '7']
        test_cases_connect_exist = ['2']
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for each in test_cases_accept_exist:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': each,
                    'tls_connect': '1'}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

            for each in test_cases_connect_exist:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': '1',
                    'tls_connect': each}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

    def test_psk_accept_w_id_key(self):
        """
        Testing the PSK encryption mode for acceptance.
        The test includes all possible settings for an existing host and
        verifies the ability to enable the PSK encryption mode with these
        settings.

        Expected result: all test cases run successfully.
        """
        input_param = {
            'host': 'test_host',
            'tls_accept': ['psk'],
            'tls_psk_identity': 'test_tls_psk_identity',
            'tls_psk': 'test_tls_psk'}
        expected_result = {
            'host': 'test_host',
            'tls_accept': '2',
            'tls_psk_identity': 'test_tls_psk_identity',
            'tls_psk': 'test_tls_psk'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for each in range(1, 8):
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': str(each),
                    'tls_connect': '1'}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

            for each in ['1', '2', '4']:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': '1',
                    'tls_connect': each}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

    def test_psk_connect_w_id_key(self):
        """
        Testing the PSK encryption mode for connection.
        The test includes all possible settings for an existing host and
        verifies the ability to enable the PSK encryption mode with these
        settings.

        Expected result: all test cases run successfully.
        """
        input_param = {
            'host': 'test_host',
            'tls_connect': 'psk',
            'tls_psk_identity': 'test_tls_psk_identity',
            'tls_psk': 'test_tls_psk'}
        expected_result = {
            'host': 'test_host',
            'tls_connect': '2',
            'tls_psk_identity': 'test_tls_psk_identity',
            'tls_psk': 'test_tls_psk'}
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for each in range(1, 8):
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': str(each),
                    'tls_connect': '1'}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

            for each in ['1', '2', '4']:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': '1',
                    'tls_connect': each}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

    def test_psk_accept_combinations(self):
        """
        Testing the ability to select multiple modes simultaneously.
        The test includes all possible combinations.

        Expected result: all test cases run successfully.
        """
        test_cases_accept = [
            {'input': ['unencrypted'], 'output': '1'},
            {'input': ['psk'], 'output': '2'},
            {'input': ['unencrypted', 'psk'], 'output': '3'},
            {'input': ['cert'], 'output': '4'},
            {'input': ['unencrypted', 'cert'], 'output': '5'},
            {'input': ['psk', 'cert'], 'output': '6'},
            {'input': ['unencrypted', 'psk', 'cert'], 'output': '7'}]

        exist_cases = [
            {'accept': '2', 'connect': '1'},
            {'accept': '3', 'connect': '1'},
            {'accept': '6', 'connect': '1'},
            {'accept': '7', 'connect': '1'},
            {'accept': '1', 'connect': '2'},
            {'accept': '2', 'connect': '2'},
            {'accept': '3', 'connect': '2'},
            {'accept': '6', 'connect': '2'},
            {'accept': '7', 'connect': '2'}]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            # ID and key are not required
            for case in exist_cases:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': case['accept'],
                    'tls_connect': case['connect']}

                for each in test_cases_accept:
                    input_param = {
                        'host': 'test_host',
                        'tls_accept': each['input']}
                    expected_result = {
                        'host': 'test_host',
                        'tls_accept': each['output']}
                    self.mock_module_functions.params = input_param
                    host = self.module.Host(self.mock_module_functions)

                    result = host.generate_zabbix_host(exist_host)
                    self.assertEqual(result, expected_result)

            # TLS all cases with ID and key
            for accept in range(1, 8):
                for connect in [1, 2, 4]:
                    exist_host = {
                        'host': 'exist host',
                        'inventory_mode': '1',
                        'tls_accept': str(accept),
                        'tls_connect': str(connect)}

                    for each in test_cases_accept:
                        input_param = {
                            'host': 'test_host',
                            'tls_accept': each['input'],
                            'tls_psk_identity': 'test_tls_psk_identity',
                            'tls_psk': 'test_tls_psk'}
                        expected_result = {
                            'host': 'test_host',
                            'tls_accept': each['output'],
                            'tls_psk_identity': 'test_tls_psk_identity',
                            'tls_psk': 'test_tls_psk'}
                        self.mock_module_functions.params = input_param
                        host = self.module.Host(self.mock_module_functions)

                        result = host.generate_zabbix_host(exist_host)
                        self.assertEqual(result, expected_result)

    def test_psk_connect_combinations(self):
        """
        Testing the ability to select each connection mode.
        The test includes all possible combinations.

        Expected result: all test cases run successfully.
        """
        test_cases_connect = [
            {'input': 'unencrypted', 'output': '1'},
            {'input': 'psk', 'output': '2'},
            {'input': 'cert', 'output': '4'}]

        exist_cases = [
            {'accept': '2', 'connect': '1'},
            {'accept': '3', 'connect': '1'},
            {'accept': '6', 'connect': '1'},
            {'accept': '7', 'connect': '1'},
            {'accept': '1', 'connect': '2'},
            {'accept': '2', 'connect': '2'},
            {'accept': '3', 'connect': '2'},
            {'accept': '6', 'connect': '2'},
            {'accept': '7', 'connect': '2'}]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            # ID and key are not required
            for case in exist_cases:
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': '1',
                    'tls_accept': case['accept'],
                    'tls_connect': case['connect']}

                for each in test_cases_connect:
                    input_param = {
                        'host': 'test_host',
                        'tls_connect': each['input']}
                    expected_result = {
                        'host': 'test_host',
                        'tls_connect': each['output']}
                    self.mock_module_functions.params = input_param
                    host = self.module.Host(self.mock_module_functions)

                    result = host.generate_zabbix_host(exist_host)
                    self.assertEqual(result, expected_result)

            # TLS all cases with ID and key
            for accept in range(1, 8):
                for connect in [1, 2, 4]:
                    exist_host = {
                        'host': 'exist host',
                        'inventory_mode': '1',
                        'tls_accept': str(accept),
                        'tls_connect': str(connect)}

                    for each in test_cases_connect:
                        input_param = {
                            'host': 'test_host',
                            'tls_connect': each['input'],
                            'tls_psk_identity': 'test_tls_psk_identity',
                            'tls_psk': 'test_tls_psk'}
                        expected_result = {
                            'host': 'test_host',
                            'tls_connect': each['output'],
                            'tls_psk_identity': 'test_tls_psk_identity',
                            'tls_psk': 'test_tls_psk'}
                        self.mock_module_functions.params = input_param
                        host = self.module.Host(self.mock_module_functions)

                        result = host.generate_zabbix_host(exist_host)
                        self.assertEqual(result, expected_result)

    def test_psk_error(self):
        """
        Testing the PSK encryption mode.
        The test includes all possible situations where the additional PSK
        parameters are required but are not present in the input data.

        Expected result: an exception with an error message.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            test_cases = [
                {
                    'host': 'test_host',
                    'tls_accept': ['psk']},
                {
                    'host': 'test_host',
                    'tls_accept': ['psk'],
                    'tls_psk_identity': 'tls_psk_identity'},
                {
                    'host': 'test_host',
                    'tls_accept': ['psk'],
                    'tls_psk': 'tls_psk'}]

            for accept in ['1', '4', '5']:
                for connect in ['1', '4']:
                    exist_host = {
                        'host': 'exist host',
                        'inventory_mode': '1',
                        'tls_accept': accept,
                        'tls_connect': connect}

                    for each in test_cases:
                        self.mock_module_functions.params = each
                        host = self.module.Host(self.mock_module_functions)

                        with self.assertRaises(AnsibleFailJson) as ansible_result:
                            host.generate_zabbix_host(exist_host)
                        self.assertTrue(ansible_result.exception.args[0]['failed'])
                        self.assertEqual(
                            'Missing TLS PSK params',
                            ansible_result.exception.args[0]['msg'])


class TestInventory(TestModules):
    """Class for testing the operation of the module with IPMI parameters"""
    module = zabbix_host

    def test_inventory(self):
        """
        Testing inventory modes. The test includes the application of
        automatic and manual mode from all possible modes.

        Expected result: automatic and manual mode successfully applied.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for input_mode in ['automatic', 'manual']:
                for exist_mode in ['1', '0', '-1']:

                    input_param = {
                        'host': 'test_host',
                        'inventory_mode': input_mode,
                        'inventory': {'type': 1, 'type_full': 2}}
                    exist_host = {
                        'host': 'exist host',
                        'inventory_mode': exist_mode,
                        'items': {'name': 'test', 'inventory_link': '0'}}
                    expected_result = {
                        'host': 'test_host',
                        'inventory_mode': inventory_mode_types.get(input_mode),
                        'inventory': {'type': 1, 'type_full': 2}}

                    self.mock_module_functions.params = input_param
                    host = self.module.Host(self.mock_module_functions)
                    host.inventory_links = {}

                    result = host.generate_zabbix_host(exist_host)
                    self.assertEqual(result, expected_result)

    def test_inventory_mode_disable(self):
        """
        Testing inventory modes. The test includes the application of
        the disable mode from all possible modes.

        Expected result: the disable mode successfully applied.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for exist_mode in ['1', '0', '-1']:

                input_param = {
                    'host': 'test_host',
                    'inventory_mode': 'disabled'}
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': exist_mode,
                    'items': {'name': 'test', 'inventory_link': '0'}}
                expected_result = {
                    'host': 'test_host',
                    'inventory_mode': inventory_mode_types.get('disabled')}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                host.inventory_links = {}

                result = host.generate_zabbix_host(exist_host)
                self.assertEqual(result, expected_result)

    def test_inventory_error_unknown_field(self):
        """
        Testing for an error in case of an attempt to specify a value
        for a non-existent inventory field.

        Expected result: an exception with an error message.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for input_mode in ['automatic', 'manual']:
                for exist_mode in ['1', '0', '-1']:

                    input_param = {
                        'host': 'test_host',
                        'inventory_mode': input_mode,
                        'inventory': {'type': 1, 'Unknown_field': 2}}
                    exist_host = {
                        'host': 'exist host',
                        'inventory_mode': exist_mode,
                        'items': {'name': 'test', 'inventory_link': '0'}}

                    self.mock_module_functions.params = input_param
                    host = self.module.Host(self.mock_module_functions)
                    host.inventory_links = {}

                    with self.assertRaises(AnsibleFailJson) as ansible_result:
                        host.generate_zabbix_host(exist_host)
                    self.assertTrue(ansible_result.exception.args[0]['failed'])
                    self.assertIn(
                        'Unknown inventory param:',
                        ansible_result.exception.args[0]['msg'])

    def test_inventory_error_disable_mode(self):
        """
        Testing disabled inventory mode.
        The test includes two options:
        1. The inventory mode is disabled in the task. In this case, an
        error will occur with any current mode.
        2. Inventory mode is disabled on the host. In this case, an attempt to
        specify any inventory field will cause an error.

        Expected result: exception with error message.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            # disabled in task
            for exist_mode in ['1', '0', '-1']:

                input_param = {
                    'host': 'test_host',
                    'inventory_mode': 'disabled',
                    'inventory': {'type': 1, 'type_full': 2}}
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': exist_mode,
                    'items': {'name': 'test', 'inventory_link': '0'}}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                host.inventory_links = {}

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    host.generate_zabbix_host(exist_host)
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    'Inventory parameters not applicable.',
                    ansible_result.exception.args[0]['msg'])

            # disabled on host
            input_param = {
                'host': 'test_host',
                'inventory': {'type': 1, 'type_full': 2}}
            exist_host = {
                'host': 'exist host',
                'inventory_mode': '-1',
                'items': {'name': 'test', 'inventory_link': '0'}}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)
            host.inventory_links = {}

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                host.generate_zabbix_host(exist_host)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertIn(
                'Inventory parameters not applicable.',
                ansible_result.exception.args[0]['msg'])

    def test_inventory_error_linked_item(self):
        """
        Testing an error when trying to set a value for an inventory
        field if this field is already associated with some metric.
        It is important to note that this case is relevant only in automatic
        inventory mode.

        Expected result: an exception with an error message.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for exist_mode in ['1', '0', '-1']:

                input_param = {
                    'host': 'test_host',
                    'inventory_mode': 'automatic',
                    'inventory': {'type': 1, 'type_full': 2}}
                exist_host = {
                    'host': 'exist host',
                    'inventory_mode': exist_mode,
                    'items': {'name': 'test', 'inventory_link': '1'}}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                host.inventory_links = {'type': 'test'}

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    host.generate_zabbix_host(exist_host)
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    'is already linked to the item',
                    ansible_result.exception.args[0]['msg'])


class TestInterfaces(TestModules):
    """Class for testing the operation of the module with IPMI parameters"""
    module = zabbix_host

    def test_agent_ipmi_jmx_interfaces(self):
        """
        Testing the creation of interfaces. The test includes
        checks only for agent, IPMI, and JMX interfaces.
        Test cases:
        1. All types with a default value.
        2. All types with a specified IP address and port.
        3. All types with a DNS name.
        4. All types with connection via DNS.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'input': [
                    {'type': 'agent', 'useip': True, 'ip': '', 'dns': '',
                     'port': None},
                    {'type': 'ipmi', 'useip': True, 'ip': '', 'dns': '',
                     'port': None},
                    {'type': 'jmx', 'useip': True, 'ip': '', 'dns': '',
                     'port': None}],
                'expected': [
                    {'type': '1', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '10050', 'dns': '', 'details': [], 'main': '1'},
                    {'type': '3', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '623', 'dns': '', 'details': [], 'main': '1'},
                    {'type': '4', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '12345', 'dns': '', 'details': [], 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'agent', 'useip': True, 'ip': '10.10.10.10',
                     'dns': '', 'port': '10051'},
                    {'type': 'ipmi', 'useip': True, 'ip': '20.20.20.20',
                     'dns': '', 'port': '650'},
                    {'type': 'jmx', 'useip': True, 'ip': '30.30.30.30',
                     'dns': '', 'port': '23456'}],
                'expected': [
                    {'type': '1', 'useip': '1', 'ip': '10.10.10.10',
                     'port': '10051', 'dns': '', 'details': [], 'main': '1'},
                    {'type': '3', 'useip': '1', 'ip': '20.20.20.20',
                     'port': '650', 'dns': '', 'details': [], 'main': '1'},
                    {'type': '4', 'useip': '1', 'ip': '30.30.30.30',
                     'port': '23456', 'dns': '', 'details': [], 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'agent', 'useip': True, 'ip': '10.10.10.10',
                     'dns': 'test_agent.com', 'port': '10051'},
                    {'type': 'ipmi', 'useip': True, 'ip': '20.20.20.20',
                     'dns': 'test_ipmi.com', 'port': '650'},
                    {'type': 'jmx', 'useip': True, 'ip': '30.30.30.30',
                     'dns': 'test_jmx.com', 'port': '23456'}],
                'expected': [
                    {'type': '1', 'useip': '1', 'ip': '10.10.10.10',
                     'port': '10051', 'dns': 'test_agent.com', 'details': [],
                     'main': '1'},
                    {'type': '3', 'useip': '1', 'ip': '20.20.20.20',
                     'port': '650', 'dns': 'test_ipmi.com', 'details': [],
                     'main': '1'},
                    {'type': '4', 'useip': '1', 'ip': '30.30.30.30',
                     'port': '23456', 'dns': 'test_jmx.com', 'details': [],
                     'main': '1'}]
            },
            {
                'input': [
                    {'type': 'agent', 'useip': False, 'ip': '10.10.10.10',
                     'dns': 'test_agent.com', 'port': '10051'},
                    {'type': 'ipmi', 'useip': False, 'ip': '20.20.20.20',
                     'dns': 'test_ipmi.com', 'port': '650'},
                    {'type': 'jmx', 'useip': False, 'ip': '30.30.30.30',
                     'dns': 'test_jmx.com', 'port': '23456'}],
                'expected': [
                    {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                     'port': '10051', 'dns': 'test_agent.com', 'details': [],
                     'main': '1'},
                    {'type': '3', 'useip': '0', 'ip': '20.20.20.20',
                     'port': '650', 'dns': 'test_ipmi.com', 'details': [],
                     'main': '1'},
                    {'type': '4', 'useip': '0', 'ip': '30.30.30.30',
                     'port': '23456', 'dns': 'test_jmx.com', 'details': [],
                     'main': '1'}]
            }
        ]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': case['input']}
                expected_result = {
                    'host': 'test_host',
                    'interfaces': case['expected']}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                self.maxDiff = None

                result = host.generate_zabbix_host(exist_host)

                self.assertEqual(
                    len(expected_result['interfaces']),
                    len(result['interfaces']))

                for expected in expected_result['interfaces']:
                    self.assertIn(expected, result['interfaces'])

    def test_require_dns(self):
        """
        Testing the creation of interfaces for monitoring via DNS. In this
        case, the DNS name field is required.

        Expected result: an exception with an error message.
        """
        input_data = [
            {'type': 'agent', 'useip': False, 'ip': '10.10.10.10', 'dns': '',
             'port': '10051'},
            {'type': 'ipmi', 'useip': False, 'ip': '20.20.20.20', 'dns': '',
             'port': '650'},
            {'type': 'jmx', 'useip': False, 'ip': '30.30.30.30', 'dns': '',
             'port': '23456'}]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            input_param = {
                'host': 'test_host',
                'interfaces': input_data}

            self.mock_module_functions.params = input_param
            host = self.module.Host(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                host.generate_zabbix_host(exist_host)
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                'Required parameter not found: dns',
                ansible_result.exception.args[0]['msg'])

    def test_validations_snmp_parameters(self):
        """
        Testing details of SNMP interfaces.
        Test cases:

        1. Interface without version.

        SNMPv1:
        2. Interface version 1 without bulk (one parameter).
        3. Interface version 1 without bulk and community (two parameters, with the list of missing parameters in error).
        4. Interface version 1 with additional parameter from SNMPv3 (context name).
        5. Interface version 1 with additional parameter (context name) and missing parameter (community).

        SNMPv2:
        6. Interface version 2 without bulk (one parameter).
        7. Interface version 2 without bulk and community (two parameters, with the list of missing parameters in error).
        8. Interface version 2 with additional parameter from SNMPv3 (context name).
        9. Interface version 2 with additional parameter (context name) and missing parameter (community).

        SNMPv3 (noAuthNoPriv):
        10. Interface version 3 without security level (checks error message).
        11. Interface version 3 without bulk (one parameter).
        12. Interface version 3 without bulk and context name (two parameters, with the list of missing parameters in error).
        13. Interface version 3 with additional parameter from SNMPv1 (community).
        14. Interface version 1 with additional parameter (community) and missing parameter (context name).

        SNMPv3 (authNoPriv):
        15. Interface version 3 without authentication protocol (checks error message).
        16. Interface version 3 without authentication protocol and context name (two parameters, with the list of missing parameters in error;
        check two independent parameters, because authentication protocol depends on security level only).
        17. Interface version 3 with additional parameters for 'authPriv'.
        18. Interface version 3 without authentication parameters, but with privacy parameters.

        SNMPv3 (authPriv):
        19. Interface version 3 without authentication parameters.
        20. Interface version 3 without privacy parameters.
        21. Interface version 3 without authentication and privacy parameters.
        22. Interface version 3 with additional parameter (community).
        23. Interface version 3 without authentication and privacy parameters and with additional parameter (community).

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'number_test_case': 1,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': None, 'bulk': True, 'community': '111', 'max_repetitions': None, 'contextname': None,
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found: version"]
            },
            {
                'number_test_case': 2,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '1', 'bulk': None, 'community': '111', 'max_repetitions': None, 'contextname': None,
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv1: bulk"]
            },
            {
                'number_test_case': 3,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '1', 'bulk': None, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv1:", 'bulk', 'community']
            },
            {
                'number_test_case': 4,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '1', 'bulk': True, 'community': 'test', 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv1:", 'contextname']
            },
            {
                'number_test_case': 5,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '1', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv1:", 'contextname']
            },
            {
                'number_test_case': 6,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '2', 'bulk': None, 'community': '111', 'max_repetitions': None, 'contextname': None,
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv2: bulk"]
            },
            {
                'number_test_case': 7,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '2', 'bulk': None, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv2:", 'bulk', 'community']
            },
            {
                'number_test_case': 8,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '2', 'bulk': True, 'community': 'test', 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv2:", 'contextname']
            },
            {
                'number_test_case': 9,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '2', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': None, 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv2:", 'contextname']
            },
            {
                'number_test_case': 10,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': 'securityname', 'securitylevel': None, 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found: securitylevel"]
            },
            {
                'number_test_case': 11,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': None, 'community': None, 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': 'securityname', 'securitylevel': 'noAuthNoPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'bulk']
            },
            {
                'number_test_case': 12,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': None, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'noAuthNoPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'bulk', 'contextname']
            },
            {
                'number_test_case': 13,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': 'test', 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': 'securityname', 'securitylevel': 'noAuthNoPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv3:", 'community']
            },
            {
                'number_test_case': 14,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': None, 'community': 'test', 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'noAuthNoPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv3:", 'community']
            },
            {
                'number_test_case': 15,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': 'securityname', 'securitylevel': 'authNoPriv', 'authprotocol': None, 'authpassphrase': 'authpassphrase',
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'authprotocol']
            },
            {
                'number_test_case': 16,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authNoPriv', 'authprotocol': None, 'authpassphrase': 'authpassphrase',
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'authprotocol', 'contextname']
            },
            {
                'number_test_case': 17,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authNoPriv', 'authprotocol': 'md5', 'authpassphrase': 'authpassphrase',
                                 'privprotocol': 'des', 'privpassphrase': 'privpassphrase'}}],
                'expected_errors': ["Incorrect arguments for SNMPv3:", 'privprotocol', 'privpassphrase']
            },
            {
                'number_test_case': 18,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authNoPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': 'des', 'privpassphrase': 'privpassphrase'}}],
                'expected_errors': ["Incorrect arguments for SNMPv3:", 'privprotocol', 'privpassphrase']
            },
            {
                'number_test_case': 19,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': 'contextname',
                                 'securityname': 'securityname', 'securitylevel': 'authPriv', 'authprotocol': None, 'authpassphrase': 'authpassphrase',
                                 'privprotocol': 'des', 'privpassphrase': 'privpassphrase'}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'authprotocol']
            },
            {
                'number_test_case': 20,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authPriv', 'authprotocol': 'md5', 'authpassphrase': 'authpassphrase',
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'privprotocol', 'privpassphrase']
            },
            {
                'number_test_case': 21,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': None, 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Required parameter not found for SNMPv3:", 'authprotocol', 'authpassphrase', 'privprotocol', 'privpassphrase']
            },
            {
                'number_test_case': 22,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': 'test', 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authPriv', 'authprotocol': 'md5', 'authpassphrase': 'authpassphrase',
                                 'privprotocol': 'des', 'privpassphrase': 'privpassphrase'}}],
                'expected_errors': ["Incorrect arguments for SNMPv3:", 'community']
            },
            {
                'number_test_case': 23,
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '3', 'bulk': True, 'community': 'test', 'max_repetitions': None, 'contextname': None,
                                 'securityname': 'securityname', 'securitylevel': 'authPriv', 'authprotocol': None, 'authpassphrase': None,
                                 'privprotocol': None, 'privpassphrase': None}}],
                'expected_errors': ["Incorrect arguments for SNMPv3:", 'community']
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for test_case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': test_case['input']}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    host.generate_zabbix_host(exist_host)
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                for expected_error in test_case['expected_errors']:
                    self.assertIn(
                        expected_error,
                        ansible_result.exception.args[0]['msg'])

    def test_snmp_v1_v2(self):
        """
        Testing SNMP interfaces version 1 and 2.
        Test cases:
        1. Interface version 1 with default parameters.
        2. Interface version 1 with all parameters.
        3. Interface version 1 with monitoring via DNS.
        4. Interface version 1 with all detailed parameters.
        5. Interface version 2 with default parameters.
        6. Interface version 2 with all parameters.
        7. Interface version 2 with monitoring via DNS.
        8. Interface version 2 with all detailed parameters.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '1', 'bulk': True, 'community': '{$SNMP_COMMUNITY}'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1', 'port': '161', 'dns': '',
                     'details': {'version': '1', 'bulk': '1', 'community': '{$SNMP_COMMUNITY}'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '10.10.10.10', 'dns': 'test_snmp.com', 'port': '170',
                     'details': {'version': '1', 'bulk': True, 'community': '{$SNMP_COMMUNITY}'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '10.10.10.10', 'port': '170', 'dns': 'test_snmp.com',
                     'details': {'version': '1', 'bulk': '1', 'community': '{$SNMP_COMMUNITY}'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': False, 'ip': '10.10.10.10', 'dns': 'test_snmp.com', 'port': '170',
                     'details': {'version': '1', 'bulk': True, 'community': '{$SNMP_COMMUNITY}'}}],
                'expected': [
                    {'type': '2', 'useip': '0', 'ip': '10.10.10.10', 'port': '170', 'dns': 'test_snmp.com',
                     'details': {'version': '1', 'bulk': '1', 'community': '{$SNMP_COMMUNITY}'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '10.10.10.10', 'dns': 'test_snmp.com', 'port': '170',
                     'details': {'version': '1', 'bulk': False, 'community': 'public'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '10.10.10.10', 'port': '170', 'dns': 'test_snmp.com',
                     'details': {'version': '1', 'bulk': '0', 'community': 'public'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '', 'port': None,
                     'details': {'version': '2', 'bulk': True, 'community': '{$SNMP_COMMUNITY}'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1', 'port': '161', 'dns': '',
                     'details': {'version': '2', 'bulk': '1', 'community': '{$SNMP_COMMUNITY}'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '10.10.10.10', 'dns': 'test_snmp.com', 'port': '170',
                     'details': {'version': '2', 'bulk': True, 'community': '{$SNMP_COMMUNITY}'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '10.10.10.10', 'port': '170', 'dns': 'test_snmp.com',
                     'details': {'version': '2', 'bulk': '1', 'community': '{$SNMP_COMMUNITY}'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': False, 'ip': '10.10.10.10', 'dns': 'test_snmp.com', 'port': '170',
                     'details': {'version': '2', 'bulk': True, 'community': '{$SNMP_COMMUNITY}'}}],
                'expected': [
                    {'type': '2', 'useip': '0', 'ip': '10.10.10.10', 'port': '170', 'dns': 'test_snmp.com',
                     'details': {'version': '2', 'bulk': '1', 'community': '{$SNMP_COMMUNITY}'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '10.10.10.10', 'dns': 'test_snmp.com', 'port': '170',
                     'details': {'version': '2', 'bulk': False, 'community': 'public'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '10.10.10.10', 'port': '170', 'dns': 'test_snmp.com',
                     'details': {'version': '2', 'bulk': '0', 'community': 'public'}, 'main': '1'}]
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': case['input']}
                expected_result = {
                    'host': 'test_host',
                    'interfaces': case['expected']}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                self.maxDiff = None

                result = host.generate_zabbix_host(exist_host)

                self.assertEqual(
                    len(expected_result['interfaces']),
                    len(result['interfaces']))

                self.assertEqual(
                    expected_result['interfaces'][0],
                    result['interfaces'][0])

    def test_snmp_v2_zabbix_64(self):
        """
        Testing SNMP version 2 for Zabbix version above 6.4. In this case,
        the 'max_repetitions' field is added.
        Test cases:
        1. Default parameters.
        2. Specifying all parameters.

        Expected result: all test cases ran successfully.
        """
        def mock_api_version_64(self):
            return ('6.4.5')

        test_cases = [
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '',
                     'port': None, 'details': {
                         'version': '2', 'bulk': True,
                         'community': '{$SNMP_COMMUNITY}',
                         'max_repetitions': '10'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '161', 'dns': '', 'details': {
                         'version': '2', 'bulk': '1',
                         'community': '{$SNMP_COMMUNITY}',
                         'max_repetitions': '10'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '10.10.10.10',
                     'dns': 'test_snmp.com', 'port': '170', 'details': {
                         'version': '2', 'bulk': False, 'community': 'public',
                         'max_repetitions': '20'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '10.10.10.10',
                     'port': '170', 'dns': 'test_snmp.com', 'details': {
                         'version': '2', 'bulk': '0', 'community': 'public',
                         'max_repetitions': '20'}, 'main': '1'}]
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_64):

            for case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': case['input']}
                expected_result = {
                    'host': 'test_host',
                    'interfaces': case['expected']}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                self.maxDiff = None

                result = host.generate_zabbix_host(exist_host)

                self.assertEqual(
                    len(expected_result['interfaces']),
                    len(result['interfaces']))

                self.assertEqual(
                    expected_result['interfaces'][0],
                    result['interfaces'][0])

    def test_snmp_v3_zabbix_60(self):
        """
        Testing SNMP version 3 for Zabbix version 6.0.
        Test cases:
        1. Default parameters.
        2. Specifying all parameters.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '',
                     'port': None, 'details': {
                         'version': '3', 'securityname': '', 'contextname': '',
                         'bulk': True, 'securitylevel': 'noAuthNoPriv'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '161', 'dns': '', 'main': '1', 'details': {
                         'version': '3', 'bulk': '1', 'contextname': '',
                         'securityname': '', 'securitylevel': '0',
                         'authprotocol': '0', 'authpassphrase': '',
                         'privprotocol': '0', 'privpassphrase': ''}}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': False, 'ip': '10.10.10.10',
                     'dns': 'test_snmp.com', 'port': '170', 'details': {
                         'version': '3', 'bulk': False,
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': 'noAuthNoPriv'}}],
                'expected': [
                    {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                     'port': '170', 'dns': 'test_snmp.com', 'details': {
                         'version': '3', 'bulk': '0',
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': '0', 'authprotocol': '0',
                         'authpassphrase': '', 'privprotocol': '0',
                         'privpassphrase': ''}, 'main': '1'}]
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': case['input']}
                expected_result = {
                    'host': 'test_host',
                    'interfaces': case['expected']}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                self.maxDiff = None

                result = host.generate_zabbix_host(exist_host)

                self.assertEqual(
                    len(expected_result['interfaces']),
                    len(result['interfaces']))

                self.assertEqual(
                    expected_result['interfaces'][0],
                    result['interfaces'][0])

    def test_snmp_v3_zabbix_64(self):
        """
        Testing SNMP version 2 for Zabbix version above 6.4. In this case,
        the 'max_repetitions' field is added.
        Test cases:
        1. Default parameters.
        2. Specifying all parameters.

        Expected result: all test cases run successfully.
        """
        def mock_api_version_64(self):
            return ('6.4.5')

        test_cases = [
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '',
                     'port': None, 'details': {
                         'version': '3', 'bulk': True, 'contextname': '',
                         'securityname': '', 'securitylevel': 'noAuthNoPriv',
                         'max_repetitions': '10'}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '161', 'dns': '', 'details': {
                         'version': '3', 'bulk': '1', 'contextname': '',
                         'securityname': '', 'securitylevel': '0',
                         'authprotocol': '0', 'authpassphrase': '',
                         'privprotocol': '0', 'privpassphrase': '',
                         'max_repetitions': '10'}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': False, 'ip': '1.1.1.1',
                     'dns': 'test_snmp.com', 'port': '170', 'details': {
                         'version': '3', 'bulk': False,
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': 'noAuthNoPriv',
                         'max_repetitions': '12'}}],
                'expected': [
                    {'type': '2', 'useip': '0', 'ip': '1.1.1.1', 'main': '1',
                     'port': '170', 'dns': 'test_snmp.com', 'details': {
                         'version': '3', 'bulk': '0',
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': '0', 'authprotocol': '0',
                         'authpassphrase': '', 'privprotocol': '0',
                         'privpassphrase': '', 'max_repetitions': '12'}}]
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_64):

            for case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': case['input']}
                expected_result = {
                    'host': 'test_host',
                    'interfaces': case['expected']}

                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)
                self.maxDiff = None

                result = host.generate_zabbix_host(exist_host)

                self.assertEqual(
                    len(expected_result['interfaces']),
                    len(result['interfaces']))

                self.assertEqual(
                    expected_result['interfaces'][0],
                    result['interfaces'][0])

    def test_snmp_v3_authNoPriv(self):
        """
        Testing SNMP parameters using authNoPriv mode.
        Test cases:
        1. Default parameters.
        2. Specifying all parameters.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '',
                     'port': None, 'details': {
                         'version': '3', 'bulk': True, 'contextname': '',
                         'securityname': '', 'securitylevel': 'authNoPriv',
                         'authpassphrase': ''}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1', 'port':
                     '161', 'dns': '', 'details': {
                         'version': '3', 'bulk': '1', 'contextname': '',
                         'securityname': '', 'securitylevel': '1',
                         'privprotocol': '0', 'privpassphrase': '',
                         'authpassphrase': ''}, 'main': '1'}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': False, 'ip': '10.10.10.10',
                     'dns': 'test_snmp.com', 'port': '170', 'details': {
                         'version': '3', 'bulk': False,
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': 'authNoPriv',
                         'authpassphrase': 'authpassphrase'}}],
                'expected': [
                    {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                     'port': '170', 'dns': 'test_snmp.com', 'details': {
                         'version': '3', 'bulk': '0',
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': '1', 'privprotocol': '0',
                         'privpassphrase': '',
                         'authpassphrase': 'authpassphrase'}, 'main': '1'}]
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for authprotocol in snmp_authprotocol_types:
                for case in test_cases:
                    input_param = {
                        'host': 'test_host',
                        'interfaces': case['input']}
                    input_param['interfaces'][0][
                        'details']['authprotocol'] = authprotocol
                    expected_result = {
                        'host': 'test_host',
                        'interfaces': case['expected']}
                    expected_result['interfaces'][0]['details'][
                        'authprotocol'] = snmp_authprotocol_types[authprotocol]

                    self.mock_module_functions.params = input_param
                    host = self.module.Host(self.mock_module_functions)
                    self.maxDiff = None

                    result = host.generate_zabbix_host(exist_host)

                    self.assertEqual(
                        len(expected_result['interfaces']),
                        len(result['interfaces']))

                    self.assertEqual(
                        expected_result['interfaces'][0],
                        result['interfaces'][0])

    def test_snmp_v3_authPriv(self):
        """
        Testing SNMP parameters using authPriv mode.
        Test cases:
        1. Default parameters.
        2. Specifying all parameters.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'input': [
                    {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '',
                     'port': None, 'details': {
                         'version': '3', 'bulk': True, 'contextname': '',
                         'securityname': '', 'securitylevel': 'authPriv',
                         'authpassphrase': '', 'privpassphrase': ''}}],
                'expected': [
                    {'type': '2', 'useip': '1', 'ip': '127.0.0.1',
                     'port': '161', 'dns': '', 'main': '1', 'details': {
                         'version': '3', 'bulk': '1', 'contextname': '',
                         'securityname': '', 'securitylevel': '2',
                         'privpassphrase': '', 'authpassphrase': ''}}]
            },
            {
                'input': [
                    {'type': 'snmp', 'useip': False, 'ip': '10.10.10.10',
                     'dns': 'test_snmp.com', 'port': '170', 'details': {
                         'version': '3', 'bulk': False,
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': 'authPriv',
                         'authpassphrase': 'authpassphrase',
                         'privpassphrase': 'privpassphrase'}}],
                'expected': [
                    {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                     'port': '170', 'dns': 'test_snmp.com', 'details': {
                         'version': '3', 'bulk': '0',
                         'contextname': 'contextname',
                         'securityname': 'securityname',
                         'securitylevel': '2',
                         'privpassphrase': 'privpassphrase',
                         'authpassphrase': 'authpassphrase'}, 'main': '1'}]
            }]

        exist_host = {'host': 'test_host', 'inventory_mode': '1'}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for authprotocol in snmp_authprotocol_types:
                for privprotocol in snmp_privprotocol_types:
                    for case in test_cases:
                        input_param = {
                            'host': 'test_host',
                            'interfaces': case['input']}
                        input_param['interfaces'][0]['details']['authprotocol'] = authprotocol
                        input_param['interfaces'][0]['details']['privprotocol'] = privprotocol
                        expected_result = {
                            'host': 'test_host',
                            'interfaces': case['expected']}
                        expected_result['interfaces'][0]['details']['authprotocol'] = snmp_authprotocol_types[authprotocol]
                        expected_result['interfaces'][0]['details']['privprotocol'] = snmp_privprotocol_types[privprotocol]

                        self.mock_module_functions.params = input_param
                        host = self.module.Host(self.mock_module_functions)
                        self.maxDiff = None

                        result = host.generate_zabbix_host(exist_host)

                        self.assertEqual(
                            len(expected_result['interfaces']),
                            len(result['interfaces']))

                        self.assertEqual(
                            expected_result['interfaces'][0],
                            result['interfaces'][0])

    def test_count_interfaces(self):
        """
        Testing the ability to work with only one interface of each type.
        If two interfaces of the same type are specified, an exception
        will be raised.
        Test cases:
        1. Two agent interfaces.
        2. Two IPMI interfaces.
        3. Two JMX interfaces.
        4. Two SNMP interfaces.
        5. One IPMI and two agent interfaces.

        Expected result: an exception with an error message.
        """
        test_cases = [
            [
                {'type': 'agent', 'useip': True, 'ip': '', 'dns': '',
                 'port': None},
                {'type': 'agent', 'useip': True, 'ip': '10.10.10.10',
                 'dns': '', 'port': None}
            ],
            [
                {'type': 'ipmi', 'useip': True, 'ip': '', 'dns': '',
                 'port': None},
                {'type': 'ipmi', 'useip': True, 'ip': '20.20.20.20',
                 'dns': '', 'port': None}
            ],
            [
                {'type': 'jmx', 'useip': True, 'ip': '', 'dns': '',
                 'port': None},
                {'type': 'jmx', 'useip': True, 'ip': '30.30.30.30',
                 'dns': '', 'port': None}
            ],
            [
                {'type': 'snmp', 'useip': True, 'ip': '', 'dns': '',
                 'port': None, 'details': {
                     'version': '1', 'bulk': True,
                     'community': '{$SNMP_COMMUNITY}'}},
                {'type': 'snmp', 'useip': True, 'ip': '40.40.40.40',
                 'dns': '', 'port': None, 'details': {
                     'version': '1', 'bulk': True,
                     'community': '{$SNMP_COMMUNITY}'}}
            ],
            [
                {'type': 'ipmi', 'useip': True, 'ip': '', 'dns': '',
                 'port': None},
                {'type': 'agent', 'useip': True, 'ip': '', 'dns': '',
                 'port': None},
                {'type': 'agent', 'useip': True, 'ip': '10.10.10.10',
                 'dns': '', 'port': None}
            ]
        ]

        exist_host = {
            'host': 'test_host',
            'inventory_mode': '1',
            'interfaces': {'type': ''}}

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                input_param = {
                    'host': 'test_host',
                    'interfaces': case}
                self.mock_module_functions.params = input_param
                host = self.module.Host(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    host.generate_zabbix_host(exist_host)
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    'interfaces defined in the task. Module supports only 1 interface of each type.',
                    ansible_result.exception.args[0]['msg'])
