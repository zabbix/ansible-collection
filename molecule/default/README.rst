=======================================
Install ansible and required python lib
=======================================

  python3 -m pip install ansible netaddr

-----------------------------------
test playbook with ansible-playbook
-----------------------------------

  ansible-playbook -i inventory converge.yml -l ubuntu -i all,debug,verify,report,host

-l group_name		# limit execution to hosts inside group

#### Task exection control by tags

-t all,test,host	# all - all tasks(excluding next 2, marked with never)

project tags:
	verify # zabbix_get from execution environment to target devices
	report # only with "verify" : records check status to file
	host # add host to Zabbix
	test # additional debug tasks

=======================
Role testing - Molecule
=======================

  python3 -m pip install molecule molecule-podman ansible-lint yamllint

-------------
testing suite
-------------

  yamllint .
  ansible-lint converge.yml
  molecule converge -- -l aarch --tags "all,debug,verify,report,host"
  molecule test -s agentd_psk --destroy-never   # do not destroy instance after test for debug

molecule
		list			# show environment
		create			# create testing environment from molecule.yml
		destroy			# destroy testing env
		converge		# run test on existent enve
		verify			# run verify tasks from verify.yml
		test			# full cycle + ansible-lint
		login -h hostname	# ssh to container



### Molecule tree structure:

molecule/[scenario_name]/
				molecule.yml	# main configuration, including provisioning
				prepare.yml		# tasks to prepare environment before testing
				verify.yml		# tasks to check the state of converge tasks
				converge.yml	# playbook with role to test
				inventory/
					group_vars/	# group based variable control
					host_vars/  # host based var control

-------------------------------------------------------------------------------
Running roles through multiple test scenarios:
-------------------------------------------------------------------------------
molecule test --all
molecule test -s agent2 -s agent2_cert -s agent2_psk

-------------------------------------------------------------------------------
Use different platforms preset
-------------------------------------------------------------------------------
molecue -c ".config/molecule/config.full.yml" create/converge/test

-------------------------------------------------------------------------------
Converge example for host module checks
-------------------------------------------------------------------------------
molecule converge -s agent2_cert -- -t all,host -e "agent_param_serveractive=host.containers.internal:17051 zabbix_api_host=192.168.13.90 zabbix_api_port=8070 zabbix_host_templates=[\"Linux by Zabbix agent active\"]"