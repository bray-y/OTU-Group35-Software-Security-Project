from shared.models import create_order, to_json
from crypto.rsa_utils import sign_data, encrypt_key
from crypto.aes_utils import encrypt_data
from security.audit_log import log_event
import json

order = create_order()

order_json = to_json(order)

signature = sign_data(order_json, "keys/purchaser_private.pem")

package = {
    "order": order,
    "signature": signature
}

encrypted = encrypt_data(json.dumps(package))

encrypted_key = encrypt_key(
    encrypted["session_key"],
    "keys/supervisor_public.pem"
)

message = {
    "payload": encrypted,
    "encrypted_key": encrypted_key.hex()
}

log_event("PO_CREATED", order)

print("Sent to supervisor")