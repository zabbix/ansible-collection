# Zabbix Ansible Collection Release Notes

**Topics**

- <a href="#v1-6-0">v1\.6\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-5-0">v1\.5\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#major-changes-1">Major Changes</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v1-4-2">v1\.4\.2</a>
    - <a href="#major-changes-2">Major Changes</a>
- <a href="#v1-4-1">v1\.4\.1</a>
    - <a href="#major-changes-3">Major Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-4-0">v1\.4\.0</a>
    - <a href="#major-changes-4">Major Changes</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v1-3-12">v1\.3\.12</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v1-3-11">v1\.3\.11</a>
    - <a href="#major-changes-5">Major Changes</a>
    - <a href="#removed-features-previously-deprecated-1">Removed Features \(previously deprecated\)</a>
- <a href="#v1-3-10">v1\.3\.10</a>
    - <a href="#major-changes-6">Major Changes</a>
    - <a href="#bugfixes-3">Bugfixes</a>
- <a href="#v1-3-9">v1\.3\.9</a>
    - <a href="#major-changes-7">Major Changes</a>
- <a href="#v1-3-8">v1\.3\.8</a>
    - <a href="#major-changes-8">Major Changes</a>
- <a href="#v1-3-7">v1\.3\.7</a>
    - <a href="#major-changes-9">Major Changes</a>
    - <a href="#bugfixes-4">Bugfixes</a>
- <a href="#v1-3-6">v1\.3\.6</a>
    - <a href="#major-changes-10">Major Changes</a>
    - <a href="#bugfixes-5">Bugfixes</a>
- <a href="#v1-3-5">v1\.3\.5</a>
    - <a href="#major-changes-11">Major Changes</a>
- <a href="#v1-3-4">v1\.3\.4</a>
    - <a href="#major-changes-12">Major Changes</a>
    - <a href="#bugfixes-6">Bugfixes</a>
- <a href="#v1-3-3">v1\.3\.3</a>
    - <a href="#major-changes-13">Major Changes</a>
- <a href="#v1-3-2">v1\.3\.2</a>
    - <a href="#major-changes-14">Major Changes</a>
    - <a href="#bugfixes-7">Bugfixes</a>
- <a href="#v1-3-1">v1\.3\.1</a>
    - <a href="#bugfixes-8">Bugfixes</a>
- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#major-changes-15">Major Changes</a>
    - <a href="#bugfixes-9">Bugfixes</a>
- <a href="#v1-2-5">v1\.2\.5</a>
    - <a href="#bugfixes-10">Bugfixes</a>
- <a href="#v1-2-4">v1\.2\.4</a>
    - <a href="#bugfixes-11">Bugfixes</a>
- <a href="#v1-2-3">v1\.2\.3</a>
    - <a href="#bugfixes-12">Bugfixes</a>
- <a href="#v1-2-2">v1\.2\.2</a>
    - <a href="#major-changes-16">Major Changes</a>
- <a href="#v1-2-1">v1\.2\.1</a>
    - <a href="#bugfixes-13">Bugfixes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#major-changes-17">Major Changes</a>
    - <a href="#bugfixes-14">Bugfixes</a>
- <a href="#v1-1-1">v1\.1\.1</a>
    - <a href="#major-changes-18">Major Changes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#major-changes-19">Major Changes</a>
    - <a href="#bugfixes-15">Bugfixes</a>
    - <a href="#new-plugins">New Plugins</a>
        - <a href="#httpapi">Httpapi</a>
        - <a href="#inventory">Inventory</a>
    - <a href="#new-modules-1">New Modules</a>
- <a href="#v1-0-6">v1\.0\.6</a>
    - <a href="#major-changes-20">Major Changes</a>
    - <a href="#bugfixes-16">Bugfixes</a>
- <a href="#v1-0-5">v1\.0\.5</a>
    - <a href="#major-changes-21">Major Changes</a>
- <a href="#v1-0-4">v1\.0\.4</a>
    - <a href="#major-changes-22">Major Changes</a>
- <a href="#v1-0-3">v1\.0\.3</a>
    - <a href="#major-changes-23">Major Changes</a>
- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#bugfixes-17">Bugfixes</a>

<a id="v1-6-0"></a>
## v1\.6\.0

<a id="release-summary"></a>
### Release Summary

<a id="major-changes"></a>
### Major Changes

* agent role \- added Zabbix agent and Zabbix agent 2 configuration templates for Zabbix 8\.0\.
* repository role \- added Zabbix 8\.0 repositories for all supported distributions\. Raspberry Pi OS is supported only on aarch64\, Zabbix 8\.0 has no armhf packages and no packages for Raspberry Pi OS 10\.

<a id="minor-changes"></a>
### Minor Changes

* agent role \- <code>Plugins\.Modbus\.Timeout</code> is not written for Zabbix 8\.0\, where the parameter was removed\.
* agent role \- added the <code>agent\_param\_allowkeyregexp</code> and <code>agent\_param\_denykeyregexp</code> parameters \(Zabbix 8\.0 and above\)\.
* agent role \- added the <code>agent\_repository\_manage</code> parameter\. Set it to <code>false</code> to skip the Zabbix repository configuration when Zabbix packages are available from repositories already configured on the target \(for example\, managed by Foreman\)\.
* agent role \- added the <code>connectiontimeout</code> key to Memcached\, MQTT and Redis plugin sessions and defaults\, and the <code>agent\_param\_plugins\_smart\_connectiontimeout</code> parameter \(Zabbix 8\.0 and above\)\.
* agent role \- the Ceph plugin is not configured for Zabbix 8\.0\, where it is no longer a built\-in plugin\.
* agent role \- the SELinux module \(<code>agent\_apply\_semodule</code>\) allows Zabbix agent 2 to access NVIDIA devices \(<code>xserver\_misc\_device\_t</code>\) when the <code>nvidia</code> plugin is in <code>agent\_2\_plugin\_list</code>\. Without the plugin the module does not reference this type\, so <code>semodule</code> does not fail on systems where it is not defined\.
* repository role \- added Amazon Linux 2023 \(Zabbix 6\.0\, 6\.5\, 7\.0\, 7\.2\, 7\.4 and 8\.0\)\.
* repository role \- added Debian 13 \(Zabbix 6\.0\, 7\.0\, 7\.4 and 8\.0\)\.
* repository role \- added Oracle Linux 10\, AlmaLinux 10 and Rocky Linux 10 \(Zabbix 6\.0\, 7\.0\, 7\.4 and 8\.0\)\.
* repository role \- added Ubuntu 26\.04 \(Zabbix 7\.0\, 7\.4 and 8\.0\) and Raspberry Pi OS 13 \(Zabbix 7\.0 and 7\.4\, Zabbix 8\.0 on aarch64 only\)\.
* repository role \- added Zabbix 6\.0 for RHEL 10 and CentOS Stream 10\.
* zabbix\_host module \- added the <code>retries</code> option to SNMP interface <code>details</code> \(Zabbix 8\.0 and above\)\.
* zabbix\_proxy module \- added the <code>timeout\_telemetry\_query</code> option to <code>custom\_timeouts</code> \(Zabbix 8\.0 and above\)\.

<a id="bugfixes"></a>
### Bugfixes

* <code>agent</code> and <code>repository</code> roles\: fixed <code>http\_proxy</code>/<code>https\_proxy</code> environment variables being rendered as the literal string <code>\"None\"</code> instead of being omitted when no proxy was configured\, which broke package installation and repository access behind a proxy\-less network\. The <code>default\(None\) \| default\(omit\)</code> filter chain never reached <code>omit</code> because Jinja\'s <code>default\(\)</code> filter only substitutes for undefined values\, not for <code>None</code>\; it now uses <code>default\(omit\, true\)</code>\.
* agent role \- README documented <code>agent\_param\_plugins\_mssql\_customqueriespath</code>\, the role uses <code>agent\_param\_plugins\_mssql\_customqueriesdir</code> \(<code>Plugins\.MSSQL\.CustomQueriesDir</code>\)\.
* agent role \- README documented <code>agent\_param\_plugins\_oracle\_default</code> as a list of dictionaries\, the role expects a dictionary\.
* agent role \- <code>agent\_repository\_priority</code> was not passed to the repository role because of a typo in the role dependency\.
* agent role \- documented the <code>agent\_param\_tlspskfile</code> parameter in README\.
* repository role \- fixed the repository URL for Debian and Ubuntu on aarch64 with Zabbix 7\.2 and 7\.4\. These versions keep all architectures in one directory\, the role added a non\-existent <code>\-arm64</code> suffix\.
* repository role \- removed Zabbix 7\.2 for CentOS Stream 10 on aarch64\, the repository has no packages for it\.
* zabbix\_host module \- fixed idempotence of SNMP interfaces with Zabbix 8\.0\, which returns the new <code>retries</code> detail\; the task reported a change on every run\.
* zabbix\_inventory plugin \- tag values in <code>filter\.tags</code> are sent to Zabbix API as strings\. Zabbix 8\.0 rejected numeric tag values with the <code>a character string is expected</code> error\.

<a id="v1-5-0"></a>
## v1\.5\.0

<a id="release-summary-1"></a>
### Release Summary

This release adds compatibility with Ansible 2\.19\+ to the <code>zabbix\_inventory</code> plugin and introduces a new <code>hostnames</code> option for building inventory hostnames from ordered Jinja2 expressions\, with supporting documentation examples\.

<a id="major-changes-1"></a>
### Major Changes

* <em class="title-reference">zabbix\_inventory</em> plugin\: added compatibility with Ansible 2\.19\+ by updating <code>TrustedAsTemplate</code> support for Jinja2 template expressions and by accepting plain <code>str</code> values \(in addition to <code>AnsibleUnicode</code>\) for the <code>query</code>\, <code>filter\.status</code>\, and <code>filter\.tags\_behavior</code> options\.

<a id="minor-changes-1"></a>
### Minor Changes

* <em class="title-reference">zabbix\_inventory</em> plugin\: added the <em class="title-reference">hostnames</em> option to build inventory hostnames from ordered Jinja2 expressions with fallback to the technical Zabbix host name\; duplicate rendered hostnames raise an error\.

<a id="v1-4-2"></a>
## v1\.4\.2

<a id="major-changes-2"></a>
### Major Changes

* added support for Zabbix 7\.4 for roles\, plugins and modules
* agent role \- added CentOs 10 Stream support
* agent role \- added Nvidia\-GPU plugin support for Zabbix\-agent2
* agent role \- added RHEL 10 support
* agent role \- added advanced encryption parameters for Zabbix\-agent2
* agent role \- changed path to the executable files of plugins in different version
* moved supported <em class="title-reference">ansible\-core</em> range to 2\.17\-2\.18

<a id="v1-4-1"></a>
## v1\.4\.1

<a id="major-changes-3"></a>
### Major Changes

* <em class="title-reference">zabbix\_inventory</em> plugin \- added strict AND logic for filtering by tags

<a id="bugfixes-1"></a>
### Bugfixes

* agent role \- fixed issue with installing of Zabbix agents for version 7\.2
* zabbix\_host module \- fixed issue of working with context macros

<a id="v1-4-0"></a>
## v1\.4\.0

<a id="major-changes-4"></a>
### Major Changes

* added support for Zabbix 7\.2 for roles\, plugins and modules
* moved supported ansible\-core range to 2\.16\-2\.18

<a id="minor-changes-2"></a>
### Minor Changes

* <em class="title-reference">zabbix\_inventory</em> plugin \- added function for resolving extra\-vars

<a id="new-modules"></a>
### New Modules

* zabbix\.zabbix\.zabbix\_proxy \- Module for creating and deleting proxies\, and updating existing ones\.
* zabbix\.zabbix\.zabbix\_proxy\_group \- Module for creating and deleting proxy groups\, and updating existing ones\.

<a id="v1-3-12"></a>
## v1\.3\.12

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* agent role \- removed Debian 9 support \(reached EOL\)
* agent role \- removed Ubuntu 18\.04 support \(reached EOM\)
* repository role \- removed Debian 9 support \(reached EOL\)
* repository role \- removed Ubuntu 18\.04 support \(reached EOM\)

<a id="bugfixes-2"></a>
### Bugfixes

* agent role \- added absolute path for verify task

<a id="v1-3-11"></a>
## v1\.3\.11

<a id="major-changes-5"></a>
### Major Changes

* <em class="title-reference">zabbix\_inventory</em> plugin \- added resolving proxyid and proxy\_groupid to names
* agent role \- Ansible rpm package management module change from <em class="title-reference">yum</em> to <em class="title-reference">dnf</em>
* host role \- added proxy group support
* host role \- removed default value from host\_proxy variable
* repository role \- Ansible rpm package management module change from <em class="title-reference">yum</em> to <em class="title-reference">dnf</em>
* zabbix\_host module \- added proxy group support

<a id="removed-features-previously-deprecated-1"></a>
### Removed Features \(previously deprecated\)

* agent role \- removed CentOS 8 Stream support \(reached EOL\)
* agent role \- removed RHEL 7 support \(reached EOM\)
* repository role \- removed CentOS 8 Stream support \(reached EOL\)
* repository role \- removed RHEL 7 support \(reached EOM\)
* zabbix\_agent role \- removed previously deprecated role

<a id="v1-3-10"></a>
## v1\.3\.10

<a id="major-changes-6"></a>
### Major Changes

* moved supported ansible\-core range to 2\.17\-2\.15

<a id="bugfixes-3"></a>
### Bugfixes

* zabbix\_api module\_utils \- removed certificate error exception\.

<a id="v1-3-9"></a>
## v1\.3\.9

<a id="major-changes-7"></a>
### Major Changes

* agent role \- added Zabbix 7\.0 support
* repository role \- added Zabbix 7\.0 support

<a id="v1-3-8"></a>
## v1\.3\.8

<a id="major-changes-8"></a>
### Major Changes

* agent role \- added default variables for agent2 plugins
* agent role \- added mssql agent2 plugin
* agent role \- added session name prefix to plugin certificate filenames on target devices
* agent role \- changed raspberry pi check to ansible\_lsb
* molecule \- updated agent2\_cert scenario for plugin testing
* molecule \- updated platforms with ubuntu24\.04
* repository role \- added ubuntu24\.04 support

<a id="v1-3-7"></a>
## v1\.3\.7

<a id="major-changes-9"></a>
### Major Changes

* agent role \- added minor version for debian\-like distributions

<a id="bugfixes-4"></a>
### Bugfixes

* fixed readme\.md links

<a id="v1-3-6"></a>
## v1\.3\.6

<a id="major-changes-10"></a>
### Major Changes

* repository role \- added sslverify option

<a id="bugfixes-5"></a>
### Bugfixes

* agent role \- changed system home folder of zabbix user for rhel\-like os
* lint fixes
* molecule default scenario fixes

<a id="v1-3-5"></a>
## v1\.3\.5

<a id="major-changes-11"></a>
### Major Changes

* event update with message added to modules
* rulebook and playbook examples for Zabbix \- EDA sequence

<a id="v1-3-4"></a>
## v1\.3\.4

<a id="major-changes-12"></a>
### Major Changes

* repository role \- added raspberry pi support

<a id="bugfixes-6"></a>
### Bugfixes

* agent role \- fixed role dependency for ansible\-core 2\.13

<a id="v1-3-3"></a>
## v1\.3\.3

<a id="major-changes-13"></a>
### Major Changes

* repository role \- added 6\.5 version
* repository role \- added aarch support for multiple distros
* repository role \- increased repository priority defaults
* repository role \- moved and updated os version assert

<a id="v1-3-2"></a>
## v1\.3\.2

<a id="major-changes-14"></a>
### Major Changes

* repository role \- removed \"allow\_insecure\" option from deb822

<a id="bugfixes-7"></a>
### Bugfixes

* agent role \- removed wildcards from agent\_disable\_repository for yum
* repository role \- added purge for Debian os family and rescue tasks to resolve repository conflict
* repository role \- fixed priority handling for yum

<a id="v1-3-1"></a>
## v1\.3\.1

<a id="bugfixes-8"></a>
### Bugfixes

* repository role \- fixed repository conflict with official release package repo by removing it\.

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="major-changes-15"></a>
### Major Changes

* agent role \- apt cache update from package state task to <em class="title-reference">repository</em> role
* agent role \- decomposed repository tasks to separate dependent role
* repository role \- added dependent role for repository customization

<a id="bugfixes-9"></a>
### Bugfixes

* agent role \- fixed repository mirror

<a id="v1-2-5"></a>
## v1\.2\.5

<a id="bugfixes-10"></a>
### Bugfixes

* host role \- fixed psk generation skip

<a id="v1-2-4"></a>
## v1\.2\.4

<a id="bugfixes-11"></a>
### Bugfixes

* host role \- fixed defaults of psk variables for independent role runs

<a id="v1-2-3"></a>
## v1\.2\.3

<a id="bugfixes-12"></a>
### Bugfixes

* host role \- fixed token auth for api tasks

<a id="v1-2-2"></a>
## v1\.2\.2

<a id="major-changes-16"></a>
### Major Changes

* agent role \- <em class="title-reference">agent\_apply\_firewalld\_rule</em> defaults set to <em class="title-reference">false</em>

<a id="v1-2-1"></a>
## v1\.2\.1

<a id="bugfixes-13"></a>
### Bugfixes

* host role \- fixed port inheritance from agent role

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="major-changes-17"></a>
### Major Changes

* decomposed <em class="title-reference">zabbix\_agent</em> role to <em class="title-reference">agent</em> and <em class="title-reference">host</em> roles
* deprecated <em class="title-reference">zabbix\_agent</em> role
* renamed all role variables to fit var\_naming\[role\_prefix\] requirement

<a id="bugfixes-14"></a>
### Bugfixes

* agent role \- fixed custom user sequence to trigger path change when <em class="title-reference">agent\_service\_group</em> stays unmodified\.

<a id="v1-1-1"></a>
## v1\.1\.1

<a id="major-changes-18"></a>
### Major Changes

* Zabbix agent role \- added Debian 12 support

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="major-changes-19"></a>
### Major Changes

* Zabbix agent role \- added config and deploy tags
* Zabbix agent role \- added host management using Zabbix API

<a id="bugfixes-15"></a>
### Bugfixes

* removed support of EOL ansible version
* set Jinja2 dependency to \=\>3\.1\.2

<a id="new-plugins"></a>
### New Plugins

<a id="httpapi"></a>
#### Httpapi

* zabbix\.zabbix\.zabbix \- Zabbix HTTP API plugin

<a id="inventory"></a>
#### Inventory

* zabbix\.zabbix\.zabbix\_inventory \- Zabbix inventory plugin

<a id="new-modules-1"></a>
### New Modules

* zabbix\.zabbix\.zabbix\_host \- Module for creating and deleting hosts\, and updating existing ones\.
* zabbix\.zabbix\.zabbix\_hostgroup \- Module for creating and deleting host groups

<a id="v1-0-6"></a>
## v1\.0\.6

<a id="major-changes-20"></a>
### Major Changes

* Zabbix agent role \- added Debian support
* Zabbix agent role \- added SELinux policy extension for Zabbix agent2
* Zabbix agent role \- extended package deployment options with the repository\_priority and repository\_disable variables\. RedHat family only

<a id="bugfixes-16"></a>
### Bugfixes

* Zabbix agent role \- fixed default home folder path for RedHat like distributions

<a id="v1-0-5"></a>
## v1\.0\.5

<a id="major-changes-21"></a>
### Major Changes

* added <em class="title-reference">remove</em> tag to uninstall agent packages \(e\.g\. <em class="title-reference">ansible\-playbook \-i inventory play\.yml \-t remove</em>\)
* added <em class="title-reference">userparam</em> tag to manage user parameters only \(e\.g\. <em class="title-reference">ansible\-playbook \-i inventory play\.yml \-t userparam</em>\)
* added logrotate customization and extended new defaults with maxsize option\.
* added self\-managed repo mirror support
* added support of self\-managed certificates for Zabbix agent connections\.
* added support of self\-managed certificates for Zabbix agent2 plugin sessions\.
* added userparameter reload to Zabbix agent role\. It will trigger if <em class="title-reference">param\_userparamater</em> was changed and no agent restart detected\.

<a id="v1-0-4"></a>
## v1\.0\.4

<a id="major-changes-22"></a>
### Major Changes

* Zabbix agent role extended distribution support for CentOS Stream 8\,9

<a id="v1-0-3"></a>
## v1\.0\.3

<a id="major-changes-23"></a>
### Major Changes

* Zabbix agent role extended distribution support for Alma Linux 8\,9\, Rocky Linux 8\,9\, and Oracle Linux 8\,9

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="bugfixes-17"></a>
### Bugfixes

* Zabbix agent parameter fixes\.
