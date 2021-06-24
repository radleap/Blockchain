zeros = []
for i in range(5):
  zeros.append('\x00')
print(zeros)


print(chr(234))
print(ord(('m')))
print(chr(109))


import random # do not use this in cryptography. Not secure. By seeing can reproduce it.
#import os  #os.urandom # use this for cryptographic uses

print(random.randint(8,24))
