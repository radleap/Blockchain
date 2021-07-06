
import socket
import Txblock
import pickle

TCP_PORT = 5002
BUFFER_SIZE = 1024

def newConnection(ip_address):
    # allowing for multiple connections
    # each time connect to a client make a new socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using
    s.bind((ip_address,TCP_PORT))
    s.listen()
    return(s)

def RecvObj(socket):
    new_sock,addr = socket.accept()
    # handling datat size limits
    all_data = b''
    while True:
        data = new_sock.recv(BUFFER_SIZE)
        if not data:
            break
        else:
            all_data = all_data + data
    return(pickle.loads(all_data))

if __name__ == "__main__":
    s = newConnection('localhost')
    newB =RecvObj(s)
    print(newB.data[0])
    print(newB.data[1])
    #check
    if newB.is_valid():
        print("Success! Tx is valid.")
    else:
        print("Error! Tx NOT valid.")
    # checking some transactions
    #input and output
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
    if newB.data[1].inputs[1][1] == 1.0:
        print("Success! Input value matches.")
    else:
        print("Error! Wrong input value for block 1, Tx 2")
    if newB.data[1].outputs[0][1] == 3.1:
        print("Success! Output value matches.")
    else:
        print("Error! Wrong Output value for block 1, Tx 2")
    # newTx = RecvObj('localhost')
    # print(newTx)

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
