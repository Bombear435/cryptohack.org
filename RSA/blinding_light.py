from socket import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json

serverName = 'socket.cryptohack.org'
serverPort = 13376
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((serverName, serverPort))
msg = sock.recv(100)
print(msg.decode('utf-8'))

def get_pubkey(sock):
    json_request = (json.dumps({"option": "get_pubkey"}) + '\n').encode()
    sock.send(json_request)
    pubkey_json = json.loads(sock.recv(1024))
    n = int(pubkey_json['N'], 16)
    e = int(pubkey_json['e'], 16)
    return n, e

# da msg = int a signature = int;   non puoi passare admin_token come msg
def get_signing(sock, msg):
    msg = long_to_bytes(msg).hex()
    json_request = (json.dumps({"option": "sign","msg":msg}) + '\n').encode()
    sock.send(json_request)
    sign_json = json.loads(sock.recv(2048))
    signature = int(sign_json['signature'], 16)
    return signature

# da msg = hex, sign = int a ciphertext = str
def verify_signing(sock, msg, sign):
    sign = long_to_bytes(sign).hex()
    json_request = (json.dumps({"option": "verify","msg":msg,"signature":sign}) + '\n').encode()
    sock.send(json_request)
    secret_json = json.loads(sock.recv(1024))
    ciphertext = secret_json['response']
    return ciphertext


# il server non esegue hasing prima di applicare la signature. possiamo effettuare un blinding attack per far
# firmare al server un qualsiasi messaggio arbitrario, come "admin=True". per farlo occore calcolare 
# M'=r^(e)*m mod N                      r lo scelgo io, e,N li ottengo con get_pubkey
# S' = (M')^d mod N = r*m^(d) mod N     faccio signare al server M'
# S = S' / r = m^(d) mod N              divido per l'r che ho scelto
# m = m^(d)^(e) mod N                  inverto utilizzando il public exponent
m = b"admin=True"
n, e = get_pubkey(sock)
r = 2                                       # scelto a piacere
M = (pow(r, e) * bytes_to_long(m)) % n      # M' = r^(e)*M mod N
SS = get_signing(sock, M)                   # S' = (M')^d mod N = r*M^(d) mod N
S = (SS // r) % n                           # S = S' / r mod N = M^(d) mod N   
flag = verify_signing(sock, m.hex(), S)     # m = M^(d)^(e) mod N
print(flag)

sock.close()
