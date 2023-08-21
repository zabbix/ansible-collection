Zabbix Plugins
=================

This file contains description, available arguments and examples of working with plugins and modules from official Zabbix collection.

The following plugins are supported:
- [http api](#http-api-plugin)
- [inventory](#inventory-plugin)

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
  * [Inventory plugin](#inventory-plugin)
    * [Overview](#inventory-plugin-overview)
    * [Parameters](#inventory-plugin-parameters)
    * [Examples](#inventory-plugin-examples)
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
Inventory plugin
------------
## Inventory plugin overview:
Inventory Plugin allows Ansible users to generate a dynamic inventory based on data from Zabbix installation. Using the available filtering methods, the user can specify the search criteria for hosts in Zabbix, as well as limit the set of returned fields.

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
            <td colspan=1 align="left">Toggle to enable/disable the caching of the inventory's source data, requires a cache plugin setup to work.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">cache_connection</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Cache connection data or path, read cache plugin documentation for specifics.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">cache_plugin</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">memory</td>
            <td colspan=1 align="left">Cache plugin to use for the inventory's source data. To see all available methods you can use <code>ansible-doc -t cache -l</code>.</td>
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
            <td colspan=1 align="left">Create vars from jinja2 expressions.</td>
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
            <td colspan=1 align="left">The parameter is used to select hosts in Zabbix. Each parameter refines the search. Between themselves, the parameters work according to the logic AND. If you specify <code>hostgroups</code> and <code>templates</code>, this means that a host will be found that is a member of any of the specified host groups and has any of the specified templates at the same time.</td>
        </tr>
        <tr>
            <td rowspan=11></td>
            <td colspan=2 align="left">host</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of host names (technical name) for search hosts in Zabbix. Will be return hosts that are match to he given technical host names. Available wildcard search. Case sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">hostgroups</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of host groups for search hosts in Zabbix. Will be return hosts that are linked to the given host groups. Available wildcard search. Case sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">name</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of host names (visible name) for search hosts in Zabbix. Will be return hosts that are match to he given visible host names. Available wildcard search. Case sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">proxy</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of proxies for search hosts in Zabbix. Will be return hosts that are linked to the given proxies. Available wildcard search. Case sensitive search.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">status</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Desired host status for search hosts in Zabbix. Can be only <code>enabled</code> or <code>disabled</code>.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tags</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of tags for search hosts in Zabbix. The logic of work between different tags is regulated by another parameter <code>tags_behavior</code>.</td>
        </tr>
        <tr>
            <td rowspan=3></td>
            <td colspan=1 align="left">operator</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">contains</td>
            <td colspan=1 align="left">Mode of searching by tags. Available values: <li>contains<li>equals<li>not like<li>not equal<li>exists<li>not exists</td>
        </tr>
        <tr>
            <td colspan=1 align="left">tag</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Tag name for search hosts in Zabbix.</td>
        </tr>
        <tr>
            <td colspan=1 align="left">value</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">''</td>
            <td colspan=1 align="left">Tag value for search hosts in Zabbix.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">tags_behavior</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">and/or</td>
            <td colspan=1 align="left">Desired logic for searching by tags.
            This parameter impacts to logic for searching by tags. Can be <code>and/or</code> or <code>or</code>.</td>
        </tr>
        <tr>
            <td colspan=2 align="left">templates</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">List of templates for search hosts in Zabbix. Will be return hosts that are linked to the given templates. Available wildcard search. Case sensitive search.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">groups</td>
            <td colspan=1 align="left"><code>dict</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">Add hosts to group based on Jinja2 conditionals.</td>
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
            <td colspan=1 align="left">Add hosts to group based on the values of a variable.</td>
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
            <td colspan=1 align="left">The key from input dictionary used to generate groups</td>
        </tr>
        <tr>
            <td colspan=2 align="left">parent_group</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">parent group for keyed group</td>
        </tr>
        <tr>
            <td colspan=2 align="left">prefix</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">A keyed group name will start with this prefix</td>
        </tr>
        <tr>
            <td colspan=2 align="left">separator</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left">_</td>
            <td colspan=1 align="left">separator used to build the keyed group name</td>
        </tr>
        <tr>
            <td colspan=2 align="left">trailing_separator</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">_</td>
            <td colspan=1 align="left">Set this option to `False' to omit the `separator' after the host variable when the value is an empty string. This option is mutually exclusive with <code>default_value</code>.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">leading_separator</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">True</td>
            <td colspan=1 align="left">Use in conjunction with keyed_groups.
            By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore. This is because the default prefix is "" and the default separator is
            "_".
            Set this option to False to omit the leading underscore (or other
            separator) if no prefix is given.
            If the group name is derived from a mapping the separator is still used
            to concatenate the items. To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">output</td>
            <td colspan=1 align="left"><code>list</code></td>
            <td colspan=1 align="left">extend</td>
            <td colspan=1 align="left">Object properties to be returned. List of available fields depends on Zabbix version. <br>See also https://www.zabbix.com/documentation/6.0/en/manual/api/reference/host/object
            <br>See also https://www.zabbix.com/documentation/current/en/manual/api/reference/host/object
            <br>Fields <code>hostid</code> and <code>host</code> always will be given from Zabbix.</td>
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
            <td colspan=1 align="left">Additional parameters for getting linked objects for  the host.
            List of available fields depends on Zabbix version. Available query for Zabbix 6.0: selectDiscoveries<li>selectDiscoveryRule<li>selectGraphs, selectHostDiscovery<li>selectHostGroups<li>selectGroups<li>selectHttpTests, selectInterfaces<li>selectInventory<li>selectItems<li>selectMacros, selectParentTemplates<li>selectDashboards<li>selectTags<li>selectInheritedTags, selectTriggers<li>selectValueMaps.<br>
            In Zabbix 6.4 selectGroups was deprecated. Please use selectHostGroups instead.<br>
            See also https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get#parameters</td>
        </tr>
        <tr>
            <td colspan=3 align="left">strict</td>
            <td colspan=1 align="left"><code>bool</code></td>
            <td colspan=1 align="left">False</td>
            <td colspan=1 align="left">If <code>yes</code> make invalid entries a fatal error, otherwise skip and continue. Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.</td>
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
            <td colspan=1 align="left">Password for login to Zabbix API.</td>
        </tr>
        <tr>
            <td colspan=3 align="left">zabbix_user</td>
            <td colspan=1 align="left"><code>str</code></td>
            <td colspan=1 align="left"></td>
            <td colspan=1 align="left">User name for login to Zabbix API.</td>
        </tr>
    </tbody>
</table>

## Inventory plugin examples:

### Example 1
Minimal set of parameters for searching.
You need specify name of plugin, url and credentials (login and password or API token).

**IMPORTANT**: Keep in mind, that with this parameters will be given all hosts from Zabbix with all host parameters. This can create an excessive load on the Zabbix server. For select host and fields use the filter and output options.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix
```


### Filter examples

### Example 2
To select hosts by host groups name you can use the following example. In this example will be given all hosts, that are linked to any host groups, which names starts from 'Linux'. (Linux, Linux servers, Linux Ubuntu and etc.)

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups (in string format with asterisk)
filter:
  hostgroups: 'Linux*'
```

### Example 3
To select hosts by certain host group name you can use the following example. In this example will be given all hosts, that are linked only to host group 'Linux'.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups (in string format)
filter:
  hostgroups: Linux
```

### Example 4
To select hosts from several host groups you can use the following example.
In this example will be given all hosts, that are linked to any host groups 'Linux', 'Linux Ubuntu' or all host group which names starts from 'Windows'.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups (in list format)
filter:
  hostgroups:
    - Linux
    - Linux Ubuntu
    - 'Windows*'
```

### Example 5
You can use all available filter options for search hosts in Zabbix.
You can use wildcard search for: hostgroups, templates, proxy, name (visible name), host (technical name).
Also you can use for filtering `status` and search only enabled or disabled hosts. 
Also you can use tags for searching by tag name or tag value.
In this example will be given all hosts, that are linked to the host groups `Linux` and linked to any `'*http*'` or `'*agent*'` templates and visible name contains `sql` or `SQL`.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups, templates and visible name at the same time.
filter:
  hostgroups: Linux
  templates: ['*HTTP*', '*agent*']
  name: ['*sql*', '*SQL*']
```

### Output examples

### Example 6
To limit fields in output you can specified list of fields in output options.
In this example will be given only name and two mandatory fields (hostid and host).

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups.
filter:
  hostgroups: Linux

# Add list of output parameters.
output: name
```

### Example 7
To give several output fields you need specify it in list format.
In this example will be given name, status and two mandatory fields (hostid and host).

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups.
filter:
  hostgroups: Linux

# Add list of output parameters
output:
  - name
  - status
```

### Post processing examples
For post processing you can use:
- keyed_groups
- groups
- compose

### Example 8
To convert digit status to verbose, you can use `compose` from next example.
To group by status (enabled, disabled) from output you can use `groups` from next example.
To group by Zabbix host groups you can use `keyed_groups` from next example.

**IMPORTANT**: Be sure, that necessary data will be present in output. For this example `groups` must be present for grouping with `keyed_groups`.

**IMPORTANT**: Keep in mind, that all parameters from Zabbix will with prefix (by default `zabbix_`). And you need specify it in post processing. (zabbix_groups, zabbix_status and etc.)

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups.
filter:
  hostgroups: 'Linux*'

# Add query for select host groups from hosts. This parameters will be used for grouping.
query:
  selectGroups: ['name']

# Compose for transformation from digit status (0, 1) to verbose (Enabled, Disabled).
compose:
  zabbix_verbose_status: zabbix_status.replace("1", "Disabled").replace("0", "Enabled")

# Grouping by status. 
# If status '0', host will be added to group 'enabled'.
# If status '1', host will be added to group 'disabled'.
groups:
  enabled: zabbix_status == "0"
  disabled: zabbix_status == "1"

# Grouping with keyed_group.
# As key for grouping will be used Jijna pattern. As result we will have the same groups as in Zabbix.
keyed_groups:
  - key: zabbix_groups | map(attribute='name')
    separator: ""
```

### Example 9
For grouping by template names.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups
filter:
  hostgroups: 'Linux*'

# Add query for select templates from hosts. This parameters will be used for grouping.
query:
  selectParentTemplates: ['name']

# Grouping with keyed_group.
# As key for grouping will be used Jijna pattern. As result we will have groups as template names in Zabbix.
keyed_groups:
  - key: zabbix_parentTemplates | map(attribute='name')
    separator: ""
```

### Example 10
For search by tag `Location` and grouping by tag names.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by tag name
filter:
  tags:
    - tag: Location

# Add query for select tags from hosts. This parameters will be used for grouping.
query:
  selectTags: 'extend'

# Grouping with keyed_group.
# As key for grouping will be used Jijna pattern. As result we will have groups tag names in Zabbix.
keyed_groups:
  - key: zabbix_tags | map(attribute='tag')
    separator: ""
```

### Example 11
For search by tag `Location` and grouping by tag values.
In this example hosts will be grouped by tag value. If you have tags: (Location: Riga, Location: Berlin),
than the following groups will be created: Riga, Berlin.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by tag name
filter:
  tags:
    - tag: Location

# Add query for select tags from hosts. This parameters will be used for grouping.
query:
  selectTags: 'extend'

# Grouping with keyed_group.
# As key for grouping will be used Jijna pattern. As result we will have groups tag values in Zabbix.
keyed_groups:
  - key: dict(zabbix_tags | items2dict(key_name="tag"))['Location']
    separator: ""
```

### Example 12
For transform given interfaces to list of ip addresses you can use `compose` and following example.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups
filter:
  hostgroups: 'Linux*'

# Add query for select interfaces from hosts. This parameters will be used for compose.
query:
  selectInterfaces: ['ip']

# Add compose for transformation Zabbix interfaces to list of ip addresses
compose:
  zabbix_ip_list: zabbix_interfaces | map(attribute='ip')
```

### Example 13
For transform given host groups to list you can use 'compose' and following example.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups
filter:
  hostgroups: 'Linux*'

# Add query for select hostgroups from hosts. This parameters will be used for compose.
query:
  selectGroups: ['name']

# Add compose for transformation Zabbix host groups to list of host groups
compose:
  zabbix_groups_list: zabbix_groups | map(attribute='name')
```

### Example 14
You can use cache for inventory.
During load cached data plugin compare input parameters. If any parameters, that impacts to given data were changed,
(login, password, API token, url, output, filter, query) than cached data will be skipped and new data will be requested from Zabbix.
For use caching you can use following example:

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search by host groups
filter:
  hostgroups: 'Linux*'

# Add caching options
cache: yes
cache_plugin: jsonfile
cache_timeout: 7200
cache_connection: /tmp/zabbix_inventory
```

### Complex examples

### Example 15
In this example you can use filter by host groups, templates, proxy, tags, names, status.
Grouping by Zabbix host groups.
Transform ip addresses to list of ip.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search
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

# Add query for host groups and interfaces
query:
  selectGroups: ['name']
  selectInterfaces: ['ip']

# Add output
output:
  - name

# Add post processing. Converting zabbix_interfaces to list of interfaces and creating groups, based on zabbix host groups.
compose:
  zabbix_ip_list: zabbix_interfaces | map(attribute='ip')
keyed_groups:
  - key: zabbix_groups | map(attribute='name')
    separator: ""
```

### Example 16
In this example you can filter by tag `Location` with empty value and grouping by status (enabled, disabled).
In this example status was transformed from digit value to verbose value and than used in `keyed_groups` for grouping by verbose statuses.

```yaml
---
plugin: "zabbix.zabbix.zabbix_inventory"

# Set credentials
zabbix_api_url: http://your-zabbix.com
zabbix_user: Admin
zabbix_password: zabbix

# Add condition for search
filter:
  tags:
    - tag: Location
      value: ''
      operator: equals

# Add query for tags
query:
  selectTags: 'extend'

# Add output
output:
  - name

# Add post processing
keyed_groups:
  - key: zabbix_verbose_status
    separator: ""
compose:
  zabbix_verbose_status: zabbix_status.replace("1", "Disabled").replace("0", "Enabled")
```

License
-------

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.
