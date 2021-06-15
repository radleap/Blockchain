# signatures.py
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# def generate_keys():
# 	private = 'aa'
# 	public = 'bb'
# 	return private,public
def generate_keys():
    key = rsa.generate_private_key(public_exponent = 65537, key_size = 2048)

    private_key = key.private_bytes(serialization.Encoding.PEM,
                                    serialization.PrivateFormat.TraditionalOpenSSL,
                                    serialization.NoEncryption()).decode('utf-8')

    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH,
                                               serialization.PublicFormat.OpenSSH)
    return(private_key, public_key)


def sign(message, private):
	sig = 'agavraehga5e'
	return sig
def verify(message, sig, public):
	return False

 #prevents it from running if loaded the module... if just invoke it as a python script will run the tests
if __name__=='__main__':
	pr, pu = generate_keys()
	message = b"This is a secret message"
	sig = sign(message, pr)
	correct = verify(message, sig, pu)

	if correct:
		print("success! Good sig")
	else:
		print('ERROR! Signature is bad')
#conda create -n blockchain pip python scipy cryptography
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
