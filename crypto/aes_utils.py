from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


def generate_aes_key():

    return get_random_bytes(32)


def encrypt_data(data, key):

    cipher = AES.new(key, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(data.encode())

    return {

        "ciphertext": base64.b64encode(ciphertext).decode(),

        "nonce": base64.b64encode(cipher.nonce).decode(),

        "tag": base64.b64encode(tag).decode()

    }


def decrypt_data(enc_data, key):

    cipher = AES.new(

        key,

        AES.MODE_EAX,

        nonce=base64.b64decode(enc_data["nonce"])

    )

    return cipher.decrypt_and_verify(

        base64.b64decode(enc_data["ciphertext"]),

        base64.b64decode(enc_data["tag"])

    ).decode()