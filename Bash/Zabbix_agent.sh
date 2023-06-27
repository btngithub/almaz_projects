#!/bin/bash

#STOP ON ERRORS
set -o errexit

#CHECK OLD ZABBIX AND REMOVE
if yum list installed "zabbix-agent" >/dev/null 2>&1; then
  yum remove zabbix-agent -y
fi

#ADD REPO AND INSTALL NEW ZABBIX
rpm -Uvh https://repo.zabbix.com/zabbix/6.0/rhel/8/x86_64/zabbix-release-6.0-2.el8.noarch.rpm
yum install zabbix-agent2 -y

#CONFIG ZABBIX FILES
echo 'Hostname=<используем FQDN в нижнем регистре>
Server=<FQDN прокси>
ServerActive=<FQDN прокси>
TLSConnect=psk
TLSAccept=psk
TLSPSKFile=/etc/zabbix/zabbix_agent2.key
TLSPSKIdentity=zbx-psk-autoreg
HostMetadata=<состав согласовывается с группой мониторинга>' > /etc/zabbix/zabbix_agent2.conf
echo '0b06bc24dcc89c2c5617290cc35ed5cc2d1e0f65b9831b7e6cadff502bae86ac' > /etc/zabbix/zabbix_agent2.key

#ENABLE ZABBIX SERVICE
systemctl enable zabbix-agent2 --now