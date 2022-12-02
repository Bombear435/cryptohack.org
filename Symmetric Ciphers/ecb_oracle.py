import requests

base_url = 'http://aes.cryptohack.org/ecb_oracle/encrypt/'

# da bytes a bytes
def encrypt_aes_ecb(msg):
    ciphertext_json = requests.get(base_url + str(msg.hex())).json()
    # json in forma {"ciphertext":"e8dfe0441f64bca83e79a3815842e11ac09c9c79734d62e597e059586512bedf"}
    ciphertext = bytes.fromhex(ciphertext_json['ciphertext'])
    return ciphertext

def find_keysize():
	prev_length = len(encrypt_aes_ecb(b'0'))
	for i in range(2, 65):
		length = len(encrypt_aes_ecb(b'0' * i))

		if abs(length - prev_length) > 1:
			return length - prev_length
	print('Errore in find_keylength')
	return 0


keysize = find_keysize()
due_keysize = keysize * 2	# alcune operazioni necessitano di questo valore
plaintext = b''
# riempio i primi 31 bytes, in modo da poter fare l'oracle su un byte alla volta
# se la flag fosse più lunga, aumenterei il padding a 3*keysize o di più se serve
for i in range(1, due_keysize):	# aggiungo un padding da 31 a 1 bytes
	pad = b'0' * (due_keysize - i)
	target = encrypt_aes_ecb(pad)

	for byte in range(256):
		byte = byte.to_bytes(length=1, byteorder="little")
		tmp = encrypt_aes_ecb(pad + plaintext + byte)
		if target[:due_keysize] == tmp[0:due_keysize]:
			plaintext += byte
			break

print(plaintext)
