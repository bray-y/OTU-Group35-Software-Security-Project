from crypto.rsa_utils import verify_signature
from security.audit_log import log_event
import json

def verify_final(package):

    order_json = json.dumps(package["order"], sort_keys=True)

    valid1 = verify_signature(
        order_json,
        package["purchaser_sig"],
        "keys/purchaser_public.pem"
    )

    valid2 = verify_signature(
        order_json,
        package["supervisor_sig"],
        "keys/supervisor_public.pem"
    )

    if valid1 and valid2:

        log_event("PO_COMPLETED", package["order"])

        print("Order fully verified")

    else:
        raise Exception("Verification failed")