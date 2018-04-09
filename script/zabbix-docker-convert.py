#!/usr/bin/python

#################################################################
#
# zabbix-docker-convert-py
#
#   A program that converts between K,M,G,T.
#
# Version: 1.1
#
# Author: Richard Sedlak
# Updated By: Janine Lawrence - use regex to correctly parse
#
#################################################################

import sys
import re


def B(b):
        return int(float(b))


def KB(b):
        return int(float(b) * 1024)


def MB(b):
        return int(float(b) * 1024 * 1024)


def GB(b):
        return int(float(b) * 1024 * 1024 * 1024)


def TB(b):
        return int(float(b) * 1024 * 1024 * 1024 * 1024)


options = {
    'k': KB,
    'K': KB,
    'm': MB,
    'M': MB,
    'g': GB,
    'G': GB,
    't': TB,
    'T': TB,
    'b': B,
    'B': B
}

#
# First read from stdin
#
lines = sys.stdin.readlines(81)

if not lines:
    print "0"
else:
    regex = re.compile(r'(?P<numbers>\d*\.?\d*)(?P<denom>.*)')
    tokens = regex.search(lines[0])

    c = tokens.group('denom')[0]

    print options[c](tokens.group('numbers'))
