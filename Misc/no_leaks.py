from socket import *
import json, base64

serverName = 'socket.cryptohack.org'
serverPort = 13370
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((serverName, serverPort))
msg = sock.recv(100)
print(msg.decode('utf-8'))

def inizializza_candidates(plain_len):
    candidates, tmp = [], []
    for i in range(128):    # le flag standard usano solo i primi 128 bytes
        tmp.append(i)
    candidates.append(tmp)
    return candidates * plain_len

def get_ciphertext(sock):
    ciphertext = -1
    while ciphertext == -1:
        json_request = (json.dumps({"msg": "request"}) + '\n').encode()
        sock.send(json_request)
        json_ciphertext = json.loads(sock.recv(1024))
        try:
            ciphertext = base64.b64decode(json_ciphertext['ciphertext'])
        except:
            pass
    return ciphertext

def remove_char_from_list(lst, char):
    if char in lst:
        lst = [el for el in lst if el != char]
    return lst


# l'idea è che il server controlla se ogni byte inviato sia diverso dal byte originario. quindi quando un 
# ciphertext viene richiesto si è sicuri che ad ogni posizione i, il byte presente non è quello corretto.
# sapendo questo, creo una lista in cui mappo ogni byte ad ogni posizione, presenti nei ciphertext ricevuti
# per tante volte quante servono a rimanere solo con un byte possibile per posizione
plaintext_len = len(get_ciphertext(sock))
candidates = inizializza_candidates(plaintext_len)
for i in range(5000):   # 5000 è anche troppo
    ciphertext = get_ciphertext(sock)
    for i in range(plaintext_len):
        candidates[i] = remove_char_from_list(candidates[i], ciphertext[i])
# candidates = [[99], [114], [121], [112], [116], [111], [123], [117], [110], [114], [52], [110], [100], [48], [109], [95], [48], [55], [112], [125]]

plaintext = ''
for candidate in candidates:
    plaintext += chr(candidate[0])
print(plaintext)

sock.close()
