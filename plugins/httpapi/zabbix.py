# Copyright: Zabbix Ltd
# GNU Affero General Public License v3.0 (see https://www.gnu.org/licenses/agpl-3.0.html#license-text)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
name: zabbix
author:
    - Zabbix Ltd (@zabbix)
short_description: Zabbix HTTP API plugin
description:
    - This plugin is designed to work with Zabbix API.
options:
    http_login:
        type: str
        description: Username for basic HTTP authorization to Zabbix API
        vars:
            - name: http_login
    http_password:
        type: str
        description: Password for basic HTTP authorization to Zabbix API
        vars:
            - name: http_password
    zabbix_api_token:
        type: str
        description: Token for authorization in Zabbix API
        env:
            - name: ZABBIX_API_TOKEN
        vars:
            - name: zabbix_api_token
    zabbix_api_url:
        type: str
        description: Path to access Zabbix API
        env:
            - name: ZABBIX_API_URL
        vars:
            - name: zabbix_api_url
'''

EXAMPLES = r'''
# You can configure Zabbix API connection settings with the following parameters:
- name: Create host groups
  zabbix.zabbix.zabbix_group:
    state: present
    host_groups:
     - Group 1
  vars:
    # Connection parameters
    ansible_host: zabbix-api.com                # Specifying Zabbix API address. You can also use 'delegate_to'.
    ansible_connection: httpapi                 # Specifying to use HTTP API plugin.
    ansible_network_os: zabbix.zabbix.zabbix    # Specifying which HTTP API plugin to use.
    ansible_httpapi_port: 80                    # Specifying the port for connecting to Zabbix API.
    ansible_httpapi_use_ssl: False              # Specifying the type of connection. True for https, False for http (by default).
    ansible_httpapi_validate_certs: False       # Specifying certificate validation.
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

# Example of using options to create a host group
# For a typical application, it is enough to specify only a few parameters
- name: Create host groups
  zabbix.zabbix.zabbix_group:
    state: present
    host_groups:
     - G1
     - G2
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
'''

import json
import base64
from uuid import uuid4

from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.basic import to_text
from ansible.module_utils.connection import ConnectionError


class HttpApi(HttpApiBase):

    def set_become(self, become_context):
        """
        Elevation is not required for Zabbix API - Skipped

        :param become_context: Unused input.

        :return: None
        """
        if self._become:
            self.connection.queue_message(
                "warning",
                "become has no effect over httpapi.")

        return None

    def update_auth(self, response, response_text):
        """
        Auth update is not required for Zabbix API - Skipped

        :param response: Unused input.
        :param response_text: Unused input.

        :return: None
        """
        return None

    def setup_connection(self):
        """
        Function for setup options for connection

        :return: None
        """
        self.auth_token = self.get_option('zabbix_api_token')
        self.http_login = self.get_option('http_login')
        self.http_password = self.get_option('http_password')

        self.url_path = ''
        if self.get_option("zabbix_api_url"):
            url = self.get_option("zabbix_api_url")
            url_parts = [u for u in url.split('/') if len(u) > 0]
            self.url_path = '/' + '/'.join(url_parts)

        return

    def login(self, username, password):
        """
        Function for login in Zabbix.
        If set option 'zabbix_api_token' use auth by token.
        If set options 'http_login' and 'http_password'
        add basic auth for request.

        :param username: username for login
        :type username: str
        :param password: password for login
        :type password: str

        :return: None
        """
        if self.auth_token:
            self.connection._auth = {'auth': self.auth_token}

            return

        if self.http_login and self.http_password:
            username = self.connection._options['remote_user']
            password = self.connection._options['password']
            self.connection.set_option('remote_user', self.http_login)
            self.connection.set_option('password', self.http_password)

        payload = self.build_payload(
            'user.login',
            username=username,
            password=password)
        code, response = self.send_request(data=payload)

        if code == 200 and len(response) > 0:
            self.connection._auth = {'auth': response}

        return

    def logout(self):
        """
        Function for logout from zabbix.

        :return: None
        """
        if self.connection._auth and not self.auth_token:
            payload = self.build_payload("user.logout")
            self.send_request(data=payload)
            self.connection._auth = None
            self.connection._connected = False

        return

    def send_request(self, data, request_method="POST", path="/api_jsonrpc.php"):
        """
        Function for sending request

        :param data: data for sending
        :type data: dict
        :param request_method: method for sending.
        :type request_method: str
        :param path: path for sending.
        :type path: str

        :return: response code and response text
        :rtype: tuple
        """
        # add auth
        methods_wo_auth = [
            'apiinfo.version',
            'user.login']
        if self.connection._auth and data['method'] not in methods_wo_auth:
            data['auth'] = self.connection._auth['auth']

        path = self.url_path + path
        self._display_request(request_method, path)

        response, response_data = self.connection.send(
            path,
            json.dumps(data),
            method=request_method,
            headers=self.build_headers())

        value = to_text(response_data.getvalue())
        result_json = self._response_to_json(value)

        if not isinstance(result_json, bool) and 'error' in result_json:
            raise ConnectionError(
                "REST API returned '{0}' when sending '{1}'".format(
                    to_text(result_json['error']),
                    to_text(data)))

        return response.getcode(), result_json

    def _display_request(self, request_method, path):
        """
        Function for adding message to queue

        :param request_method: info for message
        :type request_method: str
        :param path: info for message
        :type path: str

        :return: None
        """
        self.connection.queue_message(
            "vvv",
            "API request: {0} {1}/{2}".format(
                request_method, self.connection._url, path))

    def _response_to_json(self, response_text):
        """
        Function for transformation response to json

        :param response_text: text for transformation
        :type response_text: dict

        :return: response in json format
        :rtype: dict

        :raise: ConnectionError if get invalid json
        """
        try:
            json_data = json.loads(response_text) if response_text else {}
            if 'result' in json_data:
                json_data = json_data['result']
            return json_data
        except ValueError:
            raise ConnectionError("Invalid JSON response: {0}".format(
                response_text))

    @staticmethod
    def build_payload(method, reqid=str(uuid4()), **kwargs):
        """
        Function for build payload

        :param reqid: id for request
        :type reqid: str
        :param kwargs: additional param for request
        :type kwargs: dict

        :return: parameters for request
        :rtype: dict
        """
        req = {'jsonrpc': '2.0', 'method': method,
               'id': reqid, 'params': kwargs}

        return req

    def build_headers(self):
        """
        Function for build headers

        :return: prepared headers
        :rtype: dict
        """
        headers = {
            'Content-Type': 'application/json-rpc',
            'Accept': 'application/json'}

        if self.http_login is not None and self.http_password is not None:
            auth = base64.b64encode("{0}:{1}".format(
                self.http_login, self.http_password).encode('ascii'))
            headers['Authorization'] = 'Basic {0}'.format(auth.decode('ascii'))

        return headers

    def handle_httperror(self, exc):
        """
        Function for handle httperror

        :returns:
            * False if error code is 401 or 404
            * exc in other case
        """
        if exc.code == 401:
            return False
        if exc.code == 404:
            return False

        return exc
