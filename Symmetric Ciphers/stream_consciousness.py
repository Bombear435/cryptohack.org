import requests

base_url = 'http://aes.cryptohack.org/stream_consciousness/'

def equal_length_xor(string1, string2):
	return bytes([x ^ y for x,y in zip(string1,string2)])

def encrypt():
    chipertext_json = requests.get(base_url + 'encrypt/').json()
    return bytes.fromhex(chipertext_json['ciphertext'])


# il CTR è mal implementato e ad ogni chiamata reinizializza il counter a 1. possiamo osservare che
# streamkey ^ pt1 = ct1
# streamkey ^ pt2 = ct2
# ct1 ^ ct2 = pt1 ^ pt2 = tmp conoscendo parte di pt1 posso ricavare pt2. 
# utilizzo il metodo cribbing, aggiornando il source code in base ai risultati del run precedente
# parto da b'crypto{'
known_plaintext = b"It can't be torn out, but it can "
ct1 = encrypt()
while True:
    ct2 = encrypt()
    tmp = equal_length_xor(ct1, ct2)
    print(equal_length_xor(known_plaintext, tmp))

"""
b"I'm unhappy, I deserve it, the fa"
b'And I shall ignore it.'
b'The terrible thing is that the pa'
b'These horses, this carriage - how'
b'What a lot of things that then se'
b"How proud and happy he'll be when"
b'Three boys running, playing at ho'
b'I shall lose everything and not g'
b'Why do they go on painting and bu'
b"I shall, I'll lose everything if "
b'What a nasty smell this paint had'
b"It can't be torn out, but it can "
b"Dolly will think that I'm leaving"
b'Perhaps he has missed the train a'
b'But I will show him.'
b'Our? Why our?'
b'Would I have believed then that I'
b"No, I'll go in to Dolly and tell "
b'As if I had any wish to be in the'
b'crypto{k3y57r34m_r3u53_15_f474l}'
b"Love, probably? They don't know h"
"""
