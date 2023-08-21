#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

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
        This test checks function for normalization URL.

        Test cases:
            1. Only URL (without schema, api path)
            2. URL with schema
            3. The same as previous, but with additional slash at the end
            4. Full URL with schema and api path
            5. URL with additional path (/zabbix)
            6. The same as previous, but with additional slash at the end
            7. The same as previous, but with additional two slashes at the end
            8. Full URL with schema, additional path and api path
            9. URL with schema https
            10. The same as previous, but with additional slash at the end
            11. Full URL with https schema and api path
            12. URL with additional path (/zabbix) and schema https
            13. The same as previous, but with additional slash at the end
            14. The same as previous, but with additional two slashes at the end
            15. Full URL with https schema, additional path and api path
            16. Empty URL and expected 'localhost'

        Expected result: all cases run success
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
