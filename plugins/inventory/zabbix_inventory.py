# Copyright: Zabbix Ltd
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
name: zabbix_inventory
author:
    - Zabbix Ltd (@zabbix)
short_description: Zabbix inventory plugin
description:
    - This plugin is designed to work with Zabbix API.
    - This inventory plugin allows Ansible users to generate a dynamic inventory based on data from Zabbix installation.
    - Using the available filtering methods, the user can specify the search criteria for hosts in Zabbix, as well as limit the set of returned fields.
options:
    zabbix_user:
        type: str
        description: User name for logging in to Zabbix API.
        env:
            - name: ZABBIX_USER
    zabbix_password:
        type: str
        description: Password for logging in to Zabbix API.
        env:
            - name: ZABBIX_PASSWORD
    zabbix_api_token:
        type: str
        description: Token for authorization to Zabbix API.
        env:
            - name: ZABBIX_API_TOKEN
    zabbix_api_url:
        type: str
        required: true
        description: Path to access Zabbix API.
        env:
            - name: ZABBIX_API_URL
    connection_timeout:
        type: int
        default: 10
        description: Timeout for connecting to Zabbix API.
    validate_certs:
        type: bool
        default: true
        description: Whether the connection should be made with validation certificates.
    http_proxy:
        type: str
        description: Address of HTTP proxy for connection to Zabbix API.
    http_login:
        type: str
        description: Username for basic HTTP authorization to Zabbix API.
    http_password:
        type: str
        description: Password for basic HTTP authorization to Zabbix API.
    prefix:
        type: str
        default: 'zabbix_'
        description: Prefix to use for parameters given from Zabbix API.
    output:
        type: list
        default: ['extend']
        elements: str
        description:
            - Object properties to be returned.
            - List of available fields depends on Zabbix version.
            - See also U(https://www.zabbix.com/documentation/6.0/en/manual/api/reference/host/object)
            - See also U(https://www.zabbix.com/documentation/current/en/manual/api/reference/host/object)
            - Fields 'hostid' and 'host' will always be given from Zabbix.
    query:
        type: dict
        default: {}
        description:
            - Additional parameters for getting linked objects for the host.
            - List of available fields depends on Zabbix version.
            - Available query for Zabbix 6.0
            - selectDiscoveries, selectDiscoveryRule, selectGraphs, selectHostDiscovery, selectGroups, selectHttpTests,
              selectInterfaces, selectInventory, selectItems, selectMacros, selectParentTemplates, selectDashboards,
              selectTags, selectInheritedTags, selectTriggers, selectValueMaps.
            - In Zabbix 6.4 selectGroups was deprecated. Please use selectHostGroups instead.
            - See also U(https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get#parameters)
    filter:
        type: dict
        default: {}
        description:
            - The parameter is used to select hosts in Zabbix. Each parameter refines the search.
            - For multiple parameters, 'AND' logic is applied.
            - If you specify host groups and templates, this means a host that both is a member of any
              of the specified host groups and has any of the specified templates will be found.
        suboptions:
            templates:
                type: list
                elements: str
                description:
                    - List of templates for host search in Zabbix.
                    - Will return hosts that are linked to the given templates.
                    - Wildcard search is possible.
                    - Case-sensitive search.
            hostgroups:
                type: list
                elements: str
                description:
                    - List of host groups for host search in Zabbix.
                    - Will return hosts that are linked to the given host groups.
                    - Wildcard search is possible.
                    - Case-sensitive search.
            proxy:
                type: list
                elements: str
                description:
                    - List of proxies for host search in Zabbix.
                    - Will return hosts that are linked to the given proxies.
                    - Wildcard search is possible.
                    - Case-sensitive search.
            proxy_group:
                type: list
                elements: str
                description:
                    - List of proxy groups for host search in Zabbix.
                    - Will return hosts that are linked to the given proxy groups.
                    - Wildcard search is possible.
                    - Case-sensitive search.
                    - Used only for Zabbix versions above 7.0.
            name:
                type: list
                elements: str
                description:
                    - List of host names (visible names) for host search in Zabbix.
                    - Will return hosts that match the given visible host names.
                    - Wildcard search is possible.
                    - Case-sensitive search.
            host:
                type: list
                elements: str
                description:
                    - List of host names (technical names) for host search in Zabbix.
                    - Will return hosts that match the given technical host names.
                    - Wildcard search is possible.
                    - Case-sensitive search.
            status:
                type: str
                choices: [ enabled, disabled ]
                description:
                    - Desired host status for host search in Zabbix.
                    - Can be only 'enabled' or 'disabled'.
            tags:
                type: list
                elements: dict
                description:
                    - List of tags for host search in Zabbix.
                    - For multiple tags, the logic to be applied is determined by 'tags_behavior' parameter
                suboptions:
                    tag:
                        type: str
                        description: Tag name for host search in Zabbix.
                        required: true
                    value:
                        type: str
                        default: ''
                        description: Tag value for host search in Zabbix.
                    operator:
                        type: str
                        description: Mode of searching by tags.
                        default: contains
                        choices: [ 'contains', 'equals', 'not like', 'not equal', 'exists', 'not exists' ]
            tags_behavior:
                type: str
                default: 'and/or'
                choices: ['and/or', 'or']
                description:
                    - Desired logic for searching by tags.
                    - This parameter impacts the logic of searching by tags.
                    - Specify the logic of searching by multiple tags.
extends_documentation_fragment:
    - constructed
    - inventory_cache
'''

EXAMPLES = r'''
# Minimal set of parameters for searching.
# You need to specify the name of plugin, URL and credentials (login and password or API token).
# IMPORTANT: Keep in mind that with these parameters all hosts with all host parameters will be returned from Zabbix.
# This can create excessive load on Zabbix server. For selecting host and fields, use the filter and output options.
---
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix


# FILTER EXAMPLES

# To select hosts by host groups name, you can use the following example.
# In this example, all hosts linked to any host groups the names of which start with 'Linux' (Linux, Linux servers, Linux Ubuntu, etc.) will be returned.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups: 'Linux*'

# To select hosts by certain host group name, you can use the following example.
# In this example, all hosts linked only to host group 'Linux' will be returned.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups: Linux

# To select hosts from several host groups, you can use the following example.
# In this example, all hosts linked to any of the host groups 'Linux', 'Linux Ubuntu' or host groups the names of which start with 'Windows' will be returned.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups:
    - Linux
    - Linux Ubuntu
    - 'Windows*'

# You can use all available filter options to search for hosts in Zabbix.
# You can use wildcard search for: host groups, templates, proxy, name (visible name), host (technical name).
# Also, you can use 'status' for filtering and search only for enabled or disabled hosts.
# Also, you can use tags for searching by tag name or tag value.
# In this example, all hosts linked to the host group 'Linux' and to any of the '*http*' or '*agent*' templates as well as
# containing 'sql' or 'SQL' in their visible names will be returned.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups: Linux
  templates: ['*HTTP*', '*agent*']
  name: ['*sql*', '*SQL*']


# OUTPUT EXAMPLES

# To limit fields in output, you can specify the list of fields in output options.
# In this example, only name and two mandatory fields (hostid and host) will be returned.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups: Linux
output: name

# To have several output fields, you need to specify those in the list format.
# In this example, name, status and two mandatory fields (hostid and host) will be returned.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups: Linux
output:
  - name
  - status


# POSTPROCESSING EXAMPLES

# For postprocessing, you can use:
# - keyed_groups
# - groups
# - compose

# To convert digit status to verbose, you can use 'compose' from next example.
# To group by status (enabled, disabled) from output, you can use 'groups' from next example.
# To group by Zabbix host groups, you can use 'keyed_groups' from next example.
# IMPORTANT: Make sure that necessary data will be present in output. For this example, 'groups' must be present for
# grouping with 'keyed_groups'.
# IMPORTANT: Keep in mind that all parameters from Zabbix will have prefix (by default, 'zabbix_').
# And you need to specify it in postprocessing (zabbix_groups, zabbix_status, etc.).
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
query:
  selectGroups: ['name']
filter:
  hostgroups: Linux
compose:
  zabbix_verbose_status: zabbix_status.replace("1", "Disabled").replace("0", "Enabled")
groups:
  enabled: zabbix_status == "0"
  disabled: zabbix_status == "1"
keyed_groups:
  - key: zabbix_groups | map(attribute='name')
    separator: ""

# For grouping by template names. Other parameters (credentials, URL, etc.) were skipped in this example.
query:
  selectParentTemplates: ['name']
keyed_groups:
  - key: zabbix_parentTemplates | map(attribute='name')
    separator: ""

# For searching by 'Location' tag and grouping by tag names. Other parameters (credentials, URL, etc.) were skipped in this example.
query:
  selectTags: 'extend'
filter:
  tags:
    - tag: Location
keyed_groups:
  - key: zabbix_tags | map(attribute='tag')
    separator: ""

# For searching by 'Location' tag and grouping by tag values. Other parameters (credentials, URL, etc.) were skipped in this example.
# In this example, hosts will be grouped by tag value. If you have tags: (Location: Riga, Location: Berlin),
# then the following groups will be created: Riga, Berlin.
query:
  selectTags: 'extend'
filter:
  tags:
    - tag: Location
keyed_groups:
  - key: dict(zabbix_tags | items2dict(key_name="tag"))['Location']
    separator: ""

# For transforming given host groups to the list, you can use 'compose' and the following example.
# Other parameters (credentials, URL, etc.) were skipped in this example.
query:
  selectGroups: ['name']
compose:
  zabbix_groups_list: zabbix_groups | map(attribute='name')

# For transforming given interfaces to the list of IP addresses, you can use 'compose' and the following example.
# Other parameters (credentials, URL, etc.) were skipped in this example.
query:
  selectInterfaces: ['ip']
compose:
  zabbix_ip_list: zabbix_interfaces | map(attribute='ip')


# CACHING EXAMPLES

# You can use cache for inventory.
# During the loading of cached data, the plugin will compare the input parameters. If any parameters impacting the given data
# (login, password, API token, URL, output, filter, query) have been changed, then cached data will be skipped and new data will be requested from Zabbix.
# For caching, you can use the following example:
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
filter:
  hostgroups: Linux
cache: true
cache_plugin: jsonfile
cache_timeout: 7200
cache_connection: /tmp/zabbix_inventory

# COMPLEX EXAMPLES

# In this example, you can use filtering by host groups, templates, proxy, tags, names, status.
# Grouping by Zabbix host groups.
# Transform IP addresses to the list of IP.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
cache: true
cache_plugin: jsonfile
cache_timeout: 7200
cache_connection: /tmp/zabbix_inventory
query:
  selectGroups: ['name']
  selectInterfaces: ['ip']
filter:
  hostgroups: ['Linux', 'Linux servers']
  templates: ['*HTTP*', '*agent*']
  name: ['*sql*', '*SQL*']
  host: ['*sql*', '*SQL*']
  proxy: ['Riga*']
  status: enabled
  tags_behavior: 'and/or'
  tags:
    - tag: scope
    - tag: Location
      value: Riga
      operator: equals
output:
  - name
compose:
  zabbix_ip_list: zabbix_interfaces | map(attribute='ip')
keyed_groups:
  - key: zabbix_groups | map(attribute='name')
    separator: ""

# In this example, you can apply filtering by 'Location' tag with empty value and grouping by status (enabled, disabled).
# In this example, status was transformed from digit value to verbose value and than used in 'keyed_groups' for grouping by verbose statuses.
plugin: "zabbix.zabbix.zabbix_inventory"
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
query:
  selectTags: 'extend'
filter:
  tags:
    - tag: Location
      value: ''
      operator: equals
keyed_groups:
  - key: zabbix_verbose_status
    separator: ""
compose:
  zabbix_verbose_status: zabbix_status.replace("1", "Disabled").replace("0", "Enabled")
'''

import base64
import json
import os
from uuid import uuid4

from ansible.errors import (AnsibleAuthenticationFailure,
                            AnsibleConnectionFailure, AnsibleParserError)
from ansible.module_utils.basic import to_text
from ansible.module_utils.urls import Request
from ansible.parsing.yaml.objects import AnsibleUnicode
from ansible.plugins.inventory import (BaseInventoryPlugin, Cacheable,
                                       Constructable)
from ansible_collections.zabbix.zabbix.plugins.module_utils.helper import (
    host_subquery, tags_compare_operators, Zabbix_version, filter_params_depends_on_version)


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'zabbix.zabbix.zabbix_inventory'

    def get_absolute_url(self):
        """
        This function checks and creates URL for connection to Zabbix API.
        If there is no schema in the input, the default schema will be used (http://).
        If there is no 'api_jsonrpc.php' path in the input data, then this value will be automatically added.
        If the address is empty, the name 'localhost' will be used.

        :rtype: str
        :return: absolute URL to connect to Zabbix API.
        """
        # Default values
        DEFAULT_SCHEMA = 'http:'
        DEFAULT_API_PATH = 'api_jsonrpc.php'

        url = self.args.get('zabbix_api_url')
        if url is None:
            url = 'localhost'

        # Parse URL to separate parts
        parsed_url = [u for u in url.split('/') if len(u) > 0]

        # Check schema and API path
        if parsed_url[0] not in ['http:', 'https:']:
            parsed_url.insert(0, DEFAULT_SCHEMA)
        if parsed_url[-1] != DEFAULT_API_PATH:
            parsed_url.append(DEFAULT_API_PATH)

        return '{0}//{1}'.format(parsed_url[0], '/'.join(parsed_url[1:]))

    def get_api_version(self):
        """
        This function requests and returns current Zabbix API version

        :rtype: str
        :return: string with Zabbix API version.
        """

        return self.api_request('apiinfo.version', params={})

    def login(self):
        """
        Function for logging in to Zabbix.
        If 'zabbix_api_token'option is set, use auth by token.

        :rtype: str
        :return: string with Authorization information (token)

        :raises:
            AnsibleAuthenticationFailure:
                * If no credentials are found.
                * If response from Zabbix API is empty.
        """

        # Check token
        self.auth_token = self.args.get('zabbix_api_token')
        if self.auth_token:
            return self.auth_token

        # Check login and password
        if self.args.get('zabbix_user') is None or self.args.get('zabbix_password') is None:
            raise AnsibleAuthenticationFailure('Not found credentials')

        # Use login and password
        params = {
            'username': self.args.get('zabbix_user'),
            'password': self.args.get('zabbix_password')}
        response = self.api_request(method='user.login', params=params)

        if len(response) > 0:
            return response

        # If response is empty
        raise AnsibleAuthenticationFailure('Login failed')

    def logout(self):
        """
        This function requests user.logout method.
        If login and password were used for authorization, a logout request will be sent.
        If a token was used for authorization, then the request will not be sent.

        :rtype: bool
        :returns:
            * status of logout, if login/password were used.
            * True, if token was used.
        """

        # If login and password were used
        if self.auth_token is None and hasattr(self, "auth"):
            return self.api_request(method='user.logout', params={})

        # If token was used
        return True

    def api_request(self, method, params, reqid=str(uuid4())):
        """
        Function to send a request to Zabbix API.
        If the input parameters contain data for basic HTTP authorization,
        then this data will be added to the request header.

        :param method: Request method
        :type method: str
        :param reqid: Unique request ID
        :type reqid: str
        :param params: Additional request parameters
        :type params: dict

        :rtype: str | dict
        :returns:
            * Data from the 'result' field from the response from the server
            * If the 'result' field is not found, then the response will be returned
              in its original form

        :raises:
            * AnsibleConnectionFailure: If there was an error connecting to the server.
            * AnsibleParserError:
                - Error during parse response from Zabbix API. (Invalid JSON)
                - Any error while parsing the response from the server.
                - An 'error' field was found in the response from the server.
        """

        # Build headers and default payload
        headers = {'Content-Type': 'application/json-rpc', 'Accept': 'application/json'}
        payload = {'jsonrpc': '2.0', 'method': method, 'id': reqid, 'params': params}

        # Add Zabbix auth
        if hasattr(self, "auth"):
            payload['auth'] = self.auth

        # Add basic auth
        if self.args['http_login'] is not None and self.args['http_password'] is not None:
            auth = base64.b64encode("{0}:{1}".format(
                self.args['http_login'], self.args['http_password']).encode('ascii'))
            headers['Authorization'] = 'Basic {0}'.format(auth.decode('ascii'))

        # Prepare and run query
        zabbix_request = Request(
            http_agent='Zabbix Inventory Plugin',
            headers=headers,
            timeout=self.args['connection_timeout'],
            validate_certs=self.args['validate_certs'])
        try:
            response = zabbix_request.post(self.zabbix_api_url, data=json.dumps(payload))
        except Exception as e:
            raise AnsibleConnectionFailure(to_text(e))

        # Parse response
        try:
            result = json.load(response)
        except ValueError as e:
            raise AnsibleParserError("Error during parse response from Zabbix API: {0}".format(to_text(e)))
        except Exception as e:
            raise AnsibleParserError(to_text(e))

        if 'error' in result:
            raise AnsibleParserError('Zabbix API returned error: {0}'.format(result['error']))

        return result.get('result', result)

    def validate_params(self):
        """
        This function checks the input parameters for correct filling.
        In case of minor problems (case, parameter type), the function automatically
        corrects the input data.

        :return: None

        :raises:
            * AnsibleParserError:
                - If query parameter not found in available queries
                - Unknown status filter
                - Unknown tags_behavior filter
                - Not found tag name
                - Unknown tag operator filter
                - Unsupported filter: proxy_group
        """

        # Check depending on the Zabbix version
        # If the arguments contain parameters which depends on the version,
        # we need to get the version of the API.
        need_version = False

        for key in filter_params_depends_on_version:
            if self.args.get(key) is not None:
                if len(list(
                    set(filter_params_depends_on_version.get(key, [])) &
                        set([e.lower() for e in self.args.get(key, [])]))) != 0:
                    need_version = True

        if need_version:
            self.zabbix_version = self.get_api_version()

        # Check query parameters
        if self.args.get('query'):
            new_subquery = {}
            # Check the query from available queries list
            available_fields = dict((e.lower(), e) for e in host_subquery)
            unknown_parameters = list(set([e.lower() for e in self.args['query']]) - set(available_fields.keys()))
            if unknown_parameters:
                raise AnsibleParserError('Unknown query parameters: {0}'.format(', '.join(unknown_parameters)))

            # Check type
            for each in self.args['query']:
                if isinstance(self.args['query'][each], AnsibleUnicode):
                    new_subquery[available_fields[each.lower()]] = [self.args['query'][each].lower()]
                else:
                    new_subquery[available_fields[each.lower()]] = [e.lower() for e in self.args['query'][each]]
                if 'extend' in new_subquery[available_fields[each.lower()]]:
                    new_subquery[available_fields[each.lower()]] = 'extend'

            if new_subquery:
                self.args['query'] = new_subquery

        # Check output parameter and convert to lower case
        if self.args.get('output'):
            self.args['output'] = [e.lower() for e in self.args['output']]

        # Check filter parameter
        if self.args.get('filter'):
            # All keys to lower case
            self.args['filter'] = dict((e.lower(), self.args['filter'][e]) for e in self.args['filter'])

            # Status
            if self.args['filter'].get('status') is not None:
                if (isinstance(self.args['filter']['status'], AnsibleUnicode) is False or
                        self.args['filter']['status'].lower() not in ['enabled', 'disabled']):
                    raise AnsibleParserError(
                        'Unknown status filter: {0}. Available: enabled, disabled.'.format(self.args['filter']['status']))

            # tags_behavior
            if self.args['filter'].get('tags_behavior') is not None:
                if (isinstance(self.args['filter']['tags_behavior'], AnsibleUnicode) is False or
                        self.args['filter']['tags_behavior'].lower() not in ['and/or', 'or']):
                    raise AnsibleParserError(
                        'Unknown tags_behavior filter: {0}. Available: and/or, or.'.format(self.args['filter']['tags_behavior']))

            # Tags
            if self.args['filter'].get('tags') is not None:
                tags = []
                for tag in self.args['filter']['tags']:
                    new_tag = {}
                    for key in tag:
                        if key.lower() == 'operator':
                            new_tag[key.lower()] = tag[key].lower()
                        else:
                            new_tag[key.lower()] = tag[key]
                    if 'tag' not in new_tag:
                        raise AnsibleParserError('Not found tag name')
                    if 'operator' in new_tag and new_tag['operator'] not in tags_compare_operators:
                        raise AnsibleParserError('Unknown tag operator filter: {0}. Available: {1}.'.format(
                            new_tag['operator'],
                            ', '.join(tags_compare_operators.keys())))
                    tags.append(new_tag)
                self.args['filter']['tags'] = list(tags)

            # proxy group
            if self.args['filter'].get('proxy_group') is not None:
                if Zabbix_version(self.zabbix_version) < Zabbix_version('7.0.0'):
                    raise AnsibleParserError(
                        'Unsupported filter: proxy_group. This filter is not supported in Zabbix API v.{0}'.format(
                            self.zabbix_version))

    def parse_filter(self):
        """
        This function parses all filtering conditions and, depending on the situation,
        will request element IDs in Zabbix API or add parameters to the final host
        request.

        :rtype: dict
        :return: condition for final host request.
        """
        zabbix_filter = {}
        subquery_params = {"searchByAny": True, "searchWildcardsEnabled": True}
        self.ids = {'proxy': {}, 'proxy_group': {}}

        # Zabbix host groups
        if self.args['filter'].get('hostgroups') is not None:
            subquery_params['output'] = ["name", "groupid"]
            subquery_params['search'] = {"name": self.args['filter']['hostgroups']}
            response = self.api_request(method='hostgroup.get', params=subquery_params)
            zabbix_filter['groupids'] = [g['groupid'] for g in response]

        # Zabbix templates
        if self.args['filter'].get('templates') is not None:
            subquery_params['output'] = ["name", "templateid"]
            subquery_params['search'] = {"name": self.args['filter']['templates']}
            response = self.api_request(method='template.get', params=subquery_params)
            zabbix_filter['templateids'] = [t['templateid'] for t in response]

        # Zabbix proxies
        if self.args['filter'].get('proxy') is not None:
            param_name = "host" if Zabbix_version(self.zabbix_version) < Zabbix_version('7.0.0') else "name"
            subquery_params['output'] = [param_name, "proxyid"]
            subquery_params['search'] = {param_name: self.args['filter']['proxy']}
            response = self.api_request(method='proxy.get', params=subquery_params)
            self.ids['proxy'].update({p['proxyid']: p[param_name] for p in response})
            zabbix_filter['proxyids'] = [p['proxyid'] for p in response]

        # Zabbix proxy groups
        if self.args['filter'].get('proxy_group') is not None:
            subquery_params['output'] = ["name", "proxy_groupid"]
            subquery_params['search'] = {"name": self.args['filter']['proxy_group']}
            response = self.api_request(method='proxygroup.get', params=subquery_params)
            self.ids['proxy_group'].update({pg['proxy_groupid']: pg['name'] for pg in response})
            zabbix_filter['proxy_groupids'] = [pg['proxy_groupid'] for pg in response]

        # Host
        if self.args['filter'].get('host') is not None:
            subquery_params['output'] = ["host", "hostid"]
            subquery_params['search'] = {'host': self.args['filter']['host']}
            response = self.api_request(method='host.get', params=subquery_params)
            zabbix_filter['hostids'] = [h['hostid'] for h in response]
        # Name
        if self.args['filter'].get('name') is not None:
            subquery_params['output'] = ["name", "hostid"]
            subquery_params['search'] = {'name': self.args['filter']['name']}
            response = self.api_request(method='host.get', params=subquery_params)
            if 'hostids' in zabbix_filter:
                zabbix_filter['hostids'] = list(set(zabbix_filter['hostids']) & set([h['hostid'] for h in response]))
            else:
                zabbix_filter['hostids'] = [h['hostid'] for h in response]

        # Status
        if self.args['filter'].get('status') is not None:
            zabbix_filter.setdefault('filter', {})
            if str(self.args['filter']['status']).lower() == 'enabled':
                zabbix_filter['filter']['status'] = '0'
            else:
                zabbix_filter['filter']['status'] = '1'

        # Tags
        if self.args['filter'].get('tags') is not None:
            zabbix_filter['tags'] = []
            for tag in self.args['filter']['tags']:
                zabbix_filter['tags'].append({
                    'tag': tag.get('tag'),
                    'value': tag.get('value', ''),
                    'operator': tags_compare_operators.get(str(tag.get('operator', '')), '0')
                })

        # tags_behavior
        if self.args['filter'].get('tags_behavior') is not None:
            zabbix_filter['evaltype'] = '0' if self.args['filter']['tags_behavior'].lower() == 'and/or' else '2'

        return zabbix_filter

    def compare_cached_input_args(self, old_input_args):
        """
        This function compares the current input parameters
        with the parameters stored in the cache.

        If any of the parameters that may affect the data has been changed,
        then the cache will be discarded.

        :param old_input_args: input arguments from cache
        :type: dict

        :rtype: bool
        :returns:
            * True - If all current input parameters match those in the cache.
            * False - If any of the parameters affecting the data has been changed.
        """

        # Check simple parameters
        for parameter in ['zabbix_user', 'zabbix_password', 'zabbix_api_token', 'zabbix_api_url']:
            if self.args.get(parameter) != old_input_args.get(parameter):
                return False

        # output
        if len(list(set(self.args.get('output', [])) ^ set(old_input_args.get('output', [])))) != 0:
            return False

        # query
        old_query = dict((e.lower(), old_input_args['query'][e]) for e in old_input_args.get('query', {}))
        new_query = dict((e.lower(), self.args['query'][e]) for e in self.args.get('query', {}))
        if len(list(set(new_query) ^ set(old_query))) != 0:
            return False
        for key in new_query:
            if len(list(set(new_query[key]) ^ set(old_query[key]))) != 0:
                return False

        # filter
        old_filter_keys = old_input_args.get('filter', {}).keys()
        new_filter_keys = self.args.get('filter', {}).keys()
        if len(list(set(new_filter_keys) ^ set(old_filter_keys))) != 0:
            return False
        for key in self.args.get('filter', {}):
            if key == 'status' or key == 'tags_behavior':
                if self.args['filter'][key] != old_input_args['filter'][key]:
                    return False
            elif key == 'tags':
                for tag in old_input_args['filter'][key] + self.args['filter'][key]:
                    if tag not in old_input_args['filter'][key] or tag not in self.args['filter'][key]:
                        return False
            elif key in ['hostgroups', 'templates', 'proxy', 'proxy_group', 'name', 'host']:
                if len(list(set(self.args['filter'][key]) ^ set(old_input_args['filter'][key]))) != 0:
                    return False

        return True

    def resolve_id_to_names(self):
        """
        The function resolves IDs to names and adds them to the output
        as additional parameters. If a name for any ID is not found among
        the available ones, it will be requested from Zabbix.

        Currently, the following parameters are supported:
            - proxyid -> proxy_name
            - proxy_groupid -> proxy_group_name

        :return: None
        """

        if hasattr(self, 'ids') is False:
            self.ids = {'proxy': {}, 'proxy_group': {}}

        # find all proxyid in self.zabbix_host and request missing proxy
        if 'extend' in self.args.get('output') or 'proxyid' in self.args.get('output'):
            host_proxy_ids = [h.get('proxyid') for h in self.zabbix_hosts]
            request_ids = list(set(host_proxy_ids) - set(self.ids['proxy'].keys()))
            if len(request_ids) > 0:
                param_name = "host" if Zabbix_version(self.zabbix_version) < Zabbix_version('7.0.0') else "name"
                response = self.api_request(
                    method='proxy.get',
                    params={
                        'output': [param_name, 'proxyid'],
                        'proxyids': request_ids})
                self.ids['proxy'].update({p['proxyid']: p[param_name] for p in response})

        # find all proxy_groupid in self.zabbix_host and request missing proxy_group
        if 'extend' in self.args.get('output') or 'proxy_groupid' in self.args.get('output'):
            host_proxy_groupid_ids = [h.get('proxy_groupid') for h in self.zabbix_hosts]
            request_ids = list(set(host_proxy_groupid_ids) - set(self.ids['proxy_group'].keys()))
            if len(request_ids) > 0:
                response = self.api_request(
                    method='proxygroup.get',
                    params={
                        'output': ['name', 'proxy_groupid'],
                        'proxy_groupids': request_ids})
                self.ids['proxy_group'].update({pg['proxy_groupid']: pg['name'] for pg in response})

        for i, host in enumerate(self.zabbix_hosts):

            # resolve proxy name
            if 'proxyid' in host:
                self.zabbix_hosts[i]['proxy_name'] = self.ids['proxy'].get(host['proxyid'], '')

            # # resolve proxy group name
            if 'proxy_groupid' in host:
                self.zabbix_hosts[i]['proxy_group_name'] = self.ids['proxy_group'].get(host['proxy_groupid'], '')

    def parse(self, inventory, loader, path, cache=True):
        """
        The function processes data about hosts in Zabbix.

        Both data from Zabbix API and cached data can be processed.

        :param inventory: Object with inventory data
        :type: object
        :param loader: Loader object
        :type: object
        :param path: Path to inventory file with parameters
        :type: object
        :param cache: Cache parameter
        :type: bool

        :return: None
        """

        super(InventoryModule, self).parse(inventory, loader, path)

        # Check config
        self._read_config_data(path)

        # Get and validate input parameters
        self.args = self.get_options()
        self.zabbix_api_url = self.get_absolute_url()
        self.validate_params()

        # Get constructed parameters
        keyed_groups = self.args.get('keyed_groups')
        strict = self.args.get('strict')
        groups = self.args.get('groups')

        # Get cache parameters
        cache_key = self.get_cache_key(path)
        user_cache_setting = self.args.get('cache')
        attempt_to_read_cache = user_cache_setting and cache
        cache_needs_update = user_cache_setting and not cache

        # Check cache
        if attempt_to_read_cache:
            cached_data = {}
            try:
                cached_data = self._cache[cache_key]
            except KeyError:
                cache_needs_update = True

            # Check the data from the cache. If the data is received, compare the input parameters.
            # If the filter, output or query parameters have changed, then we will request the data again.
            if cached_data:
                if 'input_args' not in cached_data:
                    cache_needs_update = True
                elif self.compare_cached_input_args(cached_data['input_args']) is False:
                    cache_needs_update = True
                elif 'zabbix_hosts' in cached_data:
                    self.zabbix_hosts = cached_data['zabbix_hosts']
                else:
                    cache_needs_update = True

        if not attempt_to_read_cache or cache_needs_update:

            # proxy
            proxy = self.args.get('http_proxy')
            if proxy is not None:
                os.environ['http_proxy'] = proxy
                os.environ['HTTP_PROXY'] = proxy
                os.environ['https_proxy'] = proxy
                os.environ['HTTPS_PROXY'] = proxy

            if hasattr(self, "zabbix_version") is False:
                self.zabbix_version = self.get_api_version()

            self.auth = self.login()

            self.query = {
                'output': 'extend',
                'searchWildcardsEnabled': True}

            # parse query
            if self.args.get('query'):
                self.query.update(self.args['query'])

            # parse filter
            if self.args.get('filter'):
                zabbix_filter = self.parse_filter()
                if zabbix_filter:
                    self.query.update(zabbix_filter)

            # parse output
            if self.args.get('output'):
                if 'extend' in self.args['output']:
                    self.query['output'] = 'extend'
                else:
                    self.query['output'] = list(self.args['output'])
                    if 'host' not in self.query['output']:
                        self.query['output'].append('host')

            # getting result data
            self.zabbix_hosts = self.api_request('host.get', params=self.query)

            # resolve id to names
            self.resolve_id_to_names()

            # logout
            self.logout()

        # Process data from Zabbix API / cached data
        for host in self.zabbix_hosts:

            # Add data about host to inventory
            self.inventory.add_host(host['host'])
            for each in host:
                self.inventory.set_variable(
                    host['host'],
                    '{0}{1}'.format(self.args['prefix'], each),
                    host[each])

            # added for compose vars, keyed-groups and composed groups
            self._set_composite_vars(
                self.args.get('compose'),
                self.inventory.get_host(host['host']).get_vars(),
                host['host'],
                strict=strict)
            self._add_host_to_composed_groups(groups, dict(), host['host'], strict=strict)
            self._add_host_to_keyed_groups(keyed_groups, dict(), host['host'], strict=strict)

        # Save new data to cache
        if cache_needs_update:
            cached_data = {}
            cached_data['zabbix_hosts'] = self.zabbix_hosts
            cached_data['input_args'] = self.args
            self._cache[cache_key] = cached_data
