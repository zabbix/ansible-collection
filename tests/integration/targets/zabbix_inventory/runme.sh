#!/usr/bin/env bash

set -eux

# We need to prepare envairoment for testing
# This task will create two host groups and two host for testing
ansible-playbook playbooks/prepare_hosts.yml

# In this playbook we can check basic opportunities for plugin:
# - search by wildcard
# - output field
# - prefix variable
# - query and possible fixes from plugin side (invalid case, invalid format (convertation from sting to list))
# Zabbix 6.0 and Zabbix 6.4+ have different query for select host groups. We need to check all possible query in all Zabbix versions
ansible-playbook playbooks/check_inventory_basic_and_query.yml -i inventories/zabbix_inventory_basic.yml || 
ansible-playbook playbooks/check_inventory_basic_and_query_64.yml -i inventories/zabbix_inventory_basic_64.yml

# In this playbook we can check that all available filters wark as expected. 
# We will change the host step by step for not suitable filtering conditions and try to get new inventory date
# Than we will back necessary parameters for filtering conditions and try to get inventory data again
ansible-playbook playbooks/check_inventory_filtering.yml -i inventories/zabbix_inventory_filtering.yml

# Testing group, keyed-groups and compose
ansible-playbook playbooks/check_inventory_post_processing.yml -i inventories/zabbix_inventory_post_processing.yml

# Clear host groups and hosts after testing
ansible-playbook playbooks/teardown.yml
