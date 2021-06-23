# Environment used: conda create -n blockchain pip python scipy cryptography
# cryptography version 3.4.7, python version 3.9.5
# Development of code in "Transaction Implementation.ipynb"


# importing
import signature

class Tx:
    inputs = None #input addresses
    outputs = None #output addresses and amounts
    sigs = None # list of signatures
    reqd = None # required signatures that are not inputs

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
    def add_input(self, from_address, amount):
        '''takes a sending public_key and amount'''
        self.inputs.append((from_address,amount))

    def add_output(self, to_address, amount):
        '''takes a receiving public_key and amount'''
        self.outputs.append((to_address,amount))

    def add_required(self, address): # public_key is the address input here
        '''takes a required third-party public_key'''
        self.reqd.append(address)

    def sign(self, private_key):
        '''The signing user, signs using private_key creating signature'''
        message = self.__gather()
        new_sig = signature.sign(message, private_key) # returns signed message
        self.sigs.append(new_sig)

    def __gather(self):
        '''internally used method, not callable. Used for digitally signed message'''
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return(data)

    def __repr__(self):
        '''This is called when converted to a string or  printed showing all transaction objects'''
        repstr = "INPUTS:\n"
        for from_address, amount in self.inputs:
            repstr = repstr + str(amount) + " from " + str(from_address) + "\n"
        repstr = repstr + "OUTPUTS:\n"
        for to_address, amount in self.inputs:
            repstr = repstr + str(amount) + " to " + str(to_address) + "\n"
        repstr = repstr + "REQD:\n"
        for address in self.reqd:
            repstr = repstr + str(address) + "\n"
        repstr = repstr + "SIGS:\n"
        for s in self.sigs:
            repstr = repstr + str(s) + "\n"
        repstr = repstr + "END\n"
        return(repstr)

    def is_valid(self):
        '''
        Validates all signatures using the data and public keys
        Validates that no negative transactions
        Validate that total amount_in greater than total amount_out
        Validate tampering not occur
        '''
        total_in = 0
        total_out = 0
        message = self.__gather()
        # verifying all input signatures, have been signed/received
        for public_key, amount in self.inputs:
            found = False
            for s in self.sigs:
                if signature.verify(message, s, public_key):
                    found = True
            if not found:
                return False
            if amount < 0: #this checks for only positive input amounts
                return False
            total_in = total_in + amount
        for public_key in self.reqd:
            found = False
            for s in self.sigs:
                if signature.verify(message, s, public_key):
                    found = True
            if not found:
                return False
        for addr, amount in self.outputs: #this checks for only negative input amounts
            if amount < 0:
                return False
            total_out = total_out + amount
        # if total_out > total_in: #total in not less than total out -- moved to miner checking
        #     return False
        return True

#################### testing ######################

 #prevents it from running if loaded the module... if just invoke it as a python script will run the tests
if __name__ == "__main__":
    pr1, pu1 = signature.generate_keys()
    pr2, pu2 = signature.generate_keys()
    pr3, pu3 = signature.generate_keys()
    pr4, pu4 = signature.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1,1)
    Tx1.add_output(pu2,1) #sending coin to pu2
    Tx1.sign(pr1) # signing with private key so valid

    if Tx1.is_valid():
        print("Success! Tx is valid!")
    else:
        print("Error! Tx is invalid!")

    Tx2 = Tx()
    Tx2.add_input(pu1,2)
    Tx2.add_output(pu2,1)
    Tx2.add_output(pu3,1)
    Tx2.sign(pr1) # using the private key of #1 since is the input

    # Tx3 is a test for escrow transaction
    Tx3 = Tx()
    Tx3.add_input(pu3,1.2) # shouldnt have more output than input.
    Tx3.add_output(pu1,1.1) #mining and mining rewards, transaction fee usually goes to miner.
    Tx3.add_required(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)


    for t in [Tx1,Tx2,Tx3]:
        if t.is_valid():
            print(f"Success! Tx is valid!")
        else:
            print(f"Error! Tx is invalid!")

    # wrong signatures, should be pu1 signing
    Tx4 = Tx()
    Tx4.add_input(pu1,1) #user 1 is sending 1 count to Tx4
    Tx4.add_output(pu2,1)
    Tx4.sign(pr2) #but here signed with the wrong private_key

    # Escrow Tx transaction not signed by the arbiter
    Tx5 = Tx()
    Tx5.add_input(pu3,1.2)
    Tx5.add_output(pu1,1.1)
    Tx5.add_required(pu4)
    Tx5.sign(pr3)
    # Tx5.sign(pr4)

    # Two input addres, signed by one only
    Tx6 = Tx()
    Tx6.add_input(pu3,1)
    Tx6.add_input(pu4,0.1)
    Tx6.add_output(pu1,1.1)
    Tx6.sign(pr3) #Tx8.sign(pr4) # is missing so should be invalid

    # Outputs exceed the Inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1,1)
    Tx7.add_output(pu2,2)
    Tx7.sign(pr4)

    #negative value tests
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1,-1)
    Tx8.sign(pr2)

    # Modified after Transaction signed
    Tx9 = Tx()
    Tx9.add_input(pu1,1)
    Tx9.add_output(pu2,1) #sending coin to pu2
    Tx9.sign(pr1) # signing with private key so valid
    Tx9.outputs[0]=(pu3,1) #instead of pu2 which was [(pu2,1)]


    for t in [Tx4, Tx5, Tx6, Tx7, Tx8,Tx9]:
        if t.is_valid():
            print(f"Error! Tx  is valid!")
        else:
            print(f"Success! Tx  is invalid!")

####################### resources ########################
