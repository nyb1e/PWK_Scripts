#!/usr/bin/python

# A small script that prompts SMTP server for the supported options in search for VRFY.

import socket
import sys
import re
from time import sleep
if len(sys.argv) != 2:
    print("Usage: smtp_scan_vry.py <ip_list>")
    sys.exit(0)

# Read IPs from File
ip_file = open(sys.argv[1])
ips = ip_file.readlines()
ip_file.close()

supports_vrfy = []

for ip in ips:

    # Strip newline from Variable
    ip = ip.rstrip()

    print("====================================")

    # Create a Socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    print("[*] Connecting to: {}".format(ip))

    # Connect
    s.connect((ip.rstrip(),25))

    banner = s.recv(1024)
    print("[*] " + banner.rstrip())

    # Ask Server for supported Commands
    if(banner != 0):
        print("[*] Scanning for VRFY Option")
        s.send('HELP\r\n')
        result = s.recv(1024)

        # Check if VRFY is supported
        if (re.search('VRFY',result)):
            print("\33[32m[*] Server Supports VRFY\33[0m")
            supports_vrfy.append(ip)
        elif (re.search("Error",result)):
            print("\33[31m[!] Server does not support VRFY\33[0m")
        else:
            print("\33[31m[!] No Reponse from Server\33[0m")
    s.close()

print("[*] ============VRFY SUPPORTING SERVERS============ [*]")
for ip in supports_vrfy:
    print("\33[32m[+] {} \33[0m".format(ip))
