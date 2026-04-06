import json

from crypto.rsa_utils import decrypt_key, verify_signature
from crypto.aes_utils import decrypt_data
from security.audit_log import log_event
from security.timestamp_utils import validate_timestamp
from shared.models import to_json


with open("order_to_purchasing.json") as f:
    package = json.load(f)


aes_key = decrypt_key(
    package["key"],
    "keys/purchasing_private.pem"
)

order_json = decrypt_data(package["order"], aes_key)

order = json.loads(order_json)

validate_timestamp(order["timestamp"])

valid1 = verify_signature(
    order_json,
    package["purchaser_signature"],
    "keys/purchaser_public.pem"
)


valid2 = verify_signature(
    order_json,
    package["supervisor_signature"],
    "keys/supervisor_public.pem"
)


if valid1 and valid2:
    log_event(
        "purchasing",
        "verified_order",
        order["order_id"]
    )

    print("Order fully verified")

else:
    print("Signature verification failed")