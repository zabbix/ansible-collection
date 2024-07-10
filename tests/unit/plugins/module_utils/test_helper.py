#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import unittest

from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    tag_to_dict_transform, Zabbix_version)


class TestParsing(unittest.TestCase):
    """Testing the parsing of Zabbix API version"""

    def test_parse(self):
        version = Zabbix_version('6.4.0')
        self.assertEqual(version.zapi_version, [6, 4, 0])

        version = Zabbix_version('6.4')
        self.assertEqual(version.zapi_version, [6, 4])

        version = Zabbix_version('6.4.')
        self.assertEqual(version.zapi_version, [6, 4])

        version = Zabbix_version('..6.4.')
        self.assertEqual(version.zapi_version, [6, 4])

        try:
            version = Zabbix_version('6.4a')
        except Exception as error:
            self.assertEqual(type(error), ValueError)

        try:
            version = Zabbix_version('6.4.a')
        except Exception as error:
            self.assertEqual(type(error), ValueError)


class TestVersions(unittest.TestCase):
    """Testing comparison operations between Zabbix API version"""

    def test_eq(self):
        """Testing the equality operation"""
        result = Zabbix_version('6.4.0') == Zabbix_version('6.4.0')
        self.assertTrue(result)

        result = Zabbix_version('6.4.0') == Zabbix_version('6.4')
        self.assertTrue(result)

        result = Zabbix_version('6.4') == Zabbix_version('6.4.0')
        self.assertTrue(result)

        result = Zabbix_version('6.4.0') == Zabbix_version('6.4.1')
        self.assertFalse(result)

        result = Zabbix_version('6.4.2') == Zabbix_version('6.4.0')
        self.assertFalse(result)

    def test_ne(self):
        """Testing the inequality operation"""
        result = Zabbix_version('6.4.0') != Zabbix_version('6.4.1')
        self.assertTrue(result)

        result = Zabbix_version('6.4.0') != Zabbix_version('6.2')
        self.assertTrue(result)

        result = Zabbix_version('6.4') != Zabbix_version('6.2.1')
        self.assertTrue(result)

        result = Zabbix_version('6.4.0') != Zabbix_version('6.4.0')
        self.assertFalse(result)

    def test_gt(self):
        """Testing the greater operation"""
        result = Zabbix_version('6.4.1') > Zabbix_version('6.4.0')
        self.assertTrue(result)

        result = Zabbix_version('6.4.1') > Zabbix_version('6.4')
        self.assertTrue(result)

        result = Zabbix_version('6.4') > Zabbix_version('6.4.0')
        self.assertFalse(result)

        result = Zabbix_version('6.4') > Zabbix_version('6.4.1')
        self.assertFalse(result)

        result = Zabbix_version('6.4.0') > Zabbix_version('6.4.1')
        self.assertFalse(result)

    def test_ge(self):
        """Testing the greater or equals operation"""
        result = Zabbix_version('6.4.1') >= Zabbix_version('6.4.0')
        self.assertTrue(result)

        result = Zabbix_version('6.4.1') >= Zabbix_version('6.4')
        self.assertTrue(result)

        result = Zabbix_version('6.4') >= Zabbix_version('6.4.0')
        self.assertTrue(result)

        result = Zabbix_version('6.4') >= Zabbix_version('6.4.1')
        self.assertFalse(result)

        result = Zabbix_version('6.4.0') >= Zabbix_version('6.4.1')
        self.assertFalse(result)

    def test_lt(self):
        """Testing the less operation"""
        result = Zabbix_version('6.4.0') < Zabbix_version('6.4.1')
        self.assertTrue(result)

        result = Zabbix_version('6.4') < Zabbix_version('6.4.1')
        self.assertTrue(result)

        result = Zabbix_version('6.4') < Zabbix_version('6.4.0')
        self.assertFalse(result)

        result = Zabbix_version('6.4.1') < Zabbix_version('6.4')
        self.assertFalse(result)

        result = Zabbix_version('6.4.1') < Zabbix_version('6.4.0')
        self.assertFalse(result)

    def test_le(self):
        """Testing the less or equals operation"""
        result = Zabbix_version('6.4.0') <= Zabbix_version('6.4.1')
        self.assertTrue(result)

        result = Zabbix_version('6.4') <= Zabbix_version('6.4.1')
        self.assertTrue(result)

        result = Zabbix_version('6.4') <= Zabbix_version('6.4.0')
        self.assertTrue(result)

        result = Zabbix_version('6.4.1') <= Zabbix_version('6.4')
        self.assertFalse(result)

        result = Zabbix_version('6.4.1') <= Zabbix_version('6.4.0')
        self.assertFalse(result)


class TestDictTransform(unittest.TestCase):
    """Testing the function of converting a list of tags into a dictionary"""

    def test_tag_to_dict_transform(self):
        input = [
            {'tag': 'component', 'value': 'application'},
            {'tag': 'scope', 'value': 'performance'}]
        expected = {
            'component': ['application'],
            'scope': ['performance']}
        self.assertEqual(tag_to_dict_transform(input), expected)

        input = [
            {'tag': 'component', 'value': 'application'},
            {'tag': 'component', 'value': 'health'},
            {'tag': 'scope', 'value': 'performance'}]
        expected = {
            'component': ['application', 'health'],
            'scope': ['performance']}
        self.assertEqual(tag_to_dict_transform(input), expected)

        input = [
            {'tag': 'component', 'value': ''},
            {'tag': 'scope', 'value': 'performance'}]
        expected = {
            'component': [''],
            'scope': ['performance']}
        self.assertEqual(tag_to_dict_transform(input), expected)
