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
    it doesn't matter which version of API is returned.
    """
    return '6.0.18'


class TestWOProcessing(TestModules):
    """
    Class for testing the comparison function for parameters that
    do not require preprocessing
    """
    module = zabbix_host

    def test_param_wo_processing(self):
        """
        Checking the parameters that should be added without transformations.
        Test cases:
        1. New parameters not specified. No need to update.
        2. New parameters specified. Need to update.
        3. The newly specified parameters correspond to the current ones.
        No need to update.
        4. New parameters are empty. Need to update to an empty value.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host'},
                'exist': {
                    'host': 'test_host', 'status': 'enabled',
                    'description': '', 'ipmi_authtype': '-1',
                    'proxy_hostid': '0', 'ipmi_privilege': '2',
                    'ipmi_username': 'user', 'ipmi_password': 'pwd',
                    'inventory_mode': '1', 'tls_accept': '1',
                    'tls_psk_identity': 'psk_identity', 'tls_psk': 'tls_psk',
                    'tls_issuer': 'tls_issuer', 'tls_subject': 'tls_subject',
                    'tls_connect': '1'},
                'expected': {}
            },
            {
                'new': {
                    'host': 'test_host', 'status': 'disabled',
                    'description': 'test', 'ipmi_authtype': '1',
                    'proxy_hostid': '1', 'ipmi_privilege': '3',
                    'ipmi_username': 'test_user', 'ipmi_password': 'test_pwd',
                    'inventory_mode': '0', 'tls_accept': '4',
                    'tls_psk_identity': 'test_identity', 'tls_psk': 'test_psk',
                    'tls_issuer': 'test_issuer', 'tls_subject': 'test_subject',
                    'tls_connect': '2'},
                'exist': {
                    'host': 'test_host', 'status': 'enabled',
                    'description': '', 'ipmi_authtype': '0',
                    'proxy_hostid': '0', 'ipmi_privilege': '2',
                    'ipmi_username': 'user', 'ipmi_password': 'pwd',
                    'inventory_mode': '1', 'tls_accept': '1',
                    'tls_psk_identity': 'psk_identity', 'tls_psk': 'tls_psk',
                    'tls_issuer': 'tls_issuer', 'tls_subject': 'tls_subject',
                    'tls_connect': '1'},
                'expected': {
                    'status': 'disabled',
                    'description': 'test', 'ipmi_authtype': '1',
                    'proxy_hostid': '1', 'ipmi_privilege': '3',
                    'ipmi_username': 'test_user', 'ipmi_password': 'test_pwd',
                    'inventory_mode': '0', 'tls_accept': '4',
                    'tls_psk_identity': 'test_identity', 'tls_psk': 'test_psk',
                    'tls_issuer': 'test_issuer', 'tls_subject': 'test_subject',
                    'tls_connect': '2'}
            },
            {
                'new': {
                    'host': 'test_host', 'status': 'enabled',
                    'description': '', 'ipmi_authtype': '0',
                    'proxy_hostid': '0', 'ipmi_privilege': '2',
                    'ipmi_username': 'user', 'ipmi_password': 'pwd',
                    'inventory_mode': '1', 'tls_accept': '1',
                    'tls_psk_identity': 'psk_identity', 'tls_psk': 'tls_psk',
                    'tls_issuer': 'tls_issuer', 'tls_subject': 'tls_subject',
                    'tls_connect': '1'},
                'exist': {
                    'host': 'test_host', 'status': 'enabled',
                    'description': '', 'ipmi_authtype': '0',
                    'proxy_hostid': '0', 'ipmi_privilege': '2',
                    'ipmi_username': 'user', 'ipmi_password': 'pwd',
                    'inventory_mode': '1', 'tls_accept': '1',
                    'tls_psk_identity': 'psk_identity', 'tls_psk': 'tls_psk',
                    'tls_issuer': 'tls_issuer', 'tls_subject': 'tls_subject',
                    'tls_connect': '1'},
                'expected': {}
            },
            {
                'new': {
                    'host': 'test_host', 'status': 'enabled',
                    'description': '', 'ipmi_authtype': '0',
                    'proxy_hostid': '0', 'ipmi_privilege': '2',
                    'ipmi_username': '', 'ipmi_password': '',
                    'inventory_mode': '0', 'tls_accept': '1',
                    'tls_psk_identity': '', 'tls_psk': '',
                    'tls_issuer': '', 'tls_subject': '',
                    'tls_connect': '1'},
                'exist': {
                    'host': 'test_host', 'status': 'disabled',
                    'description': 'test', 'ipmi_authtype': '1',
                    'proxy_hostid': '1', 'ipmi_privilege': '3',
                    'ipmi_username': 'user', 'ipmi_password': 'pwd',
                    'inventory_mode': '1', 'tls_accept': '4',
                    'tls_psk_identity': 'psk_identity', 'tls_psk': 'tls_psk',
                    'tls_issuer': 'tls_issuer', 'tls_subject': 'tls_subject',
                    'tls_connect': '4'},
                'expected': {
                    'status': 'enabled',
                    'description': '', 'ipmi_authtype': '0',
                    'proxy_hostid': '0', 'ipmi_privilege': '2',
                    'ipmi_username': '', 'ipmi_password': '',
                    'inventory_mode': '0', 'tls_accept': '1',
                    'tls_psk_identity': '', 'tls_psk': '',
                    'tls_issuer': '', 'tls_subject': '',
                    'tls_connect': '1'}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])
                self.assertEqual(result, case['expected'])


class TestGroups(TestModules):
    """Class for testing the comparison function for groups parameter"""
    module = zabbix_host

    def test_groups(self):
        """
        Testing the groups parameter.
        Test cases:
        1. Groups are equals.
        2. New group to add.
        3. One group to remove.
        4. Change one group.
        5. Change all groups.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'groups': [{'groupid': '10', 'name': 'test'}]},
                'exist': {
                    'host': 'test_host',
                    'groups': [{'groupid': '10', 'name': 'test'}]},
                'expected': {}
            },
            {
                'new': {'host': 'test_host',
                        'groups': [
                            {'groupid': '10', 'name': 'test'},
                            {'groupid': '12', 'name': 'test2'}]},
                'exist': {
                    'host': 'test_host',
                    'groups': [
                        {'groupid': '10', 'name': 'test'}]},
                'expected': {
                    'groups': [
                        {'groupid': '10', 'name': 'test'},
                        {'groupid': '12', 'name': 'test2'}]}
            },
            {
                'new': {'host': 'test_host',
                        'groups': [
                            {'groupid': '10', 'name': 'test'}]},
                'exist': {
                    'host': 'test_host',
                    'groups': [
                        {'groupid': '10', 'name': 'test'},
                        {'groupid': '12', 'name': 'test2'}]},
                'expected': {
                    'groups': [{'groupid': '10', 'name': 'test'}]}
            },
            {
                'new': {'host': 'test_host',
                        'groups': [
                            {'groupid': '10', 'name': 'test'},
                            {'groupid': '14', 'name': 'test3'}]},
                'exist': {
                    'host': 'test_host',
                    'groups': [
                        {'groupid': '10', 'name': 'test'},
                        {'groupid': '12', 'name': 'test2'}]},
                'expected': {
                    'groups': [
                        {'groupid': '10', 'name': 'test'},
                        {'groupid': '14', 'name': 'test3'}]}
            },
            {
                'new': {'host': 'test_host',
                        'groups': [
                            {'groupid': '15', 'name': 'test4'},
                            {'groupid': '16', 'name': 'test5'}]},
                'exist': {
                    'host': 'test_host',
                    'groups': [
                        {'groupid': '10', 'name': 'test'},
                        {'groupid': '12', 'name': 'test2'}]},
                'expected': {
                    'groups': [
                        {'groupid': '16', 'name': 'test5'},
                        {'groupid': '15', 'name': 'test4'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                if 'groups' in result:

                    self.assertEqual(
                        len(case['expected']['groups']),
                        len(result['groups']))

                    for group in result['groups']:
                        self.assertIn(group, case['expected']['groups'])
                else:
                    self.assertEqual(result, case['expected'])


class TestTemplates(TestModules):
    """Class for testing the comparison function for template parameter"""
    module = zabbix_host

    def test_adding_templates(self):
        """
        Testing the templates parameter.
        Test cases:
        1. Templates are equals.
        2. New template to add.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'templates': [{'templateid': '10', 'name': 'test'}]},
                'exist': {
                    'host': 'test_host',
                    'parentTemplates': [{'templateid': '10', 'name': 'test'}]},
                'expected': {}
            },
            {
                'new': {'host': 'test_host',
                        'templates': [
                            {'templateid': '10', 'name': 'test'},
                            {'templateid': '12', 'name': 'test2'}]},
                'exist': {
                    'host': 'test_host',
                    'parentTemplates': [
                        {'templateid': '10', 'name': 'test'}]},
                'expected': {
                    'templates': [
                        {'templateid': '10', 'name': 'test'},
                        {'templateid': '12', 'name': 'test2'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                if 'templates' in result:
                    self.assertEqual(
                        len(case['expected']['templates']),
                        len(result['templates']))

                    for group in result['templates']:
                        self.assertIn(group, case['expected']['templates'])
                else:
                    self.assertEqual(result, case['expected'])

    def test_deleting_templates(self):
        """
        Testing the templates parameter.
        Test cases:
        1. One template to remove.
        2. Change one template.
        3. Change all templates.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'templates': [
                            {'templateid': '10', 'name': 'test'}]},
                'exist': {
                    'host': 'test_host',
                    'parentTemplates': [
                        {'templateid': '10', 'name': 'test'},
                        {'templateid': '12', 'name': 'test2'}]},
                'expected': {
                    'templates': [{'templateid': '10', 'name': 'test'}],
                    'templates_clear': [{'templateid': '12'}]}
            },
            {
                'new': {'host': 'test_host',
                        'templates': [
                            {'templateid': '10', 'name': 'test'},
                            {'templateid': '14', 'name': 'test3'}]},
                'exist': {
                    'host': 'test_host',
                    'parentTemplates': [
                        {'templateid': '10', 'name': 'test'},
                        {'templateid': '12', 'name': 'test2'}]},
                'expected': {
                    'templates': [
                        {'templateid': '10', 'name': 'test'},
                        {'templateid': '14', 'name': 'test3'}],
                    'templates_clear': [{'templateid': '12'}]}
            },
            {
                'new': {'host': 'test_host',
                        'templates': [
                            {'templateid': '15', 'name': 'test4'},
                            {'templateid': '16', 'name': 'test5'}]},
                'exist': {
                    'host': 'test_host',
                    'parentTemplates': [
                        {'templateid': '10', 'name': 'test'},
                        {'templateid': '12', 'name': 'test2'}]},
                'expected': {
                    'templates': [
                        {'templateid': '16', 'name': 'test5'},
                        {'templateid': '15', 'name': 'test4'}],
                    'templates_clear': [
                        {'templateid': '10'},
                        {'templateid': '12'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                self.assertEqual(
                    len(case['expected']['templates']),
                    len(result['templates']))

                self.assertEqual(
                    len(case['expected']['templates_clear']),
                    len(result['templates_clear']))

                for template in result['templates']:
                    self.assertIn(template, case['expected']['templates'])
                for cl_template in result['templates_clear']:
                    self.assertIn(cl_template, case['expected']['templates_clear'])


class TestVisibleName(TestModules):
    """Class for testing the comparison function for visible name parameter"""
    module = zabbix_host

    def test_visible_name(self):
        """
        Testing the visible name parameter.
        Test cases:
        1. Visible names are equals.
        2. New visible name.
        3. Empty visible name. Must be technical name.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'name': 'Test host'},
                'exist': {
                    'host': 'test_host',
                    'name': 'Test host'},
                'expected': {}
            },
            {
                'new': {'host': 'test_host',
                        'name': 'New name'},
                'exist': {
                    'host': 'test_host',
                    'name': 'Test host'},
                'expected': {
                    'name': 'New name'}
            },
            {
                'new': {'host': 'test_host',
                        'name': ''},
                'exist': {
                    'host': 'test_host',
                    'name': 'Test host'},
                'expected': {
                    'name': 'test_host'}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])
                self.assertEqual(result, case['expected'])


class TestTags(TestModules):
    """Class for testing the comparison function for tags parameter"""
    module = zabbix_host

    def test_tags(self):
        """
        Testing the tags parameter.
        Test cases:
        1. Tags are equals.
        2. New tag.
        3. New tag in case of empty tags on host.
        4. Remove one tag.
        5. Remove all tags.
        6. Change one tag to other.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'expected': {}
            },
            {
                'new': {'host': 'test_host',
                        'tags': [
                            {'tag': 'test1', 'value': 'test1'},
                            {'tag': 'test2', 'value': ''}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'expected': {
                    'tags': [
                        {'tag': 'test1', 'value': 'test1'},
                        {'tag': 'test2', 'value': ''}]}
            },
            {
                'new': {'host': 'test_host',
                        'tags': [
                            {'tag': 'test1', 'value': 'test1'},
                            {'tag': 'test2', 'value': ''}]},
                'exist': {
                    'host': 'test_host',
                    'tags': []},
                'expected': {
                    'tags': [
                        {'tag': 'test1', 'value': 'test1'},
                        {'tag': 'test2', 'value': ''}]}
            },
            {
                'new': {'host': 'test_host',
                        'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [
                            {'tag': 'test1', 'value': 'test1'},
                            {'tag': 'test2', 'value': ''}]},
                'expected': {
                    'tags': [{'tag': 'test1', 'value': 'test1'}]}
            },
            {
                'new': {'host': 'test_host',
                        'tags': []},
                'exist': {
                    'host': 'test_host',
                    'tags': [
                            {'tag': 'test1', 'value': 'test1'},
                            {'tag': 'test2', 'value': ''}]},
                'expected': {
                    'tags': []}
            },
            {
                'new': {'host': 'test_host',
                        'tags': [
                            {'tag': 'test1', 'value': 'test1'},
                            {'tag': 'test3', 'value': 'test3'}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [
                            {'tag': 'test1', 'value': 'test1'},
                            {'tag': 'test2', 'value': ''}]},
                'expected': {
                    'tags': [
                        {'tag': 'test1', 'value': 'test1'},
                        {'tag': 'test3', 'value': 'test3'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                if 'tags' in result:
                    self.assertEqual(
                        len(case['expected']['tags']),
                        len(result['tags']))

                    for tag in result['tags']:
                        self.assertIn(tag, case['expected']['tags'])
                else:
                    self.assertEqual(result, case['expected'])

    def test_tag_changes(self):
        """
        Testing the tags parameter.
        Test cases:
        1. Change value.
        2. Clear value.
        3. Change name.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'tags': [{'tag': 'test1', 'value': 'test2'}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'expected': {
                    'tags': [{'tag': 'test1', 'value': 'test2'}]}
            },
            {
                'new': {'host': 'test_host',
                        'tags': [{'tag': 'test1', 'value': ''}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'expected': {
                    'tags': [{'tag': 'test1', 'value': ''}]}
            },
            {
                'new': {'host': 'test_host',
                        'tags': [{'tag': 'test2', 'value': 'test1'}]},
                'exist': {
                    'host': 'test_host',
                    'tags': [{'tag': 'test1', 'value': 'test1'}]},
                'expected': {
                    'tags': [{'tag': 'test2', 'value': 'test1'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                self.assertEqual(
                    len(case['expected']['tags']),
                    len(result['tags']))

                for tag in result['tags']:
                    self.assertIn(tag, case['expected']['tags'])


class TestMacros(TestModules):
    """Class for testing the comparison function for macros parameter"""
    module = zabbix_host

    def test_macros(self):
        """
        Testing the macros parameter.
        Test cases:
        1. Macros are equals.
        2. New macro.
        3. New macro in case of empty macros on host.
        4. Remove one macro.
        5. Remove all macros.
        6. Change one macro to other.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'},
                            {'macro': '{$TEST2}',
                             'value': 'test2',
                             'type': '1',
                             'description': 'description2'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                        {'macro': '{$TEST1}',
                         'value': 'test1',
                         'type': '0',
                         'description': 'description'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'},
                            {'macro': '{$TEST2}',
                             'value': 'test2',
                             'type': '1',
                             'description': 'description2'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': []},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'},
                            {'macro': '{$TEST2}',
                             'value': 'test2',
                             'type': '1',
                             'description': 'description2'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': []},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {'macros': []}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'},
                            {'macro': '{$TEST3}',
                             'value': 'test3',
                             'type': '1',
                             'description': 'description3'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'},
                            {'macro': '{$TEST2}',
                             'value': 'test2',
                             'type': '1',
                             'description': 'description2'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'},
                            {'macro': '{$TEST3}',
                             'value': 'test3',
                             'type': '1',
                             'description': 'description3'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                if 'macros' in result:
                    self.assertEqual(
                        len(case['expected']['macros']),
                        len(result['macros']))

                    for macro in result['macros']:
                        self.assertIn(macro, case['expected']['macros'])
                else:
                    self.assertEqual(result, case['expected'])

    def test_macros_changes(self):
        """
        Testing the macros parameter.
        Test cases:
        1. Change value.
        2. Change type.
        3. Change description.
        4. Clear value.
        5. Clear description.
        6. Change value in case of secret macros (existing macro value is empty).

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test2',
                             'type': '0',
                             'description': 'description'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test2',
                             'type': '0',
                             'description': 'description'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '1',
                             'description': 'description'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '1',
                             'description': 'description'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description_NEW'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description_NEW'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': '',
                             'type': '0',
                             'description': 'description'}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': '',
                             'type': '0',
                             'description': 'description'}]}
            },
            {
                'new': {'host': 'test_host',
                        'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': ''}]},
                'exist': {
                    'host': 'test_host',
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': 'description'}]},
                'expected': {
                    'macros': [
                            {'macro': '{$TEST1}',
                             'value': 'test1',
                             'type': '0',
                             'description': ''}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                self.assertEqual(
                    len(case['expected']['macros']),
                    len(result['macros']))

                for macro in result['macros']:
                    self.assertIn(macro, case['expected']['macros'])


class TestInterfaces(TestModules):
    """Class for testing the comparison function for interfaces parameter"""
    module = zabbix_host

    def test_interface_count(self):
        """
        Testing the interface count on existing hosts.
        Test cases:
        1. One interface exists.
        2. One interface of each type exist.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [{'type': '1'}]},
                'expected': {'interfaces': []}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1'},
                        {'type': '2'},
                        {'type': '3'},
                        {'type': '4'}]},
                'expected': {'interfaces': []}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])
                self.assertEqual(result, case['expected'])

    def test_interface_count_exception(self):
        """
        Testing the interface count in case of several interfaces of some
        type.
        Test cases:
        1. Two agent interfaces exist.
        2. Two SNMP interfaces exist.
        3. Two IPMI interfaces exist.
        4. Two JMX interfaces exist.
        5. One agent and two JMX interfaces exist.

        Expected result: an exception with an error message.
        """
        test_cases = [
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1'},
                        {'type': '1'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2'},
                        {'type': '2'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '3'},
                        {'type': '3'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '4'},
                        {'type': '4'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1'},
                        {'type': '4'},
                        {'type': '4'}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                with self.assertRaises(AnsibleFailJson) as ansible_result:
                    host.compare_zabbix_host(
                        case['exist'],
                        case['new'])
                self.assertTrue(ansible_result.exception.args[0]['failed'])
                self.assertIn(
                    'Module supports only 1 interface of each type. Please resolve conflict manually.',
                    ansible_result.exception.args[0]['msg'])

    def test_interface(self):
        """
        Testing operations with interfaces.
        Test cases:
        1. Add new interface.
        2. Add another interface.
        3. Change one interface when one interface exists.
        4. Change one interface when two interfaces exist.
        5. Delete one interface when two interfaces exist.
        6. Clear all interfaces.


        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': []},
                'expected': {
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'},
                        {'type': '3', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'interfaceid': '1000', 'useip': '0',
                         'port': '10051', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'}]},
                'expected': {
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1', 'interfaceid': '1000'},
                        {'type': '3', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'interfaceid': '1000', 'useip': '0',
                         'port': '10051', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'}]},
                'expected': {
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1', 'interfaceid': '1000'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'},
                        {'type': '3', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '650', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'interfaceid': '1000', 'useip': '0',
                         'port': '10051', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'},
                        {'type': '3', 'interfaceid': '1001', 'useip': '0',
                         'port': '650', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'}]},
                'expected': {
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1', 'interfaceid': '1000'},
                        {'type': '3', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '650', 'dns': 'test_agent.com',
                         'details': [], 'main': '1', 'interfaceid': '1001'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1'}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'interfaceid': '1000', 'useip': '0',
                         'port': '10051', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'},
                        {'type': '3', 'interfaceid': '1001', 'useip': '0',
                         'port': '650', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'}]},
                'expected': {
                    'interfaces': [
                        {'type': '1', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '10051', 'dns': 'test_agent.com',
                         'details': [], 'main': '1', 'interfaceid': '1000'}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': []},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '1', 'interfaceid': '1000', 'useip': '0',
                         'port': '10051', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'},
                        {'type': '3', 'interfaceid': '1001', 'useip': '0',
                         'port': '650', 'dns': 'test_agent.com',
                         'ip': '127.0.0.1', 'details': [], 'main': '1'}]},
                'expected': {
                    'interfaces': []}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                self.assertEqual(
                    len(case['expected']['interfaces']),
                    len(result['interfaces']))

                if 'interfaces' in result:
                    for interface in result['interfaces']:
                        self.assertIn(interface, case['expected']['interfaces'])
                else:
                    self.assertEqual(result, case['expected'])

    def test_interface_snmp(self):
        """
        Testing operations with SNMP interfaces.
        Test cases:
        1. Interfaces are equals.
        2. Interfaces are equals but in a different order.
        3. Add one SNMP interface.
        4. Change parameter of SNMP interface.
        5. Change details of SNMP interface.
        6. Change parameters and details of SNMP interfaces.

        Expected result: all test cases run successfully.
        """
        test_cases = [
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details': {
                            'version': '3', 'bulk': False,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details': {
                            'version': '3', 'bulk': False,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'expected': {}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details': {
                            'version': '3', 'bulk': False,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details': {
                            'bulk': False, 'version': '3',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'privpassphrase': 'privpassphrase'}}]},
                'expected': {}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details': {
                            'version': '3', 'bulk': False,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': []},
                'expected': {
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details':
                            {'contextname': 'contextname',
                             'securityname': 'securityname',
                             'version': '3', 'bulk': False,
                             'securitylevel': 'authPriv',
                             'authpassphrase': 'authpassphrase',
                             'privpassphrase': 'privpassphrase'}}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details': {
                            'version': '3', 'bulk': False,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details': {
                            'bulk': False, 'version': '3',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'privpassphrase': 'privpassphrase'}}]},
                'expected': {
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details':
                            {'bulk': False, 'version': '3',
                             'securitylevel': 'authPriv',
                             'authpassphrase': 'authpassphrase',
                             'contextname': 'contextname',
                             'securityname': 'securityname',
                             'privpassphrase': 'privpassphrase'}}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details': {
                            'version': '3', 'bulk': True,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details': {
                            'bulk': False, 'version': '3',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'privpassphrase': 'privpassphrase'}}]},
                'expected': {
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details':
                            {'bulk': True, 'version': '3',
                             'securitylevel': 'authPriv',
                             'authpassphrase': 'authpassphrase',
                             'contextname': 'contextname',
                             'securityname': 'securityname',
                             'privpassphrase': 'privpassphrase'}}]}
            },
            {
                'new': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'details': {
                            'version': '3', 'bulk': True,
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'privpassphrase': 'privpassphrase'}}]},
                'exist': {
                    'host': 'test_host',
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '127.0.0.1',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details': {
                            'bulk': False, 'version': '3',
                            'securitylevel': 'authPriv',
                            'authpassphrase': 'authpassphrase',
                            'contextname': 'contextname',
                            'securityname': 'securityname',
                            'privpassphrase': 'privpassphrase'}}]},
                'expected': {
                    'interfaces': [
                        {'type': '2', 'useip': '0', 'ip': '10.10.10.10',
                         'port': '161', 'dns': 'test_agent.com', 'main': '1',
                         'interfaceid': '1000', 'details':
                            {'bulk': True, 'version': '3',
                             'securitylevel': 'authPriv',
                             'authpassphrase': 'authpassphrase',
                             'contextname': 'contextname',
                             'securityname': 'securityname',
                             'privpassphrase': 'privpassphrase'}}]}
            }
        ]

        with patch.multiple(
                self.zabbix_api_module_path,
                api_version=mock_api_version):

            for case in test_cases:
                host = self.module.Host(self.mock_module_functions)

                result = host.compare_zabbix_host(
                    case['exist'], case['new'])

                if 'interfaces' in result:
                    self.assertEqual(
                        len(case['expected']['interfaces']),
                        len(result['interfaces']))

                    for interface in result['interfaces']:
                        self.assertIn(interface, case['expected']['interfaces'])
                else:
                    self.assertEqual(result, case['expected'])
