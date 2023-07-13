#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import sys

if sys.version_info[0] > 2:
    import unittest
    from unittest.mock import patch, MagicMock
else:
    try:
        import unittest2 as unittest
        from mock import patch, MagicMock
    except ImportError:
        print("Error import unittest library for Python 2")

import json
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


def set_module_args(args):
    """Prepare arguments for module"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class for module.exit_json"""
    pass


class AnsibleFailJson(Exception):
    """Exception class for module.fail_json"""
    pass


def exit_json(*args, **kwargs):
    """Function to patch over exit_json"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """Function to patch over fail_json"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class TestModules(unittest.TestCase):
    """General setup function for tests"""
    def setUp(self):
        # Mock connection
        self.mock_connection = patch(
            "ansible_collections.zabbix.zabbix.plugins.module_utils.zabbix_api.Connection")
        self.connection = self.mock_connection.start()
        self.addCleanup(self.mock_connection.stop)

        # Mock module for testing module
        self.mock_module = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

        self.zabbix_api_module_path = "ansible_collections.zabbix.zabbix.plugins.module_utils.zabbix_api.ZabbixApi"

        # Mock module for testing functions
        self.mock_module_functions = MagicMock()
        self.mock_module_functions._socket_path = '/dev/null'
        self.mock_module_functions.fail_json = fail_json
        self.mock_module_functions.exit_json = exit_json
        self.mock_module_functions.start()
        self.addCleanup(self.mock_module_functions.stop)
