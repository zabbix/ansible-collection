#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zabbix_hostgroup
short_description: Module for creating and deleting host groups
description:
    - Creation of new host groups.
    - The module will only create the missing host groups if some of the listed are already created in Zabbix.
    - Removing host groups from Zabbix.
author:
    - Zabbix Ltd (@zabbix)
requirements:
    - "python >= 2.6"
options:
    state:
        description: Action with host groups. Present to create, absent to remove.
        type: str
        default: present
        required: false
        choices: [ present, absent ]
    hostgroups:
        description: List of host groups to create/remove.
        type: list
        elements: str
        required: true
        aliases: [ host_group, host_groups, name ]
'''

EXAMPLES = r'''
# To create host groups, you can use:
- name: Create host groups
  zabbix.zabbix.zabbix_hostgroup:
    state: present
    hostgroups:
      - G1
      - G2
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# To delete two host groups - G1 and G2
- name: Delete host groups by name
  zabbix.zabbix.zabbix_hostgroup:
    state: absent
    hostgroups:
      - G1
      - G2
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# You can configure Zabbix API connection settings with the following parameters:
- name: Create host groups
  zabbix.zabbix.zabbix_hostgroup:
    state: present
    hostgroups:
      - G1
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


class HostGroup(object):

    def __init__(self, module):
        self.module = module
        self.zapi = ZabbixApi(module)
        self.zbx_api_version = self.zapi.api_version()

    def create(self, hostgroups):
        """
        The function creates a host group if it doesn't exist.
        If a list of host groups is received, some of which have already
        been created, then only the missing host groups will be created.

        :param hostgroups: list of host group names
        :type hostgroups: list

        :rtype: list
        :return: list of created host groups
        """
        hostgroup_names = []
        if hostgroups:
            for group in hostgroups:
                if group is not None and len(group.strip()) > 0:
                    hostgroup_names.append(group.strip())
        if hostgroups is None or len(hostgroup_names) == 0:
            return []

        # get existing host group
        try:
            existing_hostgroups = self.zapi.send_api_request(
                method='hostgroup.get',
                params={'output': ['name'], 'filter': {'name': hostgroup_names}})
        except Exception as e:
            self.module.fail_json(
                msg="Failed to get existing host group(s): {0}".format(e))

        # search for host group to create
        hostgroup_for_create = list(
            set(hostgroup_names) - set(eg['name'] for eg in existing_hostgroups))

        if self.module.check_mode:
            self.module.exit_json(changed=True)

        # creating host group
        added_hostgroups = []
        for group in hostgroup_for_create:
            try:
                self.zapi.send_api_request(
                    method='hostgroup.create',
                    params={'name': group})
            except Exception as e:
                self.module.fail_json(
                    msg="Failed to create host group(s): {0}".format(e))
            added_hostgroups.append(group)

        return added_hostgroups

    def delete(self, hostgroups):
        """
        The function removes host groups from Zabbix.
        Before deleting, the function checks which of the required host groups
        exist.

        :param hostgroups: list of host group names
        :type hostgroups: list

        :rtype: list
        :return: list of deleted host groups
        """
        if hostgroups and len(hostgroups) > 0:
            group_filter = {'name': hostgroups}
        else:
            return []

        # get existing host group
        try:
            existing_hostgroups = self.zapi.send_api_request(
                method='hostgroup.get',
                params={
                    'output': ['name', 'groupid'],
                    'filter': group_filter,
                    'preservekeys': True})
        except Exception as e:
            self.module.fail_json(
                msg="Failed to get existing host group(s): {0}".format(e))

        # search host group(s) for deleting
        hostgroup_ids_for_delete = [existing_hostgroups[g]['groupid'] for g in existing_hostgroups]

        if len(hostgroup_ids_for_delete) == 0:
            return []
        if self.module.check_mode:
            self.module.exit_json(changed=True)

        # deleting host group(s)
        try:
            result = self.zapi.send_api_request(
                method='hostgroup.delete',
                params=hostgroup_ids_for_delete)
        except Exception as e:
            self.module.fail_json(
                msg="Failed to delete host group(s): {0}".format(e))

        return [existing_hostgroups[g]['name'] for g in result['groupids']]


def main():
    """entry point for module execution"""
    spec = {
        'state': {
            'type': 'str',
            'default': 'present',
            'choices': ['present', 'absent']},
        'hostgroups': {
            'type': 'list',
            'elements': 'str',
            'aliases': ['host_group', 'name', 'host_groups'],
            'required': True}}

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True)

    state = module.params['state']
    hostgroups = module.params['hostgroups']

    hostGroup = HostGroup(module)

    if state == 'present':
        # create host group
        result = hostGroup.create(hostgroups)
        if len(result) > 0:
            module.exit_json(
                changed=True,
                result="Successfully created host group(s): {0}".format(
                    ", ".join(result)))
        else:
            module.exit_json(
                changed=False,
                result="All specified host groups already exist")
    else:
        # delete host group
        result = hostGroup.delete(hostgroups)
        if len(result) > 0:
            module.exit_json(
                changed=True,
                result="Successfully deleted host group(s): {0}".format(
                    ", ".join(result)))
        else:
            module.exit_json(
                changed=False,
                result="No host group(s) to delete")


if __name__ == '__main__':
    main()
