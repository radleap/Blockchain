# signatures.py
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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

	if correct:
		print("success! Good sig")
	else:
		print('ERROR! Signature is bad')
#conda create -n blockchain pip python scipy cryptography
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
