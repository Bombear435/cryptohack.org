from datetime import datetime, timedelta
import requests

base_url = 'http://aes.cryptohack.org/flipping_cookie/'

def get_cookie():
    cookie_json = requests.get(base_url + 'get_cookie/').json()
    return bytes.fromhex(cookie_json['cookie'])

def check_admin(cookie, iv):
    flag_json = requests.get(base_url + 'check_admin/' + cookie.hex() + '/' + iv.hex()).json()
    return flag_json['flag']

def equal_length_xor(string1, string2):
	return bytes([x ^ y for x,y in zip(string1,string2)])


ciphertext = get_cookie()
iv, cookie_encrypted = ciphertext[:16], ciphertext[16:]

expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
plain_cookie = f"admin=False;expiry={expires_at}".encode()
target_cookie =  f"admin=True;expiry={expires_at}".encode()

# ottengo bit flipping facendo lo xor tra il cookie originale, quello desiderato e l'iv
tampered_iv = equal_length_xor(plain_cookie, equal_length_xor(target_cookie, iv))

print(check_admin(cookie_encrypted, tampered_iv))
