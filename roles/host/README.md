Zabbix host role
=================

You can use this Ansible role to deploy and configure Zabbix agents on the target machines. Both agentd and agent2 variants are available.
Currently, the following OS of target machines are supported:
- Redhat 7, 8, 9
- Oracle Linux 8, 9
- Alma Linux 8, 9
- Rocky Linux 8, 9
- CentOS Stream 8, 9
- Ubuntu 18.04, 20.04, 22.04
- Debian 10, 11, 12

Supported distribution list to be extended.

**Note**: This role is still in active development. There may be unidentified issues and the role variables may change as development continues.

Table of contents
-----------------
<!--ts-->
  * [Requirements](#requirements)
  * [Role variables](#role-variables)
    * [Zabbix host via Zabbix API](#zabbix-host-via-zabbix-api)
      * [API connection parameters](#api-connection-parameters)
      * [Zabbix host configuration parameters](#zabbix-host-configuration-parameters)
  * [Hints & Tags](#hints--tags)
  * [Playbook examples](#playbook-examples)
    * [Playbook 10: Deploy Zabbix agent with passive checks only and add hosts to Zabbix](#playbook-10)
  * [License](#license)

<!--te-->


Requirements
------------

Ansible core >= 2.13

Zabbix agent role requires additional tools from two Ansible certified collections:
- ansible.posix >= 2.8
- ansible.utils >= 1.4

You can install required collections easily:
```bash
ansible-galaxy collection install ansible.utils ansible.posix
```

Note that the role uses [**ansible.utils.ipaddr**](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html) filter, which depends on Python library [**netaddr**](https://pypi.org/project/netaddr).

Zabbix `host` role relies on [**Jinja2**](https://pypi.org/project/Jinja2/) heavily and requires version >= 3.1.2

You can install required Python libraries on the control node as follows:

```bash
python3 -m pip install netaddr>=0.8.0 Jinja2>=3.1.2
```

Or using `requirements.txt` file in the role folder:

```bash
python3 -m pip install -r requirements.txt
```

Check the [**Python documentation**](https://docs.python.org/3/installing/index.html) for more details on Python modules installation.


Role variables
--------------

You can modify variables listed in this section. Variables are not validated by the role itself. You should experiment with variable definition on a test instance before going for a full-scale deployment.

The default settings are aimed at the ease of installation. You can override those to according to a use case.


Role variables
--------------

### API connection parameters

| Variable | Type | Default | Description |
|--|--|--|--|
| zabbix_api_host | `string` | `localhost` | Hostname or IP address of Zabbix frontend (Zabbix API). Execution environment will use it to initiate connection.
| zabbix_api_url | `string` | `''` | Path to access Zabbix frontend (Zabbix API). Specify only if Zabbix frontend runs on non-default path. Empty string by default. Alternative explanation: `http[s]://<zabbix_api_host>/<zabbix_api_url>`.
| zabbix_api_port | `int` | `80` | Port which Zabbix frontend listens on.
| zabbix_api_token | `string` | | Zabbix API access token.
| zabbix_api_user | `string` | `Admin` | Zabbix API username. Ignored if token is provided instead.
| zabbix_api_password | `string` | `zabbix` | Zabbix API user password. Ignored if token is provided instead.
| zabbix_api_use_ssl | `boolean` | `False` | Set to `True` for secure connection.
| zabbix_api_validate_certs | `boolean` | `False` | Set to `True` to validate certifacates during SSL handshake.

### Zabbix host configuration parameters

| Variable | Type | Default | Description |
|--|--|--|--|
| host_state | `string` | `present` | Default value ensures presence of the host in Zabbix.
| host_name | `string` | `{{ inventory_hostname }}` | Unique name of the host.
| host_visible_name | `string` || Unique visible name of the host.
| host_description | `string` | `Managed by Ansible. Added with "zabbix_host" module.` | Describe instance.
| host_hostgroups | `list` | `{{ group_names }}` | List of hostgroup names assigned to the host. At least one hostgroup needed. By default, uses the list of groups assigned to the host in Ansible inventory.
| host_templates | `list` | `[]` | List of template names that should be linked to the host.
| host_interfaces | `list` | [↓](#zabbix-host-interfaces-default) | Holds a list of dictionaries. Each dictionary describes an [interface](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters) set for the host. Only one interface of each type is supported. Look [below](#zabbix-host-interfaces-default) for default description.
| host_tags | `list` | `[{"tag": "managed"}]` | Accepts host level tags in a list of dictionaries format.
| host_macros | `list` || Accepts macros in a list of dictionaries format.
| host_inventory_mode | `string` || Host [inventory population mode](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).
| host_inventory | `dictionary` || Define [inventory fields](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).
| host_status | `string` | `enabled` | The host status. Available values: `enabled` or `disabled`.
| host_proxy | `string` | `{{ group_names \| select("match", "^zabbix_proxy.*") \| first \| default(None) }}` | Assign proxy to the host. Default value filters groups of the host from Ansible inventory and checks for regex match. If group is matched, its name will be assigned as the host proxy. Note that proxy with the same name should exist in setup.
| host_tls_accept | `list` | `{{ agent_param_tlsconnect }}` | Linked to agent parameter to accept **active checks**. Add [more options](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters) if needed.
| host_tls_connect | `string` | `{{ agent_param_tlsconnect }}` | Mirrors agent outgoing connection behavior. Override if you need [different encryption](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters) for **passive checks**.
| host_tls_psk_identity | `string` | `{{ agent_param_tlspskidentity }}` | By default, PSK key identity is linked to agent parameter.
| zabbix_host_tls_psk_value | `string` | `{{ agent_tls_psk_value }}` | By default, sets the same key that was used in Zabbix agent deployment.
| host_get_cert_info | `boolean` | `False` | Extract issuer and subject info from certificates, defined in `agent_source_tlscertfile`. Requires Openssl installation on Ansible execution environment.
| host_tls_issuer | `string` | `None` | Set issuer of Zabbix agent certificate for TLS connection.
| host_tls_subject | `string` | `None` | Set subject of Zabbix agent certificate for TLS connection.
|--|
| host_ipmi_authtype | `string` || Set IPMI [authentication type](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).
| host_ipmi_privilege | `string` || Set IPMI [privilege level](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).
| host_ipmi_username | `string` || Set IPMI username.
| host_ipmi_password | `string` || Set IPMI password.

#### Zabbix host interfaces default

Default value describes interface of Zabbix agent type. If `ansible_host` is filled with IP address, then host will use IP field for connection.

    host_interfaces:
      - type: agent
        ip: '{{ ansible_host if ansible_host | ansible.utils.ipaddr else omit }}'
        dns: '{{ ansible_host if not ansible_host | ansible.utils.ipaddr else omit }}'
        useip: '{{ true if ansible_host | ansible.utils.ipaddr else false }}'
        port: '{{ param_listenport | default(10050) }}'

[More examples of interface configuration](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).


Playbook examples
-----------------

- ### Playbook 10:
  **Deploy Zabbix agent with passive checks only and add hosts to Zabbix.**
  1. Fill Zabbix agent configuration. Here we will allow Zabbix server to communicate with agent and apply firewall rule to accept connection only from Zabbix server.
  2. Active agent autoregistration does not work with passive checks. So we need to use Zabbix API to add new host with passive checks only. Add [**zabbix.zabbix.host**](https://github.com/zabbix/ansible-collection/blob/main/roles/host/README.md) role to the same Ansible `play` to inherit variables from the first role.
  3. Fill Zabbix API connection properties.
  4. Fill Zabbix host configuration. This time, we will add only template to assign. Default configuration will apply host name and agent connection properties from Ansible inventory.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          ### Zabbix agent configuration
          agent_param_server: 256.256.256.256                     # address of Zabbix server to accept connections from monitoring instance;
          agent_firewall_allow_from: 256.256.256.256              # address of Zabbix server to allow connections from monitoring instance using firewalld;
        - role: zabbix.zabbix.host
          ### Zabbix API properties
          zabbix_api_host: zabbix.frontend.loc             # Zabbix frontend server;
          zabbix_api_port: 443                             # Zabbix fronted connection port;
          zabbix_api_user: Admin                           # Zabbix user name for API connection;
          zabbix_api_password: zabbix                      # Zabbix user password for API connection;
          zabbix_api_use_ssl: True                         # Use secure connection;
          ### Zabbix host configuration
          host_templates: ["Linux by Zabbix agent"]  # Assign list of templates to the host;
  ```

License
-------

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.