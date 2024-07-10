##### Test playbook with ansible-playbook
```
ansible-playbook -i inventory converge.yml -l ubuntu -i all,verify,report
```
#### Project tags:

- `verify` # zabbix_get from execution environment to target devices
- `report` # only with "verify" : records check status to file
- `test` # additional debug tasks

### Role testing - Molecule install
```
python3 -m pip uninstall molecule-podman
python3 -m pip install ansible-core molecule molecule-plugins[podman] ansible-lint yamllint
```
#### Testing suite:

- `yamllint roles`
- `ansible-lint roles`
- `molecule test`  # will run default scenario sequence
- `molecule test -s agentd_psk --destroy-never`   # do not destroy instance after test for debug

*Molecule* commands:
- `list`		# show environment
- `create`		# create testing environment from molecule.yml
- `destroy`		# destroy testing env
- `converge`	# run test on existent enve
- `verify`		# run verify tasks from verify.yml
- `test`		# full cycle + ansible-lint
- `login -h hostname`	# ssh to container

### Molecule tree structure:


- molecule/[scenario_name]/
	- molecule.yml	# main configuration, including provisioning
	- prepare.yml		# tasks to prepare environment before testing
	- verify.yml		# tasks to check the state of converge tasks
	- converge.yml	# playbook with role to test
	-  inventory/
		- group_vars/	# group based variable control
		- host_vars/  # host based var control
- .config/molecule/ # path to container(platform) list for `molecule.yml`

#### Running roles through multiple test scenarios:

```molecule test --all```
```molecule test -s agent2 -s agent2_cert -s agent2_psk```

##### Use different platforms presets:

- `molecule -c ".config/molecule/config.debian.yml" create #/converge/test`
- `molecule -c ".config/molecule/config.rhel.9.yml" create #/converge/test`
- `molecule -c ".config/molecule/config.rhel.8.yml" create #/converge/test`  # use ansible 2.16 or lower
