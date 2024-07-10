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
else:
    try:
        import unittest2 as unittest
    except ImportError:
        print("Error import unittest library for Python 2")


class TestUrlNormalization(unittest.TestCase):

    def test_check_url(self):
        """
        This test checks function of URL normalization.

        Test cases:
            1. Only URL (without schema, API path).
            2. URL with schema.
            3. Same as previous but with additional slash at the end.
            4. Full URL with schema and API path.
            5. URL with additional path (/zabbix).
            6. Same as previous but with additional slash at the end.
            7. Same as previous but with two additional slashes at the end.
            8. Full URL with schema, additional path and API path.
            9. URL with https schema.
            10. Same as previous but with additional slash at the end.
            11. Full URL with https schema and API path.
            12. URL with additional path (/zabbix) and https schema.
            13. Same as previous but with additional slash at the end.
            14. Same as previous but with two additional slashes at the end.
            15. Full URL with https schema, additional path and API path.
            16. Empty URL and expected 'localhost'.

        Expected result: all cases run successfully.
        """
        test_cases = [
            {'input': '127.0.0.1', 'expected': 'http://127.0.0.1/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1', 'expected': 'http://127.0.0.1/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1/', 'expected': 'http://127.0.0.1/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1/api_jsonrpc.php', 'expected': 'http://127.0.0.1/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1/zabbix', 'expected': 'http://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1/zabbix/', 'expected': 'http://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1/zabbix//', 'expected': 'http://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'http://127.0.0.1/zabbix/api_jsonrpc.php', 'expected': 'http://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1', 'expected': 'https://127.0.0.1/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1/', 'expected': 'https://127.0.0.1/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1/api_jsonrpc.php', 'expected': 'https://127.0.0.1/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1/zabbix', 'expected': 'https://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1/zabbix/', 'expected': 'https://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1/zabbix//', 'expected': 'https://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': 'https://127.0.0.1/zabbix/api_jsonrpc.php', 'expected': 'https://127.0.0.1/zabbix/api_jsonrpc.php'},
            {'input': None, 'expected': 'http://localhost/api_jsonrpc.php'}
        ]

        inventory = InventoryModule()
        for each in test_cases:
            inventory.args = {'zabbix_api_url': each['input']}
            result = inventory.get_absolute_url()
            self.assertEqual(result, each['expected'],
                             'error with input data: {0}'.format(each['input']))
