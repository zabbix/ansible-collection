#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)


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


class TestGetZabbixProxy(TestModules):
    module = zabbix_proxy

    def test_get_zabbix_proxy_70(self):
        """
        Testing the function of getting data by proxy from Zabbix.
        Test for Zabbix version 7.0 +

        Expected result: all executions of the function returned
        empty inventory data.
        """

        def mock_send_request(self, method, params):
            proxy_data = {
                'proxyid': '4',
                'name': 'test_proxy',
                'proxy_groupid': '0',
                'local_address': '',
                'proxyGroup': [{"name": "test_proxy_group"}]
            }

            return [proxy_data]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70,
                send_api_request=mock_send_request):

            # Check simple get proxy data
            self.mock_module_functions.params = {}
            proxy = self.module.Proxy(self.mock_module_functions)

            result = proxy.get_zabbix_proxy('4')
            self.assertNotEqual(result.get('proxyGroup'), None)
            self.assertEqual(len(result.get('proxyGroup', [])), 1)

    def test_get_zabbix_proxy_60(self):
        """
        Testing the function of getting data by proxy from Zabbix.
        Test for Zabbix version 6.0

        Expected result: all executions of the function returned
        empty inventory data.
        """

        def mock_send_request(self, method, params):
            proxy_data = {
                "proxy_hostid": "0",
                "host": "test proxy",
                "status": "6",
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
                'interface': [{
                    "interfaceid": "199",
                    "hostid": "11085",
                    "main": "1",
                    "type": "0",
                    "useip": "1",
                    "ip": "127.0.0.12",
                    "dns": "localhost",
                    "port": "10053",
                    "available": "0",
                    "error": "",
                    "errors_from": "0",
                    "disable_until": "0",
                    "details": []
                }]}

            return [proxy_data]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            # Check simple get proxy data
            self.mock_module_functions.params = {}
            proxy = self.module.Proxy(self.mock_module_functions)

            result = proxy.get_zabbix_proxy('11085')
            self.assertNotEqual(result.get('interface'), None)
            self.assertEqual(len(result.get('interface', [])), 1)

    def test_get_zabbix_proxy_error(self):
        """
        Testing the function of getting data by proxy from Zabbix
        with error during request.

        Expected result: Exception.
        """

        def mock_send_request(self, method, params):
            raise Exception

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request):

            proxy = self.module.Proxy(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                proxy.get_zabbix_proxy('4')
            self.assertIn(
                'Failed to get existing proxy:',
                ansible_result.exception.args[0]['msg'])
