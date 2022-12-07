import time, hashlib
from Crypto.Util.number import long_to_bytes

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

# la flag è semplicemente xorata con lo sha256 di time.time(), possiamo quindi richiedere 
# con "nc socket.cryptohack.org 13372" il ciphertext e cercare negli istanti precedenti quello
# della richiesta e xorarlo con il ciphertext
ciphertext = bytes.fromhex("7ce8de115f903cff8e91dac20c1844d233d78646c4267dfa88112c6d") # chiesto manualmente attraverso netcat con {"option":"get_flag"}
curr_time = int(time.time())

for seconds_prior_now in range(15):
    analyside_time = generate_key(curr_time - seconds_prior_now)
    print(bytes.fromhex(encrypt(ciphertext, analyside_time)))
