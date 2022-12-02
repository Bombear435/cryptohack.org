import requests
from Crypto.Cipher import AES

base_url = 'http://aes.cryptohack.org/ecbcbcwtf/'

# da hex a bytes
def decrypt_aes_ecb(msg):
    decrypted_msg_json = requests.get(base_url + 'decrypt/' + str(msg)).json()
    # json in forma {"plaintext":"e8dfe0441f64bca83e79a3815842e11ac09c9c79734d62e597e059586512bedf"}
    decrypted_msg = bytes.fromhex(decrypted_msg_json['plaintext'])
    return decrypted_msg

# da bytes a bytes
def equal_length_xor(string1, string2):
	return bytes([x ^ y for x,y in zip(string1,string2)])

ciphertext_json = requests.get(base_url + 'encrypt_flag/').json()
# json in forma {"ciphertext":"e8dfe0441f64bca83e79a3815842e11ac09c9c79734d62e597e059586512bedf"}
ciphertext = bytes.fromhex(ciphertext_json['ciphertext'])
iv, encrypted_flag = ciphertext[:AES.block_size], ciphertext[AES.block_size:]

last_block = iv
plaintext = b''
for i in range(0, len(encrypted_flag), AES.block_size):
    current_block = encrypted_flag[i:i+AES.block_size]
    decrypted_block = decrypt_aes_ecb(current_block.hex())
    plaintext += equal_length_xor(decrypted_block, last_block)
    last_block = current_block

print(plaintext)
