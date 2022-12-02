import requests

base_url = 'http://aes.cryptohack.org/block_cipher_starter/'

encrypted_flag_json = requests.get(base_url + 'encrypt_flag/').json()
# json in forma {"ciphertext":"e8dfe0441f64bca83e79a3815842e11ac09c9c79734d62e597e059586512bedf"}
encrypted_flag = encrypted_flag_json['ciphertext']  # hex value

plaintext_json = requests.get(base_url + 'decrypt/' + encrypted_flag).json()
# json in forma {'plaintext': '63727970746f7b626c30636b5f633170683372355f3472335f663435375f217d'}
plaintext = bytes.fromhex(plaintext_json['plaintext'])

print(plaintext)
