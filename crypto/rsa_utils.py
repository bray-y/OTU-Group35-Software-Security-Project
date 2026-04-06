from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
import base64


def load_private_key(path):

    with open(path, "rb") as f:

        return RSA.import_key(f.read())


def load_public_key(path):

    with open(path, "rb") as f:

        return RSA.import_key(f.read())


def sign_data(data, private_key_path):

    key = load_private_key(private_key_path)

    h = SHA256.new(data.encode())

    signature = pkcs1_15.new(key).sign(h)

    return base64.b64encode(signature).decode()


def verify_signature(data, signature, public_key_path):

    key = load_public_key(public_key_path)

    h = SHA256.new(data.encode())

    try:

        pkcs1_15.new(key).verify(h, base64.b64decode(signature))

        return True

    except:

        return False


def encrypt_key(aes_key, public_key_path):

    key = load_public_key(public_key_path)

    cipher = PKCS1_OAEP.new(key)

    return base64.b64encode(cipher.encrypt(aes_key)).decode()


def decrypt_key(encrypted_key, private_key_path):

    key = load_private_key(private_key_path)

    cipher = PKCS1_OAEP.new(key)

    return cipher.decrypt(base64.b64decode(encrypted_key))