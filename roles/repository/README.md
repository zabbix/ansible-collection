Zabbix repository role
=================

This is the dependent role. It is initiated automatically for roles, that require Zabbix repository.
But You can use it separately to configure Zabbix repository on target devices.
Currently, the following OS of target machines are supported:
- Redhat 7, 8, 9
- Oracle Linux 8, 9
- Alma Linux 8, 9
- Rocky Linux 8, 9
- CentOS Stream 8, 9
- Ubuntu 18.04, 20.04, 22.04
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
  * [License](#license)

<!--te-->


Requirements
------------
This role uses official Zabbix packages and repository for component installation. Target machines require direct or [**HTTP proxy**](#playbook-9) internet access to Zabbix repository [**repo.zabbix.com**](https://repo.zabbix.com).

For self-hosted repository mirrors, override URL for [`repository_url`](#role-variables) variable.

Tasks require `superuser` privileges (sudo).

Ansible core >= 2.13

Zabbix agent role relies on [**Jinja2**](https://pypi.org/project/Jinja2/) heavily and requires version >= 3.1.2

You can install required Python libraries on the control node as follows:

```bash
python3 -m pip install "Jinja2>=3.1.2"
```

Or using `requirements.txt` file in the role folder:

```bash
python3 -m pip install -r requirements.txt
```

Check the [**Python documentation**](https://docs.python.org/3/installing/index.html) for more details on Python modules installation.


Role variables
--------------

**Note that dependent roles inherits variables from the initiator role. Check initiator role meta file for details.**

***If this roles is used as dependent, default values are overriden!***

| Variable | Type | Default | Description |
|--|--|--|--|
| repository_version | `string` | 6.0 | The major version of Zabbix. Defaults to the latest LTS.
| repository_state | `string` | present | The state of the repository. Use 'present' to ensure repository presence. And 'absent' to remove the repository.
| repository_http_proxy | `string` || Defines HTTP proxy address for the packager.
| repository_https_proxy | `string` || Defines HTTPS proxy address for the packager.
| repository_url | `string` | "https://repo.zabbix.com/" | Defines repository mirror URL. You can override it to use self-hosted Zabbix repo mirror.
| repository_priority | `int` | 98 | **For RedHat family OS only.** Sets the priority of the Zabbix repository. Expects integer values from 1 to 99. Covers the cases with interfering packages from central distribution repositories.

Tags
-----

The **repository role** share two tags with the **agent role** and other **initiator roles**:
  - remove
  - deploy

Note, that passing `remove` tag to playbook with **initiator role** will remove repository too. 

License
-------

Ansible Zabbix collection is released under the GNU General Public License (GPL) version 2. The formal terms of the GPL can be found at http://www.fsf.org/licenses/.