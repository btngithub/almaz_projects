# almaz_and_alexei_projects

**Ansible/playbooks/**

**_Put_server_on_Zabbix_monitoring.yaml_**

Copies Zabbix agent on a server, installs it, copies templated config file and enabless Zabbix service

**_ipv6_disable_and_reboot_if_needed.yaml_**

Checks if ipv6 is enabled, if it is, disables it and reboots the server, if disabled, does nothing


**Ansible/Roles/**

**_Post_deployment_configuration_**

Role configures newly deployed server and does next:
1. Sets hostname
2. Sets root password
3. Adds custom Linux repo
4. Updates packages
5. Formats second disk, creates and adjusts new user for backups, gets through LVM settings and mounts the file system to the backup catalog
6. Adds a script to the crontab
7. Setups Zabbix monitoring

**Bash/**

**_Backup_files.sh_**

Script to perform a backup (full on increment) of a remote folder using rsync, has Help page


**_Logs_cleanup.sh_**

Script to cleanup old logs of the backup application, uses regular expressions


**_Zabbix_agent.sh_**

Script which updates old version of Zabbix agent, server is readded to the new Zabbix server

**Python/**

**_Remote_backup_agent_installation.py_**

Remotly installs a backup application using paramiko module


**_Web_server_check_and_email.py_**

Checks if specified web site is reachable and if not sends an e-mail. (Used local test SMTP server)
