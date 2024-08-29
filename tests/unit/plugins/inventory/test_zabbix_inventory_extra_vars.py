#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.inventory.zabbix_inventory import InventoryModule
from ansible.template import Templar
from ansible.parsing.dataloader import DataLoader
from ansible.utils.vars import load_extra_vars
from ansible.errors import AnsibleUndefinedVariable

import sys

if sys.version_info[0] > 2:
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        print("Error import unittest library for Python 2")


class TestExtraVars(unittest.TestCase):

    def test_check_extra_vars_load(self):
        """
        This test checks load and resolve of the extra vars.

        Test cases:
            1. extra_vars - {}
            2. extra_vars - string value
                extra_vars = {'pass': 'test_value'}
            3. extra_vars - number value
                extra_vars = {'pass': 123}
            4. extra_vars - dict value
                extra_vars = {'pass': {'a':123}}
            5. extra_vars - list value
                extra_vars = {'pass': [1, 2, 3]}
            6. extra_vars - string value, template with additional text
                extra_vars = {'pass': 'test_value'}
            7. extra_vars - string value, template with additional text and without spaces
                extra_vars = {'pass': 'test_value'}
            8. extra_vars - string value, template with additional text and without spaces before vars
                extra_vars = {'pass': 'test_value'}

        Expected result: all cases run successfully.
        """
        test_cases = [
            {
                'number': 1,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {},
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True}
                }
            },
            {
                'number': 2,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': "test_value", 'use_extra_vars': True}
                }
            },
            {
                'number': 3,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'pass': 123}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 123},
                    'args': {'password': 123, 'use_extra_vars': True}
                }
            },
            {
                'number': 4,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'pass': {'a': 123}}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': {'a': 123}},
                    'args': {'password': {'a': 123}, 'use_extra_vars': True}
                }
            },
            {
                'number': 5,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'pass': [1, 2, 3]}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': [1, 2, 3]},
                    'args': {'password': [1, 2, 3], 'use_extra_vars': True}
                }
            },
            {
                'number': 6,
                'input': {
                    'args': {'password': 'my pass {{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': 'my pass test_value', 'use_extra_vars': True}
                }
            },
            {
                'number': 7,
                'input': {
                    'args': {'password': 'my pass {{pass}}', 'use_extra_vars': True},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': 'my pass test_value', 'use_extra_vars': True}
                }
            },
            {
                'number': 8,
                'input': {
                    'args': {'password': 'my pass{{pass}}', 'use_extra_vars': True},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': 'my passtest_value', 'use_extra_vars': True}
                }
            }
        ]

        inventory = InventoryModule()
        inventory.loader = DataLoader()
        inventory.templar = Templar(inventory.loader)

        for each in test_cases:
            load_extra_vars.extra_vars = each['input']['extra_vars']
            inventory.args = each['input']['args']
            self.assertEqual(
                inventory.templar.is_template(inventory.args),
                each['expected']['is_template'],
                'error with input case: {0}'.format(each['number']))

            inventory.resolve_extra_vars()

            self.assertEqual(
                inventory.templar.available_variables,
                each['expected']['available_variables'],
                'error with input case: {0}'.format(each['number']))
            self.assertEqual(
                inventory.args,
                each['expected']['args'],
                'error with input case: {0}'.format(each['number']))

    def test_check_extra_vars_conditions(self):
        """
        This test checks conditions in function 'resolve_extra_vars'.

        Test cases:
            Input data contains variables:
                1. extra_vars = {}
                   use_extra_vars = False
                2. extra_vars = {}
                   use_extra_vars = True
                3. extra_vars = {'pass': 'test_value'}
                   use_extra_vars = False
                4. extra_vars = {'pass': 'test_value'}
                   use_extra_vars = True
            Input data doesn't contain variables:
                5. extra_vars = {}
                   use_extra_vars = False
                6. extra_vars = {}
                   use_extra_vars = True
                7. extra_vars = {'pass': 'test_value'}
                   use_extra_vars = False
                8. extra_vars = {'pass': 'test_value'}
                   use_extra_vars = True

        Expected result: all cases run successfully.
        """
        test_cases = [
            {
                'number': 1,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': False},
                    'extra_vars': {}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {},
                    'args': {'password': '{{ pass }}', 'use_extra_vars': False}
                }
            },
            {
                'number': 2,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {},
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True}
                }
            },
            {
                'number': 3,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': False},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': '{{ pass }}', 'use_extra_vars': False}
                }
            },
            {
                'number': 4,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': 'test_value', 'use_extra_vars': True}
                }
            },
            {
                'number': 5,
                'input': {
                    'args': {'password': 'test_value', 'use_extra_vars': False},
                    'extra_vars': {}
                },
                'expected': {
                    'is_template': False,
                    'available_variables': {},
                    'args': {'password': 'test_value', 'use_extra_vars': False}
                }
            },
            {
                'number': 6,
                'input': {
                    'args': {'password': 'test_value', 'use_extra_vars': True},
                    'extra_vars': {}
                },
                'expected': {
                    'is_template': False,
                    'available_variables': {},
                    'args': {'password': 'test_value', 'use_extra_vars': True}
                }
            },
            {
                'number': 7,
                'input': {
                    'args': {'password': 'test_value', 'use_extra_vars': False},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': False,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': 'test_value', 'use_extra_vars': False}
                }
            },
            {
                'number': 8,
                'input': {
                    'args': {'password': 'test_value', 'use_extra_vars': True},
                    'extra_vars': {'pass': 'test_value'}
                },
                'expected': {
                    'is_template': False,
                    'available_variables': {'pass': 'test_value'},
                    'args': {'password': 'test_value', 'use_extra_vars': True}
                }
            }
        ]

        inventory = InventoryModule()
        inventory.loader = DataLoader()
        inventory.templar = Templar(inventory.loader)

        for each in test_cases:
            load_extra_vars.extra_vars = each['input']['extra_vars']
            inventory.args = each['input']['args']
            self.assertEqual(
                inventory.templar.is_template(inventory.args),
                each['expected']['is_template'],
                'error with input case: {0}'.format(each['number']))
            inventory.resolve_extra_vars()
            self.assertEqual(
                inventory.templar.available_variables,
                each['expected']['available_variables'],
                'error with input case: {0}'.format(each['number']))
            self.assertEqual(
                inventory.args,
                each['expected']['args'],
                'error with input case: {0}'.format(each['number']))

    def test_check_extra_vars_error(self):
        """
        This test checks sitation when config contains one variable (pass),
        but input data contains different variable (test).

        Test cases:
            1. extra_vars = {'test': 'test_value'}
               use_extra_vars = True

        Expected result: all cases run successfully.
        """
        test_cases = [
            {
                'number': 1,
                'input': {
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True},
                    'extra_vars': {'test': 'test_value'}
                },
                'expected': {
                    'is_template': True,
                    'available_variables': {'test': 'test_value'},
                    'args': {'password': '{{ pass }}', 'use_extra_vars': True}
                }
            }
        ]

        inventory = InventoryModule()
        inventory.loader = DataLoader()
        inventory.templar = Templar(inventory.loader)

        for each in test_cases:
            load_extra_vars.extra_vars = each['input']['extra_vars']
            inventory.args = each['input']['args']
            self.assertEqual(
                inventory.templar.is_template(inventory.args),
                each['expected']['is_template'],
                'error with input case: {0}'.format(each['number']))

            with self.assertRaises(AnsibleUndefinedVariable) as ansible_result:
                inventory.resolve_extra_vars()

            self.assertIn(
                "'pass' is undefined",
                str(ansible_result.exception),
                'error with input case: {0}'.format(each['number']))
            self.assertEqual(
                inventory.templar.available_variables,
                each['expected']['available_variables'],
                'error with input case: {0}'.format(each['number']))
            self.assertEqual(
                inventory.args,
                each['expected']['args'],
                'error with input case: {0}'.format(each['number']))
