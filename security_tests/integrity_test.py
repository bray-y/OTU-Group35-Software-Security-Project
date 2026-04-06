import json
import os
from crypto.rsa_utils import verify_signature

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT = os.path.join(BASE_DIR, "order_to_supervisor.json")
OUTPUT = os.path.join(BASE_DIR, "security_tests", "outputs", "modified_order.json")


def run():
    os.makedirs("security_tests/outputs", exist_ok=True)

    with open(INPUT) as f:
        package = json.load(f)

    # Modify legit data
    package["order"]["quantity"] = 999

    with open(OUTPUT, "w") as f:
        json.dump(package, f, indent=4)

    print("⚠️ Modified file created")

    order = package["order"]
    signature = package["signature"]

    order_str = json.dumps(order, sort_keys=True)

    if not verify_signature(order_str, signature, os.path.join(BASE_DIR, "keys", "purchaser_public.pem")):
        print("Integrity attack detected (PASS)")
    else:
        print("Integrity attack NOT detected (FAIL)")


if __name__ == "__main__":
    run()