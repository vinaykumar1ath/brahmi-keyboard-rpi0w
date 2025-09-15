#!/usr/bin/env python3
#from time import sleep
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def keypress(reg_key,mod_key=0,release=True):
    report=chr(mod_key)+NULL_CHAR+chr(reg_key)+NULL_CHAR*5
    if release:
        write_report(report)
        write_report(NULL_CHAR*8)
    else:
        write_report(report)