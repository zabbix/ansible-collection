#!/usr/bin/env bash

yum install policycoreutils-devel
make -f /usr/share/selinux/devel/Makefile zabbix_agent_extend.pp