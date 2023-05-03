#!/usr/bin/env bash
podman run -d --name squid-container -e TZ="Europe/Riga" -p 3128:3128 docker.io/ubuntu/squid