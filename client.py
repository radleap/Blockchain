import socket

ip_address = '192.168.0.39'
port 5005
BUFFER_SIZE = 1024 #how much data send

s = socket.socket(socket.AF_INTET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using

s.connect((ip_address,port))

s.send("Hello World!")
data = s.recv(BUFFER_SIZE)
print("Received: " + data)

s.close()
