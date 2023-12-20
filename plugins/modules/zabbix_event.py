#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zabbix_event
short_description: Module for event actions
description:
    - Update/Get existing events in Zabbix.
author:
    - Zabbix Ltd (@zabbix)
requirements:
    - "python >= 2.6"
options:
    action:
        description: Event module actions
        type: str
        default: message
        required: false
        choices: [ message severity ]
    ids:
        description: List of host groups to create/remove.
        type: list
        elements: str
        required: true
        aliases: [ eventids, event_ids ]
    message:
        description: Update event with message
        type: str
    severity:
        description: Update event severity
        type: str
        choices: [ nan info warning average high disaster ]
'''

EXAMPLES = r'''
# To create host groups, you can use:
- name: Update event with message
  zabbix.zabbix.zabbix_event:
    action: message
    ids: ["2222"]
    message: "Hello world"
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
'''

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zabbix.zabbix.plugins.module_utils.zabbix_api import ZabbixApi


class Event(object):

    def __init__(self, module):
        self.module = module
        self.zapi = ZabbixApi(module)
        self.zbx_api_version = self.zapi.api_version()

    def message(self, ids):
        """
        The function adds message to the event

        :param ids: list of event ids
        :type ids: list

        :rtype: list
        :return: list of updated events
        """
        # hostgroup_names = []
        # if hostgroups:
        #     for group in hostgroups:
        #         if group is not None and len(group.strip()) > 0:
        #             hostgroup_names.append(group.strip())
        # if hostgroups is None or len(hostgroup_names) == 0:
        #     return []

        # # get existing host group
        # try:
        #     existing_hostgroups = self.zapi.send_api_request(
        #         method='hostgroup.get',
        #         params={'output': ['name'], 'filter': {'name': hostgroup_names}})
        # except Exception as e:
        #     self.module.fail_json(
        #         msg="Failed to get existing host group(s): {0}".format(e))

        # # search for host group to create
        # hostgroup_for_create = list(
        #     set(hostgroup_names) - set(eg['name'] for eg in existing_hostgroups))

        # if self.module.check_mode:
        #     self.module.exit_json(changed=True)

        # updating event with message

        try:
            result = (self.zapi.send_api_request(
                method='event.acknowledge',
                params={'eventids': ids, 'message':'Hello World'}))
        except Exception as e:
            self.module.fail_json(
                msg="Failed to update event(s): {0}".format(e))

        return result.result.eventids

def main():
    """entry point for module execution"""
    spec = {
        'action': {
            'type': 'str',
            'default': 'message',
            'choices': ['message', 'severity']},
        'ids': {
            'type': 'list',
            'elements': 'str',
            'aliases': ['event_ids','eventids'],
            'required': True}}

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True)

    action = module.params['action']
    ids = module.params['ids']

    event = Event(module)

    if action == 'message':
        # create host group
        result = event.message(ids)
        if len(result) > 0:
            module.exit_json(
                changed=True,
                result="Successfully updated event(s): {0}".format(
                    ", ".join(result)))
        else:
            module.exit_json(
                changed=False,
                result="Failed updating events")
    else:
        pass

if __name__ == '__main__':
    main()
