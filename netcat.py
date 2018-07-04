#!/usr/bin/env python2.7
import sys
import socket
import getopt
import threading
import subprocess

"""
Replacement for netcat
"""

# Global Variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():

    print "NC Alternative"
    print "Usage: netcat.py -t target_host -p port"
    print "-l --listen          - listen on [host]:[port] \
                                for incoming connections "
    print "-e --execute=FILE    - execute the given file upon \
                                receiving a connection"
    print "-c --command         - initilize a command shell"
    print "-u --upload=DESTINATION - upon receiving connection upload a \
                                     file and write to DESTINATION"
    print
    print
    print "Examples: "
    print "netcat.py -t 192.168.0.1 -p 4444 -l -c"
    print "netcat.py -t 192.168.0.1 -p 4444 -l -u=c:\\target.exe"
    print "netcat.py -t 192.168.0.1 -p 4444 -l -e=\"cat /etc/passwd\" "
    print "echo 'ASDASD' | ./netcat.py -t 192.168.1.1 -p 135"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # Command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        # Read buffer
        buffer = sys.stdin.read()

        # Send data
        client_sender(buffer)

    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to target
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)
        while True:
            # Waiting for data
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response+=data
                if recv_len < 4096:
                    break
            print response,
            # wait for more input
            buffer = raw_input("")
            buffer += "\n"

            # send buffer
            client.send(buffer)

    except:
        print "[*] Exception! Exiting."
        client.close()


def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler,
                args=(client_socket,))
        client_thread.start()


def run_command(command):

    # trim new line
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                shell=True)
    except:
        output = "Failed to execute command. \r\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        # Read all bytes and write to dest
        file_buffer = ""

        # Read until EOF
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor, write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully save file to %s\r\n" %
                    upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" %
                    upload_destination)

    if len(execute):
        # Run cmd
        output = run_command(execute)
        client_socket.send(output)

    # Loop if command shell
    if command:
        while True:
            # Show a prompt
            client_socket.send("<MEOW:#> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            # send back
            response = run_command(cmd_buffer)
            client_socket.send(response)


main()
