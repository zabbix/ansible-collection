# Zabbix Ansible Collection

This collection is meant to help with Zabbix monitoring infrastructure management automation.
It is mainly intended for scalable tasks, for example, Zabbix agent deployment and adding hosts to monitoring.


## Ansible version compatibility

Tested with the Ansible Core 2.12, 2.13 and 2.14. Versions below 2.12 are not supported. For more details, navigate to the collection component description.


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
  - [**zabbix_agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/zabbix_agent/README.md) - the role to deploy, configure and maintain Zabbix agent on a target device.

## Under development

  - `httpapi plugin` - Zabbix API connector/wrapper. Used to manage hosts on Zabbix monitoring instance. Will extend [**zabbix_agent**](https://github.com/zabbix/ansible-collection/blob/main/roles/zabbix_agent/README.md) role to add hosts without autoregistration.
  - `inventory plugin` - The tool to synchronize Zabbix monitoring instance hosts with Ansible inventory.

## Related content

[Event-Driven Ansible integration](https://www.zabbix.com/integrations/ansible#event_driven_ansible) is based on webhook usage:
  - Zabbix media type is pushing events to EDA.
  - EDA webhook receives incoming events and passes to processing via rulebook.

EDA helps with automation of issue remediation and debugging tasks. Basically EDA receives events sent from Zabbix and triggers different playbook execution, according to conditions set.
EDA integration is included in Zabbix out of the box and available starting with Zabbix 6.0 version.
Refer to [EDA media type documentation](https://www.zabbix.com/integrations/ansible#event_driven_ansible) for more details on setup.

  
## License

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.