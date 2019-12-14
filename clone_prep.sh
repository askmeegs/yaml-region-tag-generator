#!/bin/sh

mkdir -p /root/.ssh/
echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
echo "${KNOWN_HOSTS}" > /root/.ssh/known_hosts
chmod 600 /root/.ssh/id_rsa
chmod 600 /root/.ssh/known_hosts
echo -e "Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile=/dev/null\n" > /root/.ssh/config