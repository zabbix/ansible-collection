#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zabbix_event
short_description: Module for event actions
description:
    - Update/Get existing events in Zabbix. Currently implemented only message action.
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
        choices: [ message ]
    ids:
        description: List of host groups to create/remove.
        type: list
        elements: str
        required: true
        aliases: [ eventids, event_ids ]
    msg:
        description: Update event with message
        type: str
        required: true
'''

EXAMPLES = r'''
# To create host groups, you can use:
- name: Update event with message
  zabbix.zabbix.zabbix_event:
    action: message
    ids: ["2222"]
    msg: "Hello world"
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

    def message(self, ids, msg):
        """
        The function adds message to the event

        :param ids: list of event ids
        :type ids: list

        :param msg: message for the event
        :type msg: str

        :rtype: list
        :return: list of updated event ids
        """

        try:
            result = (self.zapi.send_api_request(
                method='event.acknowledge',
                params={'action': 4, 'eventids': ids, 'message': msg}))
        except Exception as e:
            self.module.fail_json(
                msg="Failed to update event(s): {0}".format(e))

        return [str(elem) for elem in result["eventids"]]


def main():
    """entry point for module execution"""
    spec = {
        'action': {
            'type': 'str',
            'default': 'message',
            'choices': ['message']},
        'ids': {
            'type': 'list',
            'elements': 'str',
            'aliases': ['event_ids', 'eventids'],
            'required': True},
        'msg': {
            'type': 'str',
            'required': True}}

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True)

    action = module.params['action']
    ids = module.params['ids']
    message = module.params['msg']

    event = Event(module)

    if action == 'message':
        # update event with message
        result = event.message(ids, message)
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
