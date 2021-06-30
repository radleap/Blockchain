import socket

ip_address = '192.168.0.39'
port 5005

s = socket.socket(socket.AF_INTET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using
s.bind((ip_address,port))

s.listen()
for q in range(10):
    # rd = readable socket new conn/data, wt = writeable sockets, errors = error state socet
    rd, wt, err = select.select([s],[],[s],6) # 6 second time out (input sockets, output sockets, errors sockets)
    if s in rd:
        conn,addr = s.accept() #Blocking, determined not to be killed, waits until connection
        while True:
            data = conn.recv()
            if not data:
                break
            print("Received: " + data)
            conn.send(data)
s.close()






# # an echo server, accept 10 connections only
#     for q in range(10):
#         conn,addr = s.accept() #Blocking, determined not to be killed, waits until connection
#         while True:
#             data = conn.recv()
#             if not data:
#                 break
#             print("Received: " + data)
#             conn.send(data)
#     s.close()
