#!/usr/bin/env python2.7
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))

# max backlog connections set to 5

server.listen(5)
print("[*] Kusterning on %s:%d" % (bind_ip, bind_port))

# client-handling thread


def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)

    print("[*] Received: %s" % request)

    # send back a packet
    client_socket.send("ACK!")
    client_socket.close()


while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    # client thread to handle data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

