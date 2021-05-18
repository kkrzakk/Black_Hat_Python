import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('target_host', help='specify target host')
parser.add_argument('target_port', type=int, help='specify target port')
args =parser.parse_args()

#create socket(obj), AF_INET(IP4), SOCK_STREAM(TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((args.target_host,args.target_port))

#\r\n - line termination; required byte format hence encode()
client.send("GET / HTTP/1.1\r\n\r\n".encode())

#get rid of "b'" from print
response = client.recv(1024).decode()

print(response)