# Environment used: conda create -n blockchain pip python scipy cryptography
# cryptography version 3.4.7, python version 3.9.5
# Development of code in "Transaction Implementation.ipynb"


# importing
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.exceptions import InvalidSignature
import pickle
from cryptography.hazmat.primitives import serialization
from blockchain import CBlock
import signatures
import transaction

class TxBlock(CBlock):
    def __init__(self,previousBlock):
        pass
    def addTx(self, Tx_in):
        pass
    def is_valid(self):
        return False

#################### testing ######################

 #prevents it from running if loaded the module... if just invoke it as a python script will run the tests
if __name__ == "__main__":
    pr1,pu1 = signatures.generate_keys()
    pr2,pu2 = signatures.generate_keys()
    pr3,pu3 = signatures.generate_keys()

    Tx1 = transaction.Tx()
    Tx1.add_input(pu1,1)
    Tx1.add_output(pu2,1)
    Tx1.sign(pr1)

    print(Tx1.is_valid())

    def key_serialization(key):
        pem = key.private_bytes()

    # ###### saving via pickle of the public key
    # addrfile = open("public.dat","wb")
    # pickle.dump(pu1,addrfile)
    # addrfile.close()

    ###### saving via pickle of the transaction block
    savefile = open("tx.dat","wb")
    pickle.dump(Tx1,savefile)
    savefile.close()
    # #### loading and testing the public key using the signature.verify()
    # loadfile = open("public.dat","rb")
    # new_pu = pickle.load(loadfile)
    # print(signatures.verify(message,sig,new_pu))
    # loadfile.close()

    #### loading and testing the transaction using the transaction.is_valid()
    loadfile = open("tx.dat","rb")
    nexTx = pickle.load(loadfile)
    print(nexTx.is_valid())
    loadfile.close()

####################### resources ########################
