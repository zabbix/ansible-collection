#!/usr/bin/env bash

set -eux

# We need to prepare environment for testing.
# This task will create two host groups and two hosts for testing.
ansible-playbook playbooks/prepare_hosts.yml

# In this playbook we can check basic opportunities for plugin:
# - search by wildcard
# - output field
# - prefix variable
# - query and possible fixes from plugin side (invalid case, invalid format (conversion from string to list))
# Zabbix 6.0 and Zabbix 6.4+ have different queries for selecting host groups. We need to check all possible queries in all Zabbix versions.
ansible-playbook playbooks/check_inventory_basic_and_query.yml -i inventories/zabbix_inventory_basic.yml || 
ansible-playbook playbooks/check_inventory_basic_and_query_64.yml -i inventories/zabbix_inventory_basic_64.yml

# In this playbook we can check that all available filters work as expected. 
# We will change the host step by step, setting unsuitable filtering conditions, and will try to get new inventory data.
# Than we will revert necessary parameters for filtering conditions and will try to get inventory data again.
ansible-playbook playbooks/check_inventory_filtering.yml -i inventories/zabbix_inventory_filtering.yml

# Testing group, keyed groups and compose.
ansible-playbook playbooks/check_inventory_post_processing.yml -i inventories/zabbix_inventory_post_processing.yml

# Manual tests of proxy and proxy group
# Before test you need to create 3 proxy: "test proxy", "test proxy 2" and "inventory test proxy".
# For Zabbix varsions above 7.0.0 you also need to create 3 proxy group: "test proxy group", "test proxy group 2" and "inventory test proxy group"
# ansible-playbook playbooks/check_inventory_filtering_proxy.yml -i inventories/zabbix_inventory_filtering_proxy.yml
# ansible-playbook playbooks/check_inventory_filtering_proxy_group.yml -i inventories/zabbix_inventory_filtering_proxy_group.yml

# Clear host groups and hosts after testing.
ansible-playbook playbooks/teardown.yml
