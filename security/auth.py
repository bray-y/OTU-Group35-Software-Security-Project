from crypto.rsa_utils import verify_signature

def authenticate(data, signature, public_key):

    return verify_signature(data, signature, public_key)