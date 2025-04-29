#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.zabbix.zabbix.plugins.inventory.zabbix_inventory import InventoryModule

import sys

if sys.version_info[0] > 2:
    import unittest
    from unittest.mock import patch
else:
    try:
        import unittest2 as unittest
        from mock import patch
    except ImportError:
        print("Error import unittest library for Python 2")

preloaded_data = [
    {
        "hostid": "10673",
        "name": "host_1_22",
        "interfaces": [],
        "tags": [
            {
                "tag": "port",
                "value": "22",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10674",
        "name": "host_2_22_80",
        "interfaces": [],
        "tags": [
            {
                "tag": "port",
                "value": "22",
                "automatic": "0"
            },
            {
                "tag": "port",
                "value": "80",
                "automatic": "0"
            },
            {
                "tag": "search",
                "value": "additional",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10675",
        "name": "host_3_80",
        "interfaces": [],
        "tags": [
            {
                "tag": "port",
                "value": "80",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10676",
        "name": "host_4_443",
        "interfaces": [],
        "tags": [
            {
                "tag": "port",
                "value": "443",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10677",
        "name": "host_5",
        "interfaces": [],
        "tags": []
    },
    {
        "hostid": "10678",
        "name": "host_6_ssh",
        "interfaces": [],
        "tags": [
            {
                "tag": "service",
                "value": "ssh",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10679",
        "name": "host_7_ssh_22",
        "interfaces": [],
        "tags": [
            {
                "tag": "service",
                "value": "ssh",
                "automatic": "0"
            },
            {
                "tag": "port",
                "value": "22",
                "automatic": "0"
            },
            {
                "tag": "search",
                "value": "additional",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10680",
        "name": "host_8_2222",
        "interfaces": [],
        "tags": [
            {
                "tag": "port",
                "value": "2222",
                "automatic": "0"
            }
        ]
    },
    {
        "hostid": "10681",
        "name": "host_9_22_480",
        "interfaces": [],
        "tags": [
            {
                "tag": "port",
                "value": "480",
                "automatic": "0"
            },
            {
                "tag": "port",
                "value": "22",
                "automatic": "0"
            }
        ]
    }
]

query = {
    "output": [
        "hostid",
        "tags"
    ],
    "selectTags": "extend",
    "selectInterfaces": [
        "ip",
        "dns"
    ],
    "groupids": [
        "24"
    ],
    "tags": [
        {
            "tag": "port",
            "value": 22,
            "operator": "1"
        },
        {
            "tag": "port",
            "value": 80,
            "operator": "1"
        },
        {
            "tag": "search",
            "value": "additional",
            "operator": "1"
        }
    ],
    "evaltype": "0"
}


# mock for api_request
def mock_api_request(self, method, params):
    return preloaded_data


class TestPreloadData(unittest.TestCase):

    def test_strict_and_equals(self):
        """
        This test checks strict AND logic in case of using quals as first operator.

        Test cases:
            1. Tag 'port' equals 22 AND tag port quals 80;
            2. Tag 'port' equals 22 AND tag port not quals 80;
            3. Tag 'port' equals 22 AND tag port contains 80;
            4. Tag 'port' equals 22 AND tag port not like 80;
            5. Tag 'port' equals 22 AND tag service exist;
            6. Tag 'port' equals 22 AND tag service not exist;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'port', 'value': 80, 'operator': 'equals'}],
                    'tags_behavior': 'and'}},
             'expected': ['10674']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'port', 'value': 80, 'operator': 'not equal'}],
                    'tags_behavior': 'and'}},
             'expected': ['10673', '10679', '10681']},
            # case #3
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'port', 'value': 80, 'operator': 'contains'}],
                    'tags_behavior': 'and'}},
             'expected': ['10674', '10681']},
            # case #4
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'port', 'value': 80, 'operator': 'not like'}],
                    'tags_behavior': 'and'}},
             'expected': ['10673', '10679']},
            # case #5
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'operator': 'exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10679']},
            # case #6
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'operator': 'not exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10673', '10674', '10681']}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_not_equals(self):
        """
        This test checks strict AND logic in case of using NOT quals as first operator.

        Test cases:
            1. Tag 'port' not equals 22 AND tag port not quals 80;
            2. Tag 'port' not equals 22 AND tag port contains 80;
            3. Tag 'port' not equals 22 AND tag port not like 80;
            4. Tag 'port' not equals 22 AND tag service exist;
            5. Tag 'port' not equals 22 AND tag service not exist;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not equal'},
                        {'tag': 'port', 'value': 80, 'operator': 'not equal'}],
                    'tags_behavior': 'and'}},
             'expected': ['10676', '10677', '10678', '10680']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not equal'},
                        {'tag': 'port', 'value': 80, 'operator': 'contains'}],
                    'tags_behavior': 'and'}},
             'expected': ['10675']},
            # case #3
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not equal'},
                        {'tag': 'port', 'value': 80, 'operator': 'not like'}],
                    'tags_behavior': 'and'}},
             'expected': ['10676', '10677', '10678', '10680']},
            # case #4
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not equal'},
                        {'tag': 'service', 'operator': 'exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10678']},
            # case #5
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not equal'},
                        {'tag': 'service', 'operator': 'not exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10680', '10677', '10676', '10675']}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_contains(self):
        """
        This test checks strict AND logic in case of using contains as first operator.

        Test cases:
            1. Tag 'port' contains 22 AND tag port contains 80;
            2. Tag 'port' contains 22 AND tag port not like 80;
            3. Tag 'port' contains 22 AND tag service exist;
            4. Tag 'port' contains 22 AND tag service not exist;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'contains'},
                        {'tag': 'port', 'value': 80, 'operator': 'contains'}],
                    'tags_behavior': 'and'}},
             'expected': ['10674', '10681']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'contains'},
                        {'tag': 'port', 'value': 80, 'operator': 'not like'}],
                    'tags_behavior': 'and'}},
             'expected': ['10680', '10679', '10673']},
            # case #3
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'contains'},
                        {'tag': 'service', 'operator': 'exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10679']},
            # case #4
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'contains'},
                        {'tag': 'service', 'operator': 'not exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10681', '10680', '10674', '10673']}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_not_like(self):
        """
        This test checks strict AND logic in case of using not like as first operator.

        Test cases:
            1. Tag 'port' not like 22 AND tag port not like 80;
            2. Tag 'port' not like 22 AND tag service exist;
            3. Tag 'port' not like 22 AND tag service not exist;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not like'},
                        {'tag': 'port', 'value': 80, 'operator': 'not like'}],
                    'tags_behavior': 'and'}},
             'expected': ['10676', '10677', '10678']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not like'},
                        {'tag': 'service', 'operator': 'exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10678']},
            # case #3
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'not like'},
                        {'tag': 'service', 'operator': 'not exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10677', '10676', '10675']}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_exist(self):
        """
        This test checks strict AND logic in case of using exists as first operator.

        Test cases:
            1. Tag 'port' exists AND tag service exist;
            2. Tag 'port' exists AND tag service not exist;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'operator': 'exists'},
                        {'tag': 'service', 'operator': 'exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10679']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'operator': 'exists'},
                        {'tag': 'service', 'operator': 'not exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10681', '10680', '10676', '10675', '10674', '10673']}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_not_exist(self):
        """
        This test checks strict AND logic in case of using not exists as first operator.

        Test cases:
            1. Tag 'port' not exists AND tag service not exist;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'operator': 'not exists'},
                        {'tag': 'service', 'operator': 'not exists'}],
                    'tags_behavior': 'and'}},
             'expected': ['10677']}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_permutation(self):
        """
        This test checks that the result does not depend on changing the order of arguments.

        Test cases:
            1. Tag 'port' equals 22 AND tag 'port' equals 80;
            2. Tag 'port' equals 80 AND tag 'port' equals 22;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'port', 'value': 80, 'operator': 'equals'}],
                    'tags_behavior': 'and'}},
             'expected': ['10674']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 80, 'operator': 'equals'},
                        {'tag': 'port', 'value': 22, 'operator': 'equals'}],
                    'tags_behavior': 'and'}},
             'expected': ['10674']},
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_additional_check(self):
        """
        This test checks additional conditions when using tag filtering.

        Test cases:
            1. Tag 'port' equals 22 AND tag 'service' equals ssh;
            2. Tag 'port' equals 22 AND tag 'service' not equals ssh;
            3. Tag 'port' equals 22 AND tag 'service' equals ssh AND tag 'search' equals additional;
            4. Tag 'port' equals 22 AND tag 'port' equals 80 AND tag 'search' equals additional;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'value': 'ssh', 'operator': 'equals'}],
                    'tags_behavior': 'and'}},
             'expected': ['10679']},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'value': 'ssh', 'operator': 'not equal'}],
                    'tags_behavior': 'and'}},
             'expected': ['10673', '10674', '10681']},
            # case #3
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'value': 'ssh', 'operator': 'equals'},
                        {'tag': 'search', 'value': 'additional', 'operator': 'equals'}],
                    'tags_behavior': 'and'}},
             'expected': ['10679']},
            # case #4
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'port', 'value': 80, 'operator': 'equals'},
                        {'tag': 'search', 'value': 'additional', 'operator': 'equals'}],
                    'tags_behavior': 'and'}},
             'expected': ['10674']},
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(sorted(inventory.query['hostids']), sorted(each['expected']))

    def test_strict_and_with_or_and_or(self):
        """
        This test checks that when using and/or, or logic, data preloading will not occur.

        Test cases:
            1. and/or;
            2. or;

        Expected result: all cases run successfully.
        """
        test_cases = [
            # case #1
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'value': 'ssh', 'operator': 'equals'}],
                    'tags_behavior': 'and/or'}}},
            # case #2
            {'input': {
                'filter': {
                    'tags': [
                        {'tag': 'port', 'value': 22, 'operator': 'equals'},
                        {'tag': 'service', 'value': 'ssh', 'operator': 'not equal'}],
                    'tags_behavior': 'or'}}}
        ]

        with patch.multiple(
                InventoryModule,
                api_request=mock_api_request):

            for each in test_cases:
                inventory = InventoryModule()
                inventory.args = each['input']
                inventory.zabbix_version = '7.0.0'
                inventory.query = query

                inventory.preload_data()

                self.assertEqual(inventory.query.get('hostids'), None)
