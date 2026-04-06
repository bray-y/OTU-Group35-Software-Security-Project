from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

def generate_keys(name):
    key = RSA.generate(2048)

    with open(f"keys/{name}_private.pem", "wb") as f:
        f.write(key.export_key())

    with open(f"keys/{name}_public.pem", "wb") as f:
        f.write(key.publickey().export_key())


def sign_data(data, private_key_path):
    key = RSA.import_key(open(private_key_path).read())

    h = SHA256.new(data.encode())

    signature = pkcs1_15.new(key).sign(h)

    return base64.b64encode(signature).decode()


def verify_signature(data, signature, public_key_path):
    key = RSA.import_key(open(public_key_path).read())

    h = SHA256.new(data.encode())

    try:
        pkcs1_15.new(key).verify(h, base64.b64decode(signature))
        return True
    except:
        return False


def encrypt_key(session_key, public_key_path):
    key = RSA.import_key(open(public_key_path).read())

    cipher = PKCS1_OAEP.new(key)

    return cipher.encrypt(session_key)


def decrypt_key(encrypted_key, private_key_path):
    key = RSA.import_key(open(private_key_path).read())

    cipher = PKCS1_OAEP.new(key)

    return cipher.decrypt(encrypted_key)