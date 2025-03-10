#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy_group
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    TestModules, patch)


def mock_api_version_70(self):
    """
    Mock function to get Zabbix API version 7.0.
    """
    return '7.0.0'


class TestWOProcessing(TestModules):
    """Class for testing parameter comparison without processing"""
    module = zabbix_proxy_group

    def test_params_wo_processing(self):
        """
        Testing comparison of all parameters.

        Expected result: all parameters will be added to correct output field.
        """
        exist_proxy_group = {
            "proxy_groupid": "4",
            "name": "test_proxy_group",
            "failover_delay": "1m",
            "min_online": "2",
            "description": "description of proxy group"}

        test_cases = [
            {
                'number': 1,
                'input': {'failover_delay': '2m'},
                'exist_proxy_group': exist_proxy_group,
                'expected': {'failover_delay': '2m'}
            },
            {
                'number': 2,
                'input': {'min_online': '10'},
                'exist_proxy_group': exist_proxy_group,
                'expected': {'min_online': '10'}
            },
            {
                'number': 3,
                'input': {'description': 'new description'},
                'exist_proxy_group': exist_proxy_group,
                'expected': {'description': 'new description'}
            },
            {
                'number': 4,
                'input': {'description': 'new description', 'min_online': '10', 'failover_delay': '2m'},
                'exist_proxy_group': exist_proxy_group,
                'expected': {'description': 'new description', 'failover_delay': '2m', 'min_online': '10'}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            for case in test_cases:
                input_param = {
                    'state': 'present',
                    'name': 'test_proxy_group'}
                input_param.update(case['input'])
                self.mock_module_functions.params = input_param
                proxy_group = self.module.Proxy_group(self.mock_module_functions)

                result = proxy_group.compare_zabbix_proxy_group(
                    exist_proxy_group=case['exist_proxy_group'],
                    new_proxy_group=case['input'])
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))
