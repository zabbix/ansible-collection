#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_host
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleExitJson, AnsibleFailJson, TestModules, set_module_args, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of the API is returned.
    """
    return '6.0.18'


class TestDeleting(TestModules):
    """Class for testing the delete of the host"""
    module = zabbix_host

    def test_delete_not_exist_host(self):
        """
        Testing the delete host function in case the specified host
        does not exist.

        Expected result: the task has not been changed and the host
        has not been deleted.
        """
        def mock_find_zabbix_host_by_host(self, host_name):
            return []

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'absent',
            'host': zabbix_host})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No need to delete host: {0}'.format(zabbix_host))

    def test_deleting_host(self):
        """
        Testing the delete host function if the specified host exists.

        Expected result: the task has been changed and the host
        has been updated successfully.
        """
        def mock_send_request(self, method, params):
            return True

        def mock_find_zabbix_host_by_host(self, host_name):
            return [{'name': 'test_host', 'host': 'test_host', 'hostid': '2'}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'absent',
            'host': zabbix_host})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'Successfully delete host: {0}'.format(zabbix_host))

    def test_deleting_host_error(self):
        """
        Testing the delete host function in case of encountering an error
        during the deletion.

        Expected result: the task has been failed.
        """
        def mock_send_request(self, method, params):
            raise Exception

        def mock_find_zabbix_host_by_host(self, host_name):
            return [{'name': 'test_host', 'host': 'test_host', 'hostid': '2'}]

        zabbix_host = 'test_host'
        set_module_args({
            'state': 'absent',
            'host': zabbix_host})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                send_api_request=mock_send_request,
                find_zabbix_host_by_host=mock_find_zabbix_host_by_host):

            with self.assertRaises(AnsibleFailJson) as ansible_result:
                self.module.main()
            self.assertTrue(ansible_result.exception.args[0]['failed'])
            self.assertEqual(
                ansible_result.exception.args[0]['msg'],
                'Failed to delete host: {0}'.format(zabbix_host))
