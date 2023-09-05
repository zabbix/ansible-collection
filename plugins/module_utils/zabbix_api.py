#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from uuid import uuid4

from ansible.module_utils.urls import CertificateError
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.connection import Connection


class ZabbixException(Exception):
    """Base Zabbix exception class"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotExistInZabbix(ZabbixException):
    """Exception class when there are no searched objects in Zabbix"""
    pass


class NoParametersForSearch(ZabbixException):
    """Exception class when there are no objects to search for in Zabbix"""
    pass


class ZabbixApi(object):

    def __init__(self, module):
        self.module = module
        self.connection = Connection(self.module._socket_path)
        self.connection.setup_connection()
        self.jsonrpc_version = '2.0'
        self.zbx_api_version = None

    def api_version(self):
        """
        Function for getting API version

        :return: API version
        :rtype: str
        """
        if not self.zbx_api_version:
            payload = {
                'jsonrpc': self.jsonrpc_version, 'method': 'apiinfo.version',
                'id': str(uuid4()), 'params': {}}
            code, result = self.connection.send_request(data=payload)
            if code == 200 and result != '':
                self.zbx_api_version = result

        return self.zbx_api_version

    def send_api_request(self, method, params):
        """
        Function for sending request via HTTP API plugin

        :param method: required Zabbix API method
        :type method: str
        :param params: params for method
        :type params: dict

        :return: response from Zabbix API
        :rtype: dict
        """
        payload = {
            'jsonrpc': self.jsonrpc_version, 'method': method,
            'id': str(uuid4()), 'params': params}
        try:
            code, response = self.connection.send_request(data=payload)

        except ConnectionError as e:
            self.module.fail_json(msg="Connection error: {0}".format(e))

        except CertificateError as e:
            self.module.fail_json(msg="Certificate error: {0}".format(e))

        except ValueError as e:
            self.module.fail_json(msg="Certificate not found: {0}".format(e))

        if not (code >= 200 and code < 300):
            self.module.fail_json(
                msg="Zabbix API returned error {0} with message {1}".format(
                    code, response))

        return response

    # #########################################################
    # ZABBIX HOST
    def find_zabbix_host(self, search_filter):
        """
        Function to search for a host in Zabbix by a given filter

        :param search_filter: host search filter
        :type search_filter: dict

        :return: found host parameters
        :rtype: dict
        """
        existing_host = self.send_api_request(
            method='host.get',
            params={
                'output': ['name', 'host', 'hostid'],
                'filter': search_filter})

        return existing_host

    def find_zabbix_host_by_host(self, host_name):
        """
        Function to search for a host in Zabbix by host_name

        :param host_name: host_name for search
        :type host_name: str

        :return: found host
        :rtype: dict

        :raise:
            * NoParametersForSearch - if host_name is empty
        """
        if host_name and len(host_name) > 0:
            search_filter = {'host': host_name}
        else:
            raise NoParametersForSearch("No parameters for searching for Zabbix host")

        return self.find_zabbix_host(search_filter)

    def find_zabbix_host_by_visible_name(self, visible_name):
        """
        Function to search for a host in Zabbix by visible_name

        :param visible_name: visible_name for search
        :type visible_name: str

        :return: found host
        :rtype: dict

        :raise:
            * NoParametersForSearch - if visible_name is empty
        """
        if visible_name and len(visible_name) > 0:
            search_filter = {'name': visible_name}
        else:
            raise NoParametersForSearch("No parameters for searching for Zabbix host")

        return self.find_zabbix_host(search_filter)

    def find_zabbix_host_by_hostid(self, hostid):
        """
        Function to search for a host in Zabbix by hostid

        :param hostid: hostid for search
        :type hostid: str|int

        :return: found host
        :rtype: dict

        :raise:
            * NoParametersForSearch - if hostid is empty
        """
        if hostid and len(hostid) > 0:
            search_filter = {'hostid': hostid}
        else:
            raise NoParametersForSearch("No parameters for searching for Zabbix host")

        return self.find_zabbix_host(search_filter)

    # #########################################################
    # ZABBIX HOST GROUPS
    def find_zabbix_hostgroups(self, search_filter):
        """
        Function to search for host groups in Zabbix by a given filter

        :param search_filter: host groups search filter
        :type search_filter: dict

        :return: found host groups
        :rtype: dict
        """
        existing_groups = self.send_api_request(
            method='hostgroup.get',
            params={
                'output': ['name', 'groupid'],
                'filter': search_filter})

        return existing_groups

    def find_zabbix_hostgroups_by_names(self, hostgroup_names):
        """
        Function to search for host groups in Zabbix by hostgroup_names

        :param hostgroup_names: host group names for search
        :type hostgroup_names: list

        :return: found host groups
        :rtype: dict

        :raise:
            * NoParametersForSearch - if hostgroup_names is empty
        """
        if hostgroup_names and len(hostgroup_names) > 0:
            search_filter = {'name': hostgroup_names}
        else:
            raise NoParametersForSearch(
                "No parameters for searching for Zabbix host group(s)")

        return self.find_zabbix_hostgroups(search_filter)

    def find_zabbix_hostgroups_by_group_ids(self, hostgroup_ids):
        """
        Function to search for host groups in Zabbix by hostgroup_ids

        :param hostgroup_ids: host group IDs for search
        :type hostgroup_ids: list

        :return: found host groups
        :rtype: dict

        :raise:
            * NoParametersForSearch - if hostgroup_ids is empty
        """
        if hostgroup_ids and len(hostgroup_ids) > 0:
            search_filter = {'groupid': hostgroup_ids}
        else:
            raise NoParametersForSearch(
                "No parameters for searching for Zabbix host group(s)")

        return self.find_zabbix_hostgroups(search_filter)

    # #########################################################
    # ZABBIX TEMPLATES
    def find_zabbix_templates(self, search_filter):
        """
        Function to search for templates in Zabbix by a given filter

        :param search_filter: templates search filter
        :type search_filter: dict

        :return: found templates
        :rtype: dict
        """
        existing_templates = self.send_api_request(
            method='template.get',
            params={
                'output': ['name', 'templateid'],
                'filter': search_filter})
        return existing_templates

    def find_zabbix_templates_by_names(self, template_names):
        """
        Function to search for templates in Zabbix by template_names

        :param template_names: template names for search
        :type template_names: list

        :return: found templates
        :rtype: dict

        :raise:
            * NoParametersForSearch - if template_names is empty
        """
        if template_names and len(template_names) > 0:
            search_filter = {'name': template_names}
        else:
            raise NoParametersForSearch(
                "No parameters for searching for Zabbix templates")

        return self.find_zabbix_templates(search_filter)

    def find_zabbix_templates_by_ids(self, template_ids):
        """
        Function to search for templates in Zabbix by template_ids

        :param template_ids: template IDs for search
        :type template_ids: list

        :return: found templates
        :rtype: dict

        :raise:
            * NoParametersForSearch - if template_ids is empty
        """
        if template_ids and len(template_ids) > 0:
            search_filter = {'templateid': template_ids}
        else:
            raise NoParametersForSearch(
                "No parameters for searching for Zabbix templates")

        return self.find_zabbix_templates(search_filter)

    # #########################################################
    # ZABBIX PROXYS
    def find_zabbix_proxys(self, search_filter):
        """
        Function to search for a proxy in Zabbix by a given filter

        :param search_filter: proxy search filter
        :type search_filter: dict

        :return: found proxy
        :rtype: list
        """
        existing_proxys = self.send_api_request(
            method='proxy.get',
            params={
                'output': ['host', 'proxyid'],
                'filter': search_filter})

        return existing_proxys

    def find_zabbix_proxy_by_names(self, proxy_names):
        """
        Function to search for a proxy in Zabbix by proxy_names

        :param proxy_names: proxy names for search
        :type proxy_names: list

        :return: found proxies
        :rtype: list

        :raise:
            * NoParametersForSearch - if proxy_names is empty
        """
        if proxy_names and len(proxy_names) > 0:
            search_filter = {'host': proxy_names}
        else:
            raise NoParametersForSearch(
                "No parameters for searching for Zabbix proxy")

        return self.find_zabbix_proxys(search_filter)

    def find_zabbix_proxy_by_ids(self, proxy_ids):
        """
        Function to search for a proxy in Zabbix by proxy_ids

        :param proxy_ids: proxy IDs for search
        :type proxy_ids: list

        :return: found proxys
        :rtype: list

        :raise:
            * NoParametersForSearch - if proxy_ids is empty
        """
        if proxy_ids and len(proxy_ids) > 0:
            search_filter = {'proxyid': proxy_ids}
        else:
            raise NoParametersForSearch(
                "No parameters for searching for Zabbix proxy")

        return self.find_zabbix_proxys(search_filter)
