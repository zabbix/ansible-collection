Zabbix Plugins
=================

This file contains description, available arguments and examples of working with plugins and modules from official Zabbix collection.

The following plugins are supported:
- [http api](#http-api-plugin)

The following modules are supported:
- [zabbix_host](#host-module)
- [zabbix_hostgroups](#hostgroups-module)


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
<!--te-->

Requirements
------------
Plugins and modules are supported under the following conditions:
- Zabbix API >= 6.0
- Ansible core >= 2.12
- Python >= 2.6

Zabbix http api plugin requires additional tools from two Ansible certified collections:
- ansible.posix >= 2.8
- ansible.utils >= 1.4

You can install required collections easily:
```bash
ansible-galaxy collection install ansible.utils ansible.posix
```


HTTP API plugin
------------
## HTTP API plugin overview:
HTTP API plugin provides an interface for working with the Zabbix API. Using the available modules you can create, update and delete entities in Zabbix.

## HTTP API plugin parameters:
| Parameter | Type | Default | Description |
|--|--|--|--|
| zabbix_api_token | `string` || Token for authorization in Zabbix API. Available environment variables: `ZABBIX_API_TOKEN`
| zabbix_api_url | `string` | '' | Path to access Zabbix API. Available environment variables: `ZABBIX_API_URL`
| http_login | `string` || Username for Basic HTTP authorization to Zabbix API.
| http_password | `string` || Password for Basic HTTP authorization to Zabbix API.


## HTTP API plugin examples:

### Example 1
You can configure Zabbix API connection settings with the following parameters:

```yaml
- name: Create host groups
  zabbix.zabbix.zabbix_group:
    state: present
    host_groups:
     - Group 1
  vars:
    # Connection parameters
    ansible_host: zabbix-api.com                # Specifying Zabbix API address.
    ansible_connection: httpapi                 # Specifying to use httpapi plugin.
    ansible_network_os: zabbix.zabbix.zabbix    # Specifying which httpapi plugin to use.
    ansible_httpapi_port: 80                    # Specifying the port for connecting to Zabbix API.
    ansible_httpapi_use_ssl: False              # Specifying the type of connection. True for https, False for http (by default).
    ansible_httpapi_validate_certs: False       # Specifying certificate validation
    # User parameters for connecting to Zabbix API
    ansible_user: Admin                         # Username to connect to Zabbix API
    ansible_httpapi_pass: zabbix                # Password to connect to Zabbix API
    # Token for connecting to Zabbix API
    zabbix_api_token: your_secret_token         # Specify your token to connect to Zabbix API
    # Path to connect to Zabbix API
    zabbix_api_url: '/zabbix'                   # The field is empty by default. You can specify your connection path. (e.g., '/zabbix')
    # User parameters for Basic HTTP Authorization
    # These options only affect the Basic HTTP Authorization configured on the web server.
    http_login: my_http_login                   # Username for connecting to the API in case of additional Basic HTTP Authorization
    http_password: my_http_password             # Password for connecting to the API in case of additional Basic HTTP Authorization

```

### Example 2
Example of using options to create a host group. For a typical application, it is enough to specify only a few parameters.

```yaml
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
```

Hostgroup module
------------
## Hostgroup module overview:
This module provides functionality to create and delete hostgroups in Zabbix.
It supports working with a list of hostgroups. During the creation process, if any hostgroups specified in the list already exist in Zabbix, only the missing groups will be created.

## Hostgroup module parameters:
| Parameter | Type | Default | Description |
|--|--|--|--|
| state | `string` | present | Perform actions with hostgroups: `present` to add hostgroups, and `absent` to delete them.
| hostgroups | `list` || Specify a list of hostgroups to create or remove. You can use the aliases `host_group`, `host_groups`, or `name` to refer to the hostgroups.


## Hostgroup module examples:

### Example 1
To create hostgroups you can use:
```yaml
- name: Create hostgroups
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
To delete two hostgroups: G1 and G2:
```yaml
- name: Delete hostgroups by name
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

**Note**: If the task includes the tls_psk_identity and tls_psk parameters, or a macro of secret type, each execution of the task will result in an update.

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
            <td colspan=1 align="left">Perform actions with host: <code>present</code> to add host (update, in case the host is already created), and <code>absent</code> to delete them.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">host</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Hostname to create. The name of an existing host in case of an update. You can use the aliases <code>host_name</code> to refer to the host name.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">name</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The visible hostname. You can use the aliases <code>visible_name</code> to refer to the host name.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">hostgroups</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The hostgroups that will replace the current host's hostgroups. Any hostgroups not specified in the task will be unlinked. If you are creating a new host, this field is required. You can use the aliases <code>host_group</code> or <code>host_groups</code> to refer to the hostgroups.</td>
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
            <td colspan=1 align="left">The macros that will replace the current host's macros. Any macros not specified in the task will be removed. If a macro of secret type specified, each execution of the task will result in an update. To remove all macros from a host, you can specify an empty list, <code>macros=[]</code>. Has additional options.</td>
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
            <td colspan=1 align="left">PSK identity.<br>If you are creating a new host and you have PSK mode (tls_accept or tls_connect), then this parameter is required. If you are upgrading an existing host and it already has PSK mode configured, whether it is in accept or connect mode, you can skip this parameter. If the task includes this parameters, each execution of the task will result in an update.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">tls_psk</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">The preshared key, at least 32 hex digits.<br>If you are creating a new host and you have PSK mode (tls_accept or tls_connect), then this parameter is required. If you are upgrading an existing host and it already has PSK mode configured, whether it is in accept or connect mode, you can skip this parameter. If the task includes this parameters, each execution of the task will result in an update.</td>
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
            <td colspan=1 align="left">Additional details object for interface. Required with snmp interfaces. Has additional options.</td>
        </tr>
        <tr>
            <td rowspan=11></td>
            <td colspan=1 align="left">version</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMP interface version. Required with snmp interfaces. Available values: <li>1<li>2<li>3</td>
        </tr>
        <tr>
            <td colspan=1 align="left">bulk</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Whether to use bulk SNMP. Required with snmp interfaces.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">community</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMP community. Required with snmp interfaces. Used only with snmp interfaces version 1 and 2.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">max_repetitions</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Max repetition count is applicable to discovery and walk only. Required with snmp interfaces. Used only with snmp interfaces version 2 and 3. Used only for zabbix versions above 6.4.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">contextname</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 context name. Required with snmp interfaces version 3.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">securityname</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 security name. Required with snmp interfaces version 3.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">securitylevel</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 security level. Required with snmp interfaces version 3. Available values: <li>noAuthNoPriv<li>authNoPriv<li>authPriv</td>
        </tr>
        <tr>
            <td colspan=1 align="left">authprotocol</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 authentication protocol. Required with snmp interfaces version 3 and securitylevel equals <code>authNoPriv</code>. Available values: <li>md5<li>sha1<li>sha224<li>sha256<li>sha384<li>sha512</td>
        </tr>
        <tr>
            <td colspan=1 align="left">authpassphrase</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 authentication passphrase. Required with snmp interfaces version 3 and securitylevel equals <code>authNoPriv</code>.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">privprotocol</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 privacy protocol. Required with snmp interfaces version 3 and securitylevel equals <code>authPriv</code>. Available values: <li>des<li>aes128<li>aes192<li>aes256<li>aes192c<li>aes256c</td>
        </tr>
        <tr>
            <td colspan=1 align="left">privpassphrase</td>
            <td colspan=1 align="left"><code>string</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">SNMPv3 privacy passphrase. Required with snmp interfaces version 3 and securitylevel equals <code>authPriv</code>.</td>
        </tr>
    </tbody>
</table>

## Host module examples:

### Example 1
To create host with minimum parameters you can use this example. Note that the hostgroup parameter is required.
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
To create host with maximum parameters you can use this example.
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
    description: 'Example host'
    name: 'Example host'
    tags:
      - tag: scope
        value: test
    macros:
      - macro: TEST_MACRO
        value: example
        description: Description of example macros
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
      - type: agent                       # To specify an interface with default parameters (the ip will be 127.0.0.1)
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
To update host to empty parameters you can use this example.
```yaml
- name: Clean all parameters from host
  zabbix.zabbix.zabbix_host:
    state: present
    host: Example host
    hostgroups:                           # Host group must be not empty
      - Linux servers
    templates: []
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
    interfaces: []
  vars:
    ansible_network_os: zabbix.zabbix.zabbix
    ansible_connection: httpapi
    ansible_user: Admin
    ansible_httpapi_pass: zabbix
```

### Example 4
To update only one parameter, you can only specify the hostname (used for searching) and the desired parameter. The rest of the host parameters will not be changed. For example, if you want to turn off a host you can use the following example:
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

### Example 4
To remove a host you can use:
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

License
-------

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.