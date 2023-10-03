import bcrypt

passwordd2 = '123'.encode('utf-8')
passwordd1 = '123'.encode('utf-8')

# passwordd1 = b'123'
# passwordd2 = b'123'

hsh_passwd1 = bcrypt.hashpw(passwordd1, bcrypt.gensalt())
hsh_passwd2 = bcrypt.hashpw(passwordd2, bcrypt.gensalt())

print(hsh_passwd1, hsh_passwd2, sep='\n')
