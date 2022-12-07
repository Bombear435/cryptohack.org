import time, hashlib
from Crypto.Util.number import long_to_bytes
from socket import * 
import json 

serverName = 'socket.cryptohack.org'
serverPort = 13372
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((serverName, serverPort))
msg = sock.recv(100)
print(msg.decode('utf-8'))

def generate_key(time):
    current_time = time
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()

# in questo caso encryption = decryption
def encrypt(a, b): 
    ciphertext = b''
    for i in range(len(a)):
        ciphertext += bytes([a[i] ^ b[i]])
    return ciphertext.hex()

def get_ciphertext(sock):
    get_flag = {"option":"get_flag"}
    json_get_flag = (json.dumps(get_flag) + '\n').encode()
    sock.send(json_get_flag)
    json_ciphertext = sock.recv(100)
    return json.loads(json_ciphertext)['encrypted_flag']


# la flag è semplicemente xorata con lo sha256 di time.time(), possiamo quindi richiedere,
# attraverso una socket, il ciphertext e cercare negli istanti precedenti quello
# della richiesta, infine xorarlo con il ciphertext stesso
ciphertext = bytes.fromhex(get_ciphertext(sock))
curr_time = int(time.time())

for seconds_prior_now in range(15):
    analyside_time = generate_key(curr_time - seconds_prior_now)
    plaintext = bytes.fromhex(encrypt(ciphertext, analyside_time))
    if b'crypto{' in plaintext:
        print(plaintext)

sock.close()
