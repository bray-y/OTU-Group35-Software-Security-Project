from crypto.rsa_utils import verify_signature, decrypt_key, sign_data
from crypto.aes_utils import decrypt_data
from security.audit_log import log_event
import json

def process_order(message):

    session_key = decrypt_key(
        bytes.fromhex(message["encrypted_key"]),
        "keys/supervisor_private.pem"
    )

    decrypted = decrypt_data(message["payload"], session_key)

    data = json.loads(decrypted)

    valid = verify_signature(
        json.dumps(data["order"], sort_keys=True),
        data["signature"],
        "keys/purchaser_public.pem"
    )

    if not valid:
        raise Exception("Signature invalid")

    supervisor_sig = sign_data(
        json.dumps(data["order"], sort_keys=True),
        "keys/supervisor_private.pem"
    )

    log_event("PO_APPROVED", data["order"])

    return {
        "order": data["order"],
        "purchaser_sig": data["signature"],
        "supervisor_sig": supervisor_sig
    }