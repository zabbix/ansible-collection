#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class Zabbix_version:
    """
    Class for comparing Zabbix API version

    :param zapi_version: Zabbix API version
    :type zapi_version: str

    :rtype: bool
    :return: result of comparing
    """
    def __init__(self, zapi_version):
        self.zapi_version = self._parse(zapi_version)

    def _parse(self, version):
        result = []
        for v in version.split('.'):
            if len(v) > 0:
                if v.isdigit():
                    result.append(int(v))
                else:
                    raise ValueError('Unsupported element: {0}'.format(v))

        return result

    def _compare(self, other):
        max_length = max(len(self.zapi_version), len(other.zapi_version))
        if len(self.zapi_version) < max_length:
            add_num = max_length - len(self.zapi_version)
            self.zapi_version.extend([0] * add_num)
        if len(other.zapi_version) < max_length:
            add_num = max_length - len(other.zapi_version)
            other.zapi_version.extend([0] * add_num)

        for i in range(max_length):
            if self.zapi_version[i] > other.zapi_version[i]:
                return 1
            if self.zapi_version[i] < other.zapi_version[i]:
                return -1
        return 0

    def __eq__(self, other):
        result = self._compare(other)
        return result == 0

    def __ne__(self, other):
        result = self._compare(other)
        return result != 0

    def __lt__(self, other):
        result = self._compare(other)
        return result < 0

    def __gt__(self, other):
        result = self._compare(other)
        return result > 0

    def __le__(self, other):
        result = self._compare(other)
        return result <= 0

    def __ge__(self, other):
        result = self._compare(other)
        return result >= 0


def tag_to_dict_transform(tags):
    """
    The function converts tags into a dictionary,
    where the key is the tag name and the value is a list of tag values.
    Example input:
        [
            {'tag': 'component', 'value': 'application'},
            {'tag': 'component', 'value': 'health'},
            {'tag': 'scope', 'value': 'performance'}
        ]
    Example output:
        {
            'component': ['application', 'health'],
            'scope': ['performance']
        }

    :param tags: list of tag dict
    :type tags: list

    :rtype: dict
    :return: converted tags
    """
    result = {}
    for tag in tags:
        if tag['tag'] in result:
            result[tag['tag']].append(tag['value'])
        else:
            result[tag['tag']] = [tag['value']]

    return result

# Dictionaries for value conversion


# Dictionary with default values
default_values = {
    'ipmi_authtype': '-1',
    'ipmi_privilege': '2',
    'ports': {
        'agent': '10050',
        'snmp': '161',
        'ipmi': '623',
        'jmx': '12345'
    }
}

# Dictionary for converting macro types to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/usermacro/object#host-macro)
macro_types = {
    'text': '0',
    'secret': '1',
    'vault_secret': '2'}

# Dictionary for converting IPMI authtype to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/object#host)
ipmi_authtype_type = {
    'default': '-1',
    'none': '0',
    'md2': '1',
    'md5': '2',
    'straight': '4',
    'oem': '5',
    'rmcp+': '6'
}

# Dictionary for converting IPMI privilege to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/object#host)
ipmi_privilege_type = {
    'callback': '1',
    'user': '2',
    'operator': '3',
    'admin': '4',
    'oem': '5'
}

# Dictionary for converting TLS type to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/object#host)
tls_type = {
    'unencrypted': 1,
    'psk': 2,
    'cert': 4
}

# Dictionary for converting inventory mode to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/object#host)
inventory_mode_types = {
    'automatic': '1',
    'manual': '0',
    'disabled': '-1'
}

# Dictionary with available inventory fields
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/object#host-inventory)
inventory_fields = {
    '1': 'type', '2': 'type_full', '3': 'name', '4': 'alias', '5': 'os',
    '6': 'os_full', '7': 'os_short', '8': 'serialno_a', '9': 'serialno_b',
    '10': 'tag', '11': 'asset_tag', '12': 'macaddress_a', '13': 'macaddress_b',
    '14': 'hardware', '15': 'hardware_full', '16': 'software',
    '17': 'software_full', '18': 'software_app_a', '19': 'software_app_b',
    '20': 'software_app_c', '21': 'software_app_d', '22': 'software_app_e',
    '23': 'contact', '24': 'location', '25': 'location_lat',
    '26': 'location_lon', '27': 'notes', '28': 'chassis', '29': 'model',
    '30': 'hw_arch', '31': 'vendor', '32': 'contract_number',
    '33': 'installer_name', '34': 'deployment_status', '35': 'url_a',
    '36': 'url_b', '37': 'url_c', '38': 'host_networks', '39': 'host_netmask',
    '40': 'host_router', '41': 'oob_ip', '42': 'oob_netmask',
    '43': 'oob_router', '44': 'date_hw_purchase', '45': 'date_hw_install',
    '46': 'date_hw_expiry', '47': 'date_hw_decomm', '48': 'site_address_a',
    '49': 'site_address_b', '50': 'site_address_c', '51': 'site_city',
    '52': 'site_state', '53': 'site_country', '54': 'site_zip',
    '55': 'site_rack', '56': 'site_notes', '57': 'poc_1_name',
    '58': 'poc_1_email', '59': 'poc_1_phone_a', '60': 'poc_1_phone_b',
    '61': 'poc_1_cell', '62': 'poc_1_screen', '63': 'poc_1_notes',
    '64': 'poc_2_name', '65': 'poc_2_email', '66': 'poc_2_phone_a',
    '67': 'poc_2_phone_b', '68': 'poc_2_cell', '69': 'poc_2_screen',
    '70': 'poc_2_notes'}

# Dictionary for converting interface type to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/hostinterface/object#host-interface)
interface_types = {
    'agent': '1',
    'snmp': '2',
    'ipmi': '3',
    'jmx': '4'}

# Dictionary for converting security level type to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/hostinterface/object)
snmp_securitylevel_types = {
    'noAuthNoPriv': '0',
    'authNoPriv': '1',
    'authPriv': '2'
}

# Dictionary for converting authprotocol type to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/hostinterface/object)
snmp_authprotocol_types = {
    'md5': '0', 'sha1': '1', 'sha224': '2',
    'sha256': '3', 'sha384': '4', 'sha512': '5'}

# Dictionary for converting privprotocol type to a numeric value
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/hostinterface/object)
snmp_privprotocol_types = {
    'des': '0', 'aes128': '1', 'aes192': '2',
    'aes256': '3', 'aes192c': '4', 'aes256c': '5'}

# Dictionary for SNMP parameters
# If the new field only depends on the version, then it must be added here.
# If the new field needs some logic, then it must be added in file zabbix_host.py in section with SNMP checks.
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/hostinterface/object)
snmp_parameters = {
    '1': ['version', 'bulk', 'community'],
    '2': ['version', 'bulk', 'community'],
    '3': {
        'noAuthNoPriv': ['version', 'bulk', 'contextname', 'securityname', 'securitylevel'],
        'authNoPriv': ['version', 'bulk', 'contextname', 'securityname', 'securitylevel',
                       'authprotocol', 'authpassphrase'],
        'authPriv': ['version', 'bulk', 'contextname', 'securityname', 'securitylevel',
                     'authprotocol', 'authpassphrase', 'privprotocol', 'privpassphrase']}
}

# Dictionary for tag operator parameters
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/get)
tags_compare_operators = {
    'contains': '0',
    'equals': '1',
    'not like': '2',
    'not equal': '3',
    'exists': '4',
    'not exists': '5'
}

# All available query
# (See also: https://www.zabbix.com/documentation/current/manual/api/reference/host/get)
host_subquery = [
    "selectDiscoveries", "selectDiscoveryRule", "selectGraphs", "selectHostDiscovery",
    "selectHostGroups", "selectHttpTests", "selectInterfaces", "selectInventory",
    "selectItems", "selectMacros", "selectParentTemplates", "selectDashboards",
    "selectTags", "selectInheritedTags", "selectTriggers", "selectValueMaps", "selectGroups"]
