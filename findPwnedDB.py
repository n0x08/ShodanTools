#!/usr/bin/env python
# findPwnedDB.py
#
# Last update: 1/13/2020
#
# Added: 
#       CassandraDB support
#       Additional DBs
#       Docker XMR mining flags (Thanks Unit42!)
#       https://unit42.paloaltonetworks.com/graboid-first-ever-cryptojacking-worm-found-in-images-on-docker-hub/
#
# Dependencies:
# - shodan
#
# Installation:
# sudo easy_install shodan
#
# Usage:
# 1. Download a json.gz file from Shodan; either for specific DB solutions or "tag:database"
#    Example:
#       shodan download --limit -1 USA_DB country:US tag:database
#       OR
#       shodan download --limit -1 USA_DB country:US product:MongoDB
# 2. Run the tool on the file:
#        ./findPwnedDB.py USA_DB.json.gz
#
from sys import argv
import json
from shodan.helpers import iterate_files, get_ip

pwnedDBs = ['university_cybersec_experiment', 'alpine', 'How_to_restore', 'pocosow/centos:7.6.1810', 'docker.io/pocosow/centos:7.6.1810', 'hacked_by_unistellar', 'RECOVERY', 'timonmat/xmr-stak-cpu', 'arayan/monero-miner', 
'abafaeeee/monero-miner', 'docker.io/gakeaws/nginx:v2.0', 'gakeaws/nginx:v2.0', 'docker.io/gakeaws/mysql:5.6', 'gakeaws/mysql:5.6', 'docker.io/gakeaws/nginx:v8.9', 'gakeaws/nginx:v8.9',
'kannix/monero-miner', 'Warn', 'Backup1', 'Backup2', 'Backup3', 'crackit', 'trojan1', 'trojan2', 'trojan3', 'trojan4', 'Readme', 'WARNING', 'RECOVER', 
'PLEASE_READ_ME_XYZ', 'jacpos', 'jackpos', 'jackposv1', 'jackposv2', 'jackposprivate12', 'alina', 'topkek112', 'README', 'WRITE_ME', 'HACKED_BY_MARSHY', 'PLEASE_README',
'WE_HAVE_YOUR_DATA', 'your_data_has_been_backed_up', 'REQUEST_YOUR_DATA', 'DB_HAS_BEEN_DROPPED', 'Warning', 'Attention', 'Aa1_Where_is_my_data', 
'send_bitcoin_to_retrieve_the_data', 'DATA_HAS_BEEN_BACKED_UP', 'REQUEST_ME', 'CONTACTME', 'BACKUP_DB', 'db_has_been_backed_up', 
'PLEASE_READ', 'please_read', 'warning', 'DB_H4CK3D', 'CONTACTME', 'PLEASE_READ_ME', 'DB_DELETED', 'DB_DROPPED', 'PLEASEREAD', 'How_to_restore', 
'NODATA4U_SECUREYOURSHIT', 'SECUREYOURSHIT', 'pleasereadthis', 'readme', 'PLEASE_SECURE_THIS_INSTALLATION', 'ReadmePlease', 'how_to_recover',
'JUST_READ_ME', 'README_MISSING_DATABASES', 'README_YOU_DB_IS_INSECURE', 'PWNED_SECURE_YOUR_STUFF_SILLY', 'WARNING_ALERT', 'Warn',
'pleaseread']

for banner in iterate_files(argv[1:]):
    ip = get_ip(banner)
    org = banner['org']
    try:
        product = banner['product']
    except:
        pass
    try:
        if product == "MongoDB":
            data = banner['data'].replace('MongoDB Server Information\n', '').split('\n},\n')[2]
            data = json.loads(data + '}')
            for db in data['databases']:
                if db['name'] in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db['name'], product))
        elif product == "Elastic":
            data = banner['elastic']
            for db in data['indices']:
                if db in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db, product))
        elif product == "Cassandra":
            data = banner['cassandra']
            for db in data['keyspaces']:
                if db in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db, product))
        elif product == "HDFS NameNode":
            data = banner['opts']['hdfs-namenode']
            for db in data['Files']:
                if db['pathSuffix'] in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db['pathSuffix'], product))
        elif product == "CouchDB":
            data = banner['opts']['couchdb']
            for db in data['dbs']:
                if db in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db, product))
        elif product == "Redis key-value store":
            data = banner['redis']['keys']
            for db in data['data']:
                if db in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db, product))
        elif product == "Docker":
            data = banner['docker']['Containers']
            for db in data:
                if db['Image'] in pwnedDBs:
                    print('{}:{}:{}:{}'.format(ip, org, db['Image'], product))
        else:
            data = banner['product']
    except:
        pass