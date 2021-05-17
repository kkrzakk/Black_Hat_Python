import socket

target_host="google.com"
target_port=80

#create socket(obj), AF_INET(IP4), SOCK_STREAM(UDP)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#I have to bind it as it won't work without it
client.bind((target_host,target_port))

#\r\n - line termination; required byte format hence encode()
client.sendto("TEST".encode(),(target_host,target_port))

data, addr = client.recvfrom(1024)

print(data)
print(addr)