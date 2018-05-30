import socket
import threading

bind_ip = str(input("Enter TCP Source IP : "))
bind_port = str(input("Enter Source PORT : "))

# Set up server object

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

# Listen on the server for requests

server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

def handle_client(client_socket):
    # Grab the request
    request = client_socket.recv(1024)

    print("[*] Received: %s" % request)
    # Send back the ACK handshake
    client_socket.send("ACK")
    client_socket.close()

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from : %s:%d" % (addr[0], addr[1])) 
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
