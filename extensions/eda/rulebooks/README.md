# Rulebook example

This rulebook example has one event source - Zabbix.
It listens on TCP port 5001 for incoming events.
Each received event undergoes a sequential check of rules, from the first rule to the last, one by one, until it finds the rule with matching conditions or reaches the end of the rulebook.
If the conditions are met, the rule initiates an action to run a playbook for issue remediation.
These playbook examples are available in the [**playbook section**](https://github.com/zabbix/ansible-collection/blob/main/playbooks) of this collection. Playbooks include tasks for issue remediation and feedback to Zabbix (remediation status report).
You can extend reporting using Ansible ITSM modules (ServiceNow, Jira, etc.) and Zabbix media types.
