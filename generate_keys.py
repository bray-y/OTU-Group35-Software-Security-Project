from Crypto.PublicKey import RSA
import os

ROLES = ["purchaser", "supervisor", "purchasing"]

KEY_DIR = os.path.join(os.path.dirname(__file__), "keys")

def generate_keys():

    os.makedirs(KEY_DIR, exist_ok=True)

    for role in ROLES:

        print(f"Generating keys for {role}...")

        key = RSA.generate(2048)

        private_path = os.path.join(KEY_DIR, f"{role}_private.pem")
        public_path = os.path.join(KEY_DIR, f"{role}_public.pem")

        with open(private_path, "wb") as f:
            f.write(key.export_key())

        with open(public_path, "wb") as f:
            f.write(key.publickey().export_key())

        print(f"Saved:")
        print(private_path)
        print(public_path)

    print("\nAll keys generated successfully.")

if __name__ == "__main__":
    generate_keys()