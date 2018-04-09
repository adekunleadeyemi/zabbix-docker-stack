#!/usr/bin/python

#################################################################
#
# zabbix-docker-stats.py
#
#   A program that produces information for Zabbix to
#   process Docker container statistics.
#
# Version: 1.1
#
# Author: Richard Sedlak
# Updated: Jan Lawrence - use zabbox-docker-convert.py script to convert to bytes
#
#################################################################

import sys
import subprocess
import os
import time


def pcpu(data):
        pdata = data.split()
        pcpu_data = pdata[2].split('%')[0]
        return pcpu_data


def umem(data):
        pdata = data.split()[3]
        cmd = 'echo ' + pdata + ' | /etc/zabbix/docker-scripts/zabbix-docker-convert.py'
        value = local_run_command(cmd, "/tmp/zabbix-docker-umem-" + container + ".out")
        return value[0].strip("\n")


def lmem(data):
        pdata = data.split()[5]
        cmd = 'echo ' + pdata + ' | /etc/zabbix/docker-scripts/zabbix-docker-convert.py'
        value = local_run_command(cmd, "/tmp/zabbix-docker-lmem-" + container + ".out")
        return value[0].strip("\n")


def pmem(data):
        pdata = data.split()
        #pdata=data.split('/')[1].split()
        pmem_data = pdata[6].split('%')[0]
        return pmem_data


def inet(data):
        pdata = data.split()[7]
        cmd = 'echo ' + pdata + ' | /etc/zabbix/docker-scripts/zabbix-docker-convert.py'
        value = local_run_command(cmd, "/tmp/zabbix-docker-inet-" + container + ".out")
        return value[0].strip("\n")


def onet(data):
        pdata = data.split()[9]
        cmd = 'echo ' + pdata + ' | /etc/zabbix/docker-scripts/zabbix-docker-convert.py'
        value = local_run_command(cmd, "/tmp/zabbix-docker-onet-" + container + ".out")
        return value[0].strip("\n")


options = {
    'pcpu': pcpu,
    'umem': umem,
    'lmem': lmem,
    'pmem': pmem,
    'inet': inet,
    'onet': onet
}


def local_run_command(cmd, file):
        cmd = cmd + " | tee > " + file
        if os.path.isfile(file) is False:
                os.system(cmd)
        else:
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
                ticks = int(time.time())
                delta = ticks - mtime
                if (delta > 60):
                        os.system(cmd)

        strings = open(file, "r").readlines()
        return strings


container = sys.argv[1]
key = sys.argv[2]

cmd = "docker stats --no-stream=true " + container
strings = local_run_command(cmd, "/tmp/zabbix-docker-stats-" + container + ".out")
print options[key](strings[1])
