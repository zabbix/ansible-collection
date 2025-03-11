Zabbix host role
=================

This role represents the state of target device on monitoring instance. You can use it to add/remove/modify hosts of Zabbix monitoring instance using Ansible. It is made on top of our modules over Zabbix API communication.

This role is compatible with [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role. To inherit variables from [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role, place it in the same play. It is shown in the [first example](#playbook-1)

Since hostgroups are mandatory for any host, this role ensures, that hostgroups are created on monitoring instance.

[**Default host interfaces**](#zabbix-host-interfaces-default) are taken from [**ansible_host**](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html#term-ansible_host) special variable. <u>Make sure it is defined on inventory level!</u> Even for cases when inventory hostname should be taken! Here is the trick:
```yaml
hosts:
  my.host.dns.com:
    ansible_host: '{{inventory_hostname}}'
```

**Note**: This role is still in active development. There may be unidentified issues and the role variables may change as development continues.

Table of contents
-----------------
<!--ts-->
  * [Requirements](#requirements)
  * [Role variables](#role-variables)
    * [API connection parameters](#api-connection-parameters)
    * [Zabbix host configuration parameters](#zabbix-host-configuration-parameters)
      * [Zabbix host interfaces default](#zabbix-host-interfaces-default)
  * [Role Tags](#role-tags)
  * [Playbook examples](#playbook-examples)
    * [Playbook 1: Deploy Zabbix agent with passive checks only and add hosts to Zabbix](#playbook-1)
  * [License](#license)

<!--te-->


Requirements
------------

Ansible core >= 2.16

Zabbix agent role requires additional tools from 3 Ansible certified collections:
- ansible.posix >= 2.8
- ansible.utils >= 1.4
- ansible.netcommon >=3.1.1

You can install required collections easily:
```bash
ansible-galaxy collection install ansible.utils ansible.posix ansible.netcommon
```

Note that the role uses [**ansible.utils.ipaddr**](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html) filter, which depends on Python library [**netaddr**](https://pypi.org/project/netaddr).

Zabbix `host` role relies on [**Jinja2**](https://pypi.org/project/Jinja2/) heavily and requires version >= 3.1.2

You can install required Python libraries on the control node as follows:

```bash
python3 -m pip install "netaddr>=0.8.0" "Jinja2>=3.1.2"
```

Or using `requirements.txt` file in the role folder:

```bash
python3 -m pip install -r requirements.txt
```

Check the [**Python documentation**](https://docs.python.org/3/installing/index.html) for more details on Python modules installation.


Role variables
--------------

You can modify variables listed in this section. Variables are not validated by the role itself. You should experiment with variable definition on a test instance before going for a full-scale deployment.

The default settings are aimed at the ease of installation. You can override those, according to a use case.


Role variables
--------------

This set of variables explains Ansible how to connect to Zabbix API.

### API connection parameters

| Variable | Type | Default | Description |
|--|--|--|--|
| host_zabbix_api_server | `string` | `localhost` | Hostname or IP address of Zabbix frontend (Zabbix API). Execution environment will use it to initiate connection.
| host_zabbix_api_url | `string` | `''` | Path to access Zabbix frontend (Zabbix API). Specify only if Zabbix frontend runs on non-default path. Empty string by default. Alternative explanation: `http[s]://<host_zabbix_api_server>/<host_zabbix_api_url>`.
| host_zabbix_api_port | `int` | `80` | Port which Zabbix frontend listens on.
| host_zabbix_api_token | `string` | | Zabbix API access token.
| host_zabbix_api_user | `string` | `Admin` | Zabbix API username. Ignored if token is provided instead.
| host_zabbix_api_password | `string` | `zabbix` | Zabbix API user password. Ignored if token is provided instead.
| host_zabbix_api_use_ssl | `boolean` | `False` | Set to `True` for secure connection.
| host_zabbix_api_validate_certs | `boolean` | `False` | Set to `True` to validate certifacates during SSL handshake.

### Zabbix host configuration parameters

This group of variables is used to represent the state of target device in Zabbix. Defaults are adopted to use together with [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role. Override those for different use cases.
Role respects module behavior, where unset variables are omitted. For example to reassign host back to zabbix server set one of variables(`host_proxy` or `host_proxy_group`) to empty string "".

| Variable | Type | Default | Description |
|--|--|--|--|
| host_state | `string` | `present` | Default value ensures presence of the host in Zabbix.
| host_name | `string` | `{{ inventory_hostname }}` | Unique name of the host.
| host_visible_name | `string` || Unique visible name of the host.
| host_description | `string` | `Managed by Ansible. Added with "zabbix_host" module.` | Describe instance.
| host_hostgroups | `list` | `{{ group_names }}` | List of hostgroup names assigned to the host. At least one hostgroup needed. By default, uses the list of groups assigned to the host in Ansible inventory.
| host_templates | `list` || List of template names that should be linked to the host.
| host_interfaces | `list` | [↓](#zabbix-host-interfaces-default) | Holds a list of dictionaries. Each dictionary describes an [interface](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters) set for the host. Only one interface of each type is supported. Look [below](#zabbix-host-interfaces-default) for default description.
| host_tags | `list` | `[{"tag": "managed"}]` | Accepts host level tags in a list of dictionaries format.
| host_macros | `list` || Accepts macros in a list of dictionaries format.
| host_inventory_mode | `string` || Host [inventory population mode](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).
| host_inventory | `dictionary` || Define [inventory fields](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).
| host_status | `string` | `enabled` | The host status. Available values: `enabled` or `disabled`.
| host_proxy | `string` || Assign proxy to the host. Mutually exclusive with `host_proxy_group`. To assign host back to Zabbix server, set only one of them to None(or empty "").
| host_proxy_group | `string` || Assign proxy group to the host. Mutually exclusive with `host_proxy` variable. To assign host back to Zabbix server, set only one of them to None(or empty "").
| host_tls_accept | `list` | `{{ agent_param_tlsconnect \| default(["unencrypted"]) }}` | Linked to agent parameter to accept **active checks**. Add [more options](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters) if needed. Linked to [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role if used together.
| host_tls_connect | `string` | `{{ agent_param_tlsconnect \| default("unencrypted") }}` | Mirrors agent outgoing connection behavior. Override if you need [different encryption](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters) for **passive checks**. Linked to [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role if used together.
| host_tls_psk_identity | `string` | `{{ agent_param_tlspskidentity \| default("PSK_ID_" + inventory_hostname) }}` | PSK key identity formed from prefix and hostname from the Ansible inventory. Linked to [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role if used together.
| host_source_tls_psk_file | `string` | `{{ agent_source_tlspskfile \| default(".PSK/" + inventory_hostname + ".psk") }}` | Location of file with PSK key on Ansible controller/EE. Linked to [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role if used together.
| host_tls_psk_value | `string` | `{{ agent_tls_psk_value \| default(None) }}` | By default, sets the same key that was used in Zabbix agent deployment. Linked to [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role if used together. When empty, role triggers generation of the key or reading it from `host_source_tls_psk_file` location.
| host_get_cert_info | `boolean` | `False` | Extract issuer and subject info from certificates, defined in `agent_source_tlscertfile`. Requires Openssl installation on Ansible execution environment.
| host_source_tls_certfile | `string` | `{{ agent_source_tlscertfile \| default(None) }}` | Certificate location on Ansible controller or EE. Linked to [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) role if used together.
| host_tls_issuer | `string` | `None` | Set issuer of Zabbix agent certificate for TLS connection. Will be filled automatically if `host_get_cert_info` is `true`.
| host_tls_subject | `string` | `None` | Set subject of Zabbix agent certificate for TLS connection. Will be filled automatically if `host_get_cert_info` is `true`.
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
        port: '{{ agent_param_listenport | default(10050) }}'
Do not leave an **ansible_host** variable undefined, or it will be replaced with `host_zabbix_api_server` and you will fail to collect passive checks from the agents. *This is the specifics of ansible httpapi plugin usage with delegation.*

[More examples of interface configuration](https://github.com/zabbix/ansible-collection/tree/main/plugins#host-module-parameters).

Role tags
-----

-  Use `remove` tag to remove host from monitoring instance.
Usefull together with [**zabbix.zabbix.host**](https://github.com/zabbix/ansible-collection/blob/main/roles/host/README.md) role in the same playbook.

      ansible-playbook -i inventory playbook.yml -t remove

- All tasks from this role are marked with `host` tag. Helps when multiple roles are used in the same playbook.

Playbook examples
-----------------

- ### Playbook 1:
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
          host_zabbix_api_server: zabbix.frontend.loc             # Zabbix frontend server;
          host_zabbix_api_port: 443                             # Zabbix fronted connection port;
          host_zabbix_api_user: Admin                           # Zabbix user name for API connection;
          host_zabbix_api_password: zabbix                      # Zabbix user password for API connection;
          host_zabbix_api_use_ssl: True                         # Use secure connection;
          ### Zabbix host configuration
          host_templates: ["Linux by Zabbix agent"]  # Assign list of templates to the host;
  ```

License
-------

Ansible Zabbix collection is released under the GNU Affero General Public License (AGPL) version 3. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.