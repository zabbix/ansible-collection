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
    Mock function to get Zabbix API version 7.0.0.
    """
    return '7.0.0'


class TestUpdating(TestModules):
    """Class for testing the update of the proxy"""
    module = zabbix_proxy

    def test_update_proxy_wo_parameters_70(self):
        """
        Testing the proxy update function without additional parameters.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'proxy.get':
                return [{
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
                }]

            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'mode': 'passive',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_wo_parameters_60(self):
        """
        Testing the proxy update function without additional parameters.
        Test for Zabbix version 6.0

        Expected result: the task has been changed and the proxy
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'proxy.get':
                return [{
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
                }]

            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '11085'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'mode': 'passive',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_no_need_update_70(self):
        """
        Testing the proxy update function in case nothing needs to be updated.
        Test for Zabbix version 7.0 +

        Expected result: the task has not been changed and the proxy
        has not been updated.
        """
        def mock_send_request(self, method, params):
            return [{
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
            }]

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'mode': 'active',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'No need to update proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_no_need_update_60(self):
        """
        Testing the proxy update function in case nothing needs to be updated.
        Test for Zabbix version 6.0

        Expected result: the task has not been changed and the proxy
        has not been updated.
        """
        def mock_send_request(self, method, params):
            return [{
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
            }]

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '11085'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'mode': 'active',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'No need to update proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_w_all_parameters_70(self):
        """
        Testing the proxy update function with all possible options.
        Test for Zabbix version 7.0 +

        Expected result: the task has been changed and the proxy
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'proxy.get':
                return [{
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
                }]

            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

        def find_zabbix_proxy_groups_by_names(self, proxy_group_names):
            return [{'proxy_groupid': '2', 'name': proxy_group_names}]

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
            'local_port': '10052',
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
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_w_all_parameters_60(self):
        """
        Testing the proxy update function with all possible options.
        Test for Zabbix version 6.0

        Expected result: the task has been changed and the proxy
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'proxy.get':
                return [{
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
                }]

            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

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
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_error_70(self):
        """
        Testing the proxy update function in case of encountering an error
        during the update.
        Test for Zabbix version 7.0 +

        Expected result: the task has been failed.
        """
        def mock_send_request(self, method, params):
            if method == 'proxy.get':
                return [{
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
                }]

            raise Exception

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'mode': 'passive',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["failed"])
            self.assertEqual(
                ansible_result.exception.args[0]["msg"],
                'Failed to update proxy: {0}'.format(zabbix_proxy))

    def test_update_proxy_error_60(self):
        """
        Testing the proxy update function in case of encountering an error
        during the update.
        Test for Zabbix version 6.0

        Expected result: the task has been failed.
        """
        def mock_send_request(self, method, params):
            if method == 'proxy.get':
                return [{
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
                }]

            raise Exception

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '11085'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'present',
            'mode': 'passive',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["failed"])
            self.assertEqual(
                ansible_result.exception.args[0]["msg"],
                'Failed to update proxy: {0}'.format(zabbix_proxy))
