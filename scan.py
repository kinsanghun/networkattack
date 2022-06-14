import os
import platform
import time
import sys, random

from netaddr import IPNetwork
from threading import Thread
from scapy.all import *
from scapy import *
from telnetlib import IP
from scapy.layers.dns import DNS
from scapy.layers.inet import *

networkscan = list()
openport = list()


def scanner(target, port):
    alive = os.system("ping -c 1 " + str(target) + " > /dev/null")

    if alive == 0:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex((str(target), port))
        if result == 0:
            openport.append(port)
        s.close()
    return

def portscan(ip):
    print("PORTSCAN")
    ports = [20, 21, 22, 25, 53, 80, 443, 3389, 8080, 8000]

    for i in range(len(openport)):
        openport.pop()
    try:
        for port in ports:
            print(port)
            t = threading.Thread(target=scanner, args=(ip, port))
            t.setDaemon(True)
            t.start()
            t.join()

        result = f"Target {ip} Open Port is "

        for d in openport:
            result += f"{d} "
        print(result)
        return result

    except Exception as e:
        print(e)
        return str(e)

def ping_host(ip):
    current_os = 2 
    if current_os == 1:
        response = os.system("ping " + " -n 1 -w 1 " + ip)
    else:
        response = os.system("ping -c 1 " + ip + " > /dev/null")

    if response == 0:
        print("\033[35m" + ip + " is up!")
        networkscan.append(ip)
        print("\033[0m")
    else:
        return "-1"


def ping_network(network):
    networkscan = []
    threads = []

    for dst in IPNetwork(network):
        dst = str(dst)
        t = Thread(target=ping_host, args=(dst, ))
        t.start()
        threads.append(t)
        time.sleep(1)

    for t in threads:
        t.join()

    print(networkscan)

def hostscan():
    print("HOSTSCAN")
    addr = input("Input Target IP or Network : ")
    target = addr.find("/")

    if target == -1:
        print("HOST SCAN START")
        ping_host(addr)
    else:
        print("NETWORK SCAN START")
        ping_network(addr)

    return 1

def print_scanlist():
    print()
    scan_select = ""
    while scan_select != "exit":
        print("SCAN LIST")
        print("1. hostscan")
        print("2. portscan")
        scan_select = input("Select menu : ")

        if scan_select == "1":
            print()
            hostscan()

        if scan_select == "2":
            print()
            ip = input("Input target IP : ")
            portscan(ip)
