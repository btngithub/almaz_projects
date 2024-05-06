**mysql_slow_queries_kill.py**

Checks local MySQL instance for slow queries taking more x time, kills if there is any, writes JSON logs and sends a notification to a Slack server using a webhook. 
Uses bash shell to execute the script with various available options

**_Remote_backup_agent_installation.py_**

Remotly installs a backup application using paramiko module


**_Web_server_check_and_email.py_**

Checks if specified web site is reachable and if not sends an e-mail. (Used local test SMTP server)
