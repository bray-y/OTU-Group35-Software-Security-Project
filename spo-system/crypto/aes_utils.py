from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_data(plaintext: str):
    key = get_random_bytes(32)  # AES-256
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

    return {
        "ciphertext": base64.b64encode(ct_bytes).decode(),
        "iv": base64.b64encode(cipher.iv).decode(),
        "session_key": key  # raw bytes to be encrypted with RSA
    }

def decrypt_data(enc_dict, key: bytes):
    ct = base64.b64decode(enc_dict["ciphertext"])
    iv = base64.b64decode(enc_dict["iv"])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()