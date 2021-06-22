# Environment used: conda create -n blockchain pip python scipy cryptography
# cryptography version 3.4.7, python version 3.9.5
# Development of code in "Blockchain Transaction Ledger.ipynb"


# importing
import pickle
from cryptography.hazmat.primitives import serialization
from blockchain import CBlock
import signature
import transaction

class TxBlock(CBlock):
    def __init__(self,previousBlock):
        super(TxBlock, self).__init__([],previousBlock)  #reference to the parent class of TXBlock which is CBlock; initialize data
        pass
    def addTx(self, Tx_in):
        pass
    def is_valid(self):
        return False

#################### testing ######################

 #prevents it from running if loaded the module... if just invoke it as a python script will run the tests
if __name__ == "__main__":
    pr1,pu1 = signature.generate_keys()
    pr2,pu2 = signature.generate_keys()
    pr3,pu3 = signature.generate_keys()

    Tx1 = transaction.Tx()
    Tx1.add_input(pu1,1)
    Tx1.add_output(pu2,1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is valid")

    ###### saving via pickle of the transaction block
    savefile = open("data/tx.dat","wb")
    pickle.dump(Tx1,savefile)
    savefile.close()

    #### loading and testing the transaction using the transaction.is_valid()
    loadfile = open("data/tx.dat","rb")
    newTx = pickle.load(loadfile)
    if newTx.is_valid():
        print("Success! Loaded Tx is valid")
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
    Tx4.sign(pr2)
    Tx4.sign(pr3)
    B1.addTx(Tx4)



    savefile = open("data/block.dat","wb")
    pickle.dump(B1,savefile)
    savefile.close()

    loadfile = open("data/block.dat","rb")
    load_B1 = pickle.load(loadfile)
    load_B1.is_valid()

    for b in [root, B1, load_B1, load_B1.previousBlock]:
        if b.is_valid():
            print("Success! Valid Block")
        else:
            print("Error! Bad Block")

    B2 = TxBlock(B1)
    Tx5 = transaction.Tx()
    Tx5.add_input(pu3,1)
    Tx5.add_output(pu1, 100) #inputs exceed outputs
    Tx5.sign(pr3)

    load_B1.previousBlock.addTx(Tx4) # tampering with block b1
    for b in [B2, load_B1]:
        if b.is_valid():
            print("ERROR! Bad block verified.")
        else:
            print("Success! Bad blocks detected!")



####################### resources ########################
