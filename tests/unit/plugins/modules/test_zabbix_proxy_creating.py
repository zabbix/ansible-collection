#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleExitJson, AnsibleFailJson, TestModules, set_module_args, patch)


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


class TestCreating(TestModules):
    """Class for testing creation of a proxy"""
    module = zabbix_proxy

    def test_create_proxy_wo_parameters(self):
        """
        Testing the proxy creation function without additional parameters.

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_active_proxy_w_active_parameters_70(self):
        """
        Testing the active proxy creation function with all supported for active proxy options.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'proxy_groupid': '2', 'name': 'Test proxy group'}]

        def get_global_setting(self):
            return {'timeout_zabbix_agent': '1s', 'timeout_simple_check': '1s',
                    'timeout_snmp_agent': '1s', 'timeout_external_check': '1s',
                    'timeout_db_monitor': '1s', 'timeout_http_agent': '1s',
                    'timeout_ssh_agent': '1s', 'timeout_telnet_agent': '1s',
                    'timeout_script': '1s', 'timeout_browser': '1s'}

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'active',
            'proxy_group': 'Test proxy group',
            'local_address': '10.10.10.10',
            'local_port': '10051',
            'allowed_addresses': '10.10.10.10',
            'tls_accept': ['unencrypted', 'psk', 'cert'],
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'custom_timeouts': {
                'timeout_zabbix_agent': '10s',
                'timeout_simple_check': '',
                'timeout_snmp_agent': '{$MY_SNMP_TIMEOUT}',
                'timeout_external_check': '10s',
                'timeout_db_monitor': '10s',
                'timeout_http_agent': '10s',
                'timeout_ssh_agent': '10s',
                'timeout_telnet_agent': '10s',
                'timeout_script': '10s',
                'timeout_browser': '10s'},
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names,
                get_global_setting=get_global_setting):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_active_proxy_w_active_parameters_60(self):
        """
        Testing the active proxy creation function with all supported for active proxy options.
        Test for Zabbix version 6.0

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'active',
            'allowed_addresses': '10.10.10.10',
            'tls_accept': ['unencrypted', 'psk', 'cert'],
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_active_proxy_w_all_parameters_70(self):
        """
        Testing the active proxy creation function with all supported proxy options.
        Unsupported for active proxy parameters must be empty.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'proxy_groupid': '2', 'name': 'Test proxy group'}]

        def get_global_setting(self):
            return {'timeout_zabbix_agent': '1s', 'timeout_simple_check': '1s',
                    'timeout_snmp_agent': '1s', 'timeout_external_check': '1s',
                    'timeout_db_monitor': '1s', 'timeout_http_agent': '1s',
                    'timeout_ssh_agent': '1s', 'timeout_telnet_agent': '1s',
                    'timeout_script': '1s', 'timeout_browser': '1s'}

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'active',
            'proxy_group': 'Test proxy group',
            'local_address': '10.10.10.10',
            'local_port': '10051',
            'interface': {
                'address': '127.0.0.1',
                'port': '10051',
                'useip': True},
            'allowed_addresses': '10.10.10.10',
            'tls_connect': '',
            'tls_accept': ['unencrypted', 'psk', 'cert'],
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'custom_timeouts': {
                'timeout_zabbix_agent': '10s',
                'timeout_simple_check': '',
                'timeout_snmp_agent': '{$MY_SNMP_TIMEOUT}',
                'timeout_external_check': '10s',
                'timeout_db_monitor': '10s',
                'timeout_http_agent': '10s',
                'timeout_ssh_agent': '10s',
                'timeout_telnet_agent': '10s',
                'timeout_script': '10s',
                'timeout_browser': '10s'},
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names,
                get_global_setting=get_global_setting):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_active_proxy_w_all_parameters_60(self):
        """
        Testing the active proxy creation function with all supported proxy options.
        Unsupported for active proxy parameters must be empty.
        Test for Zabbix version 6.0

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'active',
            'interface': {
                'address': '127.0.0.1',
                'port': '10051',
                'useip': True},
            'allowed_addresses': '10.10.10.10',
            'tls_connect': '',
            'tls_accept': ['unencrypted', 'psk', 'cert'],
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_passive_proxy_w_passive_parameters_70(self):
        """
        Testing the passive proxy creation function with all supported for passive proxy options.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'proxy_groupid': '2', 'name': 'Test proxy group'}]

        def get_global_setting(self):
            return {'timeout_zabbix_agent': '1s', 'timeout_simple_check': '1s',
                    'timeout_snmp_agent': '1s', 'timeout_external_check': '1s',
                    'timeout_db_monitor': '1s', 'timeout_http_agent': '1s',
                    'timeout_ssh_agent': '1s', 'timeout_telnet_agent': '1s',
                    'timeout_script': '1s', 'timeout_browser': '1s'}

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'passive',
            'interface': {
                'address': '127.0.0.1',
                'port': '10051',
                'useip': True},
            'proxy_group': 'Test proxy group',
            'local_address': '10.10.10.10',
            'local_port': '10051',
            'tls_connect': 'psk',
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'custom_timeouts': {
                'timeout_zabbix_agent': '10s',
                'timeout_simple_check': '',
                'timeout_snmp_agent': '{$MY_SNMP_TIMEOUT}',
                'timeout_external_check': '10s',
                'timeout_db_monitor': '10s',
                'timeout_http_agent': '10s',
                'timeout_ssh_agent': '10s',
                'timeout_telnet_agent': '10s',
                'timeout_script': '10s',
                'timeout_browser': '10s'},
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names,
                get_global_setting=get_global_setting):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_passive_proxy_w_passive_parameters_60(self):
        """
        Testing the passive proxy creation function with all supported for passive proxy options.
        Test for Zabbix version 6.0

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'passive',
            'interface': {
                'address': '127.0.0.1',
                'port': '10051',
                'useip': True},
            'tls_connect': 'psk',
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_passive_proxy_w_all_parameters_70(self):
        """
        Testing the passive proxy creation function with all supported proxy options.
        Unsupported for passive proxy parameters must be empty.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'proxy_groupid': '2', 'name': 'Test proxy group'}]

        def get_global_setting(self):
            return {'timeout_zabbix_agent': '1s', 'timeout_simple_check': '1s',
                    'timeout_snmp_agent': '1s', 'timeout_external_check': '1s',
                    'timeout_db_monitor': '1s', 'timeout_http_agent': '1s',
                    'timeout_ssh_agent': '1s', 'timeout_telnet_agent': '1s',
                    'timeout_script': '1s', 'timeout_browser': '1s'}

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'passive',
            'proxy_group': 'Test proxy group',
            'local_address': '10.10.10.10',
            'local_port': '10051',
            'interface': {
                'address': '127.0.0.1',
                'port': '10051',
                'useip': True},
            'allowed_addresses': '',
            'tls_connect': 'psk',
            'tls_accept': [],
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'custom_timeouts': {
                'timeout_zabbix_agent': '10s',
                'timeout_simple_check': '',
                'timeout_snmp_agent': '{$MY_SNMP_TIMEOUT}',
                'timeout_external_check': '10s',
                'timeout_db_monitor': '10s',
                'timeout_http_agent': '10s',
                'timeout_ssh_agent': '10s',
                'timeout_telnet_agent': '10s',
                'timeout_script': '10s',
                'timeout_browser': '10s'},
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names,
                find_zabbix_proxy_groups_by_names=find_zabbix_proxy_groups_by_names,
                get_global_setting=get_global_setting):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_passive_proxy_w_all_parameters_60(self):
        """
        Testing the passive proxy creation function with all supported proxy options.
        Unsupported for passive proxy parameters must be empty.
        Test for Zabbix version 6.0

        Expected result: the task has been changed and the proxy
        has been created successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy,
            'mode': 'passive',
            'interface': {
                'address': '127.0.0.1',
                'port': '10051',
                'useip': True},
            'allowed_addresses': '',
            'tls_connect': 'psk',
            'tls_accept': [],
            'tls_psk_identity': 'my_tls_psk_identity',
            'tls_psk': 'my_tls_psk',
            'tls_issuer': 'my_tls_issuer',
            'tls_subject': 'my_tls_subject',
            'description': 'Description of my proxy'})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created proxy: {0}'.format(zabbix_proxy))

    def test_create_proxy_error(self):
        """
        Testing the proxy creation function in case of encountering an error
        during the creation.

        Expected result: the task has been failed.
        """

        def mock_send_request(self, method, params):
            raise Exception

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                ansible_result.exception.args[0]['msg'],
                'Failed to create proxy: {0}'.format(zabbix_proxy))
