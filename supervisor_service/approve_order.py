import json

from crypto.rsa_utils import decrypt_key, encrypt_key, verify_signature, sign_data
from crypto.aes_utils import decrypt_data, encrypt_data, generate_aes_key
from security.timestamp_utils import validate_timestamp, check_replay
from security.audit_log import log_event
from shared.models import to_json


with open("order_to_supervisor.json") as f:

    package = json.load(f)


aes_key = decrypt_key(package["key"], "keys/supervisor_private.pem")


order_json = decrypt_data(package["order"], aes_key)


order = json.loads(order_json)


validate_timestamp(order["timestamp"])

check_replay(order["order_id"])


if verify_signature(

    order_json,

    package["signature"],

    "keys/purchaser_public.pem"

):

    supervisor_signature = sign_data(

        order_json,

        "keys/supervisor_private.pem"

    )

    aes_key2 = generate_aes_key()

    encrypted_order = encrypt_data(order_json, aes_key2)

    encrypted_key = encrypt_key(

        aes_key2,

        "keys/purchasing_public.pem"

    )

    package2 = {

        "order": encrypted_order,

        "key": encrypted_key,

        "purchaser_signature": package["signature"],

        "supervisor_signature": supervisor_signature

    }

    with open("order_to_purchasing.json", "w") as f:

        json.dump(package2, f)


    log_event(

        "supervisor",

        "approved_order",

        order["order_id"]

    )

    print("Order approved")


else:

    print("Invalid purchaser signature")