from crypto.rsa_utils import verify_signature
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    fake_data = "fake order"
    sig = "deadbeef"

    result = verify_signature(
        fake_data,
        sig,
        os.path.join(BASE_DIR, "keys", "purchaser_public.pem")
    )

    if result is False:
        print("✅ Invalid signature rejected (PASS)")
    else:
        print("❌ Invalid signature accepted (FAIL)")


if __name__ == "__main__":
    run()