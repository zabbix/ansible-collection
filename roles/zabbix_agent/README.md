Zabbix agent role
=================

You can use this Ansible role to deploy and configure Zabbix agents on the target machines. Both agentd and agent2 variants are available.
Currently, the following OS of target machines are supported:
- Redhat 7, 8, 9
- Ubuntu 18.04, 20.04, 22.04

Supported distribution list to be extended.

**Note**: This role is still in active development. There may be unidentified issues and the role variables may change as development continues.

Soon this role will be extended with additional functionality to add deployed target devices to Zabbix monitoring system. Check collection's page for release plan.

Table of contents
-----------------
<!--ts-->
  * [Requirements](#requirements)
  * [Role variables](#role-variables)
    * [General settings](#general-settings)
    * [User settings](#user-settings)
    * [Firewall settings](#firewall-settings)
    * [Local path settings](#local-paths-variables-table)
    * [Common Zabbix agent configuration file parameters](#common-zabbix-agent-configuration-parameters)
      * [Zabbix agent unique parameters](#zabbix-agentd-unique-parameters)
      * [Zabbix agent2 unique parameters](#zabbix-agent2-unique-parameters)
        * [Ceph plugin parameters](#zabbix-agent2-ceph-plugin-parameters)
        * [Docker plugin parameters](#zabbix-agent2-docker-plugin-parameters)
        * [Memcached plugin parameters](#zabbix-agent2-memcached-plugin-parameters)
        * [Modbus plugin parameters](#zabbix-agent2-modbus-plugin-parameters)
        * [MongoDB plugin parameters](#zabbix-agent2-mongodb-plugin-parameters)
        * [MQTT plugin parameters](#zabbix-agent2-mqtt-plugin-parameters)
        * [Oracle plugin parameters](#zabbix-agent2-oracle-plugin-parameters)
        * [PostgreSQL plugin parameters](#zabbix-agent2-postgresql-plugin-parameters)
        * [MySQL plugin parameters](#zabbix-agent2-mysql-plugin-parameters)
        * [Redis plugin parameters](#zabbix-agent2-redis-plugin-parameters)
        * [Smart plugin parameters](#zabbix-agent2-smart-plugin-parameters)
  * [Hints](#hints)
  * [Example playbooks](#example-playbooks)
    * [Playbook 1: Latest LTS Zabbix agentd deploy for active checks only](#playbook-1)
    * [Playbook 2: 6.4 version of Zabbix agent2 for both passive and active checks + Iptables](#playbook-2)
    * [Playbook 3: Zabbix agentd for both passive and active checks with PSK encryption for autoregistration](#playbook-3)
    * [Playbook 4: Zabbix agentd with certificate secured connections](#playbook-4)
    * [Playbook 5: 6.4 version of Zabbix agent2 for MongoDB monitoring](#playbook-5)
    * [Playbook 6: Zabbix agentd downgrade from 6.4 to 6.0](#playbook-6)
    * [Playbook 7: Zabbix agentd running under custom user](#playbook-7)
    * [Playbook 8: Update Zabbix agentd to the latest minor version](#playbook-8)
    * [Playbook 9: Deploy Zabbix agentd without direct internet access, by using HTTP proxy](#playbook-9)
  * [License](#license)

<!--te-->


Requirements
------------
This role uses official Zabbix packages and repository for component installation. Target machines require direct or [**HTTP proxy**](#playbook-9) internet access to Zabbix repository [**repo.zabbix.com**](https://repo.zabbix.com).

The role contains firewalld application rule to allow agent listen port. Firewalld is required on the target machines for this rule to work. Automatic mode `apply_firewalld_rule = auto` checks if firewalld is installed. Firewalld is a recommended method as it can work with iptables and nftables both. Firewalld can be installed on RHEL and Debian based distributions.

Multiple tasks require `superuser` privileges (sudo).

Ansible core >= 2.12

Zabbix agent role requires additional tools from two Ansible certified collections:
- ansible.posix >= 2.8
- ansible.utils >= 1.4 

You can install required collections easily:
```bash
ansible-galaxy collection install ansible.utils ansible.posix
```

Note that role uses [**ansible.utils.ipaddr**](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html) filter, which depends on python library [**netaddr**](https://pypi.org/project/netaddr). 

Zabbix agent role relies on [**Jinja2**](https://pypi.org/project/Jinja2/) heavily and requires version >= 2.10.1

You can install required python libraries on the control node as follows:

```bash
python3 -m pip install netaddr>=0.8.0 Jinja2>=2.10.1
```

Or using `requirements.txt` file in the role folder:

```bash
python3 -m pip install -r requirements.txt
```

Check [**python documentation**](https://docs.python.org/3/installing/index.html) for more details on python modules installation. 

Role Variables
--------------

You can modify variables listed in this section. Variables are not validated by the role itself. You should experiment with variable definition on a test instance before going for a full-scale deployment.

The default settings are aimed at the ease of installation. You can override those to improve security. 

### General settings:

| Variable | Type | Default | Description |
|--|--|--|--|
| agent_variant | `int` | 1 | The variant of Zabbix agent (1: Zabbix agentd, 2: Zabbix agent 2).
| agent_major_version | `string` | 6.0 | The major version of Zabbix agent. Defaults to the latest LTS.
| agent_minor_version | `string` || Zabbix agent minor version customization is available **only for RedHat based OS**.
| package_state | `string` | present | The state of packages to be deployed. Available options: `present`, `latest` - update to the latest version if available in installed **zabbix-release** repository. 
| remove_previous_packages | `boolean` | `false` | Trigger removal of previous packages prior to the installation of new ones. Mandatory to deploy earlier version than the one currently installed. 
| http_proxy | `string` || Defines [**HTTP proxy**](#playbook-9) address for the packager.
| https_proxy | `string` || Defines HTTPS proxy address for the packager.
| agent2_plugins_list | `list` | [ceph, docker, memcached, modbus, mongodb, mqtt, mysql, oracle, postgresql, redis, smart] | List of Zabbix agent2 plugins to configure and deploy(if the plugin is loadable). **Note** that loadable plugins for 6.0 version are installed as dependencies of Zabbix agent2 package. Starting with 6.4, loadable plugin installation is allowed at your own discretion. Default plugin list for Zabbix agent2 >= **6.4** is `[ceph, docker, memcached, modbus, mqtt, mysql, oracle, redis, smart]`.

### User settings:

The role allows creating a custom user for Zabbix agent. User customization tasks will trigger only when `service_user` is not "zabbix".

| Variable | Type | Default | Description |
|--|--|--|--|
| service_user | `string` | zabbix | The user to run Zabbix agent.
| service_group | `string` | zabbix | User group for the custom user.
| service_uid | `string` || User id for the custom user.
| service_gid | `string` || User group id for the custom user group.

Adds next task sequence:
- Creates group.
- Creates user with home folder (defaults to `/home/{{ service_user }}`).
- Adds **systemd** overrides to manage Zabbix agent pid file (`/run/zabbix_agent[d|2]/zabbix_agent[d|2].pid`).
- Changes Zabbix agent2 sockets paths (to the folder of pid file).
- Changes logging path (to `/var/log/zabbix_agent[d|2]/zabbix_agent[d|2].log`).

### Firewall settings:

The role allows adding simple firewall rules on the target machine to accept passive checks. Advanced firewall configuration is out of the scope of Zabbix agent role.

Firewalld is a recommended way of applying firewall rule as it works with iptables and nftables both. **Note** that `iptables` does not work in Ubuntu since 22.04. Firewalld should be installed on target machines. It is supported on RHEL and Debian based distributions.

| Variable | Type | Default | Description |
|--|--|--|--|
| apply_firewalld_rule | `string` | auto | Defines application of firewalld rule. Possible options: ["auto", "force"]. Undefined or any other string will skip the rule application.
| apply_iptables_rule | `boolean` | `false` | Defines application of iptables rule. Possible options: [true, false]. 
| firewalld_zone | `string` | default | Firewalld zone for rule application.
| firewall_allow_from | `string` || Limits source address of passive check using firewall rule. For firewalld, this setting will change the rule from simple to rich rule.

### Local paths variables table:

Variables prefixed with `source_` should point to a file or folder located on Ansible controller. These files are about to be transferred to the target machines.

| Variable | Type | Default | Description |
|--|--|--|--|
| source_conf_dir | `string` || Path to the configuration folder on Ansible controller that needs to be transferred to the target machine and included in Zabbix agent configuration. For example, a folder with `Userparameters`.
| source_scripts_dir | `string` || Path to the scripts folder on Ansible controller. Will be copied under the `service_user` home folder. Scripts can be utilized by `UserParameters`.
| source_modules_dir | `string` || Path to Zabbix agentd modules folder on Ansible controller. Will be copied to default location for default user. For custom user modules, will be placed under the `service_user` home folder.
| source_tlspskfile | `string` | `.PSK/{{ inventory_hostname }}.psk` | Path to the PSK key location on Ansible controller. The role will look for the files having the same names as `inventory_hostname` (hostname from inventory) and generate new if not found. This key will be placed under `service_user` home folder and added to Zabbix agent configuration automatically.
| source_tlscafile | `string` || Path to the file on Ansible controller containing the top-level CA(s) certificates for peer certificate verification. Will be placed under `service_user` home folder and added to Zabbix agent configuration automatically.
| source_tlscertfile | `string` || Path to the file on Ansible controller containing the agent certificate or certificate chain. Will be placed under `service_user` home folder and added to Zabbix agent configuration automatically.
| source_tlscrlfile | `string` || Path to the file on Ansible controller containing revoked certificates. Will be placed under `service_user` home folder and added to Zabbix agent configuration automatically.
| source_tlskeyfile | `string` || Path to the file containing the agent private key. Will be placed under `service_user` home folder and added to Zabbix agent configuration automatically.

### Common Zabbix agent configuration parameters:

These parameters are common for both agent variants

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| param_alias | `list` || [**Alias**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#alias) |	Set an alias for the item key. Location of aliases on target machine: `/etc/zabbix/zabbix_agent[d|2].d/aliases.conf`
| param_allowkey | `list` || [**AllowKey**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#allowkey) | Allow execution of the item keys that match the pattern.
| param_buffersend | `int` || [**BufferSend**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#buffersend) |	Do not keep data in the buffer longer than N seconds.
| param_buffersize | `int` || [**BufferSize**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#buffersize) |	Maximum number of values in the memory buffer.
| param_debuglevel | `int` || [**DebugLevel**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#debuglevel) |	Debug level.
| param_denykey | `list` || [**DenyKey**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#denykey) |	Deny execution of the item keys that match the pattern.
| param_heartbeatfrequency | `int` || [**HeartbeatFrequency**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#heartbeatfrequency) | Frequency of the heartbeat messages in seconds. Added in 6.4.
| param_hostinterface | `string` || [**HostInterface**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostinterface) | Optional parameter that defines the host interface.
| param_hostinterfaceitem | `string` || [**HostInterfaceItem**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostinterfaceitem) | Optional parameter that defines the item used for getting the host interface.
| param_hostmetadata | `string` || [**HostMetadata**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostmetadata) | Optional parameter that defines the host metadata.
| param_hostmetadataitem | `string` || [**HostMetadataItem**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostmetadataitem) | Optional parameter that defines Zabbix agent item used for getting the host metadata.
| param_hostname | `string` | `{{inventory_hostname}}` | [**Hostname**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostname) | Optional parameter that defines the hostname. Defaults to the hostname taken from the inventory.
| param_hostnameitem | `string` || [**HostnameItem**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#hostnameitem) | Optional parameter that defines Zabbix agent item used for getting the hostname.
| param_include | `list` | **agentd:** ["/etc/zabbix/zabbix_agentd.d/\*.conf"] **agent2:** ["/etc/zabbix/zabbix_agent2.d/\*.conf"] | [**Include**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#include) | You may include individual files or all files in a directory in the configuration file.
| param_listenip | `string` || [**ListenIP**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#listenip) | List of comma-delimited IP addresses that the agent should listen on.
| param_listenport | `int` || [**ListenPort**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#listenport) | The agent will listen on this port for connections from the server.
| param_logfile | `string` | **agentd:** /var/log/zabbix/zabbix_agentd.log **agent2:** /var/log/zabbix/zabbix_agent2.log | [**LogFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logfile) | Name of the log file.
| param_logfilesize | `int` | 0 | [**LogFileSize**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logfilesize) | Maximum size of the log file.
| param_logtype | `string` | file | [**LogType**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logtype) | Type of the log output.
| param_pidfile | `string` | **agentd:** /run/zabbix/zabbix_agentd.pid **agent2:** /run/zabbix/zabbix_agent2.pid | [**PidFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#pidfile) | Name of the PID file.
| param_refreshactivechecks | `int` || [**RefreshActiveChecks**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#refreshactivechecks) | How often the list of active checks is refreshed.
| param_server | `string` | ::/0 | [**Server**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#server) | List of comma-delimited IP addresses, optionally in CIDR notation, or hostnames of Zabbix servers and Zabbix proxies.
| param_serveractive | `string` || [**ServerActive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#serveractive) | Zabbix server/proxy address or cluster configuration to get the active checks from.
| param_sourceip | `string` || [**SourceIP**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#sourceip) | Source IP address.
| param_timeout | `int` || [**Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#timeout) | Spend no more than Timeout seconds on processing.
| param_tlsaccept | `list` | ["unencrypted"] | [**TLSAccept**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsaccept) | Incoming connections to be accepted.
| param_tlsconnect | `string` | unencrypted | [**TLSConnect**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsconnect) | How the agent should connect to Zabbix server or proxy.
| param_tlspskidentity | `string` | `PSK_ID_{{ inventory_hostname }}` | [**TLSPSKIdentity**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlspskidentity) | Pre-shared key identity string used for encrypted communications with Zabbix server.
| param_tlsservercertissuer | `string` || [**TLSServerCertIssuer**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsservercertissuer) | Allowed server (proxy) certificate issuer.
| param_tlsservercertsubject | `string` || [**TLSServerCertSubject**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsservercertsubject) | Allowed server (proxy) certificate subject.
| param_unsafeuserparameters | `int` || [**UnsafeUserParameters**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#unsafeuserparameters) | Allow all characters to be passed in arguments to user-defined parameters.
| param_userparameter | `list` || [**UserParameter**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#userparameter) | User-defined parameter to monitor. Location of userparameters on target machine: `/etc/zabbix/zabbix_agent[d|2].d/userparameters.conf`
| param_userparameterdir | `string` || [**UserParameterDir**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#userparameterdir) | Default search path for UserParameter commands.

### Zabbix **agentd** unique parameters:

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| param_allowroot | `int` || [**AllowRoot**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#allowroot)	| Allow the agent to run as 'root'.
| param_enableremotecommands | `int` || [**EnableRemoteCommands**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#enableremotecommands) |	Whether remote commands from Zabbix server are allowed.
| param_listenbacklog | `int` || [**ListenBacklog**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#listenbacklog) | Maximum number of pending connections in the TCP queue.
| param_loadmodule | `list` || [**LoadModule**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#loadmodule) | Module to load at agent startup.
| param_loadmodulepath | `string` | /usr/lib64/zabbix/modules | [**LoadModulePath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#loadmodulepath) | Full path to the location of agent modules.
| param_logremotecommands | `int` || [**LogRemoteCommands**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#logremotecommands) | Enable logging of executed shell commands as warnings.
| param_maxlinespersecond | `int` || [**MaxLinesPerSecond**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#maxlinespersecond) | Maximum number of new lines per second that the agent will send to Zabbix server or proxy when processing 'log' and 'logrt' active checks.
| param_startagents | `int` || [**StartAgents**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#startagents) | Number of pre-forked instances of zabbix_agentd processing the passive checks.
| param_tlscipherall | `string` || [**TLSCipherAll**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherall) | Override the default ciphersuite selection criteria for certificate- and PSK-based encryption.
| param_tlscipherall13 | `string` || [**TLSCipherAll13**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherall13) | Override the default ciphersuite selection criteria for certificate- and PSK-based encryption.
| param_tlsciphercert | `string` || [**TLSCipherCert**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsciphercert) | Override the default ciphersuite selection criteria for certificate-based encryption.
| param_tlsciphercert13 | `string` || [**TLSCipherCert13**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlsciphercert13) | Override the default ciphersuite selection criteria for certificate-based encryption.
| param_tlscipherpsk | `string` || [**TLSCipherPSK**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherpsk) | Override the default ciphersuite selection criteria for PSK-based encryption.
| param_tlscipherpsk13 | `string` || [**TLSCipherPSK13**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#tlscipherpsk13) | Override the default ciphersuite selection criteria for PSK-based encryption.
| param_user | `string` || [**User**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agentd#user) | Drop privileges to a specific user existing in the system.

### Zabbix **agent2** unique parameters:

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| param_controlsocket | `string` | /run/zabbix/agent.sock | [**ControlSocket**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#controlsocket) | Control socket used to send runtime commands with the '-R' option.
| param_enablepersistentbuffer | `int` || [**EnablePersistentBuffer**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#enablepersistentbuffer) | Enable the usage of local persistent storage for active items.
| param_forceactivechecksonstart | `int` || [**ForceActiveChecksOnStart**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#forceactivechecksonstart) | Perform active checks immediately after the restart for the first received configuration.
| param_persistentbufferfile | `string` || [**PersistentBufferFile**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#persistentbufferfile) | File where Zabbix agent 2 should keep the SQLite database.
| param_persistentbufferperiod | `string` || [**PersistentBufferPeriod**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#persistentbufferperiod) | Time period of storing the data when there is no connection to the server or proxy.
| param_plugins_log_maxlinespersecond | `int` | `{{ param_maxlinespersecond }}` | [**Plugins.Log.MaxLinesPerSecond**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#plugins.log.maxlinespersecond) | Maximum number of new lines per second to be sent by the agent to Zabbix server or proxy when processing 'log' and 'logrt' active checks. By default, works like alias to `param_maxlinespersecond`.
| param_plugins_systemrun_logremotecommands | `int` | `{{ param_logremotecommands }}`| [**Plugins.SystemRun.LogRemoteCommands**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#plugins.systemrun.logremotecommands) | Enable the logging of the executed shell commands as warnings. By default, works like alias to `param_logremotecommands`.
| param_pluginsocket | `string` | /run/zabbix/agent.plugin.sock | [**PluginSocket**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#pluginsocket) | Path to the UNIX socket for loadable plugin communications.
| param_plugintimeout | `int` || [**PluginTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#plugintimeout) | Timeout for connections with loadable plugins, in seconds.
| param_refreshactivechecks | `int` || [**RefreshActiveChecks**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#refreshactivechecks) | How often the list of active checks is refreshed.
| param_statusport | `int` || [**StatusPort**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#statusport) | If set, the agent will listen on this port for HTTP status requests (`http://localhost:<port>/status`).
| param_includeplugins | `list` | ["/etc/zabbix/zabbix_agent2.d/plugins.d/*.conf"] | [**Include**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2#include) | If set, the agent will listen on this port for HTTP status requests (`http://localhost:<port>/status`).

### Zabbix **agent2 Ceph plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_ceph_insecureskipverify | `string` | [**Plugins.Ceph.InsecureSkipVerify**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Determines whether the http client should verify the server's certificate chain and host name. If true, TLS accepts any certificate presented by the server and any host name in that certificate. In this mode, TLS is susceptible to man-in-the-middle attacks (should be used only for testing).
| param_plugins_ceph_keepalive | `int` | [**Plugins.Ceph.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed. 
| param_plugins_ceph_timeout | `int` | [**Plugins.Ceph.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| param_plugins_ceph_sessions | `list of dictionaries` | [**Plugins.Ceph.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/ceph_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", apikey: "", user: "", uri: ""}`

### Zabbix **agent2 Docker plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_docker_endpoint | `string` | [**Plugins.Docker.Endpoint**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/d_plugin) |	Docker daemon unix-socket location. Must contain a scheme (only `unix://` is supported).
| param_plugins_docker_timeout | `int` | [**Plugins.Docker.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/d_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).

### Zabbix **agent2 Memcached plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_memcached_keepalive | `int` | [**Plugins.Memcached.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| param_plugins_memcached_timeout | `int` | [**Plugins.Memcached.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| param_plugins_memcached_sessions | `list of dictionaries` | [**Plugins.Memcached.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/memcached_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", password: "", user: "", uri: ""}`

### Zabbix **agent2 Modbus plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_modbus_timeout | `int` | [**Plugins.Modbus.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/modbus_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| param_plugins_modbus_sessions | `list of dictionaries` | [**Plugins.Modbus.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/modbus_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", endpoint: "", slaveid: "", timeout: ""}`

### Zabbix **agent2 MongoDB plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.
To encrypt session, define `tlsconnect` key. After `tlsconnect` session key is defined - all 3 certificate files becomes mandatory!
Parameter prefixes `source_` should point to the certificate files located on Ansible controller. The certificate files will be placed on the target machine and added to configuration automatically.

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| param_plugins_mongodb_keepalive | `int` || [**Plugins.MongoDB.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| param_plugins_mongodb_timeout | `int` || [**Plugins.MongoDB.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| param_plugins_mongodb_system_path | `string` | /usr/sbin/zabbix-agent2-plugin/zabbix-agent2-plugin-mongodb | [**Plugins.MongoDB.System.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Path to external plugin executable. Supported since Zabbix 6.0.6
| param_plugins_mongodb_sessions | `list of dictionaries` || [**Plugins.MongoDB.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mongodb_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`

### Zabbix **agent2 MQTT plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_mqtt_timeout | `int` | [**Plugins.MQTT.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mqtt_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).

### Zabbix **agent2 Oracle plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_oracle_calltimeout | `int` | [**Plugins.Oracle.CallTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Maximum time of waiting (in seconds) for a request to be done. 
| param_plugins_oracle_connecttimeout | `int` | [**Plugins.Oracle.ConnectTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Maximum time of waiting (in seconds) for a connection to be established.
| param_plugins_oracle_customqueriespath | `string` | [**Plugins.Oracle.CustomQueriesPath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Full pathname of the directory containing .sql files with custom queries. Disabled by default. Example: /etc/zabbix/oracle/sql
| param_plugins_oracle_keepalive | `int` | [**Plugins.Oracle.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| param_plugins_oracle_sessions | `list of dictionaries` | [**Plugins.Oracle.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/oracle_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", service: "", user: "", password: "" }`

### Zabbix **agent2 Postgresql plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.
To encrypt session, define `tlsconnect` key. After `tlsconnect` session key is defined - all 3 certificate files becomes mandatory!
Parameter prefixes `source_` should point to the certificate files located on Ansible controller. The certificate files will be placed on the target machine and added to configuration automatically.

| Variable | Type | Default | Parameter | Description |
|--|--|--|--|--|
| param_plugins_postgresql_calltimeout | `int` || [**Plugins.Postgresql.CallTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Maximum time of waiting (in seconds) for a request to be done. 
| param_plugins_postgresql_customqueriespath | `string` || [**Plugins.Postgresql.CustomQueriesPath**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Full pathname of the directory containing .sql files with custom queries. Disabled by default. Example: /etc/zabbix/postgresql/sql
| param_plugins_postgresql_keepalive | `int` || [**Plugins.Postgresql.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) |  Time of waiting (in seconds) for unused connections to be closed. 
| param_plugins_postgresql_timeout | `int` || [**Plugins.Postgresql.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Maximum time of waiting (in seconds) for a connection to be established.
| param_plugins_postgresql_system_path | `string` | /usr/sbin/zabbix-agent2-plugin/zabbix-agent2-plugin-postgresql | [**Plugins.Postgresql.System.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Path to the external plugin executable. Supported since Zabbix 6.0.6
| param_plugins_postgresql_sessions | `list of dictionaries` || [**Plugins.Postgresql.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/postgresql_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", database: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`

### Zabbix **agent2 MySQL plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.
To encrypt session, define `tlsconnect` key. After `tlsconnect` session key is defined - all 3 certificate files becomes mandatory!
Parameter prefixes `source_` should point to the certificate files located on Ansible controller. The certificate files will be placed on the target machine and added to configuration automatically.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_mysql_calltimeout | `int` | [**Plugins.Mysql.CallTimeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Maximum time of waiting (in seconds) for a request to be done. 
| param_plugins_mysql_keepalive | `int` | [**Plugins.Mysql.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) |  Time of waiting (in seconds) before unused connections are closed. 
| param_plugins_mysql_timeout | `int` | [**Plugins.Mysql.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Maximum time of waiting (in seconds) for a connection to be established.
| param_plugins_mysql_sessions | `list of dictionaries` | [**Plugins.Mysql.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/mysql_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "", tlsconnect: "", source_tlscafile: "", source_tlscertfile: "", source_tlskeyfile: ""}`

### Zabbix **agent2 Redis plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_redis_keepalive | `int` | [**Plugins.Redis.KeepAlive**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Maximum time of waiting (in seconds) before unused plugin connections are closed.
| param_plugins_redis_timeout | `int` | [**Plugins.Redis.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).
| param_plugins_redis_sessions | `list of dictionaries` | [**Plugins.Redis.Sessions**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/redis_plugin) | Holds the list of connection credentials in dictionary form with the keys: `{ name: "", uri: "", user: "", password: "" }`

### Zabbix **agent2 Smart plugin** parameters:

For these settings to take effect, the plugin should be listed in `agent2_plugins_list`.

| Variable | Type | Parameter | Description |
|--|--|--|--|
| param_plugins_smart_path | `string` | [**Plugins.Smart.Path**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/smart_plugin) | Path to the smartctl executable.
| param_plugins_smart_timeout | `int` | [**Plugins.Smart.Timeout**](https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2_plugins/smart_plugin) | Request execution timeout (how long to wait for a request to complete before shutting it down).

Hints
-----

- Wrong variable definition level can be punishing for starters. Begin with [**variable precedence learning**](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable). 
  We recommend [**organizing host and group variables**](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#organizing-host-and-group-variables) on inventory level. It is handy for big environments and will fit most use cases.
- Zabbix agent role uses **handlers** to reload systemd daemon and restart `zabbix-agent[2]` service.
  To trigger **handler** execution each time (not only after changes made) pass `restart` tag:

      ansible-playbook -i inventory play.yml -t restart



Example Playbooks
-----------------

- ### Playbook 1:
  **Latest LTS Zabbix agentd deployment for active checks only.**
  1. Here we will deploy Zabbix agentd (from defaults: `agent_variant = 1`).
  2. Major version defaults to current LTS version.
  3. Since we are removing passive checks with `param_startagents = 0`, firewalld rule application will be skipped.
  4. Hostname of the agent or `param_hostname` defaults to the inventory hostname.
  5. We can prepare metadata for active agent autoregistration by using Ansible special variables and filters.
  In this example we will use groups from the inventory to form the metadata. Special variable `group_names` contains the list of groups assigned to the host. Let's concatenate this list to the string separated by commas. It will look as follows: "DB,Linux,MySQL,etc"
  ```yaml
    - hosts: all 
      roles:
        - role: zabbix.zabbix.zabbix_agent
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_startagents: 0            # do not spawn passive check processes that listen for connections;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
  ```

- ### Playbook 2:
  **6.4 version of Zabbix agent2 for both passive and active checks + Iptables.**
  1. To deploy Zabbix agent2, define `agent_variant = 2`.
  2. You can specify Zabbix agent major version manually: `agent_major_version: "6.4"`.
  3. Same metadata as described in the [first example](#playbook-1).
  4. Disable application of the firewall rule using firewalld daemon: `apply_firewalld_rule: false`.
  5. Enable firewall rule application using iptables module. **Note** that modern Ubuntu distributions use nftables, and iptables are DEPRECATED.

  ```yaml
    - hosts: all 
      roles:
        - role: zabbix.zabbix.zabbix_agent
          agent_variant: 2
          agent_major_version: 6.4
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string;
          apply_firewalld_rule: false                          # "auto" is the default and recommended value;
          apply_iptables_rule: true                          # "auto" is the default value;
          firewall_allow_from: 127.0.0.1  # limit listening on agent port only from the defined source address
  ```

- ### Playbook 3:
  **Zabbix agentd for both passive and active checks with PSK encryption for autoregistration.**
  1. Same metadata for autoregistration as described in the [first example](#playbook-1).
  2. Set incoming and outgoing connection to be encrypted with `psk` 
    - `param_tlsconnect` is a single-type setting, so string input is expected;
    - `param_tlsaccept` can simultaneously work with all 3 types, so we are using list format here;
    - `source_tlspskfile` can use relative or absolute path to an existent key or a place where it should be generated. Because of autoregistration, single PSK key should be used and identity for all agents should be registered. After the key is generated, add it to Zabbix using GUI (Administration > General > Autoregistration); 
    - `param_tlspskidentity` is used for passing the identity name to be placed in Zabbix agent configuration file. The same should be placed in Zabbix autoregistration options (Administration > General > Autoregistration).

  ```yaml
    - hosts: all 
      roles:
        - role: zabbix.zabbix.zabbix_agent
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string; 
          param_tlsconnect: psk
          param_tlsaccept: [psk]
          source_tlspskfile: TEST/autoregistration.psk # "autoregistration" key will be placed to TEST folder;
          param_tlspskidentity: 'PSK_ID_AUTOREGISTRATION' # length <= 128 char
  ```

- ### Playbook 4:
  **Zabbix agentd with certificate-secured connections.**
  1. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped. 
  2. Same metadata as described in the [first example](#playbook-1).
  3. When `cert` if specified in `param_tlsconnect` or `param_tlsaccept` source, the path to certificate files becomes mandatory. Check the configuration example below. We are pointing to "certs/" folder which holds the certificate files named according to the host inventory name.
  ```yaml
    - hosts: all 
      roles:
        - role: zabbix.zabbix.zabbix_agent
          param_server: 127.0.0.1                                # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1                          # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'    # concatenate group list to the string;
          param_tlsconnect: cert                                 # restrict active checks to certificate only;
          param_tlsaccept: ["cert", "unencrypted"]               # allow encrypted and unencrypted passive checks;
          source_tlscafile: certs/ca.crt                         # provide the path to CA certificate file on Ansible controller;
          # source_tlscrlfile:                                   # certificate revocation list, can be omitted;
          source_tlscertfile: certs/{{ inventory_hostname }}.crt # Zabbix agent certificate path on the controller;
          source_tlskeyfile: certs/{{ inventory_hostname }}.key  # key file path on the controller;
          param_tlsservercertissuer: CN=root-ca                  # certificate issuer restriction (optional);
          param_tlsservercertsubject: CN=server                   # certificate subject restriction (optional);
  ```

- ### Playbook 5:
  **6.4 version of Zabbix agent2 for MongoDB monitoring.**
  1. To deploy Zabbix agent2, define `agent_variant = 2`.
  2. You can specify Zabbix agent major version manually: `agent_major_version: "6.4"`.
  3. Same metadata as described in the [first example](#playbook-1).
  4. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped.
  5. Since Zabbix 6.4, loadable plugins are not installed by `zabbix-agent2` package as dependency. We need to add it to `agent2_plugin_list`.
  6. We will configure a TLS connection session within MongoDB, using the same approach with source files. The role will transfer them to the target machine and configure automatically. The certificate files will be placed to Zabbix agent service user home folder.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.zabbix_agent
          agent_variant: 2
          agent_major_version: 6.4
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string; 
          agent2_plugin_list: [ceph, docker, memcached, modbus, mqtt, mysql, oracle, redis, smart, mongodb]
          param_plugins_mongodb_sessions: 
            - name: "sessionname"
              uri: "someuri"
              user: "someuser"
              password: "somepassword"
              tlsconnect: "required"
              ## Location of the source certificate files on Ansible controller.
              source_tlscafile: "certs/ca.crt"
              source_tlscertfile: "certs/{{ inventory_hostname }}.crt"
              source_tlskeyfile: "certs/{{ inventory_hostname }}.key"
  ```

- ### Playbook 6:
  **Zabbix agentd downgrade from 6.4 to 6.0**
  1. You can specify Zabbix agent major version manually: `agent_major_version: "6.0"`.
  2. The attempt to install earlier version will fail because the newer one is already installed. To overcome this, previous packages should be removed first.
  3. Same metadata as described in the [first example](#playbook-1).
  4. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped. 
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.zabbix_agent
          agent_major_version: "6.0"
          remove_previous_packages: true  # removes previously installed package of Zabbix agent (according to current settings);
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string; 

- ### Playbook 7:
  **Zabbix agentd running under custom user**
  1. Same metadata as described in the [first example](#playbook-1).
  2. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped. 
  3. Setting `service_user` will trigger custom user task list. It will create user, user group, home folder, systemd overrides and a separate log folder.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.zabbix_agent
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string; 
          service_user: dor               # if service_user is not "zabbix", multiple changes are applied
          service_group: blue 
          service_uid: 1115
          service_gid: 1115
  ```

- ### Playbook 8:
  **Update Zabbix agentd to latest minor version**
  1. Same metadata as described in the [first example](#playbook-1).
  2. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped. 
  3. Setting `package_state = latest` will install the latest minor version of the packages. 
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.zabbix_agent
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string; 
          package_state: latest           # use latest available minor version
  ```

- ### Playbook 9:
  **Deploy Zabbix agent without direct internet access from target machine. Using HTTP proxy.**
  1. Same metadata as described in the [first example](#playbook-1).
  2. When passive checks are enabled, the role attempts to apply **firewalld** rule to allow listening on Zabbix agent port (which defaults to `param_listenport = 10050`). Firewalld should be installed on the target machine or this step will be skipped. 
  3. Supply HTTP proxy address to the `http_proxy` variable.
  ```yaml
    - hosts: all
      roles:
        - role: zabbix.zabbix.zabbix_agent
          param_server: 127.0.0.1         # address of Zabbix server to accept connections from;
          param_serveractive: 127.0.0.1   # address of Zabbix server to connect using active checks;
          param_hostmetadata: '{{ group_names | join(",") }}'   # concatenate group list to the string; 
          http_proxy: http://host.containers.internal:8123  # HTTP proxy address. 
  ```

License
-------

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.