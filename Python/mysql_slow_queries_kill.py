#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import os.path
import subprocess
import re
import urllib
import urllib.request
import urllib.parse
import socket
import datetime
import logging

logging.basicConfig(filename='/var/log/querykiller.json', level=logging.INFO, format='%(message)s')

mysql_bin = '/usr/bin/mysql'
if os.path.exists('/usr/bin/mysql_orig'):
    mysql_bin = '/usr/bin/mysql_orig'

def slackpost(text, channel):
    url = channel
    data = json.dumps({'text': text}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    try:
        req = urllib.request.Request(url, data, headers)
        resp = urllib.request.urlopen(req)
        response = resp.read()
    except Exception as em:
        print('EXCEPTION: ' + str(em))

def running():
    global mysql_bin
    cmd = [mysql_bin, '--defaults-file=/root/.my.cnf', '-e', 'set names utf8;show full processlist;']
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        lines = output.decode('utf-8', errors='ignore').split("\n")
        names = None
        for line in lines:
            if len(line) == 0:
                continue
            fields = line.split("\t")
            if names is None:
                names = fields
            else:
                yield dict(zip(names, fields))
    except subprocess.CalledProcessError:
        return


config = {}
channels_file = open('/root/.killq',)
config = json.load(channels_file)

parser = argparse.ArgumentParser(description="show and kill slow queries")
parser.add_argument('-k', '--kill', dest='kill', action='store_const', const=True, default=False, help='Allow killing of slow queries')
parser.add_argument('-u', '--user', dest='user', default=None, help='Limit queries to user')
parser.add_argument('-t', '--timeout', dest='timeout', type=int, default=None, help='Time limit (queries running longer than N seconds)')
parser.add_argument('-c', '--channel', dest='channel', default=None, help='Post killing logs to slack channel')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True, default=False, help='Increase verbosity')

args = parser.parse_args()

user_re=None
if args.user is not None:
    user_re=re.compile(args.user)

if args.channel and args.channel[0] == '#':
    args.channel = re.sub('#', '', args.channel)

kill=[]
killpost=[]

for row in running():
    if row['Command'] not in ['Query', 'Execute']:
        continue
    if user_re is not None:
        if user_re.search(row['User']) is None:
            continue
    if row['Time'] == 'NULL':
        continue
    if args.timeout is not None:
        if (int(row['Time']) < args.timeout):
            continue
    msg='{}s {} {}'.format(row['Time'], row['User'], row['Info']).replace(r"\n", " ")
    msg =' '.join(msg.split())
    msg =' '.join(msg.split())
    if args.verbose or not args.kill:
        print(msg)
    if args.kill:
        kill.append(row['Id'])
        killpost.append(msg)

if len(kill) > 0:
    subprocess.check_call(['/usr/bin/mysqladmin', '--defaults-file=/root/.my.cnf', 'kill', ','.join(kill)])
    with open('/var/log/querykiller.json', 'at') as fp:
        for post in killpost:
            log_line = {
            '@timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': post,
            'syslog.program' : 'querykiller'
            }
            logging.info(json.dumps(log_line))
    if args.channel is not None:
        for query in killpost:
            if len(query) > 3925:
                slackpost("Next long MYSQL query is killed on: " "\n`" + socket.gethostname() + "`" + "\n```" + query[:3925] + "\n```", channel=config["channels"][args.channel])
            else:
                slackpost("Next long MYSQL query is killed on: " "\n`" + socket.gethostname() + "`" + "\n```" + query + "\n```", channel=config["channels"][args.channel])
    else:
        print("Killed timed out queries:\n\n" + "\n".join(killpost) + "\n")
