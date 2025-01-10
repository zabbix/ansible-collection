#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zabbix_proxy_group
short_description: Module for creating, deleting and updating existing proxy groups.
description:
    - The module is designed to create, update or delete a proxy group in Zabbix.
    - In case of updating an existing proxy group, only the specified parameters will be updated.
    - Supported only for Zabbix versions above 7.0.
author:
    - Zabbix Ltd (@zabbix)
requirements:
    - "python >= 2.6"
options:
    state:
        description: Create or delete proxy group.
        required: false
        type: str
        default: present
        choices: [ present, absent ]
    name:
        description: Name of the proxy group.
        type: str
        required: true
    failover_delay:
        description:
            - Failover period for each proxy in the group to have online/offline state.
            - Time suffixes are supported, e.g. 30s, 1m.
            - User macros are supported.
            - Possible values beetween 10s-15m.
            - Set empty to reset to the default value.
        type: str
    min_online:
        description:
            - Minimum number of online proxies required for the group to be online.
            - User macros are supported.
            - Possible values range 1-1000.
            - Set empty to reset to the default value.
        type: str
    description:
        description: Description of the proxy group.
        type: str
'''

EXAMPLES = r'''
# To create proxy group with minimum parameters
- name: Create proxy group
  zabbix.zabbix.zabbix_proxy_group:
    state: present
    name: My proxy group
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To create proxy group with maximum parameters
- name: Create proxy group with maximum parameters
  zabbix.zabbix.zabbix_proxy_group:
    state: present
    name: My proxy group
    failover_delay: '1m'
    min_online: '10'
    description: Proxy group description
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To update proxy group to empty parameters
- name: Clean all parameters from proxy group
  zabbix.zabbix.zabbix_proxy_group:
    state: present
    name: My proxy group
    failover_delay: ''
    min_online: ''
    description: ''
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To update only one parameter, you can specify just
# the proxy group name (used for searching) and the desired parameter.
# The rest of the proxy group parameters will not be changed.
# For example, if you want to update proxy group description
# you can use the following example
- name: Update proxy group description
  zabbix.zabbix.zabbix_proxy_group:
    name: My proxy group
    description: Description of my proxy group
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To remove a proxy group, you can use:
- name: Delete proxy group
  zabbix.zabbix.zabbix_proxy_group:
    state: absent
    name: My proxy group
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# You can configure Zabbix API connection settings with the following parameters:
- name: Create zabbix proxy group
  zabbix.zabbix.zabbix_proxy_group:
    state: present
    name: My proxy group
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
    Zabbix_version, default_values)


class Proxy_group(object):

    def __init__(self, module):
        self.module = module
        self.zapi = ZabbixApi(module)
        self.zbx_api_version = self.zapi.api_version()

        # Check Zabbix version
        if Zabbix_version(self.zbx_api_version) < Zabbix_version('7.0.0'):
            self.module.fail_json(
                msg="Proxy groups are not supported in Zabbix versions below 7.0.")

    def get_zabbix_proxy_group(self, proxy_groupid):
        """
        The function gets all information about an existing proxy group in Zabbix.

        :param proxy_groupid: proxy_groupid for search
        :type proxy_groupid: str|int

        :rtype: dict
        :returns:
            *   dict with proxy group parameters if proxy group exists
            *   empty dict if proxy group does not exist
        """
        params = {
            'output': 'extend',
            'proxy_groupids': proxy_groupid}

        try:
            proxy_group = self.zapi.send_api_request(
                method='proxygroup.get',
                params=params)
        except Exception as e:
            self.module.fail_json(msg="Failed to get existing proxy group: {0}".format(e))

        return proxy_group[0]

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

    def generate_zabbix_proxy_group(self):
        """
        The function generates the desired proxy group parameters based on the module
        parameters.
        The returned dictionary can be used to create a proxy group, as well as to
        compare with an existing proxy group.

        :rtype: dict
        :return: parameters of desired proxy group
        """
        proxy_group_params = {}

        # All parameters don't require additional processing
        params = ['description', 'name']
        for each in params:
            if self.module.params.get(each) is not None:
                proxy_group_params[each] = self.module.params[each]

        # failover_delay
        if self.module.params.get('failover_delay') is not None:
            if len(self.module.params['failover_delay']) == 0:
                proxy_group_params['failover_delay'] = default_values['proxy_group_failover_delay']
            else:
                proxy_group_params['failover_delay'] = self.module.params['failover_delay']

        # min_online
        if self.module.params.get('min_online') is not None:
            if len(self.module.params['min_online']) == 0:
                proxy_group_params['min_online'] = default_values['proxy_group_min_online']
            else:
                proxy_group_params['min_online'] = self.module.params['min_online']

        return proxy_group_params

    def compare_zabbix_proxy_group(self, exist_proxy_group, new_proxy_group):
        """
        The function compares the parameters of an existing proxy group with the
        desired new proxy group parameters.

        :param exist_proxy_group: parameters of existing Zabbix proxy group
        :type exist_proxy_group: dict
        :param new_proxy_group: parameters of desired (generated) proxy group
        :type new_proxy_group: dict

        :rtype: dict
        :return: difference between existing and desired parameters.
        """
        param_to_update = {}

        # These parameters don't require additional processing
        params = ['description', 'name', 'failover_delay', 'min_online']
        for each in params:
            if (new_proxy_group.get(each) is not None and
                    new_proxy_group.get(each) != exist_proxy_group.get(each)):
                param_to_update[each] = new_proxy_group[each]

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
        'failover_delay': {'type': 'str'},
        'min_online': {'type': 'str'},
        'description': {'type': 'str'}}

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True)

    state = module.params['state']
    proxy_group_name = module.params['name']

    proxy_group = Proxy_group(module)

    # Find a proxy_group in Zabbix
    result = proxy_group.zapi.find_zabbix_proxy_groups_by_names(proxy_group_name)

    if state == 'present':

        if len(result) > 0:
            # Get the parameters of an existing proxy group
            exist_proxy_group_params = proxy_group.get_zabbix_proxy_group(result[0]['proxy_groupid'])
            # Generate new proxy group parameters
            new_proxy_group_params = proxy_group.generate_zabbix_proxy_group()

            # Compare all parameters
            compare_result = proxy_group.compare_zabbix_proxy_group(
                exist_proxy_group_params,
                new_proxy_group_params)

            if compare_result:
                # Update proxy group
                compare_result['proxy_groupid'] = result[0]['proxy_groupid']

                update_result = proxy_group.api_request(
                    method='proxygroup.update',
                    params=compare_result)

                if update_result:
                    module.exit_json(
                        changed=True,
                        result="Successfully updated proxy group: {0}".format(
                            proxy_group_name))
                else:
                    module.fail_json(
                        msg="Failed to update proxy group: {0}".format(proxy_group_name))
            else:
                # No need to update
                module.exit_json(
                    changed=False,
                    result="No need to update proxy group: {0}".format(proxy_group_name))
        else:
            # Create proxy group
            new_proxy_group_params = proxy_group.generate_zabbix_proxy_group()

            result = proxy_group.api_request(
                method='proxygroup.create',
                params=new_proxy_group_params)
            if result:
                module.exit_json(
                    changed=True,
                    result="Successfully created proxy group: {0}".format(proxy_group_name))
            else:
                module.fail_json(
                    msg="Failed to create proxy group: {0}".format(proxy_group_name))
    else:
        if len(result) > 0:
            # delete proxy group
            delete_result = proxy_group.api_request(
                method='proxygroup.delete',
                params=[result[0]['proxy_groupid']])
            if delete_result:
                module.exit_json(
                    changed=True,
                    result="Successfully delete proxy group: {0}".format(proxy_group_name))
            else:
                module.fail_json(
                    msg="Failed to delete proxy group: {0}".format(proxy_group_name))
        else:
            # No need to delete proxy group
            module.exit_json(
                changed=False,
                result="No need to delete proxy group: {0}".format(proxy_group_name))


if __name__ == '__main__':
    main()
