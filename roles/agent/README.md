Zabbix agent role
=================

You can use this Ansible role to deploy and configure Zabbix agents on the target machines. Both agentd and agent2 variants are available.
Currently, the following OS of target machines are supported:
- Redhat 8, 9
- Oracle Linux 8, 9
- Alma Linux 8, 9
- Rocky Linux 8, 9
- CentOS Stream 9
- Ubuntu 18.04, 20.04, 22.04, 24.04
- Debian 10, 11, 12
- Raspberry Pi Os

Supported distribution list to be extended.

**Note**: This role is still in active development. There may be unidentified issues and the role variables may change as development continues.

Table of contents
-----------------
<!--ts-->
  * [Requirements](#requirements)
  * [Role variables](#role-variables)
    * [General settings](#general-settings)
    * [User settings](#user-settings)
    * [Firewall settings](#firewall-settings)
    * [Logrotate configuration for Zabbix agent](#logrotate-configuration-for-zabbix-agent)
    * [Local path settings](#local-path-variables-table)
    * [SELinux settings](#selinux-settings)
    * [Common Zabbix agent configuration file parameters](#common-zabbix-agent-configuration-parameters)
      * [Zabbix agent unique parameters](#zabbix-agentd-unique-parameters)
      * [Zabbix agent 2 unique parameters](#zabbix-agent-2-unique-parameters)
        * [Ceph plugin parameters](#zabbix-agent-2-ceph-plugin-parameters)
        * [Docker plugin parameters](#zabbix-agent-2-docker-plugin-parameters)
        * [Memcached plugin parameters](#zabbix-agent-2-memcached-plugin-parameters)
        * [Modbus plugin parameters](#zabbix-agent-2-modbus-plugin-parameters)
        * [MongoDB plugin parameters](#zabbix-agent-2-mongodb-plugin-parameters)
        * [MQTT plugin parameters](#zabbix-agent-2-mqtt-plugin-parameters)
        * [Oracle plugin parameters](#zabbix-agent-2-oracle-plugin-parameters)
        * [PostgreSQL plugin parameters](#zabbix-agent-2-postgresql-plugin-parameters)
        * [MySQL plugin parameters](#zabbix-agent-2-mysql-plugin-parameters)
        * [MSSQL plugin parameters](#zabbix-agent-2-mssql-plugin-parameters)
        * [Redis plugin parameters](#zabbix-agent-2-redis-plugin-parameters)
        * [Smart plugin parameters](#zabbix-agent-2-smart-plugin-parameters)
  * [Hints & Tags](#hints--tags)
  * [Playbook examples](#playbook-examples)
    * [Playbook 1: Latest LTS Zabbix agentd deployment for active checks only](#playbook-1)
    * [Playbook 2: 6.4 version of Zabbix agent 2 for both passive and active checks + Iptables](#playbook-2)
    * [Playbook 3: Zabbix agentd for both passive and active checks with PSK encryption for autoregistration](#playbook-3)
    * [Playbook 4: Zabbix agentd with certificate-secured connections](#playbook-4)
    * [Playbook 5: 6.4 version of Zabbix agent 2 for MongoDB monitoring](#playbook-5)
    * [Playbook 6: Zabbix agentd downgrade from 6.4 to 6.0](#playbook-6)
    * [Playbook 7: Zabbix agentd running under custom user](#playbook-7)
    * [Playbook 8: Update Zabbix agentd to the latest minor version](#playbook-8)
    * [Playbook 9: Deploy Zabbix agentd without direct internet access, by using HTTP proxy](#playbook-9)
    * [Playbook 10: Deploy Zabbix agent with passive checks only and add hosts to Zabbix](#playbook-10)
  * [License](#license)

<!--te-->


Requirements
------------
This role uses official Zabbix packages and repository for component installation. Target machines require direct or [**HTTP proxy**](#playbook-9) internet access to Zabbix repository [**repo.zabbix.com**](https://repo.zabbix.com).

For self-hosted repository mirrors, override URL for [`agent_repository_mirror`](#general-settings) variable.

The role contains firewalld application rule to allow agent listen port. Firewalld is required on the target machines for this rule to work. Automatic mode `agent_apply_firewalld_rule = auto` checks if firewalld is installed. Firewalld is a recommended method as it can work with both iptables and nftables. Firewalld can be installed on RHEL- and Debian-based distributions.

Multiple tasks require `superuser` privileges (sudo).

Ansible core >= 2.13

Zabbix agent role requires additional tools from two Ansible certified collections:
- ansible.posix >= 2.8
- ansible.utils >= 1.4

You can install required collections easily:
```bash
ansible-galaxy collection install ansible.utils ansible.posix
```

Note that the role uses [**ansible.utils.ipaddr**](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html) filter, which depends on Python library [**netaddr**](https://pypi.org/project/netaddr).

Zabbix agent role relies on [**Jinja2**](https://pypi.org/project/Jinja2/) heavily and requires version >= 3.1.2

You can install required Python libraries on the control node as follows:

```bash
python3 -m pip install "netaddr>=0.8.0" "Jinja2>=3.1.2"
```

Or using `requirements.txt` file in the role folder:

```bash
python3 -m pip install -r requirements.txt
```

Check the [**Python documentation**](https://docs.python.org/3/installing/index.html) for more details on Python modules installation.

SELinux tasks depend on `policycoreutils` package. It will be installed as dependency with `zabbix-selinux-policy` package.

Note that Ansible-core 2.17 requires at least python3.7 on the target devices. Check the [**compatibility matrix**](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix) for other versions.

Role variables
--------------

You can modify variables listed in this section. Variables are not validated by the role itself. You should experiment with variable definition on a test instance before going for a full-scale deployment.

The default settings are aimed at the ease of installation. You can override those to improve security.

### General settings:

| Variable | Type | Default | Description |
|--|--|--|--|
| agent_variant | `int` | 1 | The variant of Zabbix agent (1: Zabbix agentd, 2: Zabbix agent 2).
| agent_major_version | `string` | 6.0 | The major version of Zabbix agent. Defaults to the latest LTS.
| agent_minor_version | `string` || Zabbix agent minor version customization. For downgrade use with `agent_remove_previous_packages=true`. Minor version example for debian family distributions: `25-1` (minor version - package version). For RHEL family: `25` (minor version). In both cases minor version will be applied to all packages in `agent_package_list`.
| agent_package_state | `string` | present | The state of packages to be deployed. Available options: `present`, `latest` - update to the latest version if available in the installed **zabbix-managed** repository.
| agent_remove_previous_packages | `boolean` | `false` | Trigger removal of previous packages prior to the installation of the new ones. Mandatory to deploy earlier version than the one currently installed.
| agent_2_plugin_list | `list` | [ceph, docker, memcached, modbus, mongodb, mqtt, mysql, oracle, postgresql, redis, smart] | List of Zabbix agent 2 plugins to configure and deploy (if the plugin is loadable). **Note** that loadable plugins for 6.0 version are installed as dependencies of Zabbix agent 2 package. Starting with 6.4, loadable plugin installation is allowed at your own discretion. Default plugin list for Zabbix agent 2 >= **6.4** is `[ceph, docker, memcached, modbus, mqtt, mysql, oracle, redis, smart]`.
| agent_http_proxy | `string` || Defines [**HTTP proxy**](#playbook-9) address for the packager.
| agent_https_proxy | `string` || Defines HTTPS proxy address for the packager.
| agent_repository_mirror | `string` | "https://repo.zabbix.com/" | Defines repository mirror URL. You can override it to use self-hosted Zabbix repo mirror.
| agent_repository_priority | `int` | 99 | **For RedHat family OS only.** Sets the priority of the Zabbix repository. Expects integer values from 1 to 99. Covers the cases with interfering packages from central distribution repositories.
| agent_repository_disable | `string` | "epel" | **For RedHat family OS only.** Disables defined repository during package deployment. Disables EPEL by default.

### User settings:

The role allows creating a custom user for Zabbix agent. User customization tasks will trigger only when `agent_service_user` is not "zabbix".

| Variable | Type | Default | Description |
|--|--|--|--|
| agent_service_user | `string` | zabbix | The user to run Zabbix agent.
| agent_service_group | `string` | zabbix | User group for the custom user.
| agent_service_uid | `string` || User ID for the custom user.
| agent_service_gid | `string` || User group ID for the custom user group.

Adds next task sequence:
- Creates group.
- Creates user with home folder (defaults to `/home/{{ agent_service_user }}`).
- Adds **systemd** overrides to manage Zabbix agent pid file (`/run/zabbix_agent[d|2]/zabbix_agent[d|2].pid`).
- Changes Zabbix agent 2 sockets paths (to the folder of pid file).
- Changes logging path (to `/var/log/zabbix_agent[d|2]/zabbix_agent[d|2].log`).

### Firewall settings:

The role allows adding simple firewall rules on the target machine to accept passive checks. Advanced firewall configuration is out of the scope of Zabbix agent role.

Firewalld is a recommended way of applying firewall rule as it works with both iptables and nftables. **Note** that `iptables` does not work in Ubuntu since 22.04. Firewalld should be installed on target machines. It is supported on RHEL- and Debian-based distributions.

| Variable | Type | Default | Description |
|--|--|--|--|
| agent_apply_firewalld_rule | `string` | `false` | Defines application of firewalld rule. Possible options: ["auto", "force"]. Undefined or any other string will skip the rule application.
| agent_apply_iptables_rule | `boolean` | `false` | Defines application of iptables rule. Possible options: [true, false].
| agent_firewalld_zone | `string` | default | Firewalld zone for the rule application.
| agent_firewall_allow_from | `string` || Only IP addresses allowed. Limits source address of passive check using the firewall rule. For firewalld, this setting will change the rule from simple to rich rule.

***You can notice Python module "firewall" sometimes failing to import during these tasks. Most common issue is that Ansible chooses wrong Python interpreter from multiple versions available on host. A solution to this is to provide `ansible_python_interpreter` with a correct path to legit Python installation on target hosts for specific operating systems. Normally it is defined on inventory level.***

### **Logrotate** configuration for Zabbix agent

You can modify rotation options of Zabbix agent[2] log file. It requires default option overriding in `agent_logrotate_options` variable.
This is a `list` type variable, and it defaults to the list of the following options:
  - weekly
  - maxsize 5M
  - rotate 12
  - compress
  - delaycompress
  - missingok
  - notifempty
  - create 0640 {{ agent_service_user }} {{ agent_service_group }}

**Note** that most distributions execute logrotate jobs on a daily basis by default. If you wish to change rotation calendar, modify cronjob or systemd timer accordingly or add separate cronjob/timer to process only Zabbix agent[2] log.

### Local path variables table:

Variables prefixed with `source_` should point to a file or folder located on Ansible execution environment. These files are about to be transferred to the target machines.

| Variable | Type | Default | Description |
|--|--|--|--|
| agent_source_conf_dir | `string` || Path to the configuration folder on Ansible execution environment that needs to be transferred to the target machine and included in Zabbix agent configuration. For example, a folder with `Userparameters`.
| agent_source_scripts_dir | `string` || Path to the scripts folder on Ansible execution environment. Will be copied under the `agent_service_user` home folder. Scripts can be utilized by `UserParameters`.
| agent_source_modules_dir | `string` || Path to Zabbix agentd modules folder on Ansible execution environment. Will be copied to default location for default user. For custom user modules, will be placed under the `agent_service_user` home folder.
| agent_source_tlspskfile | `string` | `.PSK/{{ inventory_hostname }}.psk` | Path to the PSK key location on Ansible execution environment. The role will look for the files having the same names as `inventory_hostname` (hostname from inventory) and generate new if not found. This key will be placed under `agent_service_user` home folder and added to Zabbix agent configuration automatically.
| agent_source_tlscafile | `string` || Path to the file on Ansible execution environment containing the top-level CA(s) certificates for peer certificate verification. Will be placed under `agent_service_user` home folder and added to Zabbix agent configuration automatically.
| agent_source_tlscertfile | `string` || Path to the file on Ansible execution environment containing the agent certificate or certificate chain. Will be placed under `agent_service_user` home folder and added to Zabbix agent configuration automatically.
| agent_source_tlscrlfile | `string` || Path to the file on Ansible execution environment containing revoked certificates. Will be placed under `agent_service_user` home folder and added to Zabbix agent configuration automatically.
| agent_source_tlskeyfile | `string` || Path to the file containing the agent private key. Will be placed under `agent_service_user` home folder and added to Zabbix agent configuration automatically.

### SELinux settings:

SELinux tasks will be processed only when SELinux status on the target machine is `enabled`
SELinux tasks depend on `policycoreutils` package. It will be installed as dependency with `zabbix-selinux-policy` package.

| Variable | Type | Default | Description |
|--|--|--|--|
| agent_apply_seport | `boolean` | `true` | Adds custom agent port defined in `agent_param_listenport` to SELinux port type `zabbix_agent_port_t`. Enabled by default and triggers when `agent_param_listenport` is not equal to 10050.
| agent_apply_semodule | `boolean` | `false` | Adds SELinux policy extension to make a transition of Zabbix agent 2 to SE domain `zabbix_agent_t`. Additionally, it allows socket usage for the same domain. It also enables read permission on RPM database for `system.sw.packages.get` key.
| agent_seboolean_zabbix_run_sudo | `string` || Enables/disables default SELinux boolean `zabbix_run_sudo`. For task processing, expects string values "on" or "off". Undefined by default, in order to skip task processing. Use with caution as it holds allow rules for a set of domains.

Why `audit2allow` tool is not included in the role:
  - not secure (it just allows everything that was denied);
  - requires several days of auditlog to collect all needed denials.
Use it only as a policy creation consultant.

Default SE boolean `zabbix_run_sudo` does not fit all possible privileged usage and should be avoided in most cases.
Create custom policies for environments with specific security requirements.

### Common Zabbix agent configuration parameters:

These parameters are common for both agent variants

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| agent_param_alias | `list` || [**Alias**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#alias) |	Set an alias for the item key. Location of aliases on target machine: `/etc/zabbix/zabbix_agent[d|2].d/aliases.conf`
| agent_param_allowkey | `list` || [**AllowKey**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#allowkey) | Allow execution of the item keys that match the pattern.
| agent_param_buffersend | `int` || [**BufferSend**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#buffersend) |	Do not keep data in the buffer longer than N seconds.
| agent_param_buffersize | `int` || [**BufferSize**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#buffersize) |	Maximum number of values in the memory buffer.
| agent_param_debuglevel | `int` || [**DebugLevel**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#debuglevel) |	Debug level.
| agent_param_denykey | `list` || [**DenyKey**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#denykey) |	Deny execution of the item keys that match the pattern.
| agent_param_heartbeatfrequency | `int` || [**HeartbeatFrequency**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#heartbeatfrequency) | Frequency of the heartbeat messages in seconds. Added in 6.4.
| agent_param_hostinterface | `string` || [**HostInterface**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostinterface) | Optional parameter that defines the host interface.
| agent_param_hostinterfaceitem | `string` || [**HostInterfaceItem**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostinterfaceitem) | Optional parameter that defines the item used for getting the host interface.
| agent_param_hostmetadata | `string` || [**HostMetadata**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostmetadata) | Optional parameter that defines the host metadata.
| agent_param_hostmetadataitem | `string` || [**HostMetadataItem**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostmetadataitem) | Optional parameter that defines Zabbix agent item used for getting the host metadata.
| agent_param_hostname | `string` | `{{inventory_hostname}}` | [**Hostname**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostname) | Optional parameter that defines the hostname. Defaults to the hostname taken from the inventory.
| agent_param_hostnameitem | `string` || [**HostnameItem**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostnameitem) | Optional parameter that defines Zabbix agent item used for getting the hostname.
| agent_param_include | `list` | **agentd:** ["/etc/zabbix/zabbix_agentd.d/\*.conf"] **agent2:** ["/etc/zabbix/zabbix_agent2.d/\*.conf"] | [**Include**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#include) | You may include individual files or all files in a directory in the configuration file.
| agent_param_listenip | `string` || [**ListenIP**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#listenip) | List of comma-delimited IP addresses that the agent should listen on.
| agent_param_listenport | `int` || [**ListenPort**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#listenport) | The agent will listen on this port for connections from the server.
| agent_param_logfile | `string` | **agentd:** /var/log/zabbix/zabbix_agentd.log **agent2:** /var/log/zabbix/zabbix_agent2.log | [**LogFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logfile) | Name of the log file.
| agent_param_logfilesize | `int` | 0 | [**LogFileSize**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logfilesize) | Maximum size of the log file.
| agent_param_logtype | `string` | file | [**LogType**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logtype) | Type of the log output.
| agent_param_pidfile | `string` | **agentd:** /run/zabbix/zabbix_agentd.pid **agent2:** /run/zabbix/zabbix_agent2.pid | [**PidFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#pidfile) | Name of the PID file.
| agent_param_refreshactivechecks | `int` || [**RefreshActiveChecks**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#refreshactivechecks) | How often the list of active checks is refreshed.
| agent_param_server | `string` | ::/0 | [**Server**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#server) | List of comma-delimited IP addresses, optionally in CIDR notation, or hostnames of Zabbix servers and Zabbix proxies.
| agent_param_serveractive | `string` || [**ServerActive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#serveractive) | Zabbix server/proxy address or cluster configuration to get the active checks from.
| agent_param_sourceip | `string` || [**SourceIP**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#sourceip) | Source IP address.
| agent_param_timeout | `int` || [**Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#timeout) | Spend no more than Timeout seconds on processing.
| agent_param_tlsaccept | `list` | ["unencrypted"] | [**TLSAccept**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsaccept) | Incoming connections to be accepted. Available options: `unencrypted`, `cert`, `psk`.
| agent_param_tlsconnect | `string` | unencrypted | [**TLSConnect**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsconnect) | How the agent should connect to Zabbix server or proxy. Available options: `unencrypted`, `cert`, `psk`.
| agent_param_tlscafile | `string` || [**TLSCAFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscafile) | Path to the top-level CA(s) certificates for peer certificate verification. Use only when [`agent_source_tlscafile`](#local-paths-variables-table) is not defined!
| agent_param_tlscertfile | `string` || [**TLSCertFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscertfile) | Path to the agent certificate or certificate chain. Use only when [`agent_source_tlscertfile`](#local-paths-variables-table) is not defined!
| agent_param_tlscrlfile | `string` || [**TLSCRLFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscrlfile) | Path to revoked certificates. Use only when [`agent_source_tlscrlfile`](#local-paths-variables-table) is not defined!
| agent_param_tlskeyfile | `string` || [**TLSKeyFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlskeyfile) | Path to the agent private key. Use only when [`agent_source_tlskeyfile`](#local-paths-variables-table) is not defined!
| agent_param_tlspskidentity | `string` | `PSK_ID_{{ inventory_hostname }}` | [**TLSPSKIdentity**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlspskidentity) | Pre-shared key identity string used for encrypted communications with Zabbix server. Default value uses prefixed hostname from inventory.
| agent_param_tlsservercertissuer | `string` || [**TLSServerCertIssuer**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsservercertissuer) | Allowed server (proxy) certificate issuer.
| agent_param_tlsservercertsubject | `string` || [**TLSServerCertSubject**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsservercertsubject) | Allowed server (proxy) certificate subject.
| agent_param_unsafeuserparameters | `int` || [**UnsafeUserParameters**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#unsafeuserparameters) | Allow all characters to be passed in arguments to user-defined parameters.
| agent_param_userparameter | `list` || [**UserParameter**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#userparameter) | User-defined parameter to monitor. Listed user parameters will be placed into the target machine folder: `/etc/zabbix/zabbix_agent[d|2].d/userparameters.conf`. If changed, this parameter triggers *userparameter reload*(agent runtime command).
| agent_param_userparameterdir | `string` || [**UserParameterDir**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#userparameterdir) | Default search path for UserParameter commands.

### Zabbix **agentd** unique parameters:

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| agent_param_allowroot | `int` || [**AllowRoot**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#allowroot)	| Allow the agent to run as 'root'.
| agent_param_enableremotecommands | `int` || [**EnableRemoteCommands**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#enableremotecommands) |	Whether remote commands from Zabbix server are allowed.
| agent_param_listenbacklog | `int` || [**ListenBacklog**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#listenbacklog) | Maximum number of pending connections in the TCP queue.
| agent_param_loadmodule | `list` || [**LoadModule**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#loadmodule) | Module to load at agent startup.
| agent_param_loadmodulepath | `string` | /usr/lib64/zabbix/modules | [**LoadModulePath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#loadmodulepath) | Full path to the location of agent modules.
| agent_param_logremotecommands | `int` || [**LogRemoteCommands**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logremotecommands) | Enable logging of executed shell commands as warnings.
| agent_param_maxlinespersecond | `int` || [**MaxLinesPerSecond**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#maxlinespersecond) | Maximum number of new lines per second that the agent will send to Zabbix server or proxy when processing 'log' and 'logrt' active checks.
| agent_param_startagents | `int` || [**StartAgents**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#startagents) | Number of pre-forked instances of zabbix_agentd processing the passive checks.
| agent_param_tlscipherall | `string` || [**TLSCipherAll**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherall) | Override the default ciphersuite selection criteria for certificate- and PSK-based encryption.
| agent_param_tlscipherall13 | `string` || [**TLSCipherAll13**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherall13) | Override the default ciphersuite selection criteria for certificate- and PSK-based encryption.
| agent_param_tlsciphercert | `string` || [**TLSCipherCert**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsciphercert) | Override the default ciphersuite selection criteria for certificate-based encryption.
| agent_param_tlsciphercert13 | `string` || [**TLSCipherCert13**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsciphercert13) | Override the default ciphersuite selection criteria for certificate-based encryption.
| agent_param_tlscipherpsk | `string` || [**TLSCipherPSK**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherpsk) | Override the default ciphersuite selection criteria for PSK-based encryption.
| agent_param_tlscipherpsk13 | `string` || [**TLSCipherPSK13**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherpsk13) | Override the default ciphersuite selection criteria for PSK-based encryption.
| agent_param_user | `string` || [**User**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#user) | Drop privileges to a specific user existing in the system.

### Zabbix **agent 2** unique parameters:

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| agent_param_controlsocket | `string` | /run/zabbix/agent.sock | [**ControlSocket**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#controlsocket) | Control socket used to send runtime commands with the '-R' option.
| agent_param_enablepersistentbuffer | `int` || [**EnablePersistentBuffer**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#enablepersistentbuffer) | Enable the usage of local persistent storage for active items.
| agent_param_forceactivechecksonstart | `int` || [**ForceActiveChecksOnStart**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#forceactivechecksonstart) | Perform active checks immediately after the restart for the first received configuration.
| agent_param_persistentbufferfile | `string` || [**PersistentBufferFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#persistentbufferfile) | File where Zabbix agent 2 should keep the SQLite database.
| agent_param_persistentbufferperiod | `string` || [**PersistentBufferPeriod**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#persistentbufferperiod) | Time period of storing the data when there is no connection to the server or proxy.
| agent_param_plugins_log_maxlinespersecond | `int` | `{{ agent_param_maxlinespersecond }}` | [**Plugins.Log.MaxLinesPerSecond**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#plugins.log.maxlinespersecond) | Maximum number of new lines per second to be sent by the agent to Zabbix server or proxy when processing 'log' and 'logrt' active checks. By default, works like alias to `agent_param_maxlinespersecond`.
| agent_param_plugins_systemrun_logremotecommands | `int` | `{{ agent_param_logremotecommands }}`| [**Plugins.SystemRun.LogRemoteCommands**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#plugins.systemrun.logremotecommands) | Enable the logging of the executed shell commands as warnings. By default, works like alias to `agent_param_logremotecommands`.
| agent_param_pluginsocket | `string` | /run/zabbix/agent.plugin.sock | [**PluginSocket**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#pluginsocket) | Path to the UNIX socket for loadable plugin communications.
| agent_param_plugintimeout | `int` || [**PluginTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#plugintimeout) | Timeout for connections with loadable plugins, in seconds.
| agent_param_refreshactivechecks | `int` || [**RefreshActiveChecks**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#refreshactivechecks) | How often the list of active checks is refreshed.
| agent_param_statusport | `int` || [**StatusPort**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#statusport) | If set, the agent will listen on this port for HTTP status requests (`http://localhost:<port>/status`).
| agent_param_includeplugins | `list` | ["/etc/zabbix/zabbix_agent2.d/plugins.d/*.conf"] | [**Include**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#include) | Path to plugin configuration files. You may include individual files or all files in a directory in the configuration file.
### Zabbix **agent 2 Ceph plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_ceph_insecureskipverify | `string` | [**Plugins.Ceph.InsecureSkipVerify**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Determines whether the HTTP client should verify the server's certificate chain and host name. If true, TLS accepts any certificate presented by the server and any host name in that certificate. In this mode, TLS is susceptible to man-in-the-middle attacks (should be used only for testing).
| agent_param_plugins_ceph_keepalive | `int` | [**Plugins.Ceph.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| agent_param_plugins_ceph_timeout | `int` | [**Plugins.Ceph.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| agent_param_plugins_ceph_sessions | `list of dictionaries` | [**Plugins.Ceph.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", apikey: "", user: "", uri: ""}`
| agent_param_plugins_ceph_default | `dictionary` | [**Plugins.Ceph.Default**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ apikey: "", user: "", uri: ""}`

### Zabbix **agent 2 Docker plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_docker_endpoint | `string` | [**Plugins.Docker.Endpoint**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/d_plugin) |	Docker daemon unix-socket location. Must contain a scheme (only `unix://` is supported).
| agent_param_plugins_docker_timeout | `int` | [**Plugins.Docker.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/d_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).

### Zabbix **agent 2 Memcached plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_memcached_keepalive | `int` | [**Plugins.Memcached.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| agent_param_plugins_memcached_timeout | `int` | [**Plugins.Memcached.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| agent_param_plugins_memcached_sessions | `list of dictionaries` | [**Plugins.Memcached.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", password: "", user: "", uri: ""}`
| agent_param_plugins_memcached_default| `dictionary` | [**Plugins.Memcached.Default**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ password: "", user: "", uri: ""}`

### Zabbix **agent 2 Modbus plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_modbus_timeout | `int` | [**Plugins.Modbus.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/modbus_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| agent_param_plugins_modbus_sessions | `list of dictionaries` | [**Plugins.Modbus.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/modbus_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", endpoint: "", slaveid: "", timeout: ""}`

### Zabbix **agent 2 MongoDB plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).
To encrypt session, define `tlsconnect` key. After `tlsconnect` session key is defined, all 3 certificate files become mandatory!
Parameter prefixes `source_` should point to the certificate files located on Ansible execution environment. The certificate files will be placed on the target machine and added to configuration automatically.

You can also manage session certificate files outside this role. In this case, use same keys without `source_` prefix and fill them with final path to files on the target machine.
Here is the dictionary skeleton for self-managed certificate files:
`{ name: "", uri: "", user: "", password: "", tlsconnect: "", tlscafile: "", tlscertfile: "", tlskeyfile: ""}`

Don't use both local path and final path to avoid unpredictable results!

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| agent_param_plugins_mongodb_keepalive | `int` || [**Plugins.MongoDB.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| agent_param_plugins_mongodb_timeout | `int` || [**Plugins.MongoDB.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| agent_param_plugins_mongodb_system_path | `string` | /usr/sbin/zabbix-agent2-plugin/zabbix-agent2-plugin-mongodb | [**Plugins.MongoDB.System.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Path to external plugin executable. Supported since Zabbix 6.0.6.
| agent_param_plugins_mongodb_sessions | `list of dictionaries` || [**Plugins.MongoDB.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`
| agent_param_plugins_mongodb_default | `dictionary` || [**Plugins.MongoDB.Default**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ uri: "", user: "", password: "",}`

### Zabbix **agent 2 MQTT plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

You can also manage session certificate files outside this role. In this case, use same keys without `source_` prefix and fill them with final path to files on the target machine.
Here is the dictionary skeleton for self-managed certificate files:
`{ name: "", url: "", topic: "", user: "", password: "", tlscafile: "", tlscertfile: "", tlskeyfile: ""}`

Don't use both local path and final path to avoid unpredictable results!

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_mqtt_timeout | `int` | [**Plugins.MQTT.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mqtt_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| agent_param_plugins_mqtt_sessions | `list of dictionaries` | [**Plugins.MQTT.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mqtt_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", url: "", topic: "", user: "", password: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`
| agent_param_plugins_mqtt_default | `dictionary` | [**Plugins.MQTT.Default**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mqtt_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ url: "", topic: "", user: "", password: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`

### Zabbix **agent 2 Oracle plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_oracle_calltimeout | `int` | [**Plugins.Oracle.CallTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Maximum time of waiting (in seconds) for a request to be done.
| agent_param_plugins_oracle_connecttimeout | `int` | [**Plugins.Oracle.ConnectTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Maximum time of waiting (in seconds) for a connection to be established.
| agent_param_plugins_oracle_customqueriespath | `string` | [**Plugins.Oracle.CustomQueriesPath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Full pathname of the directory containing .sql files with custom queries. Disabled by default. Example: /etc/zabbix/oracle/sql
| agent_param_plugins_oracle_keepalive | `int` | [**Plugins.Oracle.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| agent_param_plugins_oracle_sessions | `list of dictionaries` | [**Plugins.Oracle.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", service: "", user: "", password: "" }`
| agent_param_plugins_oracle_default | `list of dictionaries` | [**Plugins.Oracle.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ uri: "", service: "", user: "", password: "" }`

### Zabbix **agent 2 PostgreSQL plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).
To encrypt session, define `tlsconnect` key. After `tlsconnect` session key is defined, all 3 certificate files become mandatory!
Parameter prefixes `source_` should point to the certificate files located on Ansible execution environment. The certificate files will be placed on the target machine and added to configuration automatically.

You can also manage session certificate files outside this role. In this case, use same keys without `source_` prefix and fill them with final path to files on the target machine.
Here is the dictionary skeleton for self-managed certificate files:
`{ name: "", uri: "", user: "", password: "", database: "", tlsconnect: "", tlscafile: "", tlscertfile: "", tlskeyfile: "", cachemode: ""}`

Don't use both local path and final path to avoid unpredictable results!

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| agent_param_plugins_postgresql_calltimeout | `int` || [**Plugins.Postgresql.CallTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Maximum time of waiting (in seconds) for a request to be done.
| agent_param_plugins_postgresql_customqueriespath | `string` || [**Plugins.Postgresql.CustomQueriesPath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Full pathname of the directory containing .sql files with custom queries. Disabled by default. Example: /etc/zabbix/postgresql/sql
| agent_param_plugins_postgresql_keepalive | `int` || [**Plugins.Postgresql.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Time of waiting (in seconds) for unused connections to be closed.
| agent_param_plugins_postgresql_timeout | `int` || [**Plugins.Postgresql.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Maximum time of waiting (in seconds) for a connection to be established.
| agent_param_plugins_postgresql_system_path | `string` | /usr/sbin/zabbix-agent2-plugin/zabbix-agent2-plugin-postgresql | [**Plugins.Postgresql.System.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Path to the external plugin executable. Supported since Zabbix 6.0.6.
| agent_param_plugins_postgresql_sessions | `list of dictionaries` || [**Plugins.Postgresql.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", database: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: "", cahcemode: ""}`
| agent_param_plugins_postgresql_default | `dictionary` || [**Plugins.Postgresql.Default**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ uri: "", user: "", password: "", database: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: "", cachemode: ""}`

### Zabbix **agent 2 MySQL plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).
To encrypt session, define `tlsconnect` key. After `tlsconnect` session key is defined, all 3 certificate files become mandatory!
Parameter prefixes `source_` should point to the certificate files located on Ansible execution environment. The certificate files will be placed on the target machine and added to configuration automatically.

You can also manage session certificate files outside this role. In this case, use same keys without `source_` prefix and fill them with final path to files on the target machine.
Here is the dictionary skeleton for self-managed certificate files:
`{ name: "", uri: "", user: "", password: "", tlsconnect: "", tlscafile: "", tlscertfile: "", tlskeyfile: ""}`

Don't use both local path and final path to avoid unpredictable results!

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_mysql_calltimeout | `int` | [**Plugins.Mysql.CallTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Maximum time of waiting (in seconds) for a request to be done.
| agent_param_plugins_mysql_keepalive | `int` | [**Plugins.Mysql.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Time of waiting (in seconds) before unused connections are closed.
| agent_param_plugins_mysql_timeout | `int` | [**Plugins.Mysql.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Maximum time of waiting (in seconds) for a connection to be established.
| agent_param_plugins_mysql_customqueriespath | `string` | [**Plugins.Mysql.CustomQueriesPath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Full pathname of a directory containing *.sql* files with custom queries.
| agent_param_plugins_mysql_sessions | `list of dictionaries` | [**Plugins.Mysql.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`
| agent_param_plugins_mysql_default | dictionary | [**Plugins.Mysql.Default.\***](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ uri: "", user: "", password: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`

### Zabbix **agent 2 MSSQL plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).
Parameter prefixes `source_` should point to the certificate files located on Ansible execution environment. The certificate files will be placed on the target machine and added to configuration automatically.

You can also manage session certificate files outside this role. In this case, use same keys without `source_` prefix and fill them with final path to files on the target machine.
Here is the dictionary skeleton for self-managed certificate files:
`{ name: "", uri: "", user: "", password: "", cacertpath: "", trustservercertificate: "", hostnameincertificate: "", encrypt: "", tlsminversion: ""}`

Don't use both local path and final path to avoid unpredictable results!

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_mssql_keepalive | `int` | [**Plugins.MSSQL.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mssql_plugin) | Time of waiting (in seconds) before unused connections are closed.
| agent_param_plugins_mssql_timeout | `int` | [**Plugins.MSSQL.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mssql_plugin) | The amount of time to wait for a server to respond when first connecting and on follow-up operations in the session.
| agent_param_plugins_mssql_customqueriespath | `string` | [**Plugins.MSSQL.CustomQueriesPath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mssql_plugin) | Full pathname of a directory containing *.sql* files with custom queries. Changes requires Zabbix agent2 restart.
| agent_param_plugins_mssql_system_path | `string` | /usr/sbin/zabbix-agent2-plugin/zabbix-agent2-plugin-mssql | [**Plugins.MSSQL.System.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mssql_plugin) | Path to the external plugin executable.
| agent_param_plugins_mssql_sessions | `list of dictionaries` | [**Plugins.MSSQL.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mssql_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", source_cacertpath: "", trustservercertificate: "", hostnameincertificate: "", encrypt: "", tlsminversion: ""}`
| agent_param_plugins_mssql_default | dictionary | [**Plugins.MSSQL.Default.\***](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mssql_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ uri: "", user: "", password: "", source_cacertpath: "", trustservercertificate: "", hostnameincertificate: "", encrypt: "", tlsminversion: ""}`

### Zabbix **agent 2 Redis plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_redis_keepalive | `int` | [**Plugins.Redis.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| agent_param_plugins_redis_timeout | `int` | [**Plugins.Redis.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| agent_param_plugins_redis_sessions | `list of dictionaries` | [**Plugins.Redis.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", password: "" }`
| agent_param_plugins_redis_default | `dictionary` | [**Plugins.Redis.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Holds the default connection credentials in dictionary form with the keys: `{ uri: "", password: "" }`

### Zabbix **agent 2 Smart plugin** parameters:

For these settings to take effect, the plugin should be listed in [`agent_2_plugin_list`](#general-settings).

| Variable | Type | Parameter | Description |
|--|--|--|--|
| agent_param_plugins_smart_path | `string` | [**Plugins.Smart.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/smart_plugin) | Path to the smartctl executable.
| agent_param_plugins_smart_timeout | `int` | [**Plugins.Smart.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/smart_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).


Hints & Tags
-----

- Wrong variable definition level can be punishing for starters. Begin with [**variable precedence learning**](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable).
  We recommend [**organizing host and group variables**](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#organizing-host-and-group-variables) on inventory level. It is handy for big environments and will fit most use cases.
- Zabbix agent role uses **handlers** to reload systemd daemon and restart `zabbix-agent[2]` service.
  To trigger **handler** execution each time (not only after changes made), compliment your run with `restart` tag. Add it after `all` tag or other tasks (those not marked with `restart` tag will be skipped).

      ansible-playbook -i inventory play.yml -t all,restart

- To stop and remove `zabbix-agent[2]` service, use `remove` tag. This will clear custom overrides if present and uninstall packages, according to variables defined.

      ansible-playbook -i inventory play.yml -t remove

- If `agent_param_userparameter` is modified and registered as the only change during role run, it will trigger Zabbix agent[2] runtime command to reload user parameters without agent restart.

- To run only tasks that modify user parameters, pass `userparam` tag. Task sequence will be limited to:
  - Copying include folder.
  - Copying script folder.
  - Adding a list of user parameters from `agent_param_userparameter` variable to configuration file.
  - Executing runtime command to reload user parameters.

        ansible-playbook -i inventory play.yml -t userparam


Playbook examples
-----------------

- ### Playbook 1:
  **Latest LTS Zabbix agentd deployment for active checks only.**
  1. Here we will deploy Zabbix agentd (from defaults: `agent_variant = 1`).
  2. Major version defaults to current LTS version.
  3. Since we are removing passive checks with `agent_param_startagents = 0`, firewalld rule application will be skipped.
  4. Hostname of the agent or `agent_param_hostname` defaults to the inventory hostname.
  5. We can prepare metadata for active agent autoregistration by using Ansible special variables and filters.
  In this example we will use groups from the inventory to form the metadata. Special variable `group_names` contains the list of groups assigned to the host. Let's concatenate this list to the string separated by commas. It will look as follows: "DB,Linux,MySQL,etc"
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_startagents: 0            # do not spawn passive check processes that listen for connections;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
  ```

- ### Playbook 2:
  **6.4 version of Zabbix agent 2 for both passive and active checks + Iptables.**
  1. To deploy Zabbix agent 2, define `agent_variant = 2`.
  2. You can specify Zabbix agent major version manually: `agent_major_version: "6.4"`.
  3. Same metadata as described in the [first example](#playbook-1).
  4. Disable application of the firewall rule using firewalld daemon: `agent_apply_firewalld_rule: false`.
  5. Enable firewall rule application using iptables module. **Note** that modern Ubuntu distributions use nftables, and iptables are DEPRECATED.

  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_variant: 2
          agent_major_version: 6.4
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          agent_apply_firewalld_rule: false                          # "auto" is the default and recommended value;
          agent_apply_iptables_rule: true                          # "auto" is the default value;
          agent_firewall_allow_from: 127.0.0.1  # limit listening on agent port only from the defined source address
  ```

- ### Playbook 3:
  **Zabbix agentd for both passive and active checks with PSK encryption for autoregistration.**
  1. Same metadata for autoregistration as described in the [first example](#playbook-1).
  2. Set incoming and outgoing connection to be encrypted with `psk`
    - `agent_param_tlsconnect` is a single-type setting, so string input is expected;
    - `agent_param_tlsaccept` can simultaneously work with all 3 types, so we are using list format here;
    - `agent_source_tlspskfile` can use relative or absolute path to an existent key or a place where it should be generated. Because of autoregistration, single PSK key should be used and identity for all agents should be registered. After the key is generated, add it to Zabbix using GUI (Administration > General > Autoregistration);
    - `agent_param_tlspskidentity` is used for passing the identity name to be placed in Zabbix agent configuration file. The same should be placed in Zabbix autoregistration options (Administration > General > Autoregistration).

  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          agent_param_tlsconnect: psk
          agent_param_tlsaccept: [psk]
          agent_source_tlspskfile: TEST/autoregistration.psk # "autoregistration" key will be placed to TEST folder;
          agent_param_tlspskidentity: 'PSK_ID_AUTOREGISTRATION' # length <= 128 char
  ```

- ### Playbook 4:
  **Zabbix agentd with certificate-secured connections.**
  1. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `agent_param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  2. Same metadata as described in the [first example](#playbook-1).
  3. When `cert` is specified in `agent_param_tlsconnect` or `agent_param_tlsaccept` source, the path to certificate files becomes mandatory. Check the configuration example below. We are pointing to "certs/" folder which holds the certificate files named according to the host inventory name.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_param_server: 127.0.0.1                                # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1                          # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'    # concatenate group list to the string;
          agent_param_tlsconnect: cert                                 # restrict active checks to certificate only;
          agent_param_tlsaccept: ["cert", "unencrypted"]               # allow encrypted and unencrypted passive checks;
          agent_source_tlscafile: certs/ca.crt                         # provide the path to CA certificate file on Ansible execution environment;
          # agent_source_tlscrlfile:                                   # certificate revocation list, can be omitted;
          agent_source_tlscertfile: certs/{{ inventory_hostname }}.crt # Zabbix agent certificate path on the execution environment;
          agent_source_tlskeyfile: certs/{{ inventory_hostname }}.key  # key file path on the execution environment;
          agent_param_tlsservercertissuer: CN=root-ca                  # certificate issuer restriction (optional);
          agent_param_tlsservercertsubject: CN=server                   # certificate subject restriction (optional);
  ```

- ### Playbook 5:
  **6.4 version of Zabbix agent 2 for MongoDB monitoring.**
  1. To deploy Zabbix agent 2, define `agent_variant = 2`.
  2. You can specify Zabbix agent major version manually: `agent_major_version: "6.4"`.
  3. Same metadata as described in the [first example](#playbook-1).
  4. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `agent_param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  5. Since Zabbix 6.4, loadable plugins are not installed by `zabbix-agent2` package as dependency. We need to add it to `agent_2_plugin_list`.
  6. We will configure a TLS connection session within MongoDB, using the same approach with source files. The role will transfer them to the target machine and configure automatically. The certificate files will be placed to Zabbix agent service user home folder.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_variant: 2
          agent_major_version: 6.4
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          agent_2_plugin_list: [ceph, docker, memcached, modbus, mqtt, mysql, oracle, redis, smart, mongodb]
          agent_param_plugins_mongodb_sessions:
            - name: "sessionname"
              uri: "someuri"
              user: "someuser"
              password: "somepassword"
              tlsconnect: "required"
              ## Location of the source certificate files on Ansible execution environment.
              source_tlscafile: "certs/ca.crt"
              source_tlscertfile: "certs/{{ inventory_hostname }}.crt"
              source_tlskeyfile: "certs/{{ inventory_hostname }}.key"
  ```

- ### Playbook 6:
  **Zabbix agentd downgrade from 6.4 to 6.0**
  1. You can specify Zabbix agent major version manually: `agent_major_version: "6.0"`.
  2. The attempt to install earlier version will fail because the newer one is already installed. To overcome this, previous packages should be removed first.
  3. Same metadata as described in the [first example](#playbook-1).
  4. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `agent_param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_major_version: "6.0"
          agent_remove_previous_packages: true  # removes previously installed package of Zabbix agent (according to current settings);
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;

- ### Playbook 7:
  **Zabbix agentd running under custom user**
  1. Same metadata as described in the [first example](#playbook-1).
  2. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `agent_param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  3. Setting `agent_service_user` will trigger custom user task list. It will create user, user group, home folder, systemd overrides and a separate log folder.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          agent_service_user: dor               # if agent_service_user is not "zabbix", multiple changes are applied
          agent_service_group: blue
          agent_service_uid: 1115
          agent_service_gid: 1115
  ```

- ### Playbook 8:
  **Update Zabbix agentd to latest minor version**
  1. Same metadata as described in the [first example](#playbook-1).
  2. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `agent_param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  3. Setting `agent_package_state = latest` will install the latest minor version of the packages.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          agent_package_state: latest           # use latest available minor version
  ```

- ### Playbook 9:
  **Deploy Zabbix agent without direct internet access from target machine, by using HTTP proxy.**
  1. Same metadata as described in the [first example](#playbook-1).
  2. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `agent_param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  3. Supply HTTP proxy address to the `agent_http_proxy` variable.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.agent
          agent_param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          agent_param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          agent_param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          agent_http_proxy: http://host.containers.internal:8123  # HTTP proxy address.
  ```

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