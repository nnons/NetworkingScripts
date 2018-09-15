#!/usr/bin/env python2.7
import socket

target_host = "127.0.0.1"
target_port = 80
message = "AAABBBCCC"
# create socket obj
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto(message.encode('utf-8'), (target_host, target_port))

# receive some data
data, addr = client.recvfrom(4096)

print(data)
