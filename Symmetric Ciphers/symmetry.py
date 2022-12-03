import requests

base_url = 'http://aes.cryptohack.org/symmetry/'

def encrypt(iv, plaintext):
    chipertext_json = requests.get(base_url + 'encrypt/' + str(plaintext) + '/' + str(iv)).json()
    return bytes.fromhex(chipertext_json['ciphertext'])    

def encrypt_flag():
    chipertext_json = requests.get(base_url + 'encrypt_flag/').json()
    return chipertext_json['ciphertext']    
 

# in OFB, encryption e decryption sono la stessa cosa
# quindi dopo aver ottenuto l'iv e la flag encryptata posso passare nuovamente nella funzione 
# di encrypt questi due parametri e ottenere il plaintext, cioé la flag
ciphertext = encrypt_flag()
iv, encrypted_flag = ciphertext[:32], ciphertext[32:]   # i primi 16 bytes sono di iv
print(encrypt(iv, encrypted_flag))
