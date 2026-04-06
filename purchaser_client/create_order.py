from shared.models import create_order, to_json
from crypto.rsa_utils import sign_data, encrypt_key
from crypto.aes_utils import encrypt_data, generate_aes_key
from security.audit_log import log_event
import json

print("[STATUS] Preparing and signing order...")

order = create_order()

order_json = to_json(order)

signature = sign_data(order_json, "keys/purchaser_private.pem")

aes_key = generate_aes_key()

encrypted_order = encrypt_data(order_json, aes_key)

encrypted_key = encrypt_key(aes_key, "keys/supervisor_public.pem")

package = {
    "order": encrypted_order,
    "key": encrypted_key,
    "signature": signature
}

with open("order_to_supervisor.json", "w") as f:
    json.dump(package, f)

log_event("purchaser", "created_order", order["order_id"])

print("[STATUS] Order sent to supervisor")