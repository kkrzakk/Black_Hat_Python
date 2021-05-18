import socket
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('bind_ip', help='specify server ip')
parser.add_argument(dest='bind_port', type=int, help='specify server port')
args = parser.parse_args()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((args.bind_ip,args.bind_port))

#backlog of connections
server.listen(5)

print("[*] Listening on %s:%d"% (args.bind_ip,args.bind_port))

def handle_client(client_socket):

	request = client_socket.recv(1024).decode()

	print("[*] Received: %s"% request)

	client_socket.send("ACK".encode())

	client_socket.close()

while True:
	client, addr = server.accept()

	print("[*] Connection from: %s:%d"% (addr[0],addr[1]))

	client_handler = threading.Thread(target=handle_client,args=(client,))

	client_handler.start()