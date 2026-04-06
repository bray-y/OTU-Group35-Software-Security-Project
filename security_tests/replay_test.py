import json
import shutil
import os

from crypto.rsa_utils import decrypt_key, verify_signature
from crypto.aes_utils import decrypt_data
from security_tests.replay_detector import is_duplicate, mark_processed, reset

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT = os.path.join(BASE_DIR, "order_to_purchasing.json")
OUTPUT = os.path.join(BASE_DIR, "security_tests", "outputs", "replay_order.json")


def process(file_path):
    print("🔍 Verifying order...")

    with open(file_path) as f:
        package = json.load(f)

    # Decrypt AES key
    aes_key = decrypt_key(
        package["key"],
        os.path.join(BASE_DIR, "keys", "purchasing_private.pem")
    )

    # Decrypt order
    order_json = decrypt_data(package["order"], aes_key)
    order = json.loads(order_json)

    # Verify BOTH signatures
    purchaser_sig = package["purchaser_signature"]
    supervisor_sig = package["supervisor_signature"]

    valid1 = verify_signature(
        order_json,
        purchaser_sig,
        os.path.join(BASE_DIR, "keys", "purchaser_public.pem")
    )

    valid2 = verify_signature(
        order_json,
        supervisor_sig,
        os.path.join(BASE_DIR, "keys", "supervisor_public.pem")
    )

    if not (valid1 and valid2):
        print("[FAILED] Signature verification failed")
        return

    # Replay detection
    order_id = order.get("order_id")

    if is_duplicate(order_id):
        print("Duplicate order detected (PASS)")
        return

    mark_processed(order_id)
    print("First processing OK")


def run():
    os.makedirs(os.path.join(BASE_DIR, "security_tests", "outputs"), exist_ok=True)

    # Copy original file to simulate replay
    shutil.copy(INPUT, OUTPUT)

    print("[STATUS] Replay file ready")

    # Reset tracking for clean demo
    reset()

    # Run twice to simulate replay
    process(OUTPUT)
    process(OUTPUT)


if __name__ == "__main__":
    run()