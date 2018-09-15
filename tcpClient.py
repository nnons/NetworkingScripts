#!/usr/bin/env python2.7
import socket
import pprint
target_host = "www.google.com"
target_port = 80
message = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
# socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
client.connect((target_host, target_port))

# send data

client.send(message.encode('utf-8'))

# receive data
response = client.recv(4096)

pprint.pprint(response)

