#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_host
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    AnsibleFailJson, TestModules, patch)


def mock_api_version(self):
    """
    Mock function to get Zabbix API version. In this case,
    it doesn't matter which version of the API is returned.
    """
    return '6.0.18'


class TestCheckElements(TestModules):
    module = zabbix_host

    def test_check_elements(self):
        """
        Testing the function of checking the presence of the required elements
        in the resulting list.

        Expected result: all executions of the function return True.
        """
        test_cases_success = [
            {'require': ['first'], 'exist': ['first']},
            {'require': ['first'], 'exist': ['first', 'two']},
            {'require': ['first', 'two'], 'exist': ['first', 'two']},
            {'require': ['two', 'first'], 'exist': ['first', 'two']},
            {'require': ['first', 'two'], 'exist': ['two', 'first']},
            {'require': [''], 'exist': ['']}]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):
            host = self.module.Host(self.mock_module_functions)

            for each in test_cases_success:
                result = host.check_elements(each['require'], each['exist'])
                self.assertEqual(result, True)

    def test_check_elements_error(self):
        """
        Testing the function of checking the presence of the required
        elements in the received list in case any elements are not present in
        the received list.

        Expected result: all executions of the function return False.
        """
        test_cases = [
            {'require': ['first'], 'exist': ['']},
            {'require': ['first', 'two'], 'exist': ['first']},
            {'require': ['first', 'two'], 'exist': ['first', 'third']},
            {'require': ['two', 'first'], 'exist': ['first', 'third']}]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):
            host = self.module.Host(self.mock_module_functions)

            with self.assertRaises(AnsibleFailJson):
                for each in test_cases:
                    host.check_elements(each['require'], each['exist'])
