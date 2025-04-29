# Zabbix Ansible Collection

This collection is meant to help with Zabbix monitoring infrastructure management automation.
It is mainly intended for scalable tasks, for example, Zabbix agent deployment and adding hosts to monitoring.


## Ansible version compatibility

Tested with the Ansible Core 2.16, 2.17 and 2.18. EOL Versions are not supported. For more details, navigate to the collection component description.


## Installing this collection

You can install this collection with the Ansible Galaxy CLI by entering the following command:

    ansible-galaxy collection install zabbix.zabbix

For collection component dependencies and other details, navigate to the component documentation.

<details>
  <summary>Development version</summary>
  Latest development version. Do not use it in production environment.

    ansible-galaxy collection install git+https://github.com/zabbix/ansible-collection.git

</details>


## Collection components

Roles:
  - [**zabbix.zabbix.agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/agent/README.md) - the role to deploy, configure and maintain Zabbix agent on a target device.
  - [**zabbix.zabbix.host**](https://github.com/zabbix/ansible-collection/blob/main/roles/host/README.md) - this role represents target device on Zabbix server.

Plugins:
  - [**HTTP API**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#http-api-plugin) - Zabbix API interface for Ansible.
  - [**Inventory**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#inventory-plugin) - the tool to synchronize Zabbix monitoring instance hosts with Ansible inventory.

Modules:
  - [**zabbix_hostgroup**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#hostgroup-module) - Ansible module for Zabbix host groups management (uses [**HTTP API**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#http-api-plugin) plugin).
  - [**zabbix_host**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#host-module) - Ansible module for Zabbix hosts management (uses [**HTTP API**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#http-api-plugin) plugin).
  - [**zabbix_proxy**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#proxy-module) - Ansible module for Zabbix proxy management (uses [**HTTP API**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#http-api-plugin) plugin).
  - [**zabbix_proxy_group**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#proxy-group-module) - Ansible module for Zabbix proxy group management (uses [**HTTP API**](https://github.com/zabbix/ansible-collection/blob/main/plugins/README.md#http-api-plugin) plugin).

Rulebooks:
  - [**zabbix.zabbix.example**](https://github.com/zabbix/ansible-collection/blob/main/extensions/eda/rulebooks) - Ansible rulebook example for remediation of issues, detected by Zabbix.

## Related content

[Event-Driven Ansible integration](https://www.zabbix.com/integrations/ansible#event_driven_ansible) is based on webhook usage:
  - Zabbix media type pushes events to EDA;
  - EDA webhook receives incoming events and passes those to processing via the rulebook.

EDA helps with the automation of issue remediation and debugging tasks. Basically, EDA receives events sent from Zabbix and triggers different playbook execution, according to the conditions set.
EDA integration is included in Zabbix out of the box and is available starting with Zabbix 6.0 version. Refer to the [EDA media type documentation](https://www.zabbix.com/integrations/ansible#event_driven_ansible) for more details on setup.

## Release notes

See [CHANGELOG](https://github.com/zabbix/ansible-collection/blob/main/CHANGELOG.md) for the release notes and release history of this collection.

## License

Ansible Zabbix collection is released under the GNU Affero General Public License (AGPL) version 3. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.
