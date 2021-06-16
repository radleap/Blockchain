# importing
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Environment used: conda create -n blockchain pip python scipy cryptography

# def generate_keys():
# 	private = 'aa'
# 	public = 'bb'
# 	return private,public
def generate_keys():
    ''' This function uses RSA encryption with 2048 bits'''
    private_key = rsa.generate_private_key(public_exponent = 65537, key_size = 2048)
    public_key = private_key.public_key()
    return(private_key, public_key)


# def sign(message, private):
# 	sig = 'agavraehga5e'
# 	return sig
def sign(message, private_key):
    signature = private_key.sign(message,
                                 padding.PSS(
                                 mgf = padding.MGF1(hashes.SHA256()),
                                 salt_length = padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())
    return(signature)



# def verify(message, sig, public):
# 	return False

def verify(message, signature, public_key):
    public_key = private_key.public_key() # need to refactor the argument of function and this line.
    try:
        public_key.verify(
        signature,
        message,
        padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
        return(True)
    except:
        return(False)


 #prevents it from running if loaded the module... if just invoke it as a python script will run the tests
if __name__=='__main__':
	private_key, public_key = generate_keys()
	message = b"This is a secret message"
	signature = sign(message, private_key)
	correct = verify(message, signature, public_key)

# testing the correct implementation
	if correct:
		print("Test 1: Success! Good signature!")
	else:
		print('Test 1: ERROR! Signature is bad!')
# testing the wrong signature singing a message (if someone sent us something pretending to be the correct private key)
	pr2, pu2 = generate_keys()
	sig2 = sign(message,pr2)
	correct = verify(message,sig2, public_key)
	if correct:
		print("Test 2: ERROR! Bad Signature checks out!")
	else:
		print("Test 2: Success! Bad signature detected!")
# testing a tampered message
	bad_message = message + b"Q"
	correct = verify(bad_message,signature, public_key)
	if correct:
		print("Test 3: Error! A tampered message passed that shouldn't!")
	else:
		print("Test 3: Success! Tampered message detected causing error!")


# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
