from Crypto.Cipher import AES
import base64

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    key = base64.b64decode(key)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(enc)

ciphertext = "V3Vqirostg6qW26sle5mnyrwEYSrteN6oHkilO50e9dFkN+0JhC3yu0LcQNw/hXU"
key = "r7y1dhmTvjQrcra7A1UQFw=="

print decrypt(key, ciphertext)
