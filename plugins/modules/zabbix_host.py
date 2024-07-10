#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zabbix_host
short_description: Module for creating hosts, deleting and updating existing hosts.
description:
    - The module is designed to create, update or delete a host in Zabbix.
    - In case of updating an existing host, only the specified parameters will be updated.
author:
    - Zabbix Ltd (@zabbix)
requirements:
    - "python >= 2.6"
options:
    state:
        description: Create or delete host.
        required: false
        type: str
        default: present
        choices: [ present, absent ]
    host:
        description:
            - Host name to create.
            - The name of an existing host in case of an update.
        type: str
        required: true
        aliases: [ host_name ]
    name:
        description: Visible host name
        type: str
        aliases: [ visible_name ]
    hostgroups:
        description:
            - Host groups to replace the current host groups the host belongs to.
            - All host groups that are not listed in the task will be unlinked.
        type: list
        elements: str
        aliases: [ host_group, host_groups ]
    templates:
        description:
            - Templates to replace the currently linked templates.
            - All templates that are not listed in the task will be unlinked.
        type: list
        elements: str
        aliases: [ link_templates, host_templates, template ]
    status:
        description: Host status (enabled or disabled).
        type: str
        choices: [ enabled, disabled ]
    description:
        description: Host description.
        type: str
    tags:
        description:
            - Host tags to replace the current host tags.
            - All tags that are not listed in the task will be removed.
        type: list
        elements: dict
        suboptions:
            tag:
                description: Host tag name.
                type: str
                required: true
            value:
                description: Host tag value.
                type: str
                default: ''
        aliases: [ host_tags ]
    macros:
        description:
            - User macros to replace the current user macros.
            - All macros that are not listed in the task will be removed.
            - If a secret macro is specified, the host will be updated every time the task is run.
        type: list
        elements: dict
        suboptions:
            macro:
                description: Macro string.
                type: str
                required: true
            value:
                description:
                    - Value of the macro.
                    - Write-only if I(type=secret).
                type: str
                default: ''
            description:
                description: Description of the macro.
                type: str
                default: ''
            type:
                description: Type of the macro.
                type: str
                default: text
                choices: [ text, secret, vault_secret ]
        aliases: [ user_macros, user_macro ]
    ipmi_authtype:
        description: IPMI authentication algorithm.
        type: str
        choices: [ default, none, md2, md5, straight, oem, rmcp+ ]
    ipmi_privilege:
        description: IPMI privilege level.
        type: str
        choices: [ callback, user, operator, admin, oem ]
    ipmi_username:
        description: IPMI username.
        type: str
    ipmi_password:
        description: IPMI password.
        type: str
    tls_accept:
        description: Connections from host.
        type: list
        elements: str
        choices: [ unencrypted, psk, cert ]
    tls_connect:
        description: Connections to host.
        type: str
        choices: [ '', unencrypted, psk, cert ]
    tls_psk_identity:
        description:
            - PSK identity.
            - Required if I(tls_connect=psk) , or I(tls_accept) contains the 'psk'.
            - In case of updating an existing host, if the host already has PSK enabled, the parameter is not required.
            - If the parameter is defined, then every launch of the task will update the host,
              because Zabbix API does not have access to an existing PSK key and we cannot compare the specified key with the existing one.
        type: str
    tls_psk:
        description:
            - The pre-shared key, at least 32 hex digits.
            - Required if I(tls_connect=psk), or I(tls_accept) contains the 'psk'.
            - In case of updating an existing host, if the host already has PSK enabled, the parameter is not required.
            - If the parameter is defined, then every launch of the task will update the host,
              because Zabbix API does not have access to an existing PSK key and we cannot compare the specified key with the existing one.
        type: str
    tls_issuer:
        description: Certificate issuer.
        type: str
    tls_subject:
        description: Certificate subject.
        type: str
    proxy:
        description: Name of the proxy that is used to monitor the host.
        type: str
    proxy_group:
        description:
            - Name of the proxy group that is used to monitor the host.
            - Used only for Zabbix versions above 7.0.
        type: str
    inventory_mode:
        description: Host inventory population mode.
        choices: [ automatic, manual, disabled ]
        type: str
    inventory:
        description:
            - The host inventory object.
            - "All possible fields:"
            - type, type_full, name, alias, os, os_full, os_short, serialno_a, serialno_b, tag, asset_tag, macaddress_a,
              macaddress_b, hardware, hardware_full, software, software_full, software_app_a, software_app_b, software_app_c, software_app_d,
              software_app_e, contact, location, location_lat, location_lon, notes, chassis, model, hw_arch, vendor, contract_number,
              installer_name, deployment_status, url_a, url_b, url_c, host_networks, host_netmask, host_router, oob_ip, oob_netmask,
              oob_router, date_hw_purchase, date_hw_install, date_hw_expiry, date_hw_decomm, site_address_a, site_address_b, site_address_c,
              site_city, site_state, site_country, site_zip, site_rack, site_notes, poc_1_name, poc_1_email, poc_1_phone_a,
              poc_1_phone_b, poc_1_cell, poc_1_screen, poc_1_notes, poc_2_name, poc_2_email, poc_2_phone_a, poc_2_phone_b, poc_2_cell,
              poc_2_screen, poc_2_notes.
            - See U(https://www.zabbix.com/documentation/current/en/manual/api/reference/host/object#host-inventory) for an overview.
        type: dict
        aliases: [ inventory_zabbix, host_inventory ]
    interfaces:
        type: list
        elements: dict
        description:
            - Host interfaces to replace the current host interfaces.
            - Only one interface of each type is supported.
            - All interfaces that are not listed in the request will be removed.
        suboptions:
            type:
                type: str
                description: Interface type.
                choices: [ agent, snmp, ipmi, jmx ]
                required: True
            useip:
                type: bool
                description: Whether the connection should be made through IP.
                default: True
            ip:
                type: str
                description:
                    - IP address used by the interface.
                    - Can be empty if the connection is made through DNS.
                default: ''
            dns:
                type: str
                description:
                    - DNS name used by the interface.
                    - Can be empty if the connection is made through IP.
                    - Require if I(useip=False).
                default: ''
            port:
                type: str
                description:
                    - Port number used by the interface.
                    - Can contain user macros.
            details:
                description:
                    - Additional details object for interface.
                    - Required if I(type=snmp).
                type: dict
                suboptions:
                    version:
                        description: SNMP interface version.
                        type: str
                        choices: [ '1', '2', '3' ]
                    bulk:
                        description: Whether to use bulk SNMP requests.
                        type: bool
                    community:
                        description:
                            - SNMP community.
                            - Used only if I(version=1) or I(version=2).
                        type: str
                    max_repetitions:
                        description:
                            - Max repetition count is applicable to discovery and walk only.
                            - Used only if I(version=2) or I(version=3).
                            - Used only for Zabbix versions above 6.4.
                        type: str
                    contextname:
                        description:
                            - SNMPv3 context name.
                            - Used only if I(version=3).
                        type: str
                    securityname:
                        description:
                            - SNMPv3 security name.
                            - Used only if I(version=3).
                        type: str
                    securitylevel:
                        description:
                            - SNMPv3 security level.
                            - Used only if I(version=3).
                        type: str
                        choices: [ noAuthNoPriv, authNoPriv, authPriv ]
                    authprotocol:
                        description:
                            - SNMPv3 authentication protocol.
                            - Used only if I(version=3).
                        type: str
                        choices: [ md5, sha1, sha224, sha256, sha384, sha512 ]
                    authpassphrase:
                        description:
                            - SNMPv3 authentication passphrase.
                            - Used only if I(version=3).
                        type: str
                    privprotocol:
                        description:
                            - SNMPv3 privacy protocol.
                            - Used only if I(version=3).
                        type: str
                        choices: [ des, aes128, aes192, aes256, aes192c, aes256c ]
                    privpassphrase:
                        description:
                            - SNMPv3 privacy passphrase.
                            - Used only if I(version=3).
                        type: str
notes:
    - If I(tls_psk_identity) or I(tls_psk) is defined or macro I(type=secret), then every launch of the task will update the host,
      because Zabbix API does not have access to an existing PSK key or secret macros and we cannot compare the specified value with the existing one.
    - Only one interface of each type is supported.
'''

EXAMPLES = r'''
# To create host with minimum parameters
# Host group is required
- name: Create host
  zabbix.zabbix.zabbix_host:
    state: present
    host: Example host
    hostgroups:
      - Linux servers
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To create host with maximum parameters
- name: Create host with maximum parameters
  zabbix.zabbix.zabbix_host:
    state: present
    host: Example host
    hostgroups:
      - Linux servers
    templates:
      - Zabbix agent active
    status: enabled
    description: 'Host example'
    name: 'Example host'
    tags:
      - tag: scope
        value: test
    macros:
      - macro: TEST_MACRO
        value: example
        description: Description of macro example
        type: text
    ipmi_authtype: default
    ipmi_privilege: user
    ipmi_username: admin
    ipmi_password: your_password
    tls_accept:
      - unencrypted
      - psk
      - certificate
    tls_psk_identity: my_example_identity
    tls_psk: SET_YOUR_PSK_KEY
    tls_issuer: Example Issuer
    tls_subject: Example Subject
    tls_connect: psk
    inventory_mode: automatic
    inventory:
      type: ""  # To specify an empty value
      serialno_b: example value
      hardware_full: |
        very very long
        multiple string value
    interfaces:
      - type: agent # To specify an interface with default parameters (the IP will be 127.0.0.1)
      - type: ipmi
      - type: jmx
        ip: 192.168.100.51
        dns: test.com
        useip: true
        port: 12345
      - type: snmp
        ip: 192.168.100.50
        dns: switch.local
        port: 169   # To specify a non-standard value
        details:
          version: 3
          bulk: true
          contextname: my contextname name
          securityname: my securityname name
          securitylevel: authPriv
          authprotocol: md5
          authpassphrase: SET_YOUR_PWD
          privprotocol: des
          privpassphrase: SET_YOUR_PWD
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To update host to empty parameters
- name: Clean all parameters from host
  zabbix.zabbix.zabbix_host:
    state: present
    host: Example host
    hostgroups:    # Host group must be not empty
      - Linux servers
    templates: []
    status: enabled
    description: ''
    name: '' # The technical name will be used
    tags: []
    macros: []
    ipmi_authtype: default
    ipmi_privilege: user
    ipmi_username: ''
    ipmi_password: ''
    tls_accept:
      - unencrypted
    tls_issuer: ''
    tls_subject: ''
    tls_connect: unencrypted
    proxy: ''
    inventory_mode: disabled
    interfaces: []
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To update only one parameter, you can specify just
# the hostname (used for searching) and the desired parameter.
# The rest of the host parameters will not be changed.
# For example, you want to turn off a host
- name: Update host status
  zabbix.zabbix.zabbix_host:
    host: Example host
    status: disabled
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To remove a host, you can use:
- name: Delete host
  zabbix.zabbix.zabbix_host:
    state: absent
    host: Example host
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# You can configure Zabbix API connection settings with the following parameters:
- name: Create host groups
  zabbix.zabbix.zabbix_host:
    state: present
    host: Example host
    hostgroups:
      - Linux servers
  vars:
    # Connection parameters
    ansible_host: zabbix-api.com                # Specifying Zabbix API address. You can also use 'delegate_to'.
    ansible_connection: httpapi                 # Specifying to use HTTP API plugin.
    ansible_network_os: zabbix.zabbix.zabbix    # Specifying which HTTP API plugin to use.
    ansible_httpapi_port: 80                    # Specifying the port for connecting to Zabbix API.
    ansible_httpapi_use_ssl: false              # Specifying the type of connection. True for https, False for http (by default).
    ansible_httpapi_validate_certs: false       # Specifying certificate validation.
    # User parameters for connecting to Zabbix API
    ansible_user: Admin                         # Username to connect to Zabbix API.
    ansible_httpapi_pass: zabbix                # Password to connect to Zabbix API.
    # Token for connecting to Zabbix API
    zabbix_api_token: your_secret_token         # Specify your token to connect to Zabbix API.
    # Path to connect to Zabbix API
    zabbix_api_url: '/zabbix'                   # The field is empty by default. You can specify your connection path (e.g., '/zabbix').
    # User parameters for basic HTTP authorization
    # These options only affect the basic HTTP authorization configured on the web server.
    http_login: my_http_login                   # Username for connecting to API in case of additional basic HTTP authorization.
    http_password: my_http_password             # Password for connecting to API in case of additional basic HTTP authorization.
'''

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zabbix.zabbix.plugins.module_utils.zabbix_api import (
    ZabbixApi)
from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    tag_to_dict_transform, macro_types, ipmi_authtype_type,
    ipmi_privilege_type, default_values, tls_type, inventory_mode_types,
    inventory_fields, interface_types, snmp_securitylevel_types,
    snmp_authprotocol_types, snmp_privprotocol_types, Zabbix_version, snmp_parameters)


class Host(object):

    def __init__(self, module):
        self.module = module
        self.zapi = ZabbixApi(module)
        self.zbx_api_version = self.zapi.api_version()

    def get_zabbix_host(self, hostid):
        """
        The function gets information about an existing host in Zabbix.

        :param hostid: hostid for search
        :type hostid: str|int

        :rtype: dict
        :returns:
            *   dict with host parameters if host exists
            *   empty dict if host does not exist
        """
        host = {}
        params = {
            'output': 'extend',
            'selectGroups': ['groupid', 'name'],
            'selectParentTemplates': ['templateid', 'name'],
            'selectTags': ['tag', 'value'],
            'selectMacros': ['macro', 'value', 'type', 'description'],
            'selectInterfaces': [
                'interfaceid', 'main', 'type', 'useip',
                'ip', 'dns', 'port', 'details'],
            'hostids': hostid}

        if self.module.params.get('inventory') is not None:
            params['selectItems'] = ['name', 'inventory_link']
            params['selectInventory'] = 'extend'

        try:
            host = self.zapi.send_api_request(
                method='host.get',
                params=params)
        except Exception as e:
            self.module.fail_json(
                msg="Failed to get existing host: {0}".format(e))

        if 'items' in host[0]:
            self.inventory_links = {}
            for each in host[0]['items']:
                if each['inventory_link'] != '0':
                    self.inventory_links[inventory_fields[each['inventory_link']]] = each['name']

        return host[0]

    def host_api_request(self, method, params):
        """
        The function sends a request to Zabbix API.

        :param method: method for request
        :type method: str
        :param params: parameters for request
        :type params: dict

        :rtype: bool
        :return: result of request
        """
        # Check mode
        if self.module.check_mode:
            self.module.exit_json(changed=True)

        try:
            self.zapi.send_api_request(
                method=method,
                params=params)
        except Exception:
            return False

        return True

    def check_elements(self, require, exist):
        """
        The function checks that all required elements are found in Zabbix.
        If any element from the required list is missing,
        the module will be stopped.

        :param method: list of required elements
        :type method: list
        :param params: list of existing elements
        :type params: list

        :rtype: bool
        :return: True if all required elements are found in Zabbix.

        notes::
            *  If an element from the required list is missing,
            the module will be stopped.
        """
        missing = list(set(require) - set(exist))
        if missing:
            self.module.fail_json(
                msg="Not found in Zabbix: {0}".format(
                    ', '.join(missing)))

        return True

    def check_macro_name(self, macro):
        """
        The function checks and normalizes the macro name.

        :param macro: macro name
        :type macro: str

        :rtype: str
        :return: normalized macro name

        notes::
            *  If spaces are found in the macro name,
            the module will be stopped.
        """
        for element in ['{', '$', '}']:
            macro = macro.replace(element, '')
        if ' ' in macro:
            self.module.fail_json(
                msg="Invalid macro name: {0}".format(macro))

        return '{$' + macro.upper() + '}'

    def generate_zabbix_host(self, exist_host=None):
        """
        The function generates the desired host parameters based on the module
        parameters.
        The returned dictionary can be used to create a host, as well as to
        compare with an existing host.

        :param exist_host: parameters of existing Zabbix host
        :type exist_host: dict

        :rtype: dict
        :return: parameters of desired host

        note::
            *  The 'exist_host' parameter is used to determine the current
               encryption, inventory, and host group settings on existing host.
        """
        host_params = {}

        host_params['host'] = self.module.params['host']

        # These parameters don't require additional processing
        param_wo_process = [
            'description', 'name', 'tags', 'ipmi_username', 'ipmi_password',
            'tls_psk', 'tls_psk_identity', 'tls_issuer', 'tls_subject']
        for each in param_wo_process:
            if self.module.params.get(each) is not None:
                host_params[each] = self.module.params[each]

        # host groups
        if self.module.params.get('hostgroups') is not None:
            # Check host groups for empty
            if len(self.module.params.get('hostgroups')) == 0:
                self.module.fail_json(
                    msg="Cannot remove all host groups from a host")
            # Get existing groups from Zabbix
            groups = self.zapi.find_zabbix_hostgroups_by_names(
                self.module.params['hostgroups'])
            if self.check_elements(
                    self.module.params['hostgroups'],
                    [g['name'] for g in groups]):
                groups = [{'groupid': g['groupid']} for g in groups]
                host_params['groups'] = groups
        else:
            if exist_host is None:
                self.module.fail_json(
                    msg="Required parameter not found: hostgroups")

        # templates
        if self.module.params.get('templates') is not None:
            host_params['templates'] = []
            if len(self.module.params.get('templates')) != 0:
                templates = self.zapi.find_zabbix_templates_by_names(
                    self.module.params['templates'])
                if self.check_elements(
                        self.module.params['templates'],
                        [t['name'] for t in templates]):
                    templ = [{'templateid': t['templateid']} for t in templates]
                    host_params['templates'] = templ

        # proxy
        if self.module.params.get('proxy') is not None:
            if len(self.module.params.get('proxy')) == 0:
                if Zabbix_version(self.zbx_api_version) < Zabbix_version('7.0.0'):
                    host_params['proxy_hostid'] = '0'
                else:
                    host_params['proxyid'] = '0'
                    host_params['monitored_by'] = '0'
            else:
                proxy = self.zapi.find_zabbix_proxy_by_names(
                    self.module.params['proxy'])
                if len(proxy) > 0:
                    if Zabbix_version(self.zbx_api_version) < Zabbix_version('7.0.0'):
                        host_params['proxy_hostid'] = proxy[0]['proxyid']
                    else:
                        host_params['proxyid'] = proxy[0]['proxyid']
                        host_params['monitored_by'] = '1'
                else:
                    self.module.fail_json(
                        msg="Proxy not found in Zabbix: {0}".format(
                            self.module.params.get('proxy')))

        # proxy group
        if self.module.params.get('proxy_group') is not None:
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
                if len(self.module.params.get('proxy_group')) == 0:
                    host_params['proxy_groupid'] = '0'
                    host_params['monitored_by'] = '0'
                else:
                    proxy_groups = self.zapi.find_zabbix_proxy_groups_by_names(
                        self.module.params['proxy_group'])
                    if len(proxy_groups) > 0:
                        host_params['proxy_groupid'] = proxy_groups[0]['proxy_groupid']
                        host_params['monitored_by'] = '2'
                    else:
                        self.module.fail_json(
                            msg="Proxy group not found in Zabbix: {0}".format(
                                self.module.params.get('proxy_group')))
            else:
                self.module.fail_json(msg="Incorrect arguments for Zabbix version < 7.0.0: proxy_group")

        # status
        if self.module.params.get('status'):
            if self.module.params['status'] == 'enabled':
                host_params['status'] = '0'
            else:
                host_params['status'] = '1'

        # macros
        if self.module.params.get('macros') is not None:
            host_params['macros'] = []
            for each in self.module.params.get('macros'):
                macro = {
                    'macro': self.check_macro_name(each['macro']),
                    'value': each['value'],
                    'type': macro_types.get(each['type']),
                    'description': each['description']}
                host_params['macros'].append(macro)

        # IPMI
        if self.module.params.get('ipmi_authtype') is not None:
            host_params['ipmi_authtype'] = ipmi_authtype_type.get(
                self.module.params.get('ipmi_authtype'))
        if self.module.params.get('ipmi_privilege') is not None:
            host_params['ipmi_privilege'] = ipmi_privilege_type.get(
                self.module.params.get('ipmi_privilege'))

        # Check the current encryption settings if the host exists.
        # If the host exists and already has PSK encryption,
        # then the tls_psk and tls_psk_identity parameters are optional.
        if (self.module.params.get('tls_accept') is not None or
                self.module.params.get('tls_connect') is not None):
            exist_psk_keys = False
            if exist_host is not None:
                if (exist_host['tls_accept'] in ['2', '3', '6', '7'] or
                        exist_host['tls_connect'] == '2'):
                    exist_psk_keys = True

        # tls_accept
        if self.module.params.get('tls_accept') is not None:
            result_dec_num = 0
            for each in self.module.params.get('tls_accept'):
                result_dec_num += tls_type.get(each)
            # if empty list of types == unencrypted
            if result_dec_num == 0:
                result_dec_num = 1
            host_params['tls_accept'] = str(result_dec_num)
            # check PSK params
            if 'psk' in self.module.params.get('tls_accept'):
                if (('tls_psk_identity' not in host_params or
                        'tls_psk' not in host_params) and exist_psk_keys is False):
                    self.module.fail_json(msg="Missing TLS PSK params")

        # tls_connect
        if self.module.params.get('tls_connect') is not None:
            if self.module.params.get('tls_connect') == '':
                host_params['tls_connect'] = '1'
            else:
                host_params['tls_connect'] = str(tls_type.get(
                    self.module.params.get('tls_connect')))
            # check PSK params
            if host_params['tls_connect'] == '2':
                if (('tls_psk_identity' not in host_params or
                        'tls_psk' not in host_params) and exist_psk_keys is False):
                    self.module.fail_json(msg="Missing TLS PSK params")

        # inventory mode
        if self.module.params.get('inventory_mode') is not None:
            host_params['inventory_mode'] = inventory_mode_types[
                self.module.params.get('inventory_mode')]

        # future inventory mode
        future_inventory_mode = '0'
        if self.module.params.get('inventory_mode') is not None:
            future_inventory_mode = host_params['inventory_mode']
            inventory_disable_reason_msg = 'Inventory mode is set to disabled in the task'
        else:
            if exist_host is not None:
                future_inventory_mode = exist_host['inventory_mode']
                inventory_disable_reason_msg = 'Inventory mode is set to disabled on the host'

        # Inventory
        if self.module.params.get('inventory') is not None:
            if future_inventory_mode == '-1':
                self.module.fail_json(
                    msg="Inventory parameters not applicable. {0}".format(inventory_disable_reason_msg))
            inventory = {}
            param_inventory = self.module.params.get('inventory')
            for each in param_inventory:
                if each in inventory_fields.values():
                    if (future_inventory_mode == '1' and hasattr(self, 'inventory_links') and
                            each in self.inventory_links):
                        self.module.fail_json(
                            msg="Inventory field '{0}' is already linked to the item '{1}' and cannot be updated".format(
                                each, self.inventory_links[each]))
                    else:
                        inventory[each] = param_inventory[each]
                else:
                    self.module.fail_json(
                        msg="Unknown inventory param: {0} Available: {1}".format(
                            each, ', '.join(inventory_fields.values())))
            if inventory:
                host_params['inventory'] = inventory

        # interface
        if self.module.params.get('interfaces') is not None:
            host_params['interfaces'] = []
            interface_by_type = dict((k, []) for k in interface_types)
            for each in self.module.params.get('interfaces'):
                interface = {}
                # resolve_type
                interface['type'] = interface_types.get(each['type'])
                interface['main'] = '1'
                interface['useip'] = '1' if each['useip'] else '0'
                # ip
                if (each['useip'] is True and (each['ip'] is None or len(each['ip']) == 0)):
                    interface['ip'] = '127.0.0.1'
                else:
                    interface['ip'] = each['ip']
                # DNS
                if (each['useip'] is False and (each['dns'] is None or len(each['dns']) == 0)):
                    self.module.fail_json(msg="Required parameter not found: dns")
                else:
                    interface['dns'] = each['dns']
                # ports
                if each['port'] is not None:
                    interface['port'] = each['port']
                else:
                    interface['port'] = default_values['ports'][each['type']]
                # SNMP
                details = []
                if each['type'] == 'snmp':
                    # Check the required fields for SNMP
                    if each['details'] is None:
                        self.module.fail_json(msg="Required parameter for SNMP interface not found: details")
                    if each['details']['version'] is None:
                        self.module.fail_json(msg="Required parameter not found: version")
                    if each['details']['version'] in ['1', '2']:
                        req_parameters = snmp_parameters[each['details']['version']]
                    else:
                        if each['details']['securitylevel'] is None:
                            self.module.fail_json(msg="Required parameter not found: securitylevel")
                        req_parameters = snmp_parameters[each['details']['version']][each['details']['securitylevel']]

                    # If additional fields need to be added and some logic is required, then this can be done here.
                    # If the new field only depends on the version, then it must be added to the helper.
                    if each['details']['version'] in ['2', '3'] and (Zabbix_version(self.zbx_api_version) >= Zabbix_version('6.4.0')):
                        req_parameters.append('max_repetitions')

                    input_arguments = [e for e in each['details'] if each['details'][e] is not None]
                    more_parameters = list(set(input_arguments) - set(req_parameters))
                    less_parameters = list(set(req_parameters) - set(input_arguments))
                    if more_parameters:
                        self.module.fail_json(msg="Incorrect arguments for SNMPv{0}: {1}".format(
                            each['details']['version'],
                            ', '.join(more_parameters)))
                    if less_parameters:
                        self.module.fail_json(msg="Required parameter not found for SNMPv{0}: {1}".format(
                            each['details']['version'],
                            ', '.join(less_parameters)))

                    details = {}
                    # v1 and v2c
                    details['version'] = each['details']['version']
                    details['bulk'] = '1' if each['details']['bulk'] else '0'
                    # Only for Zabbix versions above 6.4
                    if Zabbix_version(self.zbx_api_version) >= Zabbix_version('6.4.0'):
                        if details['version'] == '2' or details['version'] == '3':
                            details['max_repetitions'] = each['details']['max_repetitions']
                    # v3
                    if details['version'] == '3':
                        details['contextname'] = each['details']['contextname']
                        details['securityname'] = each['details']['securityname']
                        details['securitylevel'] = snmp_securitylevel_types[each['details']['securitylevel']]
                        details['authprotocol'] = '0'
                        details['authpassphrase'] = ''
                        details['privprotocol'] = '0'
                        details['privpassphrase'] = ''
                        # authNoPriv
                        if details['securitylevel'] in ['1', '2']:
                            details['authprotocol'] = snmp_authprotocol_types[each['details']['authprotocol']]
                            details['authpassphrase'] = each['details']['authpassphrase']
                        # authPriv
                        if details['securitylevel'] == '2':
                            details['privprotocol'] = snmp_privprotocol_types[each['details']['privprotocol']]
                            details['privpassphrase'] = each['details']['privpassphrase']
                    else:
                        details['community'] = each['details']['community']

                interface['details'] = details

                interface_by_type[each['type']].append(interface)

            # Check count of interfaces
            for interface in interface_by_type:
                if len(interface_by_type[interface]) == 0:
                    continue
                if len(interface_by_type[interface]) > 1:
                    # If more than 1 interface of any type is specified in task
                    self.module.fail_json(
                        msg="{0} {1} interfaces defined in the task. Module supports only 1 interface of each type.".format(
                            len(interface_by_type[interface]), interface))
                else:
                    host_params['interfaces'].extend(interface_by_type[interface])

        return host_params

    def compare_zabbix_host(self, exist_host, new_host):
        """
        The function compares the parameters of an existing host with the
        desired new host parameters.

        :param exist_host: parameters of existing Zabbix host
        :type exist_host: dict
        :param new_host: parameters of desired host
        :type new_host: dict

        :rtype: dict
        :return: difference between existing and desired parameters.
        """
        param_to_update = {}

        # These parameters don't require additional processing
        wo_process = ['status', 'description', 'ipmi_authtype', 'proxy_hostid',
                      'ipmi_privilege', 'ipmi_username', 'ipmi_password',
                      'inventory_mode', 'tls_accept', 'tls_psk_identity',
                      'tls_psk', 'tls_issuer', 'tls_subject', 'tls_connect',
                      'monitored_by', 'proxy_groupid', 'proxyid']
        for each in wo_process:
            if (new_host.get(each) is not None and
                    new_host.get(each) != exist_host.get(each)):
                param_to_update[each] = new_host[each]

        # hostgroups
        if new_host.get('groups'):
            diff_groups = list(
                set([g['groupid'] for g in new_host['groups']]) ^
                set([g['groupid'] for g in exist_host['groups']]))
            if diff_groups:
                param_to_update['groups'] = new_host['groups']

        # templates
        if new_host.get('templates') is not None:
            diff_templ = list(
                set([g['templateid'] for g in new_host['templates']]) ^
                set([g['templateid'] for g in exist_host['parentTemplates']]))

            if diff_templ:
                param_to_update['templates'] = new_host['templates']
                # list of templates to clean
                templates_clear = list(
                    set([g['templateid'] for g in exist_host['parentTemplates']]) -
                    set([g['templateid'] for g in new_host['templates']]))
                if templates_clear:
                    param_to_update['templates_clear'] = [{'templateid': t} for t in templates_clear]

        # visible name
        if new_host.get('name') is not None:
            if len(new_host['name']) == 0:
                new_host['name'] = exist_host['host']
            if new_host.get('name') != exist_host['name']:
                param_to_update['name'] = new_host['name']

        # tags
        if new_host.get('tags') is not None:
            old_tags = tag_to_dict_transform(exist_host['tags'])
            new_tags = tag_to_dict_transform(new_host['tags'])

            if len(list(set(old_tags) ^ set(new_tags))) != 0:
                param_to_update['tags'] = new_host['tags']
            else:
                for tag in new_tags:
                    if len(list(set(new_tags[tag]) ^ set(old_tags[tag]))) > 0:
                        param_to_update['tags'] = new_host['tags']
                        break

        # macros
        if new_host.get('macros') is not None:
            # dict() for compatibility with python 2.6
            new_macro = dict((m['macro'], m) for m in new_host['macros'])
            old_macro = dict((m['macro'], m) for m in exist_host['macros'])

            if len(list(set(new_macro) ^ set(old_macro))) != 0:
                param_to_update['macros'] = new_host['macros']
            else:
                for macro in new_macro:
                    if new_macro[macro]['value'] != old_macro[macro].get('value'):
                        param_to_update['macros'] = new_host['macros']
                        break
                    if new_macro[macro]['type'] != old_macro[macro]['type']:
                        param_to_update['macros'] = new_host['macros']
                        break
                    if new_macro[macro]['description'] != old_macro[macro]['description']:
                        param_to_update['macros'] = new_host['macros']
                        break

        # inventory
        if new_host.get('inventory') is not None:
            new_inventory = {}
            if len(exist_host['inventory']) > 0:
                for each in new_host['inventory']:
                    if new_host['inventory'][each] != exist_host['inventory'].get(each):
                        new_inventory[each] = new_host['inventory'][each]
            else:
                new_inventory = dict(new_host['inventory'])
            if new_inventory:
                param_to_update['inventory'] = new_inventory

        # interfaces
        if new_host.get('interfaces') is not None:
            # Check the number of interfaces by type on the host
            interfaces_types_name = dict((v, k) for k, v in interface_types.items())
            exist_interfaces_by_type = dict((v, 0) for v in interface_types.values())
            for interface in exist_host['interfaces']:
                exist_interfaces_by_type[interface['type']] += 1

            for each in exist_interfaces_by_type:
                if exist_interfaces_by_type[each] > 1:
                    self.module.fail_json(
                        msg="Detected {0} {1} interfaces on the host. Module supports only 1 interface of each type. Please resolve conflict manually.".format(
                            exist_interfaces_by_type[each],
                            interfaces_types_name[each]))

            # Check the differences between interfaces
            interface_updating_flag = False
            new_interfaces = []
            if len(new_host['interfaces']) != len(exist_host['interfaces']):
                interface_updating_flag = True

            for each in new_host['interfaces']:
                for interface in exist_host['interfaces']:
                    if each['type'] == interface['type']:
                        total_interface = each
                        total_interface['interfaceid'] = interface['interfaceid']
                        new_interfaces.append(total_interface)
                        if total_interface != interface:
                            interface_updating_flag = True
                        break
                else:
                    new_interfaces.append(each)
                    interface_updating_flag = True

            if interface_updating_flag is True:
                param_to_update['interfaces'] = new_interfaces

        return param_to_update


def main():
    """entry point for module execution"""

    spec = {
        'state': {
            'type': 'str',
            'default': 'present',
            'choices': ['present', 'absent']},
        'host': {
            'type': 'str',
            'required': True,
            'aliases': ['host_name']},
        'hostgroups': {
            'type': 'list',
            'elements': 'str',
            'aliases': ['host_group', 'host_groups']},
        'templates': {
            'type': 'list',
            'elements': 'str',
            'aliases': ['link_templates', 'host_templates', 'template']},
        'status': {
            'type': 'str',
            'choices': ['enabled', 'disabled']},
        'description': {'type': 'str'},
        'name': {
            'type': 'str',
            'aliases': ['visible_name']},
        'tags': {
            'type': 'list',
            'elements': 'dict',
            'aliases': ['host_tags'],
            'options': {
                'tag': {'type': 'str', 'required': True},
                'value': {'type': 'str', 'default': ''}}},
        'macros': {
            'type': 'list',
            'elements': 'dict',
            'aliases': ['user_macros', 'user_macro'],
            'options': {
                'macro': {'type': 'str', 'required': True},
                'value': {'type': 'str', 'default': ''},
                'description': {'type': 'str', 'default': ''},
                'type': {
                    'type': 'str',
                    'choices': ['text', 'secret', 'vault_secret'],
                    'default': 'text'}}},
        'ipmi_authtype': {
            'type': 'str',
            'choices': ['default', 'none', 'md2', 'md5',
                        'straight', 'oem', 'rmcp+']},
        'ipmi_privilege': {
            'type': 'str',
            'choices': ['callback', 'user', 'operator', 'admin', 'oem']},
        'ipmi_username': {'type': 'str'},
        'ipmi_password': {'type': 'str', 'no_log': True},
        'tls_accept': {
            'type': 'list',
            'elements': 'str',
            'choices': ['unencrypted', 'psk', 'cert']},
        'tls_connect': {
            'type': 'str',
            'choices': ['', 'unencrypted', 'psk', 'cert']},
        'tls_psk_identity': {'type': 'str', 'no_log': True},
        'tls_psk': {'type': 'str', 'no_log': True},
        'tls_issuer': {'type': 'str'},
        'tls_subject': {'type': 'str'},
        'proxy': {'type': 'str'},
        'proxy_group': {'type': 'str'},
        'inventory_mode': {
            'type': 'str',
            'choices': ['automatic', 'manual', 'disabled']},
        'inventory': {
            'type': 'dict',
            'aliases': ['inventory_zabbix', 'host_inventory']},
        'interfaces': {
            'type': 'list',
            'elements': 'dict',
            'options': {
                'type': {
                    'type': 'str',
                    'required': True,
                    'choices': ['agent', 'snmp', 'ipmi', 'jmx']},
                'useip': {'type': 'bool', 'default': True},
                'ip': {'type': 'str', 'default': ''},
                'dns': {'type': 'str', 'default': ''},
                'port': {'type': 'str'},
                'details': {
                    'type': 'dict',
                    'options': {
                        'version': {'type': 'str', 'choices': ['1', '2', '3']},
                        'bulk': {'type': 'bool'},
                        'community': {'type': 'str'},
                        'max_repetitions': {'type': 'str'},
                        'contextname': {'type': 'str'},
                        'securityname': {'type': 'str'},
                        'securitylevel': {
                            'type': 'str',
                            'choices': ['noAuthNoPriv', 'authNoPriv', 'authPriv']},
                        'authprotocol': {
                            'type': 'str',
                            'choices': ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']},
                        'authpassphrase': {'type': 'str', 'no_log': True},
                        'privprotocol': {
                            'type': 'str',
                            'choices': ['des', 'aes128', 'aes192', 'aes256', 'aes192c', 'aes256c']},
                        'privpassphrase': {'type': 'str', 'no_log': True}}}}}}

    module = AnsibleModule(
        argument_spec=spec,
        mutually_exclusive=[('proxy', 'proxy_group')],
        required_together=[('tls_psk_identity', 'tls_psk')],
        supports_check_mode=True)

    state = module.params['state']
    host_name = module.params['host']

    host = Host(module)

    # Find a host in Zabbix
    result = host.zapi.find_zabbix_host_by_host(host_name)

    if state == 'present':

        if len(result) > 0:
            # Get the parameters of an existing host
            exist_host_params = host.get_zabbix_host(result[0]['hostid'])
            # Generate new host parameters
            new_host_params = host.generate_zabbix_host(exist_host_params)

            # Compare all parameters
            compare_result = host.compare_zabbix_host(
                exist_host_params,
                new_host_params)

            if compare_result:
                # Update host
                compare_result['hostid'] = result[0]['hostid']

                update_result = host.host_api_request(
                    method='host.update',
                    params=compare_result)

                if update_result:
                    module.exit_json(
                        changed=True,
                        result="Successfully updated host: {0}".format(
                            host_name))
                else:
                    module.fail_json(
                        msg="Failed to update host: {0}".format(host_name))
            else:
                # No need to update
                module.exit_json(
                    changed=False,
                    result="No need to update host: {0}".format(host_name))

        else:
            # Create host
            new_host_params = host.generate_zabbix_host()

            result = host.host_api_request(
                method='host.create',
                params=new_host_params)
            if result:
                module.exit_json(
                    changed=True,
                    result="Successfully created host: {0}".format(host_name))
            else:
                module.fail_json(
                    msg="Failed to create host: {0}".format(host_name))

    else:
        if len(result) > 0:
            # delete host
            delete_result = host.host_api_request(
                method='host.delete',
                params=[result[0]['hostid']])
            if delete_result:
                module.exit_json(
                    changed=True,
                    result="Successfully delete host: {0}".format(host_name))
            else:
                module.fail_json(
                    msg="Failed to delete host: {0}".format(host_name))
        else:
            # No need to delete host
            module.exit_json(
                changed=False,
                result="No need to delete host: {0}".format(host_name))


if __name__ == '__main__':
    main()
