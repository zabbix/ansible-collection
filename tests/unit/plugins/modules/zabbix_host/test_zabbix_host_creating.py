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


class TestCreating(TestModules):
    """Class for testing the create of the host"""
    module = zabbix_host

    def test_create_host_wo_parameters(self):
        """
        Testing the host create function without additional parameters.

        Expected result: the task has been changed and the host
        has been created successfully.
        """
        def mock_send_request(self, method, params):
            return True

        def mock_find_zabbix_host_by_host(self, host_name):
            return []

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{'groupid': '2', 'name': 'Linux servers'}]

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
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created host: {0}'.format(zabbix_host))

    def test_create_host_w_all_parameters(self):
        """
        Testing the host create function with all possible options.

        Expected result: the task has been changed and the host
        has been created successfully.
        """
        def mock_send_request(self, method, params):
            return True

        def mock_find_zabbix_host_by_host(self, host_name):
            return []

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{'groupid': '2', 'name': 'Linux servers'}]

        def mock_find_zabbix_templates_by_names(self, hostgroup_names):
            return [{'templateid': '2', 'name': 'Basic Linux'}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'present',
            'host': zabbix_host,
            'hostgroups': ['Linux servers'],
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
            'tls_psk_identity': 'my_example_identy',
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
                     'version': 3, 'contextname': 'contextname',
                     'securityname': 'securityname', 'securitylevel': 'authPriv',
                     'authprotocol': 'md5', 'privprotocol': 'des',
                     'authpassphrase': uuid.uuid4().hex, 'privpassphrase': uuid.uuid4().hex}}]})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host,
                find_zabbix_hostgroups_by_names=mock_find_zabbix_hostgroups_by_names,
                find_zabbix_templates_by_names=mock_find_zabbix_templates_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully created host: {0}'.format(zabbix_host))

    def test_create_host_error(self):
        """
        Testing the host create function in case of encountering an error
        during the creation.

        Expected result: the task has been failed.
        """
        def mock_send_request(self, method, params):
            raise Exception

        def mock_find_zabbix_host_by_host(self, host_name):
            return []

        def mock_find_zabbix_hostgroups_by_names(self, hostgroup_names):
            return [{'groupid': '2', 'name': 'Linux servers'}]

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

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                ansible_result.exception.args[0]['msg'],
                'Failed to create host: {0}'.format(zabbix_host))
