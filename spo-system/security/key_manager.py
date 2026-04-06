from crypto.rsa_utils import generate_keys

roles = [
    "purchaser",
    "supervisor",
    "dept"
]

for r in roles:
    generate_keys(r)

print("Keys generated")