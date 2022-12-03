import requests

base_url = 'http://aes.cryptohack.org/triple_des/'

def encrypt(key, plaintext):
    chipertext_json = requests.get(base_url + 'encrypt/' + str(key) + '/' + str(plaintext)).json()
    return bytes.fromhex(chipertext_json['ciphertext'])    

def encrypt_flag(key):
    chipertext_json = requests.get(base_url + 'encrypt_flag/' + str(key)).json()
    return chipertext_json['ciphertext']    
 
# è possibile ottenere la flag utilizzando una weak key, ossia una chiave tale per cui l'encryption di un
# ciphertext encryptato con la stessa chiave, restituisce il plaintext. compongo i 16 bytes di weak key
# componendo due weak keys da 8 bytes listate su wikipedia
# tldr due DES weak keys concatenate danno una DES3 weak key
weak_key = '01' * 8 + 'fe' * 8  # 16 bytes weak key

ciphertext = encrypt_flag(weak_key)
print(encrypt(weak_key, ciphertext))
