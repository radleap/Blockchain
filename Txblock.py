# Environment used: conda create -n blockchain pip python scipy cryptography
# cryptography version 3.4.7, python version 3.9.5
# Development of code in "Blockchain Transaction Ledger.ipynb"


# importing
import pickle
import time
import random
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import blockchain
import signature
import transaction

reward = 25.0
leading_zeros = 2
next_char_limit = 20

class TxBlock(blockchain.CBlock):
    nonce = None
    def __init__(self,previousBlock):
        super(TxBlock, self).__init__([],previousBlock)  #reference to the parent class of TXBlock which is CBlock; initialize data as []
        self.nonce = "AAAAA"
    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def __count_totals(self):   #this is an internal only function. Not callable from outside the TxBlock Class
        total_in = 0
        total_out = 0
        for tx in self.data:
            for from_address,amount in tx.inputs:
                total_in = total_in + amount
            for to_address, amount in tx.outputs:
                total_out = total_out + amount
        return(total_in, total_out)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        # checking transactions are valid
        for tx in self.data:
            if not tx.is_valid():
                return(False)
        # checking the sum of transaction in and out
        total_in, total_out = self.__count_totals()
        if total_out - total_in - reward > 0.00000000001: # handling floatin point error, also limit transaction size
            return(False)
        return(True)
    #defining Nonce
    def good_nonce(self):
        h1 = bytes(str(self.data), 'utf-8')
        h2 = bytes(str(self.previousHash), 'utf-8')
        h3 = bytes(str(self.nonce),'utf-8')

        digest = hashes.Hash(hashes.SHA256())
        digest.update(h1)
        digest.update(h2)
        digest.update(h3)
        this_hash = digest.finalize()
        # print(str(this_hash[:leading_zeros]) +" -- " str(bytes(''.join()))
        return(this_hash[:leading_zeros] == bytes(''.join(['\x4f' for i in range(leading_zeros)]),'utf-8')) # '\00' is a zero hexidecimal character
        # if this_hash[:leading_zeros] != bytes(''.join(['\x4f' for i in range(leading_zeros)]),'utf-8'): # '\00' is a zero hexidecimal character
        #     return(False)
        # return(int(this_hash[leading_zeros]) < next_char_limit)

    def find_nonce(self):
        '''generate random nonces and check if the nonce is good using good_nonce'''
        for i in range(1000000):
            self.nonce = ''.join(
                        [chr(random.randint(0,255)) for i in range(10*leading_zeros)])
            if self.good_nonce():
                return(self.nonce)
        return(None)

#################### testing ######################

 #prevents it from running if loaded the module... if just invoke it as a python script will run the tests
if __name__ == "__main__":
    #################### testing ######################
    pr1,pu1 = signature.generate_keys()
    pr2,pu2 = signature.generate_keys()
    pr3,pu3 = signature.generate_keys()

    Tx1 = transaction.Tx()
    Tx1.add_input(pu1,1)
    Tx1.add_output(pu2,1)
    Tx1.sign(pr1)

    ########### Test 1 #############
    if Tx1.is_valid():
        print("Test 1: Success! Tx1 is valid")

    ###### saving via pickle of the transaction block
    savefile = open("data/tx.dat","wb")
    pickle.dump(Tx1,savefile)
    savefile.close()

    ########### Test 2 #############
    # loading and testing the transaction using the transaction.is_valid()
    loadfile = open("data/tx.dat","rb")
    newTx = pickle.load(loadfile)
    if newTx.is_valid():
        print("Test 2: Success! Loaded newTx is valid")
    loadfile.close()

    root = TxBlock(None) # cretae a root block, no parent
    root.addTx(Tx1)

    Tx2 = transaction.Tx() #transactions in root block
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    B1 = TxBlock(root) # next block and transactions after root
    Tx3 = transaction.Tx()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu2, 1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)

    Tx4 = transaction.Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_required(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)

    ########### Test 3 #############
    start = time.time() # grabbing CPU time
    print("Nonce: ",B1.find_nonce())
    elapsed = time.time() - start
    print("Check: Elapse time: " + str(elapsed) + " seconds.")
    if elapsed < 60:
        print("Test 3: Error! Mining is too fast.")

    ########### Test 4 #############
    if B1.good_nonce():
        print("Test 4: Success! Nonce is good!")
    else:
        print("Test 4: Error! Bad Nonce")


    savefile = open("data/block.dat","wb")
    pickle.dump(B1,savefile)
    savefile.close()

    loadfile = open("data/block.dat","rb")
    load_B1 = pickle.load(loadfile)
    load_B1.is_valid()

    # print(bytes(str(load_B1.data), 'utf-8')) # this prints all the data

    ##### THESE ARE TESTS FOR BLOCKS #########
    Print("------ THESE ARE TESTS FOR BLOCKS -----")
    for b in [root, B1, load_B1, load_B1.previousBlock]:
        if b.is_valid():
            print("Success! Valid Block")
        else:
            print("Error! Bad Block")

    # this allows the network to check
    if B1.good_nonce():
        print("Success! Nonce is good after save and load!")
    else:
        print("Error! Bad Nonce after loading.")

    # This should throw an error - transaction output exceeds input
    B2 = TxBlock(B1)
    Tx5 = transaction.Tx()
    Tx5.add_input(pu3,1)
    Tx5.add_output(pu1, 100) #inputs exceed outputs
    Tx5.sign(pr3)
    B2.addTx(Tx5)
    #print(Tx5.is_valid())

    # tampering with Block 1
    load_B1.previousBlock.addTx(Tx4) # tampering with block b1, using a repeat of Tx4
    for b in [B2, load_B1]:
        if b.is_valid():
            print("ERROR! Bad block verified.")
        else:
            print("Success! Bad blocks detected!")

    '''test mining rewards and transaction fee'''
    pr4,pu4 = signature.generate_keys() # for the miner
    B3 = TxBlock(B2)
    B3.addTx(Tx2) # these are suigned, and miner not need the priavte keys
    B3.addTx(Tx3)
    B3.addTx(Tx4)
    Tx6 = transaction.Tx()
    Tx6.add_output(pu4,25) # adds own transaction to earn the requred
    B3.addTx(Tx6) # would be falgged as invalid, due to our in/out rules.
    if B3.is_valid():
        print("Success! Block reward succeeds")
    else:
        print("Error! Block reward fail.")

    '''Transaction fees test'''
    B4 = TxBlock(B3)
    B4.addTx(Tx2) # these are signed, and miner not need the priavte keys
    B4.addTx(Tx3)
    B4.addTx(Tx4)
    Tx7 = transaction.Tx()
    Tx7.add_output(pu4,25.2) # takes the extra points/transaction fees from each, here .2
    B4.addTx(Tx7) # would be falgged as invalid, due to our in/out rules.
    if B4.is_valid():
        print("Success! Transaction Fees succeeds")
    else:
        print("Error! Transaction Fees fail.")

    '''Greedy Miner'''
    B5 = TxBlock(B4)
    B5.addTx(Tx2) # these are signed, and miner not need the priavte keys
    B5.addTx(Tx3)
    B5.addTx(Tx4)
    Tx8 = transaction.Tx()
    Tx8.add_output(pu4,26) # takes the extra points/transaction fees from each, here .2
    B5.addTx(Tx8) # would be falgged as invalid, due to our in/out rules.
    if not B5.is_valid():
        print("Success! Greedy miner detected!")
    else:
        print("Error! Greedy miner NOT detected.")
###################### resources ########################
