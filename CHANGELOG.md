# v1.3.11

## Feature

- `zabbix_host module`: added proxy group support
- `host role`: added proxy group support

# v1.3.10

## Feature

- moved supported ansible-core range to 2.17-2.15

## Bug

- `zabbix_api module_utils`: removed certificate error exception.

# v1.3.9

## Feature

- `repository role`: added Zabbix 7.0 support
- `agent role`: added Zabbix 7.0 support

# v1.3.8

## Feature

- `agent role`: added mssql agent2 plugin
- `agent role`: added default variables for agent2 plugins
- `agent role`: added session name prefix to plugin certificate filenames on target devices
- `agent role`: changed raspberry pi check to ansible_lsb
- `repository role`: added ubuntu24.04 support
- `molecule`: updated agent2_cert scenario for plugin testing
- `molecule`: updated platforms with ubuntu24.04

## Bug

# v1.3.7

## Feature

- `agent role`: added minor version for debian-like distributions

## Bug

- fixed readme.md links

# v1.3.6

## Feature

- `repository role`: added sslverify option

## Bug

- `agent role`: changed system home folder of zabbix user for rhel-like os
- molecule default scenario fixes
- lint fixes

# v1.3.5

## Feature

- rulebook and playbook examples for Zabbix - EDA sequence
- event update with message added to modules

# v1.3.4

## Feature

- `repository` role: added raspberry pi support

## Bug

- `agent` role: fixed role dependency for ansible-core 2.13

# v1.3.3

## Feature

- `repository` role: added 6.5 version
- `repository` role: added aarch support for multiple distros
- `repository` role: moved and updated os version assert
- `repository` role: increased repository priority defaults

# v1.3.2

- `agent` role: removed wildcards from agent_disable_repository for yum
- `repository` role: fixed priority handling for yum

## Feature

- `repository` role: removed "allow_insecure" option from deb822

## Bug

- `repository` role: added purge for Debian os family and rescue tasks to resolve repository conflict

# v1.3.1

## Bug

- `repository` role: fixed repository conflict with official release package repo by removing it.

# v1.3.0

## Feature

- `agent` role: decomposed repository tasks to separate dependent role
- `agent` role: apt cache update from package state task to `repository`` role
- `repository` role: added dependent role for repository customization

## Bug

- `agent` role: fixed repository mirror

# v1.2.5

## Bug

- `host` role: fixed psk generation skip

# v1.2.4

## Bug

- `host` role: fixed defaults of psk variables for independent role runs

# v1.2.3

## Bug

- `host` role: fixed token auth for api tasks

# v1.2.2

## Feature

- `agent` role: `agent_apply_firewalld_rule` defaults set to `false`

# v1.2.1

## Bug

- `host` role: fixed port inheritance from `agent` role

# v1.2.0

## Feature

- Decomposed `zabbix_agent` role to `agent` and `host` roles
- Renamed all role variables to fit **var_naming\[role_prefix\]** requirement
- Deprecated `zabbix_agent` role

## Bug

- agent role: fixed custom user sequence to trigger path change when  `agent_service_group` stays unmodified.

# v1.1.1

## Feature

- Zabbix agent role: added Debian 12 support

# v1.1.0

## Feature

- Zabbix agent role: added config and deploy tags
- Zabbix agent role: added host management using Zabbix API
- Modules: Added zabbix_host module
- Modules: Added zabbix_hostgroup module
- Plugins: Added httpapi plugin
- Plugins: Added inventory plugin

## Bug

- Removed support of EOL ansible version
- Set Jinja2 dependency to =>3.1.2

# v1.0.6

## Feature

- Zabbix agent role: extended package deployment options with variables: repository_priority, repository_disable. RedHat family only
- Zabbix agent role: added Debian support
- Zabbix agent role: added SELinux policy extension for Zabbix agent2

## Bug

- Zabbix agent role: fixed default home folder path for RedHat like distributions

# v1.0.5

## Feature

- Added userparameter reload to Zabbix agent role. It will trigger if `param_userparamater` was changed and no agent restart detected.
- Added logrotate customization and extended new defaults with maxsize option.
- Added support of self-managed certificates for Zabbix agent connections.
- Added support of self-managed certificates for Zabbix agent2 plugin sessions.
- Added `remove` tag to uninstall agent packages.
  ```bash
  ansible-playbook -i inventory play.yml -t remove
  ```
- Added `userparam` tag to manage user parameters only.
  ```bash
  ansible-playbook -i inventory play.yml -t userparam
  ```
- Added self-managed repo mirror support

# v1.0.4

## Feature

- Zabbix agent role extended distribution support for:
    - CentOS Stream 8,9

# v1.0.3

## Feature

- Zabbix agent role extended distribution support for:
    - Alma Linux 8,9
    - Rocky Linux 8,9
    - Oracle Linux 8,9

# v1.0.2

## Bug fix

- Zabbix agent parameter fixes.
