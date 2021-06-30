
import socket
import Txblock
TCP_PORT = 5004

def RecvObj(ip_address):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using
    s.bind((ip_address,TCP_PORT))
    s.listen()
    new_sock,addr = s.accept()
    return(new_sock.recv())

if __name__ == "__main__":
    newB =RecvObj('localhost')
    print(newB.data[1])
    print(newB.data[2])
    #check
    if newB.is_valid():
        print("Success! Tx is valid.")
    else:
        print("Error! Tx NOT valid.")
    # checking some transactions
    #input
    if newB.data[0].inputs[0][1] == 2.3:
        print("Success! Input value matches.")
    else:
        print("Error! Wrong input value for block 1, Tx 1")
    #output
    if newB.data[0].outputs[1][1] == 1.1:
        print("Success! Output value matches.")
    else:
        print("Error! Wrong Output value for block 1, Tx 1")

    # checking some transactions
    if newB.data[1].inputs[0][1] == 2.3:
        print("Success! Input value matches.")
    else:
        print("Error! Wrong input value for block 1, Tx 1")

    # checking some transactions
    #input
    if newB.data[1].inputs[1][1] == 1.0:
        print("Success! Input value matches.")
    else:
        print("Error! Wrong input value for block 1, Tx 2")
    if newB.data[1].outputs[0][1] == 3.1:
        print("Success! Output value matches.")
    else:
        print("Error! Wrong Output value for block 1, Tx 2")


# import socket
#
# ip_address = '192.168.0.39'
# port 5005
#
# s = socket.socket(socket.AF_INTET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using
# s.bind((ip_address,port))
#
# s.listen()
# for q in range(10):
#     # rd = readable socket new conn/data, wt = writeable sockets, errors = error state socet
#     rd, wt, err = select.select([s],[],[s],6) # 6 second time out (input sockets, output sockets, errors sockets)
#     if s in rd:
#         conn,addr = s.accept() #Blocking, determined not to be killed, waits until connection
#         while True:
#             data = conn.recv()
#             if not data:
#                 break
#             print("Received: " + data)
#             conn.send(data)
# s.close()






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
