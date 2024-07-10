#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_host
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of API is returned.
    """
    return '6.0.18'


class TestMacro(TestModules):
    module = zabbix_host

    def test_check_macro_name(self):
        """
        Testing the conversion of macro names. This test verifies the
        functionality of the function on all valid cases.

        Expected result: all macros from the list have been successfully
        converted to the standard format.
        """
        test_cases = [
            'test', '{test', '$test', '{$test',
            'test}', '$test}', '{test}', 'TEST']

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):
            host = self.module.Host(self.mock_module_functions)
            for each in test_cases:
                result = host.check_macro_name(each)
                self.assertEqual(result, '{$TEST}')

    def test_check_macro_name_error(self):
        """
        Test the conversion of macro names. This test verifies the
        functionality of the function on invalid cases.

        Expected result: an exception should be raised when a space is found
        in a macro name.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):
            host = self.module.Host(self.mock_module_functions)
            with self.assertRaises(AnsibleFailJson):
                host.check_macro_name('test test')
