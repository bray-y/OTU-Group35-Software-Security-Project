# Secure Purchase Order (SPO) System
Software and Computer Security
- Group 35 - CRN 75327

## Overview
The **Secure Purchase Order (SPO) System** is a cryptographically secure workflow designed to protect the creation, approval, and verification of purchase orders within an organization.

The system applies modern security principles to ensure:
- Confidentiality of sensitive purchasing data
- Integrity of purchase order information
- Authentication of system participants
- Non-repudiation of approvals
- Protection against replay and tampering attacks

The system simulates a real-world enterprise approval process involving three roles:
- **Purchaser** – creates and signs purchase orders
- **Supervisor** – reviews and approves purchase orders
- **Purchasing Department** – verifies approved orders before processing

## Security Features
The system uses a hybrid cryptographic architecture combining symmetric and asymmetric encryption.

| Security Property  | Implementation |
| ------------- | ------------- |
| Authentication | RSA digital signatures |
| Confidentiality | AES-256 encryption |
| Integrity | SHA-256 hashing |
| Non-repudiation | RSA signed transactions |
| Replay attack prevention | timestamps + order ID tracking |
| Secure key exchange | RSA encrypted AES keys |
| Audit logging | transaction logs |

## System Architecture
The project is divided into modular components responsible for specific functionality.
```
spo-system/
│
├── purchaser_client/
│   └── create_order.py
│
├── supervisor_service/
│   └── approve_order.py
│
├── purchasing_service/
│   └── verify_order.py
│
├── crypto/
│   ├── rsa_utils.py
│   └── aes_utils.py
│
├── security/
│   ├── auth.py
│   ├── timestamp_utils.py
│   └── audit_log.py
│
├── shared/
│   └── models.py
│
├── security_tests/ 
│   ├── run_all_tests.py
│   ├── tamper_test.py
│   ├── replay_test.py
│   ├── integrity_test.py
│   ├── signature_failure_test.py
│   ├── replay_detector.py
│   ├── reset_outputs.py
│   └── outputs/
│
├── keys/
│
├── generate_keys.py
├── requirements.txt
└── audit_log.txt
```
## Installation
### 1. Clone Repository
```bash
git clone https://github.com/bray-y/OTU-Group35-Software-Security-Project.git
cd OTU-Group35-Software-Security-Project
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
## How to Run the System
### Step 1 – Generate RSA Keys
```bash
python generate_keys.py
```
This creates RSA pairs for:
- purchaser
- supervisor
- purchasing department
The keys are stored in the ```keys``` folder

### Step 2 - Create Purchase Order
```bash
python -m purchaser_client.create_order
```
- creates purchase order
- generates timestamp
- signs order
- encrypts order
- sends order to supervisor

### Step 3 - Supervisor Approval
```bash
python -m supervisor_service.approve_order
```
- decrypts purchase order
- verifies purchaser signature
- checks timestamp validity
- signs approved order
- encrypts order for purchasing department

### Step 4 - Final Verification
```bash
python -m purchasing_service.verify_order
```
- decrypts order
- verifies both signatures
- logs successful transaction

## Security Testing (Attack Simulations)
The system includes automated security tests that simulate real-world attacks.
### Run All Tests (Recommended)
```bash
python -m security_tests.run_all_tests
```
## Implemented Attack Tests

### 1. Tampering Attack
Modifies encrypted order data
- Expected result: ```Signature verification failed```

### What the attack does

The test:

```bash
data["order"]["ciphertext"] = "tampereddata"
```
This modifies the encrypted order data after it was signed.

This simulates:
- A malicious attacker intercepting the message
- Changing its contents before it reaches the supervisor

### 2. Replay Attack
Reuses a previously processed order
- Expected result: ```Duplicate order detected```

### What the attack does

The test:

```bash
shutil.copy("order_to_purchasing.json", "replay_order.json")
```
Then processes the same order twice.

This simulates:

- An attacker re-sending a valid transaction
- Attempting duplicate purchases or fraud

### 3. Integrity Attack
Modifies order fields (e.g., quantity)
- Expected result: ```Invalid purchaser signature```

### What the attack does

The test:

```bash
package["order"]["quantity"] = 999
```
This modifies a valid order field (not ciphertext).

This simulates:

- Insider attack
- Data manipulation after decryption
- Changing order details (e.g., price, quantity)

### 4. Signature Forgery Test
Uses invalid signature data
- Expected result: ```Signature valid: False```

### What the attack does

The test:
```bash
fake_data = "fake order"
sig = "deadbeef"
```
This simulates:
- Forged signature
- Attacker pretending to be a valid user

## Example Audit Log Entry
```bash
2026-04-05 20:15:10 | purchaser | created_order | 12345
2026-04-05 20:15:15 | supervisor | approved_order | 12345
2026-04-05 20:15:20 | purchasing | verified_order | 12345
```
Provides:

- Traceability
- Accountability
- Non-repudiation
