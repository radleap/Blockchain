import Txblock
import transaction
import signature
import pickle
import socket

TCP_PORT = 5004

def sendBlock(ip_address,blk):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using
    s.connect((ip_address,TCP_PORT))

    s.send(blk)
    data = s.recv(BUFFER_SIZE)
    return False



if __name__ == "__main__":
    #generating generate_keys
    pr1, pu1 = signature.generate_keys()
    pr2, pu2 = signature.generate_keys()
    pr3, pu3 = signature.generate_keys()
    #build transactions
    Tx1 = transaction.Tx()
    Tx1.add_input(pu1, 2.3)
    Tx1.add_output(pu2, 1.0)
    Tx1.add_output(pu3, 1.1)
    Tx1.sign(pr1)

    Tx2 = transaction.Tx()
    Tx2.add_input(pu3, 2.3)
    Tx2.add_input(pu2, 1.0)
    Tx2.add_output(pu1, 3.1)
    Tx2.sign(pr2)
    Tx2.sign(pr3)
    #adding transactions to block
    B1 = Txblock.TxBlock(None)
    B1.addTx(Tx1)
    B1.addTx(Tx2)

    sendBlock('localhost',B1) # use internal IP addresss



# ip_address = '192.168.0.39'
# port 5005
# BUFFER_SIZE = 1024 #how much data send
#
# s = socket.socket(socket.AF_INTET,socket.SOCK_STREAM) # AF_INET using IPV4, can use 6... SOC_STREAM = TCP using
#
# s.connect((ip_address,port))
#
# s.send("Hello World!")
# data = s.recv(BUFFER_SIZE)
# print("Received: " + data)
#
# s.close()
