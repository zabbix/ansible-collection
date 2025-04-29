Zabbix Plugins
=================

This file contains a description, available arguments, and examples of working with plugins and modules from the official Zabbix collection.

The following plugins are supported:
- [HTTP API](#http-api-plugin)
- [Inventory](#inventory-plugin)

The following modules are supported:
- [zabbix_host](#host-module)
- [zabbix_hostgroups](#hostgroups-module)
- [zabbix_proxy](#proxy-module)
- [zabbix_proxy_group](#proxy-group-module)


**Note**: This plugin is still in active development. There may be unidentified issues and the plugin and module arguments may change as development continues.


Table of contents
-----------------
<!--ts-->
  * [Requirements](#requirements)
  * [HTTP API plugin](#http-api-plugin)
    * [Overview](#http-api-plugin-overview)
    * [Parameters](#http-api-plugin-parameters)
    * [Examples](#http-api-plugin-examples)
  * [Hostgroup module](#hostgroup-module)
    * [Overview](#hostgroup-module-overview)
    * [Parameters](#hostgroup-module-parameters)
    * [Examples](#hostgroup-module-examples)
  * [Host module](#host-module)
    * [Overview](#host-module-overview)
    * [Parameters](#host-module-parameters)
    * [Examples](#host-module-examples)
  * [Proxy module](#proxy-module)
    * [Overview](#proxy-module-overview)
    * [Parameters](#proxy-module-parameters)
    * [Examples](#proxy-module-examples)
  * [Proxy group module](#proxy-group-module)
    * [Overview](#proxy-group-module-overview)
    * [Parameters](#proxy-group-module-parameters)
    * [Examples](#proxy-group-module-examples)
  * [Inventory plugin](#inventory-plugin)
    * [Overview](#inventory-plugin-overview)
    * [Parameters](#inventory-plugin-parameters)
    * [Examples](#inventory-plugin-examples)
<!--te-->

Requirements
------------
Plugins and modules are supported under the following conditions:
- Zabbix API >= 6.0
- Ansible core >= 2.16
- Python >= 2.6

Zabbix HTTP API plugin requires additional tools from two Ansible-certified collections:
- ansible.posix >= 2.8
- ansible.utils >= 1.4

You can install the required collections easily via:
```bash
ansible-galaxy collection install ansible.utils ansible.posix
```


HTTP API plugin
------------
## HTTP API plugin overview:
HTTP API plugin provides an interface for working with Zabbix API. Using the available modules, you can create, update, and delete entities in Zabbix.

**Note**: Basic HTTP authentication is not supported since version 7.2.0 of Zabbix API.

## HTTP API plugin parameters:
| Parameter | Type | Default | Description |
|--|--|--|--|
| zabbix_api_token | `string` || Token for authorization in Zabbix API. Available environment variables: `ZABBIX_API_TOKEN`.
| zabbix_api_url | `string` | '' | Path to access Zabbix API. Available environment variables: `ZABBIX_API_URL`.
| http_login | `string` || Username for basic HTTP authentication to Zabbix API. Basic HTTP authentication is not supported since version 7.2.0 of Zabbix API.
| http_password | `string` || Password for basic HTTP authentication to Zabbix API. Basic HTTP authentication is not supported since version 7.2.0 of Zabbix API.

## HTTP API plugin examples:

### Example 1
You can configure the Zabbix API connection settings with the following parameters:

```yaml
- name: Create host groups
  zabbix.zabbix.zabbix_hostgroup:
    state: present
    host_groups:
     - Group 1
  vars:
    # Connection parameters
    ansible_host: zabbix-api.com                # Specify Zabbix API address.
    ansible_connection: httpapi                 # Specify HTTP API plugin.
    ansible_network_os: zabbix.zabbix.zabbix    # Specify which HTTP API plugin to use.
    ansible_httpapi_port: 80                    # Specify the port for connecting to Zabbix API.
    ansible_httpapi_use_ssl: False              # Specify the type of connection. True for https, False for http (by default).
    ansible_httpapi_validate_certs: False       # Specify certificate validation.
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

```

### Example 2
Example of using options to create a host group. For a typical application, it is enough to specify only a few parameters.

```yaml
- name: Create host groups
  zabbix.zabbix.zabbix_hostgroup:
    state: present
    host_groups:
     - G1
     - G2
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

Hostgroup module
------------
## Hostgroup module overview:
This module provides functionality to create and delete host groups in Zabbix.
It supports working with a list of host groups. During the creation process, if any host groups specified in the list already exist in Zabbix, only the missing groups will be created.

## Hostgroup module parameters:
| Parameter | Type | Default | Description |
|--|--|--|--|
| state | `string` | present | Perform actions with host groups: `present` to add host groups, and `absent` to delete them.
| hostgroups | `list` || Specify a list of host groups to create or remove. You can use the aliases `host_group`, `host_groups`, or `name` to refer to the host groups.


## Hostgroup module examples:

### Example 1
To create host groups, you can use:
```yaml
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
```

### Example 2
To delete two host groups - G1 and G2:
```yaml
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
```

Host module
------------
## Host module overview:
This module provides functionality to create, update, and delete hosts in Zabbix. If the specified host already exists, its settings will be updated based on the provided input parameters. Only the specified settings will be updated, while any settings not included in the task will remain unchanged.

**Note**: This module supports only one interface of each type. If the host already has multiple interfaces of the same type, the module will raise an error indicating the need to manually resolve the conflict.

**Note**: If the task includes the <code>tls_psk_identity</code> and <code>tls_psk</code> parameters, or a macro of the secret type, each execution of the task will result in an update.

## Host module parameters:
<table>
    <thead>
        <tr>
            <th colspan="3">Parameter</th>
            <th>Type</th>
            <th>Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=3 align="left">state</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">present</td>
            <td colspan=1 align="left">Perform actions with host: <code>present</code> to add host (update, in case the host is already created) and <code>absent</code> to delete it.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">host</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Host name to create. The name of an existing host in case of an update. You can use the aliases <code>host_name</code> to refer to the host name.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">name</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The visible host name. You can use the aliases <code>visible_name</code> to refer to the host name.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">hostgroups</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The host groups that will replace the current host's host groups. Any host groups not specified in the task will be unlinked. If you are creating a new host, this field is required. You can use the aliases <code>host_group</code> or <code>host_groups</code> to refer to the host groups.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">templates</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The templates that will replace the current host's templates. Any templates not specified in the task will be unlinked. You can use the aliases <code>link_templates</code>, <code>template</code> or <code>host_templates</code> to refer to the templates. To remove all templates from a host, you can specify an empty list, <code>templates=[]</code>.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">status</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The host status. Available values: <code>enabled</code> or <code>disabled</code>.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">description</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The host description.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tags</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The tags that will replace the current host's tags. Any tags not specified in the task will be removed. You can use the alias <code>host_tags</code> to refer to the tags. To remove all tags from a host, you can specify an empty list, <code>tags=[]</code>. Has additional options.</td>
        </tr>
        <tr>
            <td rowspan=2></td>
            <td colspan=2 align="left">tag</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The host tag name.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">value</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">''</td>
            <td colspan=1 align="left">The host tag value.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">macros</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The macros that will replace the current host's macros. Any macros not specified in the task will be removed. If a macro of the secret type is specified, each execution of the task will result in an update. To remove all macros from a host, you can specify an empty list, <code>macros=[]</code>. Has additional options.</td>
        </tr>
        <tr>
            <td rowspan=4></td>
            <td colspan=2 align="left">macro</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The macro name. The parameter is required when describing macros.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">value</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">''</td>
            <td colspan=1 align="left">The value of the macro.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">description</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">''</td>
            <td colspan=1 align="left">The description of the macro.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">type</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">text</td>
            <td colspan=1 align="left">The type of the macro. Available types: <li>text<li>secret<li>vault_secret</td>
        </tr>
        <tr>
            <td colspan=3 align="left">ipmi_authtype</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">IPMI authentication algorithm. Available values: <li>default<li>none<li>md2<li>md5<li>straight<li>oem<li>rmcp+</td>
        </tr>
        <tr>
            <td colspan=3 align="left">ipmi_privilege</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">IPMI privilege level. Available values: <li>callback<li>user<li>operator<li>admin<li>oem</td>
        </tr>
        <tr>
            <td colspan=3 align="left">ipmi_username</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">IPMI username.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">ipmi_password</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">IPMI password.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_accept</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Connections type from host. Available values: <li>unencrypted<li>psk<li>cert</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_connect</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Connections to the host. Available values: <li>unencrypted<li>psk<li>cert</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_psk_identity</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">PSK identity.<br>If you are creating a new host and you have PSK mode (tls_accept or tls_connect), then this parameter is required. If you are upgrading an existing host and it already has PSK mode configured, whether it is in accept or connect mode, you can skip this parameter. If the task includes this parameter, each execution of the task will result in an update.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_psk</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The preshared key, at least 32 hex digits.<br>If you are creating a new host and you have PSK mode (tls_accept or tls_connect), then this parameter is required. If you are upgrading an existing host and it already has PSK mode configured, whether it is in accept or connect mode, you can skip this parameter. If the task includes this parameter, each execution of the task will result in an update.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_issuer</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Certificate issuer.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_subject</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Certificate subject.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">proxy</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Name of the proxy that is used to monitor the host.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">proxy_group</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Name of the proxy group that is used to monitor the host. Used only for Zabbix versions above 7.0.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">inventory_mode</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Host inventory population mode. Available values: <li>automatic<li>manual<li>disabled</td>
        </tr>
        <tr>
            <td colspan=3 align="left" valign="top">inventory</td>
            <td colspan=1 align="left" valign="top"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The host inventory object.<br>Available values:<br>type, type_full, name, alias, os, os_full, os_short, serialno_a, serialno_b, tag, asset_tag, macaddress_a, macaddress_b, hardware, hardware_full, software, software_full, software_app_a, software_app_b, software_app_c, software_app_d, software_app_e, contact, location, location_lat, location_lon, notes, chassis, model, hw_arch, vendor, contract_number, installer_name, deployment_status, url_a, url_b, url_c, host_networks, host_netmask, host_router, oob_ip, oob_netmask, oob_router, date_hw_purchase, date_hw_install, date_hw_expiry, date_hw_decomm, site_address_a, site_address_b, site_address_c, site_city, site_state, site_country, site_zip, site_rack, site_notes, poc_1_name, poc_1_email, poc_1_phone_a, poc_1_phone_b, poc_1_cell, poc_1_screen, poc_1_notes, poc_2_name, poc_2_email, poc_2_phone_a, poc_2_phone_b, poc_2_cell, poc_2_screen, poc_2_notes.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">interfaces</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The interfaces that will replace the current host's interfaces. Any interfaces not specified in the task will be removed. Only one interface of each type is supported. Has additional options.</td>
        </tr>
        <tr>
            <td rowspan=17></td>
            <td colspan=2 align="left">type</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Interface type. Available values: <li>agent<li>snmp<li>ipmi<li>jmx</td>
        </tr>
        <tr>
            <td colspan=2 align="left">useip</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">True</td>
            <td colspan=1 align="left">Whether the connection should be made through IP.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">ip</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">127.0.0.1</td>
            <td colspan=1 align="left">The IP address used by the interface. Can be empty if the connection is made through DNS.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">dns</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">''</td>
            <td colspan=1 align="left">The DNS name used by the interface. Can be empty if the connection is made through IP.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">port</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"><nobr><li>agent: 10050</nobr><nobr><li>snmp: 161</nobr><nobr><li>ipmi: 623</nobr><nobr><li>jmx: 12345</nobr></td>
            <td colspan=1 align="left">Port number used by the interface. Can contain user macros.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">details</td>
            <td colspan=1 align="left"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Additional detail object for interface. Required with SNMP interfaces. Has additional options.</td>
        </tr>
        <tr>
            <td rowspan=11></td>
            <td colspan=1 align="left">version</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMP interface version. Required with SNMP interfaces. Available values: <li>1<li>2<li>3</td>
        </tr>
        <tr>
            <td colspan=1 align="left">bulk</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Whether to use bulk SNMP. Required with SNMP interfaces.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">community</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMP community. Required with SNMP interfaces. Used only with SNMP interface versions 1 and 2.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">max_repetitions</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Max repetition count is applicable to discovery and walk only. Required with SNMP interfaces. Used only with SNMP interface versions 2 and 3. Used only for Zabbix versions above 6.4.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">contextname</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 context name. Required with SNMP interface version 3.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">securityname</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 security name. Required with SNMP interface version 3.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">securitylevel</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 security level. Required with SNMP interface version 3. Available values: <li>noAuthNoPriv<li>authNoPriv<li>authPriv</td>
        </tr>
        <tr>
            <td colspan=1 align="left">authprotocol</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 authentication protocol. Required with SNMP interface version 3 and <code>securitylevel</code> set to <code>authNoPriv</code>. Available values: <li>md5<li>sha1<li>sha224<li>sha256<li>sha384<li>sha512</td>
        </tr>
        <tr>
            <td colspan=1 align="left">authpassphrase</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 authentication passphrase. Required with SNMP interface version 3 and <code>securitylevel</code> set to <code>authNoPriv</code>.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">privprotocol</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 privacy protocol. Required with SNMP interface version 3 and <code>securitylevel</code> set to <code>authPriv</code>. Available values: <li>des<li>aes128<li>aes192<li>aes256<li>aes192c<li>aes256c</td>
        </tr>
        <tr>
            <td colspan=1 align="left">privpassphrase</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 privacy passphrase. Required with SNMP interface version 3 and <code>securitylevel</code> set to <code>authPriv</code>.</td>
        </tr>
    </tbody>
</table>

## Host module examples:

### Example 1
To create a host with minimum parameters, you can use this example. Note that the <code>hostgroup</code> parameter is required.
```yaml
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
```

### Example 2
To create a host with maximum parameters, you can use this example.
```yaml
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
      type: ""                            # To specify an empty value
      serialno_b: example value
      hardware_full: |
        very very long
        multiple string value
    interfaces:
      - type: agent                       # To specify an interface with default parameters (the IP will be 127.0.0.1)
      - type: ipmi
      - type: jmx
        ip: 192.168.100.51
        dns: test.com
        useip: true
        port: 12345
      - type: snmp
        ip: 192.168.100.50
        dns: switch.local
        port: 169                         # To specify a non-standard value
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
```

### Example 3
To update the host to empty parameters, you can use this example.
```yaml
- name: Clean all parameters from host
  zabbix.zabbix.zabbix_host:
    state: present
    host: Example host
    hostgroups:                           # Host group must not be empty
      - Linux servers
    templates: []                         # Read important note in this example
    status: enabled
    description: ''
    name: ''                              # The technical name will be used
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
    interfaces: []                        # Read important note in this example
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

**IMPORTANT**: If you want to clear templates and interfaces on the host, but the template contains items that use this interface, then you need to perform this operation in two tasks: first, unassign the templates; then, remove the interfaces in the second task. If the template contains items that do not use an interface, clearing the template and removing the interfaces can be done in one task.

First step: clearing templates
```yaml
- name: Clearing templates
  zabbix.zabbix.zabbix_host:
    host: Example host
    templates: []
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

Second step: clearing interfaces
```yaml
- name: Clearing interfaces
  zabbix.zabbix.zabbix_host:
    host: Example host
    interfaces: []
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 4
To update only one parameter, you can specify just the host name (used for searching) and the desired parameter. The rest of the host parameters will not be changed. For example, if you want to turn off a host, you can use the following example:
```yaml
- name: Update host status
  zabbix.zabbix.zabbix_host:
    host: Example host
    status: disabled
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 5
To remove a host, you can use:
```yaml
- name: Delete host
  zabbix.zabbix.zabbix_host:
    state: absent
    host: Example host
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

Proxy module
------------
## Proxy module overview:
This module provides the functionality to create, update, and delete a proxy in Zabbix. If the specified proxy already exists, its settings will be updated based on the provided input parameters. Only the specified settings will be updated, while any settings not included in the task will remain unchanged.

**Note**: If the task includes the <code>tls_psk_identity</code> and <code>tls_psk</code> parameters, each execution of the task will result in an update.

## Proxy module parameters:
<table>
    <thead>
        <tr>
            <th colspan="2">Parameter</th>
            <th>Type</th>
            <th>Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=2 align="left">state</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">present</td>
            <td colspan=1 align="left">Perform actions with the proxy: <code>present</code> to add the proxy (update, in case the proxy is already created) and <code>absent</code> to delete it.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">name</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Proxy name to create. The name of an existing proxy in case of an update.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">mode</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">active</td>
            <td colspan=1 align="left">Type of proxy. Available values: <code>active</code> or <code>passive</code>. You can use the aliases <code>operating_mode</code>.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">proxy_group</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The name of the proxy group to which this proxy belongs. Used only for Zabbix versions above 7.0. Set the value to empty to exclude the proxy from the proxy group <code>proxy_group=''</code>.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">local_address</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Address for active agents. IP address or DNS name to connect to. Used only for Zabbix versions above 7.0. Required if <code>proxy_group</code> is not empty when adding a proxy to a proxy group. Set <code>local_address=''</code> to clean.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">local_port</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Local proxy port number to connect to. Used only for Zabbix versions above 7.0. Required if <code>proxy_group</code> is not empty when adding a proxy to a proxy group. Set <code>local_port=''</code> or <code>local_port='10051'</code> to clean or reset to the default value.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">interface</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The proxy interface object defines the interface used to connect to a passive proxy. Supported only in passive proxy mode. Has additional options.</td>
        </tr>
        <tr>
            <td rowspan=3></td>
            <td colspan=1 align="left">address</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">127.0.0.1</td>
            <td colspan=1 align="left">IP address or DNS name to connect to. Supported only in passive proxy mode. Set <code>address=''</code> or <code>address='127.0.0.1'</code> to clean or reset to the default value.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">port</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">10051</td>
            <td colspan=1 align="left">Port number to connect to. Supported only in passive proxy mode. Set <code>port=''</code> or <code>port='10051'</code> to clean or reset to the default value.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">useip</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">True</td>
            <td colspan=1 align="left">Whether the connection should be made through IP or DNS. In Zabbix versions 7.0 and above, this parameter will be ignored!</td>
        </tr>
        <tr>
            <td colspan=2 align="left">allowed_addresses</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Comma-delimited IP addresses or DNS names of an active Zabbix proxy. Supported only in active proxy mode. You can use the aliases <code>proxy_address</code>. Set <code>allowed_addresses=''</code> to clean.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tls_connect</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Connections to the proxy. Supported only in passive proxy mode. Available values: <li>''<li>unencrypted<li>psk<li>cert.<br>Set <code>tls_connect=''</code> to clean.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tls_accept</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Connections from the proxy. Supported only in active proxy mode. Available values: <li>unencrypted<li>psk<li>cert.<br>Set <code>tls_accept=[]</code> to clean.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tls_psk_identity</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">PSK identity.<br>If you are creating a new proxy and have the PSK mode (tls_accept or tls_connect), then this parameter is required. If you are upgrading an existing proxy and it already has the PSK mode configured, whether it is in accept or connect mode, you can skip this parameter. If the parameter is defined, each execution of the task will result in an update.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tls_psk</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The pre-shared key, at least 32 hex digits.<br>If you are creating a new proxy and have the PSK mode (tls_accept or tls_connect), then this parameter is required. If you are upgrading an existing proxy and it already has PSK mode configured, whether it is in accept or connect mode, you can skip this parameter. If the parameter is defined, each execution of the task will result in an update.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tls_issuer</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Certificate issuer.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tls_subject</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Certificate subject.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">custom_timeouts</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Whether to override global item timeouts on the proxy level. You can use the aliases <code>timeouts</code>. Has additional options. Set <code>custom_timeouts={}</code> to clear all configured timeouts and use global ones. Used only for Zabbix versions above 7.0.</td>
        </tr>
        <tr>
            <td rowspan=10></td>
            <td colspan=1 align="left">timeout_zabbix_agent</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing Zabbix agent checks. You can use the aliases <code>zabbix_agent</code>. Set <code>timeout_zabbix_agent=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_simple_check</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing simple checks. You can use the aliases <code>simple_check</code>. Set <code>timeout_simple_check=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_snmp_agent</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing SNMP checks. You can use the aliases <code>snmp_agent</code>. Set <code>timeout_snmp_agent=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_external_check</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing external checks. You can use the aliases <code>external_check</code>. Set <code>timeout_external_check=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_db_monitor</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing database checks. You can use the aliases <code>db_monitor</code>. Set <code>timeout_db_monitor=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_http_agent</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing HTTP agent checks. You can use the aliases <code>http_agent</code>. Set <code>timeout_http_agent=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_ssh_agent</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing SSH agent checks. You can use the aliases <code>ssh_agent</code>. Set <code>timeout_ssh_agent=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_telnet_agent</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing Telnet checks. You can use the aliases <code>telnet_agent</code>. Set <code>timeout_telnet_agent=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_script</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing script checks. You can use the aliases <code>script</code>. Set <code>timeout_script=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">timeout_browser</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Spend no more than the time specified (in seconds) on processing browser checks. You can use the aliases <code>browser</code>. Set <code>timeout_browser=''</code> to clear the value and use the global timeout for this type of checks.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">description</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Proxy description.</td>
        </tr>
    </tbody>
</table>

## Proxy module examples:

### Example 1
To create a proxy with minimum parameters, you can use this example.
```yaml
- name: Create proxy
  zabbix.zabbix.zabbix_proxy:
    state: present
    name: My Zabbix proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 2
To create a proxy with maximum parameters, you can use this example. Note that some of the parameters depend on the proxy operating mode: active or passive.
```yaml
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
        timeout_snmp_agent: '{$MY_SNMP_TIMEOUT}'    # To use global macro (this macro must exist in global macro)
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
```

### Example 3
To update the proxy to empty parameters, you can use this example.
```yaml
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
```

### Example 4
To update only one parameter, you can specify just the proxy name (used for searching) and the desired parameter. The rest of the proxy parameters will not be changed. For example, if you want to update the proxy description, you can use the following example:
```yaml
- name: Update proxy description
  zabbix.zabbix.zabbix_proxy:
    name: My Zabbix proxy
    description: Description of my proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 5
To remove a proxy, you can use:
```yaml
- name: Delete proxy
  zabbix.zabbix.zabbix_proxy:
    state: absent
    name: My Zabbix proxy
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

Proxy group module
------------
## Proxy group module overview:
This module provides the functionality to create, update, and delete a proxy group in Zabbix. If the specified proxy group already exists, its settings will be updated based on the provided input parameters. Only the specified settings will be updated, while any settings not included in the task will remain unchanged. Supported only for Zabbix versions above 7.0.

## Proxy group module parameters:
<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>Type</th>
            <th>Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=1 align="left">state</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left">present</td>
            <td colspan=1 align="left">Perform actions with the proxy group: <code>present</code> to add a proxy group (update, in case the proxy group is already created) and <code>absent</code> to delete it.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">name</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Proxy group name to create. The name of an existing proxy group in case of an update.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">failover_delay</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Failover period for each proxy in the group to have the online/offline state. Time suffixes are supported, e.g. 30s, 1m. User macros are supported. Possible values between 10s-15m. Set to empty to reset to the default value.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">min_online</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Minimum number of online proxies required for the group to be online. User macros are supported. Possible value range 1-1000. Set to empty to reset to the default value.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">description</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Description of the proxy group.</td>
        </tr>
    </tbody>
</table>

## Proxy group module examples:

### Example 1
To create a proxy group with minimum parameters, you can use this example.
```yaml
- name: Create proxy group
  zabbix.zabbix.zabbix_proxy_group:
    state: present
    name: My proxy group
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 2
To create a proxy group with maximum parameters, you can use this example.
```yaml
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
```

### Example 3
To update a proxy group to empty parameters, you can use this example.
```yaml
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
```

### Example 4
To update only one parameter, you can specify just the proxy group name (used for searching) and the desired parameter. The rest of the proxy group parameters will not be changed. For example, if you want to update the proxy group description, you can use the following example.
```yaml
- name: Update proxy group description
  zabbix.zabbix.zabbix_proxy_group:
    name: My proxy group
    description: Description of my proxy group
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 5
To remove a proxy group, you can use:
```yaml
- name: Delete proxy group
  zabbix.zabbix.zabbix_proxy_group:
    state: absent
    name: My proxy group
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

Inventory plugin
------------
## Inventory plugin overview:
The inventory plugin allows Ansible users to generate a dynamic inventory based on data from the Zabbix installation. Using the available filtering methods, the user can specify the search criteria for hosts in Zabbix, as well as limit the set of returned fields.

**Note**: Basic HTTP authentication is not supported since version 7.2.0 of Zabbix API.

## Inventory plugin parameters:
<table>
    <thead>
        <tr>
            <th colspan="3">Parameter</th>
            <th>Type</th>
            <th>Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=3 align="left">cache</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">False</td>
            <td colspan=1 align="left">Toggle to enable/disable the caching of inventory source data; requires a cache plugin setup to work.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">cache_connection</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Cache connection data or path; please see cache plugin documentation for specifics.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">cache_plugin</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">memory</td>
            <td colspan=1 align="left">Cache plugin to use for inventory source data. To see all available methods, you can use <code>ansible-doc -t cache -l</code>.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">cache_prefix</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">ansible_inventory_</td>
            <td colspan=1 align="left">Prefix to use for cache plugin files/tables.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">cache_timeout</td>
            <td colspan=1 align="left"><code>int</code></td>
            <td colspan=1 align="left">3600</td>
            <td colspan=1 align="left">Cache duration in seconds.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">compose</td>
            <td colspan=1 align="left"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Create variables from Jinja2 expressions.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">connection_timeout</td>
            <td colspan=1 align="left"><code>int</code></td>
            <td colspan=1 align="left">10</td>
            <td colspan=1 align="left">Timeout for connecting to Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">filter</td>
            <td colspan=1 align="left"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The parameter is used to select hosts in Zabbix. Each parameter refines the search. For multiple parameters, 'AND' logic is applied. Specifying <code>hostgroups</code> and <code>templates</code> will return a host that is both a member of any of the specified host groups and has any of the specified templates.</td>
        </tr>
        <tr>
            <td rowspan=11></td>
            <td colspan=2 align="left">host</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of host names (technical names) for host search in Zabbix. Will return hosts that match the given technical host names. Wildcard search is possible. Case-sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">hostgroups</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of host groups for host search in Zabbix. Will return hosts that are linked to the given host groups. Wildcard search is possible. Case-sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">name</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of host names (visible names) for host search in Zabbix. Will return hosts that match the given visible host names. Wildcard search is possible. Case-sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">proxy</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of proxies for host search in Zabbix. Will return hosts that are linked to the given proxies. Wildcard search is possible. Case-sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">proxy_group</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of proxy groups for host search in Zabbix. Will return hosts that are linked to the given proxy groups. Wildcard search is possible. Case-sensitive search. Used only for Zabbix versions above 7.0.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">status</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Desired host status for host search in Zabbix. Can be only <code>enabled</code> or <code>disabled</code>.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tags</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of tags for host search in Zabbix. For multiple tags, the logic to be applied is determined by the <code>tags_behavior</code> parameter.</td>
        </tr>
        <tr>
            <td rowspan=3></td>
            <td colspan=1 align="left">operator</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">contains</td>
            <td colspan=1 align="left">Mode of searching by tags. Available values: <li>contains<li>equals<li>not like<li>not equal<li>exists<li>not exists.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">tag</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Tag name for host search in Zabbix.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">value</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">''</td>
            <td colspan=1 align="left">Tag value for host search in Zabbix.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tags_behavior</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">and/or</td>
            <td colspan=1 align="left">Desired logic for searching by tags.
            This parameter impacts the logic of searching by tags. Can be <code>and</code>, <code>and/or</code> or <code>or</code>.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">templates</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of templates for host search in Zabbix. Will return hosts that are linked to the given templates. Wildcard search is possible. Case-sensitive search.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">groups</td>
            <td colspan=1 align="left"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Add hosts to a group based on Jinja2 conditionals.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">http_login</td>
            <td colspan=1 align="left"><code>srt</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Username for basic HTTP authorization to Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">http_password</td>
            <td colspan=1 align="left"><code>srt</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Password for basic HTTP authorization to Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">http_proxy</td>
            <td colspan=1 align="left"><code>srt</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Address of HTTP proxy for connection to Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">keyed_groups</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Add hosts to a group based on the values of a variable.</td>
        </tr>
        <tr>
            <td rowspan=6></td>
            <td colspan=2 align="left">default_value</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The default value when the host variable's value is an empty string. This option is mutually exclusive with <code>trailing_separator</code>.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">key</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The key from the input dictionary used to generate groups.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">parent_group</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Parent group for a keyed group.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">prefix</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">A keyed group name will start with this prefix.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">separator</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">_</td>
            <td colspan=1 align="left">Separator used to build the keyed group name.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">trailing_separator</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">_</td>
            <td colspan=1 align="left">Set this option to <code>False</code> to omit the <code>separator</code> after the host variable when the value is an empty string. This option is mutually exclusive with <code>default_value</code>.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">leading_separator</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">True</td>
            <td colspan=1 align="left">Use in conjunction with <code>keyed_groups</code>.
            By default, a keyed group that does not have a prefix or separator provided will have a name that starts with an underscore. This is because the default prefix is <code>""</code> and the default separator is <code>"_"</code>.
            Set this option to <code>False</code> to omit the leading underscore (or other separator) if no prefix is given.
            If the group name is derived from a mapping, the separator is still used
            to concatenate the items. To not use a separator in the group name at all, set the separator for the keyed group to an empty string.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">output</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left">extend</td>
            <td colspan=1 align="left">Object properties to be returned. List of available fields depends on the Zabbix version.<br>See also:<br>https://www.zabbix.com/documentation/6.0/en/manual/api/reference/host/object
            <br>https://www.zabbix.com/documentation/current/en/manual/api/reference/host/object
            <br><br>The fields <code>hostid</code> and <code>host</code> will always be given from Zabbix.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">prefix</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">zabbix_</td>
            <td colspan=1 align="left">Prefix to use for parameters given from Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">query</td>
            <td colspan=1 align="left"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Additional parameters for getting linked objects for the host.
            List of available fields depends on the Zabbix version. Available query for Zabbix 6.0: selectDiscoveries<li>selectDiscoveryRule<li>selectGraphs, selectHostDiscovery<li>selectHostGroups<li>selectGroups<li>selectHttpTests, selectInterfaces<li>selectInventory<li>selectItems<li>selectMacros, selectParentTemplates<li>selectDashboards<li>selectTags<li>selectInheritedTags, selectTriggers<li>selectValueMaps.<br>
            In Zabbix 6.4, <code>selectGroups</code> was deprecated. Please use <code>selectHostGroups</code> instead.<br>
            See also https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get#parameters</td>
        </tr>
        <tr>
            <td colspan=3 align="left">strict</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">False</td>
            <td colspan=1 align="left">If <code>true</code>, make invalid entries a fatal error, otherwise skip and continue. Since it is possible to use facts in the expressions, they might not always be available and those errors are ignored by default.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">use_extra_vars</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">False</td>
            <td colspan=1 align="left">Merge extra vars into the available variables for composition (highest precedence).</td>
        </tr>
        <tr>
            <td colspan=3 align="left">validate_certs</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">True</td>
            <td colspan=1 align="left">Whether the connection should be made with validation certificates.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">zabbix_api_token</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Token for authorization to Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">zabbix_api_url</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Path to access Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">zabbix_password</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Password for logging into Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">zabbix_user</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Username for logging into Zabbix API.</td>
        </tr>
    </tbody>
</table>

## Inventory plugin examples:

### Example 1
Minimum set of parameters for searching.
You need to specify the name of the plugin, URL, and credentials (login and password or API token).

**IMPORTANT**: Keep in mind that with these parameters, all hosts with all host parameters will be returned from Zabbix. This can create an excessive load on Zabbix server. For selecting the host and fields, use the filter and output options.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
```


### Filter examples

### Example 2
To select hosts by host group name, you can use the following example. In this example, all hosts linked to any host groups starting with 'Linux' (Linux, Linux servers, Linux Ubuntu, etc.) will be returned.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group (in string format with asterisk).
filter:
  hostgroups: 'Linux*'
```

### Example 3
To select hosts from a particular host group, you can use the following example. In this example, only hosts linked to the host group 'Linux' will be returned.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group (in string format).
filter:
  hostgroups: Linux
```

### Example 4
To select hosts from several host groups, you can use the following example.
In this example, all hosts linked to any of the host groups 'Linux', 'Linux Ubuntu', or host groups starting with 'Windows' will be returned.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group (in list format).
filter:
  hostgroups:
    - Linux
    - Linux Ubuntu
    - 'Windows*'
```

### Example 5
You can use all available filter options to search for hosts in Zabbix.
You can use the wildcard search for: host groups, templates, proxy, name (visible name), host (technical name).
Additionally, you can use `status` for filtering, and search only for enabled or disabled hosts. You can use tags for searching by tag name or tag value.
In this example, all hosts linked to the host group `Linux` and to any of the `'*http*'` or `'*agent*'` templates as well as containing `sql` or `SQL` in their visible names will be returned.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group, template, and visible name at the same time.
filter:
  hostgroups: Linux
  templates: ['*HTTP*', '*agent*']
  name: ['*sql*', '*SQL*']
```

### Output examples

### Example 6
To limit fields in the output, specify the list of fields in the output options.
In this example, only the name and two mandatory fields (hostid and host) will be returned.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: Linux

# Add list of output parameters.
output: name
```

### Example 7
To have several output fields, you need to specify them in list format.
In this example, name, status, and two mandatory fields (hostid and host) will be returned.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: Linux

# Add the list of output parameters.
output:
  - name
  - status
```

### Postprocessing examples
For postprocessing, you can use:
- keyed_groups
- groups
- compose

### Example 8
To convert the digit status to verbose, you can use `compose` from the next example.
To group by status (enabled, disabled) from the output, you can use `groups` from the next example.
To group by Zabbix host group, you can use `keyed_groups` from the next example.

**IMPORTANT**: Make sure that the necessary data is present in the output. For this example, `groups` must be present for grouping with `keyed_groups`.

**IMPORTANT**: Keep in mind that all parameters from Zabbix will have a prefix (by default, `zabbix_`) that you need to specify in postprocessing (zabbix_groups, zabbix_status, etc.).

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: 'Linux*'

# Add query for selecting host groups from hosts. This parameter will be used for grouping.
query:
  selectGroups: ['name']

# Compose for transformation from digit status (0, 1) to verbose (Enabled, Disabled).
compose:
  zabbix_verbose_status: zabbix_status.replace("1", "Disabled").replace("0", "Enabled")

# Grouping by status.
# If status is '0', host will be added to group 'enabled'.
# If status is '1', host will be added to group 'disabled'.
groups:
  enabled: zabbix_status == "0"
  disabled: zabbix_status == "1"

# Grouping with keyed_group.
# Jinja pattern will be used as a key for grouping. As a result, we will have the same groups as in Zabbix.
keyed_groups:
  - key: zabbix_groups | map(attribute='name')
    separator: ""
```

### Example 9
For grouping by template name.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: 'Linux*'

# Add query for selecting templates from hosts. This parameter will be used for grouping.
query:
  selectParentTemplates: ['name']

# Grouping with keyed_group.
# Jinja pattern will be used as a key for grouping. As a result, we will have groups corresponding to the template names in Zabbix.
keyed_groups:
  - key: zabbix_parentTemplates | map(attribute='name')
    separator: ""
```

### Example 10
For searching by the `Location` tag and grouping by tag name.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by tag name.
filter:
  tags:
    - tag: Location

# Add query for selecting tags from hosts. This parameter will be used for grouping.
query:
  selectTags: 'extend'

# Grouping with keyed_group.
# Jinja pattern will be used as a key for grouping. As a result, we will have groups corresponding to the tag name in Zabbix.
keyed_groups:
  - key: zabbix_tags | map(attribute='tag')
    separator: ""
```

### Example 11
For searching by the `Location` tag and grouping by tag values.
In this example, hosts will be grouped by tag value. If you have the tags: (Location: Riga, Location: Berlin),
then the following groups will be created: Riga, Berlin.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by tag name.
filter:
  tags:
    - tag: Location

# Add query for selecting tags from hosts. This parameter will be used for grouping.
query:
  selectTags: 'extend'

# Grouping with keyed_group.
# Jinja pattern will be used as a key for grouping. As a result, we will have groups corresponding to the tag values in Zabbix.
keyed_groups:
  - key: dict(zabbix_tags | items2dict(key_name="tag"))['Location']
    separator: ""
```

### Example 12
For transforming given interfaces to the list of IP addresses, you can use `compose` and the following example.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: 'Linux*'

# Add query for selecting interfaces from hosts. This parameter will be used for composing.
query:
  selectInterfaces: ['ip']

# Add 'compose' for transforming Zabbix interfaces to the list of IP addresses.
compose:
  zabbix_ip_list: zabbix_interfaces | map(attribute='ip')
```

### Example 13
For transforming given host groups to the list, you can use 'compose' and the following example.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: 'Linux*'

# Add query for selecting host groups from hosts. This parameter will be used for composing.
query:
  selectGroups: ['name']

# Add 'compose' for transforming Zabbix host groups to the list of host groups.
compose:
  zabbix_groups_list: zabbix_groups | map(attribute='name')
```

### Example 14
You can use cache for inventory.
During the loading of cached data, the plugin will compare the input parameters. If any parameters impacting the given data
(login, password, API token, URL, output, filter, query) have been changed, then cached data will be skipped and new data will be requested from Zabbix.
For caching, you can use the following example:

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching by host group.
filter:
  hostgroups: 'Linux*'

# Add caching options.
cache: yes
cache_plugin: jsonfile
cache_timeout: 7200
cache_connection: /tmp/zabbix_inventory
```

### Complex examples

### Example 15
In this example, you can use filtering by host group, template, proxy, tag, name, status.
Grouping by Zabbix host groups.
Transforming IP addresses to the list of IP.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching.
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

# Add query for host groups and interfaces.
query:
  selectGroups: ['name']
  selectInterfaces: ['ip']

# Add output.
output:
  - name

# Add postprocessing for converting 'zabbix_interfaces' to the list of interfaces and creating groups based on Zabbix host groups.
compose:
  zabbix_ip_list: zabbix_interfaces | map(attribute='ip')
keyed_groups:
  - key: zabbix_groups | map(attribute='name')
    separator: ""
```

### Example 16
In this example, you can apply filtering by the `Location` tag with an empty value and grouping by status (enabled, disabled).
In the example, the status was transformed from a digit value to a verbose value and then used in `keyed_groups` for grouping by verbose statuses.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials.
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for searching.
filter:
  tags:
    - tag: Location
      value: ''
      operator: equals

# Add query for tags.
query:
  selectTags: 'extend'

# Add output.
output:
  - name

# Add postprocessing.
keyed_groups:
  - key: zabbix_verbose_status
    separator: ""
compose:
  zabbix_verbose_status: zabbix_status.replace("1", "Disabled").replace("0", "Enabled")
```

### Using extra-vars examples
For using extra-vars, you need to meet 3 conditions:
- add `use_extra_vars: true` to the inventory file or specify the use of extra-vars in the Ansible configuration file;
- specify a variable in the inventory file in 'Jinja' format. (e.g., `{{ url }}`);
- add `--extra-vars` or `-e` with the value in the command line. (e.g., `--extra-vars url="http://localhost"`);

### Example 17
To use extra-vars in your inventory file, see the example below:
- To pass a parameter as a `list`, use the following construct: `-e macros="['macro','value']"`
- To pass a parameter as a `dict`, use the following construct: `-e host_tag="{'tag':'My host test','value':'host 1'}"`
- To pass a parameter as a `string`, use the following construct: `-e os_tag_value="Linux"`, `-e inventory_field="Model"`, `-e url="your-zabbix.com"`

The final command for this example will look like this: `ansible-playbook -e macros="['macro','value']" -e host_tag="{'tag':'My host test','value':'host 1'}" -e os_tag_value="Linux" -e inventory_field="Model" -e url="your-zabbix.com" playbook.yaml -i inventory.yml`

**IMPORTANT**: Please note that the value types of all fields in the inventory file are checked before the extra-vars values are expanded! For example, you cannot specify `query: '{{ my_query }}'` in the inventory file and pass all query fields as extra-vars. The `query` field should accept a value of type `dict`, but it receives a value of type `string` (`'{{ my_query }}'`). In this case, you need to specify query parameters as in the example below.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: 'http://{{ url }}'
zabbix_user: Admin
zabbix_password: zabbix
use_extra_vars: true

# Add additional queries
query:
  selectMacros: '{{ macros }}'
  selectInventory: ['Name', 'OS', '{{ inventory_field }}']

# Filtering by tags
# You can specify the tag value as a variable or the tag as a dictionary.
filter:
  tags: 
    - tag: OS
      value: '{{ os_tag_value }}'
    - '{{ host_tag }}'

# Add output fields
output: 
  - status
  - name
```

License
-------

The Ansible Zabbix collection is released under the GNU Affero General Public License (AGPL) version 3. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.
