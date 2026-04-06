import json
import os
from crypto.rsa_utils import verify_signature

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT = os.path.join(BASE_DIR, "order_to_supervisor.json")
OUTPUT = os.path.join(BASE_DIR, "security_tests", "outputs", "tampered_order.json")


def run():
    os.makedirs("security_tests/outputs", exist_ok=True)

    with open(INPUT) as f:
        data = json.load(f)

    # Tamper
    data["order"]["ciphertext"] = "tampereddata"

    with open(OUTPUT, "w") as f:
        json.dump(data, f, indent=4)

    print("🔧 Tampered file created")

    # Verify
    order = data["order"]
    signature = data["signature"]

    order_str = json.dumps(order, sort_keys=True)

    if not verify_signature(order_str, signature, os.path.join(BASE_DIR, "keys", "purchaser_public.pem")):
        print("Signature verification failed (PASS)")
    else:
        print("Tampering NOT detected (FAIL)")


if __name__ == "__main__":
    run()