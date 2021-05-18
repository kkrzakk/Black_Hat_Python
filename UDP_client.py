import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('target_host', help='specify target host')
parser.add_argument('target_port', type=int, help='specify target port')
args = parser.parse_args()


#create socket(obj), AF_INET(IP4), SOCK_STREAM(UDP)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#I have to bind it as it won't work without it
client.bind((args.target_host,args.target_port))

#\r\n - line termination; required byte format hence encode()
client.sendto("TEST".encode(),(args.target_host,args.target_port))

data, addr = client.recvfrom(1024)

print(data.decode())