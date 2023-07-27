#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import uuid
from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_host
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleExitJson, AnsibleFailJson, TestModules, set_module_args, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of the API is returned.
    """
    return '6.0.18'


class TestUpdating(TestModules):
    """Class for testing the update of the host"""
    module = zabbix_host

    def test_update_host_wo_parameters(self):
        """
        Testing the host update function without additional parameters.

        Expected result: the task has been changed and the host
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'host.get':
                return [{
                    "hostid": "2",
                    "proxy_hostid": "0",
                    "host": "test_host",
                    "status": "0",
                    "lastaccess": "0",
                    "ipmi_authtype": "-1",
                    "ipmi_privilege": "2",
                    "ipmi_username": "",
                    "ipmi_password": "",
                    "maintenanceid": "0",
                    "maintenance_status": "0",
                    "maintenance_type": "0",
                    "maintenance_from": "0",
                    "name": "test_host",
                    "flags": "0",
                    "templateid": "0",
                    "description": "",
                    "tls_connect": "1",
                    "tls_accept": "1",
                    "tls_issuer": "",
                    "tls_subject": "",
                    "proxy_address": "",
                    "auto_compress": "1",
                    "custom_interfaces": "0",
                    "uuid": "",
                    "inventory_mode": "-1",
                    "macros": [],
                    "groups": [
                        {
                            "groupid": "2",
                            "name": "Linux servers"
                        }
                    ],
                    "parentTemplates": [],
                    "items": [],
                    "tags": [],
                    "inventory": [],
                    "interfaces": []}]
            return True

        def mock_find_zabbix_host_by_host(self, host_name):
            return [{'name': 'test_host', 'host': 'test_host', 'hostid': '2'}]

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{"groupid": "20", "name": "Linux"}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'present',
            'host': zabbix_host,
            'hostgroups': ['Linux']})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host,
                find_zabbix_hostgroups_by_names=mock_find_zabbix_hostgroups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated host: {0}'.format(zabbix_host))

    def test_update_host_no_need_update(self):
        """
        Testing the host update function in case nothing needs to be updated.

        Expected result: the task has not been changed and the host
        has not been updated.
        """
        def mock_send_request(self, method, params):
            if method == 'host.get':
                return [{
                    "hostid": "2",
                    "proxy_hostid": "0",
                    "host": "test_host",
                    "status": "0",
                    "lastaccess": "0",
                    "ipmi_authtype": "-1",
                    "ipmi_privilege": "2",
                    "ipmi_username": "",
                    "ipmi_password": "",
                    "maintenanceid": "0",
                    "maintenance_status": "0",
                    "maintenance_type": "0",
                    "maintenance_from": "0",
                    "name": "test_host",
                    "flags": "0",
                    "templateid": "0",
                    "description": "",
                    "tls_connect": "1",
                    "tls_accept": "1",
                    "tls_issuer": "",
                    "tls_subject": "",
                    "proxy_address": "",
                    "auto_compress": "1",
                    "custom_interfaces": "0",
                    "uuid": "",
                    "inventory_mode": "-1",
                    "macros": [],
                    "groups": [
                        {
                            "groupid": "2",
                            "name": "Linux servers"
                        }
                    ],
                    "parentTemplates": [],
                    "items": [],
                    "tags": [],
                    "inventory": [],
                    "interfaces": []}]
            return True

        def mock_find_zabbix_host_by_host(self, host_name):
            return [{'name': 'test_host', 'host': 'test_host', 'hostid': '2'}]

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{"groupid": "2", "name": "Linux servers"}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'present',
            'host': zabbix_host,
            'hostgroups': ['Linux servers']})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host,
                find_zabbix_hostgroups_by_names=mock_find_zabbix_hostgroups_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'No need to update host: {0}'.format(zabbix_host))

    def test_update_host_w_all_parameters(self):
        """
        Testing the host update function with all possible options.

        Expected result: the task has been changed and the host
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            if method == 'host.get':
                return [{
                    "hostid": "2",
                    "proxy_hostid": "0",
                    "host": "test_host",
                    "status": "0",
                    "lastaccess": "0",
                    "ipmi_authtype": "-1",
                    "ipmi_privilege": "2",
                    "ipmi_username": "",
                    "ipmi_password": "",
                    "maintenanceid": "0",
                    "maintenance_status": "0",
                    "maintenance_type": "0",
                    "maintenance_from": "0",
                    "name": "test_host",
                    "flags": "0",
                    "templateid": "0",
                    "description": "",
                    "tls_connect": "1",
                    "tls_accept": "1",
                    "tls_issuer": "",
                    "tls_subject": "",
                    "proxy_address": "",
                    "auto_compress": "1",
                    "custom_interfaces": "0",
                    "uuid": "",
                    "inventory_mode": "-1",
                    "macros": [],
                    "groups": [
                        {
                            "groupid": "2",
                            "name": "Linux servers"
                        }
                    ],
                    "parentTemplates": [],
                    "items": [],
                    "tags": [],
                    "inventory": [],
                    "interfaces": []}]
            return True

        def mock_find_zabbix_host_by_host(self, host_name):
            return [{'name': 'test_host', 'host': 'test_host', 'hostid': '2'}]

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{"groupid": "20", "name": "Linux"}]

        def mock_find_zabbix_templates_by_names(self, hostgroup_names):
            return [{"templateid": "2", "name": "Basic Linux"}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'present',
            'host': zabbix_host,
            'hostgroups': ['Linux'],
            'templates': ['Basic Linux'],
            'status': 'enabled',
            'description': 'Example host',
            'name': 'Test host',
            'tags': [{'tag': 'scope', 'value': 'test'}],
            'macros': [
                {'macro': 'TEST_MACRO',
                 'value': 'example',
                 'description': 'Description of example macros',
                 'type': 'text'}],
            'ipmi_authtype': 'default',
            'ipmi_privilege': 'user',
            'ipmi_username': 'admin',
            'ipmi_password': 'test_pwd',
            'tls_accept': ['unencrypted', 'psk', 'cert'],
            'tls_psk_identity': 'my_example_identity',
            'tls_psk': uuid.uuid4().hex,
            'tls_issuer': 'Example Issuer',
            'tls_subject': 'Example Subject',
            'tls_connect': 'psk',
            'inventory_mode': 'automatic',
            'inventory': {
                'type': '',
                'serialno_b': 'example value'},
            'interfaces': [
                {'type': 'agent'},
                {'type': 'ipmi'},
                {'type': 'jmx', 'ip': '192.168.100.51', 'dns': 'test.com',
                    'useip': True, 'port': '23456'},
                {'type': 'snmp', 'ip': '192.168.100.51', 'dns': 'switch.local',
                    'useip': False, 'port': '164', 'details': {
                        'version': '3', 'bulk': True, 'max_repetitions': None, 'contextname': 'contextname',
                        'securityname': 'securityname', 'securitylevel': 'authPriv', 'authprotocol': 'md5', 'authpassphrase': 'authpassphrase',
                        'privprotocol': 'des', 'privpassphrase': 'privpassphrase'}}]})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host,
                find_zabbix_hostgroups_by_names=mock_find_zabbix_hostgroups_by_names,
                find_zabbix_templates_by_names=mock_find_zabbix_templates_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["changed"])
            self.assertEqual(
                ansible_result.exception.args[0]["result"],
                'Successfully updated host: {0}'.format(zabbix_host))

    def test_update_host_error(self):
        """
        Testing the host update function in case of encountering an error
        during the update.

        Expected result: the task has been failed.
        """
        def mock_send_request(self, method, params):
            if method == 'host.get':
                return [{
                    "hostid": "2",
                    "proxy_hostid": "0",
                    "host": "test_host",
                    "status": "0",
                    "lastaccess": "0",
                    "ipmi_authtype": "-1",
                    "ipmi_privilege": "2",
                    "ipmi_username": "",
                    "ipmi_password": "",
                    "maintenanceid": "0",
                    "maintenance_status": "0",
                    "maintenance_type": "0",
                    "maintenance_from": "0",
                    "name": "test_host",
                    "flags": "0",
                    "templateid": "0",
                    "description": "",
                    "tls_connect": "1",
                    "tls_accept": "1",
                    "tls_issuer": "",
                    "tls_subject": "",
                    "proxy_address": "",
                    "auto_compress": "1",
                    "custom_interfaces": "0",
                    "uuid": "",
                    "inventory_mode": "-1",
                    "macros": [],
                    "groups": [
                        {
                            "groupid": "2",
                            "name": "Linux servers"
                        }
                    ],
                    "parentTemplates": [],
                    "items": [],
                    "tags": [],
                    "inventory": [],
                    "interfaces": []}]
            raise Exception

        def mock_find_zabbix_host_by_host(self, host_name):
            return [{'name': 'test_host', 'host': 'test_host', 'hostid': '2'}]

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{"groupid": "20", "name": "Linux"}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'present',
            'host': zabbix_host,
            'hostgroups': ['Linux']})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host,
                find_zabbix_hostgroups_by_names=mock_find_zabbix_hostgroups_by_names):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]["failed"])
            self.assertEqual(
                ansible_result.exception.args[0]["msg"],
                'Failed to update host: {0}'.format(zabbix_host))
