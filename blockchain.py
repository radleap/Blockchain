# Environment used: conda create -n blockchain pip python scipy cryptography
# cryptography version 3.4.7, python version 3.9.5
# Development of code in "Blockchain Implementation.ipynb"


# importing
from cryptography.hazmat.primitives import hashes

# class definition
class CBlock:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock

        if self.previousBlock == None:
            self.previousHash = None
        else:
            self.previousHash = previousBlock.computeHash() #calculating the previous hash, setting as attribute

    def computeHash(self):
        '''
        Takes this blocks data, and previous block hash
        Returns hash of combined data
        '''
        h1 = bytes(str(self.data), 'utf-8')
        h2 = bytes(str(self.previousHash), 'utf-8')

        digest = hashes.Hash(hashes.SHA256())
        digest.update(h1)
        digest.update(h2)
        hash = digest.finalize()
        return(hash)

# another class definition for B4 instance
class someClass:
    string = None
    num = 123456
    def __init__(self, mystring):
        self.string = mystring
    def __repr__(self):
        return self.string + str(self.num) # removing the ability to tamper attributes of this class

################## testing ###############
if __name__ == '__main__':
    # defining blocks
    root = CBlock('I am root', None)
    B1 = CBlock('I am a child', root)
    B2 = CBlock('I am B1s brother', root) #branching
    B3 = CBlock(12345, B1)
    B4 = CBlock(someClass('Hi there!!'), B3)
    B5 = CBlock("Top Block", B4)
    # testing that the current block's computation of the previous blocks hash matches, or gives error.
    for b in [B1,B2,B3,B4,B5]:
        if b.previousBlock.computeHash() == b.previousHash:
            print(f"Success! {b} hash is good!")
        else:
            print(f"Error! {b} hash is wrong!")

    # testing for tampering with previous data
    B3.data = 23456 # single test case
    if B4.previousBlock.computeHash() == B4.previousHash:
        print("Error! Did not detect tampering with data!")
    else:
        print("Success! Detected error in tampering!")

    # testing for tampering with previous data, within class
    B4.data.num = 999999 # single test case
    if B5.previousBlock.computeHash() == B5.previousHash:
        print("Error! Did not detect tampering with class internal data!")
    else:
        print("Success! Detected error in tampering class internal data!")

####################### resources ########################
# https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/
