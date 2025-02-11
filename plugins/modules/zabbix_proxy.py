#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zabbix_proxy
short_description: Module for creating, deleting and updating existing proxyes.
description:
    - The module is designed to create, update or delete a proxy in Zabbix.
    - In case of updating an existing proxy, only the specified parameters will be updated.
author:
    - Zabbix Ltd (@zabbix)
requirements:
    - "python >= 2.6"
options:
    state:
        description: Create or delete proxy.
        required: false
        type: str
        default: present
        choices: [ present, absent ]
    name:
        description: Name of the proxy.
        type: str
        required: true
    mode:
        description: Type of proxy. Active or passive.
        type: str
        choices: [ active, passive ]
        aliases: [ operating_mode ]
    proxy_group:
        description:
            - Name of the proxy group that is used to monitor the host.
            - Used only for Zabbix versions above 7.0.
            - Set empty to exclude the proxy from the proxy group.
        type: str
    local_address:
        description:
            - Address for active agents. IP address or DNS name to connect to.
            - Used only for Zabbix versions above 7.0.
            - Required if I(proxy_group) is not empty.
            - Set empty to clean.
        type: str
    local_port:
        description:
            - Local proxy port number to connect to.
            - Used only for Zabbix versions above 7.0.
            - Supported if I(proxy_group) is not empty.
            - Set empty or '10051' to clean or reset to the default value.
        type: str
    interface:
        description:
            - The proxy interface object defines the interface used to connect to a passive proxy.
            - Supported if I(proxy_mode) is passive.
        type: dict
        suboptions:
            address:
                description:
                    - IP address or DNS name to connect to.
                    - Supported if I(proxy_mode) is passive.
                    - Set empty or '127.0.0.1' to clean or reset to the default value.
                type: str
            port:
                description:
                    - Port number to connect to.
                    - Supported if I(proxy_mode) is passive.
                    - Set empty or '10051' to clean or reset to the default value.
                type: str
            useip:
                description:
                    - Whether the connection should be made through IP or DNS.
                    - In Zabbix versions higher than 7.0 the parameter will be ignored!
                type: bool
    allowed_addresses:
        description:
            - Comma-delimited IP addresses or DNS names of active Zabbix proxy.
            - Supported if I(proxy_mode) is active.
            - Set empty to clean.
        type: str
        aliases: [ proxy_address ]
    tls_connect:
        description:
            - Connections to proxy. Supported only in passive proxy mode.
            - Set empty to clean.
        type: str
        choices: [ '', unencrypted, psk, cert ]
    tls_accept:
        description:
            - Connections from proxy. Supported only in active proxy mode.
            - Set empty list ([]) to clean.
        type: list
        elements: str
        choices: [ unencrypted, psk, cert ]
    tls_psk_identity:
        description:
            - PSK identity.
            - Required if I(tls_connect=psk), or I(tls_accept) contains the 'psk'.
            - If you are creating a new proxy and you have PSK mode (tls_accept or tls_connect), then this parameter is required.
            - In case of updating an existing proxy, if the proxy already has PSK enabled, the parameter is not required.
            - If the parameter is defined, then every launch of the task will update the proxy,
              because Zabbix API does not have access to an existing PSK key and we cannot compare the specified key with the existing one.
        type: str
    tls_psk:
        description:
            - The pre-shared key, at least 32 hex digits.
            - Required if I(tls_connect=psk), or I(tls_accept) contains the 'psk'.
            - If you are creating a new proxy and you have PSK mode (tls_accept or tls_connect), then this parameter is required.
            - In case of updating an existing proxy, if the proxy already has PSK enabled, the parameter is not required.
            - If the parameter is defined, then every launch of the task will update the proxy,
              because Zabbix API does not have access to an existing PSK key and we cannot compare the specified key with the existing one.
        type: str
    tls_issuer:
        description: Certificate issuer.
        type: str
    tls_subject:
        description: Certificate subject.
        type: str
    custom_timeouts:
        description:
            - Whether to override global item timeouts on the proxy level.
            - Set '{}' to clear value and use global timeouts.
            - Used only for Zabbix versions above 7.0.
        type: dict
        aliases: [ timeouts ]
        suboptions:
            timeout_zabbix_agent:
                description: Spend no more than specified seconds on processing of Zabbix agent checks.
                type: str
                aliases: [ zabbix_agent ]
            timeout_simple_check:
                description: Spend no more than specified seconds on processing of simple checks.
                type: str
                aliases: [ simple_check ]
            timeout_snmp_agent:
                description: Spend no more than specified seconds on processing of SNMP checks.
                type: str
                aliases: [ snmp_agent ]
            timeout_external_check:
                description: Spend no more than specified seconds on processing of external checks.
                type: str
                aliases: [ external_check ]
            timeout_db_monitor:
                description: Spend no more than specified seconds on processing of database checks.
                type: str
                aliases: [ db_monitor ]
            timeout_http_agent:
                description: Spend no more than specified seconds on processing of HTTP agent checks.
                type: str
                aliases: [ http_agent ]
            timeout_ssh_agent:
                description: Spend no more than specified seconds on processing of SSH agent checks.
                type: str
                aliases: [ ssh_agent ]
            timeout_telnet_agent:
                description: Spend no more than specified seconds on processing of Telnet checks.
                type: str
                aliases: [ telnet_agent ]
            timeout_script:
                description: Spend no more than specified seconds on processing of script checks.
                type: str
                aliases: [ script ]
            timeout_browser:
                description: Spend no more than specified seconds on processing of browser checks.
                type: str
                aliases: [ browser ]
    description:
        description: Proxy description.
        type: str
'''

EXAMPLES = r'''
# To create proxy with minimum parameters
- name: Create proxy
  zabbix.zabbix.zabbix_proxy:
    state: present
    name: My Zabbix proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To create proxy with maximum parameters
# Part of the parameters depend on the proxy operating mode: active or passive
- name: Create proxy with maximum parameters
  zabbix.zabbix.zabbix_proxy:
    state: present
    name: My Zabbix proxy
    mode: active
    proxy_group: My proxy group
    local_address: 10.10.10.10
    local_port: 10051
    interface:
      address: 127.0.0.1
      port: 10051
    allowed_addresses: 10.10.10.10
    tls_connect: ''
    tls_accept:
      - psk
      - cert
    tls_psk_identity: my_psk
    tls_psk: 12345abcde...
    tls_issuer: my_tls_issuer
    tls_subject: my_tls_subject
    custom_timeouts:
      timeout_zabbix_agent: 10s
      timeout_simple_check: ''                    # To use value from Zabbix global setting
      timeout_snmp_agent: '{$MY_SNMP_TIMEOUT}'    # To use global macro (this macro must exist in the global macro)
      timeout_external_check: 10s
      timeout_db_monitor: 10s
      timeout_http_agent: 10s
      timeout_ssh_agent: 10s
      timeout_telnet_agent: 10s
      timeout_script: 10s
      timeout_browser: 10s
    description: Description of my proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To update proxy to empty parameters
- name: Clean all parameters from proxy
  zabbix.zabbix.zabbix_proxy:
    name: My Zabbix proxy
    mode: active
    proxy_group: ''
    local_address: ''
    local_port: ''
    interface:
      address: ''
      port: ''
    allowed_addresses: ''
    tls_connect: ''
    tls_accept: []
    tls_psk_identity: ''
    tls_psk: ''
    tls_issuer: ''
    tls_subject: ''
    custom_timeouts: {}
    description: ''
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To update only one parameter, you can specify just
# the proxy name (used for searching) and the desired parameter.
# The rest of the proxy parameters will not be changed.
# For example, if you want to update proxy description
# you can use the following example
- name: Update proxy description
  zabbix.zabbix.zabbix_proxy:
    name: My Zabbix proxy
    description: Description of my proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To remove a proxy, you can use:
- name: Delete proxy
  zabbix.zabbix.zabbix_proxy:
    state: absent
    name: My Zabbix proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# You can configure Zabbix API connection settings with the following parameters:
- name: Create zabbix proxy
  zabbix.zabbix.zabbix_proxy:
    state: present
    name: My Zabbix proxy
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
from ansible_collections.zabbix.zabbix.plugins.module_utils.zabbix_api import ZabbixApi
from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    Zabbix_version, default_values, tls_type, proxy_timeouts)


class Proxy(object):

    def __init__(self, module):
        self.module = module
        self.zapi = ZabbixApi(module)
        self.zbx_api_version = self.zapi.api_version()

    def get_zabbix_proxy(self, proxyid):
        """
        The function gets all information about an existing proxy in Zabbix.

        :param proxyid: proxyid for search
        :type proxyid: str|int

        :rtype: dict
        :returns:
            *   dict with proxy parameters if proxy exists
            *   empty dict if proxy does not exist
        """
        proxy = {}
        if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
            params = {
                'output': 'extend',
                'selectProxyGroup': ['name'],
                'proxyids': proxyid}
        else:
            params = {
                'output': 'extend',
                'selectInterface': 'extend',
                'proxyids': proxyid}

        try:
            proxy = self.zapi.send_api_request(
                method='proxy.get',
                params=params)
        except Exception as e:
            self.module.fail_json(msg="Failed to get existing proxy: {0}".format(e))

        return proxy[0]

    def api_request(self, method, params):
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

    def check_interface_param(self, param, proxy_mode, default_pname=None):
        """
        This function checks that the current interface settings can be used
        with the specified proxy mode.
        The function also returns default settings when an empty parameter is specified.

        :param param: name of the parameter
        :type param: str
        :param proxy_mode: current (desired) proxy mode ('0','5' - active, '1','6' - passive)
        :type proxy_mode: str
        :param default_pname: name of the parameter in dict of default values
        :type default_pname: str

        :rtype: str
        :return: value of the parameter
        """
        value = self.module.params['interface'][param]
        default_pname = default_pname or 'proxy_{}'.format(param)

        if len(value) == 0:
            return default_values[default_pname]

        elif (proxy_mode in ['0', '5']
                and self.module.params['interface'][param] != default_values[default_pname]):
            self.module.fail_json(
                msg="Incorrect argument: {}. Available only in passive proxy mode. "
                "In active proxy mode value must be empty or '{}'.".format(
                    param,
                    default_values[default_pname]))

        return value

    def generate_zabbix_proxy(self, exist_proxy=None):
        """
        The function generates the desired proxy parameters based on the module
        parameters.
        The returned dictionary can be used to create a proxy, as well as to
        compare with an existing proxy.

        :param exist_proxy: parameters of existing Zabbix proxy
        :type exist_proxy: dict

        :rtype: dict
        :return: parameters of desired proxy

        note::
            *  The 'exist_proxy' parameter is used to determine the current
               operational mode and all dependent settings on existing proxy.
        """
        # Proxy field names for compatibility beetwen 6.0 and 7.0+
        proxy_fnames = {}
        if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
            proxy_fnames['mode'] = 'operating_mode'
            proxy_fnames['name'] = 'name'
            proxy_fnames['allowed_addresses'] = 'allowed_addresses'
        else:
            proxy_fnames['mode'] = 'status'
            proxy_fnames['name'] = 'host'
            proxy_fnames['allowed_addresses'] = 'proxy_address'

        proxy_params = {}

        # Name
        proxy_params[proxy_fnames['name']] = self.module.params['name']

        # These parameters don't require additional processing
        param_wo_process = ['description', 'tls_psk', 'tls_psk_identity', 'tls_issuer', 'tls_subject']
        for each in param_wo_process:
            if self.module.params.get(each) is not None:
                proxy_params[each] = self.module.params[each]

        # Operating mode (active / passive)
        #
        # 'operating_mode' for Zabbix version 7.0 +
        # 'status' for Zabbix version 6.0
        if self.module.params.get('mode') is not None:
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
                proxy_params[proxy_fnames['mode']] = '0' if self.module.params['mode'] == 'active' else '1'
            else:
                proxy_params[proxy_fnames['mode']] = '5' if self.module.params['mode'] == 'active' else '6'
        else:
            # Set proxy mode based on existing proxy
            if exist_proxy is not None:
                proxy_params[proxy_fnames['mode']] = exist_proxy[proxy_fnames['mode']]
            else:
                # Set proxy mode based on default value
                if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
                    proxy_params[proxy_fnames['mode']] = default_values['proxy_mode']['7']
                else:
                    proxy_params[proxy_fnames['mode']] = default_values['proxy_mode']['6.0']

        # Find the future proxy group status
        # Used for 'local address'
        feature_proxy_group, configured_proxy_group = False, False
        if exist_proxy is not None and exist_proxy.get('proxy_groupid', '0') != '0':
            feature_proxy_group, configured_proxy_group = True, True

        # proxy_group
        #
        # Only for Zabbix version 7.0 +
        if self.module.params.get('proxy_group') is not None:
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):

                # Clear proxy group
                if len(self.module.params.get('proxy_group')) == 0:
                    proxy_params['proxy_groupid'] = '0'
                    feature_proxy_group = False

                # Find proxy group by name and set it's id
                else:
                    proxy_groups = self.zapi.find_zabbix_proxy_groups_by_names(
                        self.module.params['proxy_group'])
                    if len(proxy_groups) > 0:
                        proxy_params['proxy_groupid'] = proxy_groups[0]['proxy_groupid']
                        feature_proxy_group = True
                    else:
                        self.module.fail_json(msg="Proxy group not found in Zabbix: {0}".format(
                            self.module.params.get('proxy_group')))
            else:
                self.module.fail_json(msg="Incorrect arguments for Zabbix version < 7.0.0: proxy_group")

        # local_address
        #
        # Only for Zabbix version 7.0 +
        if self.module.params.get('local_address') is not None:
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
                # Proxy group will be used on proxy (in task or already exist on proxy)
                if feature_proxy_group is True:
                    if len(self.module.params['local_address']) > 0:
                        proxy_params['local_address'] = self.module.params['local_address']
                    else:
                        self.module.fail_json(
                            msg="Incorrect argument: local_address. Can not be empty with configured proxy group.")
                # Proxy group will NOT be used on proxy
                else:
                    if len(self.module.params['local_address']) > 0:
                        self.module.fail_json(
                            msg="Incorrect argument: local_address. Can be used only with proxy group.")
            else:
                self.module.fail_json(msg="Incorrect arguments for Zabbix version < 7.0.0: local_address.")
        else:
            if feature_proxy_group is True and configured_proxy_group is False:
                self.module.fail_json(msg="Not found required argument: local_address")

        # local_port
        #
        # Only for Zabbix verion 7.0 +
        if self.module.params.get('local_port') is not None:
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
                proxy_params['local_port'] = self.module.params['local_port']

                # Cleaning of value / reset to default
                if len(proxy_params['local_port']) == 0:
                    proxy_params['local_port'] = default_values['proxy_port']

                # Check value
                elif self.module.params['local_port'] != default_values['proxy_port']:
                    if feature_proxy_group is False:
                        self.module.fail_json(
                            msg="Incorrect argument: local_port. Can be used only with proxy group. "
                            "Without proxy group value must be '{}' or empty.".format(default_values['proxy_port']))
            else:
                self.module.fail_json(msg="Incorrect arguments for Zabbix version < 7.0.0: local_port.")

        # Interface
        #
        # Versions 6.0 and 7.0+ have different structure and therefore
        # this block is divided based on the Zabbox version.
        if self.module.params.get('interface') is not None:
            # Zabbix version >= 7.0
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):
                # Address
                if self.module.params['interface'].get('address') is not None:
                    proxy_params['address'] = self.check_interface_param(
                        'address', proxy_params[proxy_fnames['mode']])

                # Port
                if self.module.params['interface'].get('port') is not None:
                    proxy_params['port'] = self.check_interface_param(
                        'port', proxy_params[proxy_fnames['mode']])

            # Zabbix version < 7.0
            else:
                # Useip
                if self.module.params['interface'].get('useip') is not None:
                    # Use value from task
                    proxy_useip = self.module.params['interface']['useip']
                elif exist_proxy is not None and len(exist_proxy['interface']) > 0:
                    # Use value from existing proxy
                    proxy_useip = True if exist_proxy['interface']['useip'] == '1' else False
                else:
                    # Use default value
                    proxy_useip = default_values['proxy_useip']

                # Address
                if self.module.params['interface'].get('address') is not None:
                    # Use value from task
                    if proxy_useip is True:
                        proxy_address = self.check_interface_param('address', proxy_params[proxy_fnames['mode']])
                    else:
                        proxy_address = self.check_interface_param(
                            'address', proxy_params[proxy_fnames['mode']], 'proxy_dns')
                elif exist_proxy is not None and len(exist_proxy['interface']) > 0:
                    # Use value from existing proxy
                    if proxy_useip is True:
                        proxy_address = exist_proxy['interface']['ip'] or default_values['proxy_address']
                    else:
                        proxy_address = exist_proxy['interface']['dns'] or default_values['proxy_dns']
                else:
                    # Use default value
                    if proxy_useip is True:
                        proxy_address = default_values['proxy_address']
                    else:
                        proxy_address = default_values['proxy_dns']

                # Port
                if self.module.params['interface'].get('port') is not None:
                    # Use value from task
                    proxy_port = self.check_interface_param('port', proxy_params[proxy_fnames['mode']])
                elif exist_proxy is not None and len(exist_proxy['interface']) > 0:
                    # Use value from existing proxy
                    proxy_port = exist_proxy['interface']['port']
                else:
                    # Use default value
                    proxy_port = default_values['proxy_port']

                # Set interface structure
                if proxy_params[proxy_fnames['mode']] in ['0', '5']:
                    proxy_params['interface'] = []
                else:
                    proxy_params['interface'] = {'port' : proxy_port}
                    if proxy_useip is True:
                        proxy_params['interface']['ip'] = proxy_address
                        proxy_params['interface']['useip'] = '1'
                        proxy_params['interface']['dns'] = ''
                    else:
                        proxy_params['interface']['ip'] = ''
                        proxy_params['interface']['useip'] = '0'
                        proxy_params['interface']['dns'] = proxy_address

        else:
            if (proxy_params[proxy_fnames['mode']] == '6' and
                    Zabbix_version(self.zbx_api_version) < Zabbix_version('7.0.0')):
                if exist_proxy is not None and isinstance(exist_proxy['interface'], dict):
                    # Set interface based on existing proxy interface
                    proxy_params['interface'] = {
                        'port': exist_proxy['interface']['port'],
                        'ip': exist_proxy['interface']['ip'],
                        'useip': exist_proxy['interface']['useip'],
                        'dns': exist_proxy['interface']['dns']}
                else:
                    # Set interface by default
                    proxy_params['interface'] = {
                        'port': default_values['proxy_port'],
                        'ip': default_values['proxy_address'],
                        'useip': '1' if default_values['proxy_useip'] is True else '0',
                        'dns': default_values['proxy_dns']}

        # allowed_addresses
        #
        # 'allowed_addresses' for Zabbix verion 7.0 +
        # 'proxy_address' for Zabbix verion 6.0
        if self.module.params.get('allowed_addresses') is not None:
            proxy_params[proxy_fnames['allowed_addresses']] = self.module.params['allowed_addresses']

            # Check for error
            if (proxy_params[proxy_fnames['mode']] in ['1', '6']
                    and self.module.params['allowed_addresses'] != ''):
                self.module.fail_json(
                    msg="Incorrect argument: {}. Available only in active proxy mode. "
                        "In passive proxy mode value must be empty.".format(
                            proxy_fnames['allowed_addresses']))

        # Check the current encryption settings if the proxy exists.
        # If the proxy exists and already has PSK encryption,
        # then the 'tls_psk' and 'tls_psk_identity' parameters are optional.
        if (self.module.params.get('tls_accept') is not None or
                self.module.params.get('tls_connect') is not None):
            exist_psk_keys = False
            if exist_proxy is not None:
                if (exist_proxy['tls_accept'] in ['2', '3', '6', '7'] or
                        exist_proxy['tls_connect'] == '2'):
                    exist_psk_keys = True

        # tls_accept
        #
        # Only for active proxy mode
        if self.module.params.get('tls_accept') is not None:
            result_dec_num = 0
            for each in self.module.params.get('tls_accept'):
                result_dec_num += tls_type.get(each)
            # if empty list of types == unencrypted
            if result_dec_num == 0:
                result_dec_num = 1
            proxy_params['tls_accept'] = str(result_dec_num)

            # check PSK params
            if 'psk' in self.module.params.get('tls_accept'):
                if (('tls_psk_identity' not in proxy_params or
                        'tls_psk' not in proxy_params) and exist_psk_keys is False):
                    self.module.fail_json(msg="Missing TLS PSK params")
            if proxy_params[proxy_fnames['mode']] in ['1', '6'] and proxy_params['tls_accept'] != '1':
                self.module.fail_json(msg="Incorrect argument: tls_accept. Available only in active proxy mode.")

        # tls_connect
        #
        # Only for passive proxy mode
        if self.module.params.get('tls_connect') is not None:
            if self.module.params.get('tls_connect') == '':
                # Reset to default
                proxy_params['tls_connect'] = '1'
            else:
                proxy_params['tls_connect'] = str(tls_type.get(
                    self.module.params.get('tls_connect')))

            # check PSK params
            if proxy_params['tls_connect'] == '2':
                if (('tls_psk_identity' not in proxy_params or
                        'tls_psk' not in proxy_params) and exist_psk_keys is False):
                    self.module.fail_json(msg="Missing TLS PSK params")
            if proxy_params[proxy_fnames['mode']] in ['0', '5'] and proxy_params['tls_connect'] != '1':
                self.module.fail_json(msg="Incorrect argument: tls_connect. Available only in passive proxy mode.")

        # custom_timeouts
        #
        # Only for Zabbix verion 7.0 +
        if self.module.params.get('custom_timeouts') is not None:
            if Zabbix_version(self.zbx_api_version) >= Zabbix_version('7.0.0'):

                # Check that needs to update custom timeouts
                use_global_timeout = True
                for timeout in proxy_timeouts:
                    if self.module.params['custom_timeouts'].get(timeout) is not None:
                        use_global_timeout = False
                        proxy_params[timeout] = self.module.params['custom_timeouts'][timeout]

                # Get global timeouts and add it or exist timeout to the params to update
                if use_global_timeout is False:
                    proxy_params['custom_timeouts'] = '1'
                    global_setting = self.zapi.get_global_setting()
                    for setting in global_setting:
                        if setting.startswith('timeout_') and setting not in proxy_params:
                            if exist_proxy is not None and exist_proxy.get(setting) != '':
                                # Use value from existing proxy
                                proxy_params[setting] = exist_proxy[setting]
                            else:
                                # Use global timeout
                                proxy_params[setting] = global_setting[setting]
                        # Reset to the global timeouts
                        elif setting.startswith('timeout_') and proxy_params.get(setting) == '':
                            proxy_params[setting] = global_setting[setting]
                else:
                    # Use global timeouts
                    proxy_params['custom_timeouts'] = '0'

            else:
                self.module.fail_json(msg="Incorrect arguments for Zabbix version < 7.0.0: custom_timeouts.")

        return proxy_params

    def compare_zabbix_proxy(self, exist_proxy, new_proxy):
        """
        The function compares the parameters of an existing proxy with the
        desired new proxy parameters.

        :param exist_proxy: parameters of existing Zabbix proxy
        :type exist_proxy: dict
        :param new_proxy: parameters of desired (generated) proxy
        :type new_proxy: dict

        :rtype: dict
        :return: difference between existing and desired parameters.
        """
        param_to_update = {}

        # These parameters don't require additional processing
        wo_process = ['tls_accept', 'tls_psk_identity',
                      'tls_psk', 'tls_issuer', 'tls_subject', 'tls_connect',
                      'custom_timeouts', 'timeout_zabbix_agent', 'timeout_simple_check',
                      'timeout_snmp_agent', 'timeout_external_check', 'timeout_db_monitor',
                      'timeout_http_agent', 'timeout_ssh_agent', 'timeout_telnet_agent',
                      'timeout_script', 'timeout_browser', 'status', 'operating_mode',
                      'proxy_groupid', 'local_address', 'local_port', 'address', 'port',
                      'allowed_addresses', 'proxy_address', 'description']
        for each in wo_process:
            if (new_proxy.get(each) is not None and
                    new_proxy.get(each) != exist_proxy.get(each)):
                param_to_update[each] = new_proxy[each]

        # Interface
        #
        # Only for 6.0
        if new_proxy.get('interface') is not None:
            if isinstance(exist_proxy['interface'], list) or isinstance(new_proxy['interface'], list):
                if exist_proxy['interface'] != new_proxy['interface']:
                    param_to_update['interface'] = new_proxy['interface']
            else:
                for each in ['ip', 'dns', 'useip', 'port']:
                    if new_proxy['interface'].get(each) != exist_proxy['interface'].get(each):
                        param_to_update['interface'] = new_proxy['interface']
                        break

        return param_to_update


def main():
    """entry point for module execution"""
    spec = {
        'state': {
            'type': 'str',
            'default': 'present',
            'choices': ['present', 'absent']},
        'name': {
            'type': 'str',
            'required': True},
        'mode': {
            'type': 'str',
            'choices': ['active', 'passive'],
            'aliases': ['operating_mode']},
        'proxy_group': {'type': 'str'},
        'local_address': {'type': 'str'},
        'local_port': {'type': 'str'},
        'interface': {
            'type': 'dict',
            'options': {
                'address': {'type': 'str'},
                'port': {'type': 'str'},
                'useip': {'type': 'bool'}}},
        'allowed_addresses': {'type': 'str', 'aliases': ['proxy_address']},
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
        'custom_timeouts': {
            'type': 'dict',
            'aliases': ['timeouts'],
            'options': {
                'timeout_zabbix_agent': {'type': 'str', 'aliases': ['zabbix_agent']},
                'timeout_simple_check': {'type': 'str', 'aliases': ['simple_check']},
                'timeout_snmp_agent': {'type': 'str', 'aliases': ['snmp_agent']},
                'timeout_external_check': {'type': 'str', 'aliases': ['external_check']},
                'timeout_db_monitor': {'type': 'str', 'aliases': ['db_monitor']},
                'timeout_http_agent': {'type': 'str', 'aliases': ['http_agent']},
                'timeout_ssh_agent': {'type': 'str', 'aliases': ['ssh_agent']},
                'timeout_telnet_agent': {'type': 'str', 'aliases': ['telnet_agent']},
                'timeout_script': {'type': 'str', 'aliases': ['script']},
                'timeout_browser': {'type': 'str', 'aliases': ['browser']}}},
        'description': {'type': 'str'}}

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True)

    state = module.params['state']
    proxy_name = module.params['name']

    proxy = Proxy(module)

    # Find a proxy in Zabbix
    result = proxy.zapi.find_zabbix_proxy_by_names(proxy_name)

    if state == 'present':

        if len(result) > 0:
            # Get the parameters of an existing proxy
            exist_proxy_params = proxy.get_zabbix_proxy(result[0]['proxyid'])
            # Generate new proxy parameters
            new_proxy_params = proxy.generate_zabbix_proxy(exist_proxy_params)

            # Compare all parameters
            compare_result = proxy.compare_zabbix_proxy(
                exist_proxy_params,
                new_proxy_params)

            if compare_result:
                # Update host
                compare_result['proxyid'] = result[0]['proxyid']

                update_result = proxy.api_request(
                    method='proxy.update',
                    params=compare_result)

                if update_result:
                    module.exit_json(
                        changed=True,
                        result="Successfully updated proxy: {0}".format(
                            proxy_name))
                else:
                    module.fail_json(
                        msg="Failed to update proxy: {0}".format(proxy_name))
            else:
                # No need to update
                module.exit_json(
                    changed=False,
                    result="No need to update proxy: {0}".format(proxy_name))
        else:
            # Create proxy
            new_proxy_params = proxy.generate_zabbix_proxy()

            result = proxy.api_request(
                method='proxy.create',
                params=new_proxy_params)
            if result:
                module.exit_json(
                    changed=True,
                    result="Successfully created proxy: {0}".format(proxy_name))
            else:
                module.fail_json(
                    msg="Failed to create proxy: {0}".format(proxy_name))
    else:
        if len(result) > 0:
            # delete proxy
            delete_result = proxy.api_request(
                method='proxy.delete',
                params=[result[0]['proxyid']])
            if delete_result:
                module.exit_json(
                    changed=True,
                    result="Successfully delete proxy: {0}".format(proxy_name))
            else:
                module.fail_json(
                    msg="Failed to delete proxy: {0}".format(proxy_name))
        else:
            # No need to delete proxy
            module.exit_json(
                changed=False,
                result="No need to delete proxy: {0}".format(proxy_name))


if __name__ == '__main__':
    main()
