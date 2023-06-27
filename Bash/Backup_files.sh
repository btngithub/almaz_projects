#!/bin/bash

#HELP
while getopts ":h" option; do
   case $option in
      h) # display Help
echo
echo "           ##########################################HELP#################################################"
echo
echo "                                                Backup script"
echo "           1. Пользователь, сервер и папка для бэкапа указываются в теле скрипта"
echo "           2. Для 'Full backup', используйте флаг 'full'"
echo
echo "           ###############################################################################################"
         exit;;
   esac
done

#type of the backup
echo choose type of the backup: f or i
read type

#MAIN
user=xxx
server=xxx
remote_folder=/tmp/logs/
local_full_folder=/tmp/Full/
local_increment_folder=/tmp/Inc/

if [ $type == f ]; then
        rsync -havzPI --stats --backup --suffix=_old --backup-dir="/tmp/Full(old)" $user@$server:$remote_folder $local_full_folder
elif [ $type == i ]; then
        rsync -havzP --stats --backup --suffix=_old --backup-dir="/tmp/Inc(old)" $user@$server:$remote_folder $local_increment_folder
else
        echo "Wrong option"

fi