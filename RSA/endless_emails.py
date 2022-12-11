from Crypto.Util.number import long_to_bytes
from gmpy2 import iroot

e = 3

# avendo a disposizione 3 n e 3 ct, sapendo che e = 3, posso applicare l'Hastad broadcast attack
def hastad_broadcast_attack(n1, n2, n3, c1, c2, c3, e):
    plaintext = b''
    M = n1 * n2 * n3
    m1 = M // n1
    m2 = M // n2
    m3 = M // n3
    t1 = c1 * m1 * pow(m1, -1, n1)
    t2 = c2 * m2 * pow(m2, -1, n2)
    t3 = c3 * m3 * pow(m3, -1, n3)
    x = (t1 + t2 + t3) % M  # Chinese reminder theorem (CTR)
    m, exact = iroot(x, e) # recover m
    if exact:
        plaintext = long_to_bytes(m)
    return plaintext

def read_next(fl):
    n = fl.readline().rstrip('\n')[4:]
    fl.readline()
    ct = fl.readline().rstrip('\n')[4:]
    fl.readline()
    return int(n), int(ct)


f = open("/endless_emails.txt", "r")
modulus, ciphertexts = [], []   # riempio modulus con tutti gli n, ciphertexts con tutti i ct
n, ct = read_next(f)
modulus.append(n)
ciphertexts.append(ct)
while f.readline(): # fino a EOF
    n, ct = read_next(f)
    modulus.append(n)
    ciphertexts.append(ct)
f.close()   # ho letto dal file quello che mi serviva 

num_messages = len(modulus)
# provo tutte le combinazioni di 3 email per capire quali sono ripetute. dato che e = 3, mi servono almeno 3 email uguali
for i in range(0, num_messages - 2):
    for j in range(i + 1, num_messages - 1):
        for k in range(j + 1, num_messages):
            plaintext = hastad_broadcast_attack(modulus[i], modulus[j], modulus[k], ciphertexts[i], ciphertexts[j], ciphertexts[k], e)
            if b'crypto{' in plaintext:
                print(plaintext)
