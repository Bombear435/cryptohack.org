from socket import *
from Crypto.Util.number import long_to_bytes
import json

serverName = 'socket.cryptohack.org'
serverPort = 13374
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((serverName, serverPort))
msg = sock.recv(100)
print(msg.decode('utf-8'))

def get_secret(sock):
    json_request = (json.dumps({"option": "get_secret"}) + '\n').encode()
    sock.send(json_request)
    secret_json = json.loads(sock.recv(1024))
    ciphertext = int(secret_json['secret'], 16)
    return ciphertext

def get_signing(sock, mm):
    json_request = (json.dumps({"option": "sign","msg":hex(mm)}) + '\n').encode()
    sock.send(json_request)
    sign_json = json.loads(sock.recv(1024))
    signature = int(sign_json['signature'], 16)
    return signature


# ct = get_secret = pow(flag, e, n)
# flag = sign = pow(ct, d, n)
# la funzione di signing è mal implementata e decrypta qualsiasi messaggio riceva. non serve neanche la pubkey
ct = get_secret(sock)
flag = long_to_bytes(get_signing(sock, ct))
print(flag)

sock.close()
