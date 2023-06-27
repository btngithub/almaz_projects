from paramiko import SSHClient, AutoAddPolicy

hostname = input("Specify server name\n")
user = input("Specify user name\n")
passs = input("Specify password for ssh\n")

client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect(hostname, username=user, password=passs)
ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(
    "wget -q -O /tmp/agent.sh https://bashupload.com/ulq7c/W1rW-.sh &&\n\
    chmod +x /tmp/agent.sh &&\n\
    bash /tmp/agent.sh > /tmp/agent_installation_logs 2>&1 &&\n\
    rm -f /tmp/agent.sh"
)
client.close()