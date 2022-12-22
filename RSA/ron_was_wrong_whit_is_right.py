from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from math import gcd
from itertools import combinations

# leggo il public exponent di tutte le 50 parti
base_file_name = '/home/bombear435/Downloads/keys_and_messages/'
exps, modulus, cts, pems = [], [], [], []

for i in range(1, 51):
    key_file = base_file_name + str(i) + '.pem'
    ct_file = base_file_name + str(i) + '.ciphertext'
    pubkey = RSA.importKey(open(key_file).read())  # è un RSA object che contiene (e, n)
    exps.append(pubkey.e)
    modulus.append(pubkey.n)
    cts.append(open(ct_file).read())
    pems.append(open(key_file).read())

# guardo quali coppie sono composte da fattori uguali e trovo solo una coppia. salvo le info interessanti
same_p_module = []
for coppia in list(combinations(modulus, 2)):
    tmp = gcd(coppia[0], coppia[1])
    if tmp != 1 and tmp not in coppia:      # algoritmo migliorabile
        index1 = modulus.index(coppia[0])
        index2 = modulus.index(coppia[1])
        same_p_module.append((exps[index1], coppia[0], cts[index1], pems[index1]))
        same_p_module.append((exps[index2], coppia[1], cts[index2], pems[index2]))
        p = tmp

# conoscendo un fattore e il modulo posso trovare d e decryptare
for e, n, ct, pem in same_p_module:
    ct = bytes.fromhex(ct)
    q = n // p
    phi = (p - 1) * (q - 1)
    d = pow(e , -1, phi)
    key = RSA.construct((n, e, d))
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ct)
    print(plaintext)
