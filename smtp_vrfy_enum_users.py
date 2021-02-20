#!/usr/bin/python

# A small script that prompts SMTP server for the supported options in search for VRFY.

import socket
import sys
import re
from time import sleep
if len(sys.argv) != 3:
    print("Usage: smtp_vry_enum_user.py <userlist> <ip>")
    sys.exit(0)

# Read IPs from File
username_file = open(sys.argv[1])
ip = sys.argv[2]
usernames = username_file.readlines()
username_file.close()

username_found = []

print("====================================")

# Create a Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("[*] Connecting to: {}".format(ip))

# Connect
s.connect((ip.rstrip(),25))

banner = s.recv(1024)
print("[*] " + banner.rstrip())

if(banner != 0):

    for username in usernames:

        # Strip newline from Variable
        username = username.rstrip()

        print("[*] Testing User: {}".format(username))
        s.send("VRFY {}\r\n".format(username))
        result = s.recv(1024)
        print(result)
        sleep(2)
        if (re.search('220|250', result)):
            print("\33[32m[*] User Found: {}\33[0m".format(username))
            username_found.append(username)
        if (re.search('550', result)):
            print("\33[31m[*] User not found {}\33[0m".format(username))

s.close()

print("[*] ============USERNAMES FOUND============ [*]")
for username in username_found:
    print("\33[32m[+] {} \33[0m".format(username))
