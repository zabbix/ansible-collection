#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.modules import zabbix_proxy_group
from ansible_collections.zabbix.zabbix.tests.unit.plugins.modules.common import (
    TestModules, patch)
from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    default_values)


def mock_api_version_70(self):
    """
    Mock function to get Zabbix API version 7.0.
    """
    return '7.0.0'


class TestProxyGroupName(TestModules):
    """Class for testing name of the proxy group"""
    module = zabbix_proxy_group

    def test_proxy_group_name_param(self):
        """
        Testing proxy group name. Result depends on the Zabbix API version.

        Expected result: name parameter will be added to the correct output field.
        """
        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version_70):

            input_param = {
                'state': 'present',
                'name': 'test_proxy_group'}
            self.mock_module_functions.params = input_param
            proxy = self.module.Proxy_group(self.mock_module_functions)

            result = proxy.generate_zabbix_proxy_group()
            self.assertEqual(result, {'name': 'test_proxy_group'})


class TestProxyGroupDescription(TestModules):
    """Class for testing description of the proxy group"""
    module = zabbix_proxy_group

    def test_proxy_group_description_param(self):
        """
        Testing description parameter.

        Expected result: description parameter will be added
        to the correct output field.

        Test cases:
        1. Empty description field
        2. New description
        """
        test_cases = [
            {
                'number': 1,
                'input': {},
                'expected': {'name': 'test_proxy_group'}},
            {
                'number': 2,
                'input': {'description': 'Description of the proxy group'},
                'expected': {
                    'name': 'test_proxy_group',
                    'description': 'Description of the proxy group'}}
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

                result = proxy_group.generate_zabbix_proxy_group()
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))


class TestProxyGroupFailoverDelay(TestModules):
    """Class for testing fileover delay of the proxy group"""
    module = zabbix_proxy_group

    def test_proxy_group_fileover_delay_param(self):
        """
        Testing fileover delay parameter.

        Expected result: fileover delay parameter will be added
        to the correct output field.

        Test cases:
        1. New fileover delay
        2. Fileover delay == 0 (default falue)
        """
        test_cases = [
            {
                'number': 1,
                'input': {'failover_delay': '2m'},
                'expected': {'name': 'test_proxy_group', 'failover_delay': '2m'}},
            {
                'number': 2,
                'input': {'failover_delay': ''},
                'expected': {
                    'name': 'test_proxy_group',
                    'failover_delay': default_values['proxy_group_failover_delay']}}
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

                result = proxy_group.generate_zabbix_proxy_group()
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))


class TestProxyGroupMinOnline(TestModules):
    """Class for testing min online parameter of the proxy group"""
    module = zabbix_proxy_group

    def test_proxy_group_fileover_delay_param(self):
        """
        Testing min online parameter.

        Expected result: min online parameter will be added
        to the correct output field.

        Test cases:
        1. New min online
        2. min online == 0 (default falue)
        """
        test_cases = [
            {
                'number': 1,
                'input': {'min_online': '2'},
                'expected': {'name': 'test_proxy_group', 'min_online': '2'}},
            {
                'number': 2,
                'input': {'min_online': ''},
                'expected': {
                    'name': 'test_proxy_group',
                    'min_online': default_values['proxy_group_min_online']}}
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

                result = proxy_group.generate_zabbix_proxy_group()
                self.assertEqual(result, case['expected'], 'Error in case number {}'.format(case['number']))
