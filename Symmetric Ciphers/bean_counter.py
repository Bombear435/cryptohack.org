import requests

base_url = 'http://aes.cryptohack.org/bean_counter/'

def equal_length_xor(string1, string2):
	return bytes([x ^ y for x,y in zip(string1,string2)])

def encrypt():
    chipertext_json = requests.get(base_url + 'encrypt/').json()
    return bytes.fromhex(chipertext_json['encrypted'])    


# la CTR encrynption è implementata male e la keystream è sempre la stessa. posso allora ricavare 
# la keystream usata conoscendo il primo blocco di plaintext e il risultato del suo xor con il
#  keystream. sapendo che l'immagine ha estensione png, so che inizia con i magic bytes propri dei png
png_magic_bytes = bytes.fromhex('89504E470D0A1A0A0000000D49484452') # primo blocco di plaintext
keysize = 16
encrypted_image = encrypt()
keystream = equal_length_xor(png_magic_bytes, encrypted_image[:keysize])

image_bytes = b''
for i in range(0, len(encrypted_image), keysize):
    image_bytes += equal_length_xor(keystream, encrypted_image[i:i+keysize])

with open("bean_counter.png", "wb") as f:
    f.write(image_bytes)
