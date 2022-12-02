import requests

base_url = 'http://aes.cryptohack.org/lazy_cbc/'

def encrypt(plaintext):
    chipertext_json = requests.get(base_url + 'encrypt/' + plaintext).json()
    return chipertext_json['ciphertext']    # tengo gli hex

def decrypt(ciphertext):
    chipertext_json = requests.get(base_url + 'receive/' + ciphertext).json()
    ciphertext = chipertext_json['error']   
    return ciphertext[19:]  # tengo solo la parte di errore utile

def get_flag(key):
    flag_json = requests.get(base_url + 'get_flag/' + key).json()
    return flag_json


keysize = 16
# se poni il primo blocco del plaintext a 0, verrà effettuato l'ecb encryption dell'iv, cioè della key
# il blocco di ciphertext ottenuto può essere poi messo in decryption come secondo blocco, preceduto da un blocco di 0
# in questo modo avviene l'ecb decryption e si ottiene la key
key_ecb_encrypted = encrypt('00' * keysize)
key = decrypt('00' * keysize + str(key_ecb_encrypted))[32:]
print(bytes.fromhex(get_flag(key)['plaintext']))
