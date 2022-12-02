import requests, hashlib
from Crypto.Cipher import AES

with open("/home/bombear435/Desktop/password_as_keys.txt", "r") as f:
    passwords = f.read().split('\n')

base_url = 'http://aes.cryptohack.org/passwords_as_keys/'

ciphertext_json = requests.get(base_url + 'encrypt_flag/').json()
# json in forma {"ciphertext":"e8dfe0441f64bca83e79a3815842e11ac09c9c79734d62e597e059586512bedf"}
ciphertext = bytes.fromhex(ciphertext_json['ciphertext'])

for password in passwords:
    key = hashlib.md5(password.encode('utf-8')).digest()

    #plaintext_json = requests.get(base_url + '/decrypt/' + ciphertext + '/' + key.hex()).json()
    # json in forma {"ciphertext":"e8dfe0441f64bca83e79a3815842e11ac09c9c79734d62e597e059586512bedf"}
    #plaintext = bytes.fromhex(plaintext_json['plaintext']) 

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    if b'crypto{' in plaintext:
        print(password)
        print(plaintext)
