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


class TestDeleting(TestModules):
    """Class for testing proxy deletion"""
    module = zabbix_proxy

    def test_delete_not_exist_proxy(self):
        """
        Testing proxy deletion function in case specified proxy
        does not exist.

        Expected result: task has not been changed and proxy
        has not been deleted.
        """

        def find_zabbix_proxy_by_names(self, proxy_name):
            return []

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'absent',
            'name': zabbix_proxy})

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version,
                find_zabbix_proxy_by_names=find_zabbix_proxy_by_names):

            with self.assertRaises(AnsibleExitJson) as ansible_result:
                self.module.main()
            self.assertFalse(ansible_result.exception.args[0]['changed'])
            self.assertEqual(
                ansible_result.exception.args[0]['result'],
                'No need to delete proxy: {0}'.format(zabbix_proxy))

    def test_deleting_proxy(self):
        """
        Testing proxy deletion function if specified proxy exists.

        Expected result: task has been changed and proxy
        has been updated successfully.
        """

        def mock_send_request(self, method, params):
            return True

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'absent',
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
                'Successfully delete proxy: {0}'.format(zabbix_proxy))

    def test_deleting_proxy_error(self):
        """
        Testing proxy deletion function in case of encountering error
        during deletion.

        Expected result: task has been failed.
        """

        def mock_send_request(self, method, params):
            raise Exception

        def find_zabbix_proxy_by_names(self, proxy_name):
            return [{'name': proxy_name, 'proxyid': '4'}]

        zabbix_proxy = 'test_proxy'
        set_module_args({
            'state': 'absent',
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
                'Failed to delete proxy: {0}'.format(zabbix_proxy))
