#!/bin/bash

# vstorage логи
cd /var/log/vstorage/acrgw77/

rm -f vstorage-mount.?.blog
rm -f vstorage-mount.log.?.zst

# остальное
cd /var/log/
rm -f vzctl.log*
rm -f vstorage-ui-agent/messages.log*
rm -f vz-events.log*
rm -f vstorage/iscsi/*
rm -f vstorage-ui-agent/uwsgi.log*
rm -f ploop.log*