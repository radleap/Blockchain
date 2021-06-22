# Environment used: conda create -n blockchain pip python scipy cryptography
# cryptography version 3.4.7, python version 3.9.5
# Development of code in "Digital Signature and Asymmetric Cryptography Implementation.ipynb"


# importing
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

def generate_keys():
    '''
    This function uses RSA encryption with 2048 bits to create public and private key
    Serializes the public key for pickle saving
    Returns two objects, the public key and the private key
    '''
    private_key = rsa.generate_private_key(
                        public_exponent = 65537,
                        key_size = 2048)
    public_key = private_key.public_key()
    #serializing for saving/loading of the public key
    pu_ser = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return(private_key, pu_ser)


def sign(message, private_key):
    '''
    Takes the private key and a message to give a digital signature
    Returns a digital signature
    '''
    message = bytes(str(message), 'utf-8')
    signature = private_key.sign(message,
                                 padding.PSS(
                                 mgf = padding.MGF1(hashes.SHA256()),
                                 salt_length = padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())
    return(signature)


def verify(message, signature, pu_ser):
    '''
    Takes a message, digital_signature, and public key to verify message from the sender untampered.
    Deserializes the public key that is loaded
    Returns True if verified, else False
    '''
    public_key = serialization.load_pem_public_key(pu_ser) #loading the serialized pem public key

    message = bytes(str(message), 'utf-8') # if message bytes converts to a string and then to bytes
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
    except InvalidSignature:
        return(False)
    except:
        print("Error executing public key verify")

#################### testing ######################

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

####################### resources ########################
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
# public_key = private_key.public_key() # need to refactor the argument of function and this line.
