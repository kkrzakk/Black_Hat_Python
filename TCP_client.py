import socket

target_host="www.google.com"
target_port=80

#create socket(obj), AF_INET(IP4), SOCK_STREAM(TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host,target_port))

#\r\n - line termination; required byte format hence encode()
client.send("GET / HTTP/1.1\r\n\r\n".encode())

response = client.recv(1024)

print(response)