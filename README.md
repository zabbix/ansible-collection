# Zabbix Ansible Collection

This collection is meant to help with Zabbix monitoring infrastructure management automation.
Mainly targeted for scalable tasks, like Zabbix agent deploy and adding hosts to monitoring.


## Ansible version compatibility

Tested with the Ansible Core 2.12, 2.13 and 2.14. Versions less than 2.12 are not supported. For more details navigate to collection component description.


## Installing this collection

You can install this collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install zabbix.zabbix

For collection component dependencies and other details navigate to component documentation.


## Collection components

Roles:
  - `zabbix_agent` role to deploy, configure and maintain Zabbix agent on a target device.


## Under development

  - `httpapi plugin` Zabbix API connector/wrapper. Used to manage hosts on Zabbix monitoring instance. Will extend **zabbix_agent** role to add hosts without autoregistration.
  - `inventory plugin` Tool to synchronize Zabbix monitoring instance hosts with Ansible inventory.


## License

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.
