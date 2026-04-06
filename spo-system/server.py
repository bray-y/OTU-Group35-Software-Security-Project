import os, sys, json, time, uuid, sqlite3, base64
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from shared.models import to_json
from crypto.rsa_utils import sign_data, verify_signature, encrypt_key, decrypt_key
from crypto.aes_utils import encrypt_data, decrypt_data
from security.audit_log import log_event

app = Flask(__name__)
CORS(app)

DB_FILE = "spo_system.db"
TIME_WINDOW = 300  # seconds for timestamp freshness

# -------------------- DB Init --------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            payload TEXT,
            encrypted_key TEXT,
            purchaser_sig TEXT,
            supervisor_sig TEXT,
            status TEXT,
            timestamp REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------- Helpers --------------------
def current_utc_timestamp():
    return time.time()

def is_fresh_timestamp(ts):
    return abs(current_utc_timestamp() - ts) <= TIME_WINDOW

def serialize_encrypted(encrypted: dict) -> dict:
    """Convert AES encryption output to JSON-serializable strings."""
    def to_b64(val):
        if isinstance(val, bytes):
            return base64.b64encode(val).decode()
        elif isinstance(val, str):
            return val
        else:
            raise TypeError(f"Cannot serialize type {type(val)}")
    
    result = {
        "ciphertext": to_b64(encrypted["ciphertext"]),
        "session_key": to_b64(encrypted["session_key"])
    }

    # Include IV if it exists
    if "iv" in encrypted:
        result["iv"] = to_b64(encrypted["iv"])
    
    return result

def deserialize_encrypted(encrypted: dict) -> dict:
    """Convert JSON-serialized AES dict back to bytes."""
    def from_b64(val):
        if isinstance(val, str):
            try:
                return base64.b64decode(val)
            except Exception:
                return val.encode()
        return val
    result = {
        "ciphertext": from_b64(encrypted["ciphertext"]),
        "session_key": from_b64(encrypted["session_key"])
    }
    if "iv" in encrypted:
        result["iv"] = from_b64(encrypted["iv"])
    return result

# -------------------- Purchaser --------------------
@app.route("/purchaser/order", methods=["POST"])
def create_order():
    order = {
        "item": request.json.get("item"),
        "quantity": request.json.get("quantity"),
        "price": request.json.get("price"),
        "department": request.json.get("department"),
        "justification": request.json.get("justification"),
        "order_id": str(uuid.uuid4()),
        "timestamp": current_utc_timestamp()
    }
    order_json = to_json(order)
    signature = sign_data(order_json, "keys/purchaser_private.pem")
    package = {"order": order, "signature": signature}

    # AES encrypt
    encrypted = encrypt_data(json.dumps(package))
    encrypted_serializable = serialize_encrypted(encrypted)
    encrypted_key = encrypt_key(encrypted["session_key"], "keys/supervisor_public.pem")

    # Store in SQLite
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO orders(order_id, payload, encrypted_key, purchaser_sig, supervisor_sig, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        order["order_id"],
        json.dumps(encrypted_serializable),
        encrypted_key.hex(),
        signature,
        None,
        "created",
        order["timestamp"]
    ))
    conn.commit()
    conn.close()

    log_event("PO_CREATED", {"order_id": order["order_id"]})
    return jsonify({"message": "Order sent securely", "order_id": order["order_id"]})

# -------------------- Supervisor --------------------
@app.route("/supervisor/load_order", methods=["GET"])
def supervisor_load_order():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT order_id, payload, encrypted_key FROM orders WHERE status='created' ORDER BY timestamp ASC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "No order available"})

    order_id, payload_json, encrypted_key_hex = row
    payload = deserialize_encrypted(json.loads(payload_json))

    # Use RSA-encrypted session key from DB, not payload["session_key"]
    encrypted_session_key = bytes.fromhex(encrypted_key_hex)
    session_key = decrypt_key(encrypted_session_key, "keys/supervisor_private.pem")

    decrypted = decrypt_data(payload, session_key)
    data = json.loads(decrypted)
    return jsonify(data)

@app.route("/supervisor/approve", methods=["POST"])
def supervisor_approve():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT order_id, payload, encrypted_key, purchaser_sig FROM orders WHERE status='created' ORDER BY timestamp ASC LIMIT 1")
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "No order to approve"})
    order_id, payload_json, encrypted_key_hex, purchaser_sig = row
    payload = deserialize_encrypted(json.loads(payload_json))
    session_key = decrypt_key(payload["session_key"], "keys/supervisor_private.pem")
    decrypted = decrypt_data(payload, session_key)
    data = json.loads(decrypted)
    order_json = json.dumps(data["order"], sort_keys=True)

    # Verify purchaser signature
    if not verify_signature(order_json, purchaser_sig, "keys/purchaser_public.pem"):
        conn.close()
        return jsonify({"error": "Invalid purchaser signature"})
    if not is_fresh_timestamp(data["order"]["timestamp"]):
        conn.close()
        return jsonify({"error": "Timestamp expired"})

    supervisor_sig = sign_data(order_json, "keys/supervisor_private.pem")
    c.execute("UPDATE orders SET supervisor_sig=?, status='approved' WHERE order_id=?", (supervisor_sig, order_id))
    conn.commit()
    conn.close()
    log_event("PO_APPROVED", {"order_id": order_id})
    return jsonify({"message": "Order approved"})

# -------------------- Dept Verification --------------------
@app.route("/dept/verify", methods=["POST"])
def dept_verify():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT order_id, purchaser_sig, supervisor_sig, timestamp FROM orders WHERE status='approved' ORDER BY timestamp ASC LIMIT 1")
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "No approved order"})
    order_id, purchaser_sig, supervisor_sig, ts = row
    c.execute("SELECT payload, encrypted_key FROM orders WHERE order_id=?", (order_id,))
    row = c.fetchone()
    conn.close()
    payload_json, encrypted_key_hex = row
    payload = deserialize_encrypted(json.loads(payload_json))
    session_key = decrypt_key(payload["session_key"], "keys/supervisor_private.pem")
    decrypted = decrypt_data(payload, session_key)
    data = json.loads(decrypted)
    order_json = json.dumps(data["order"], sort_keys=True)
    valid1 = verify_signature(order_json, purchaser_sig, "keys/purchaser_public.pem")
    valid2 = verify_signature(order_json, supervisor_sig, "keys/supervisor_public.pem")
    if valid1 and valid2 and is_fresh_timestamp(ts):
        log_event("PO_COMPLETED", {"order_id": order_id})
        return jsonify({"message": "Order fully verified"})
    return jsonify({"error": "Verification failed"})

# -------------------- Audit Logs --------------------
@app.route("/audit/logs", methods=["GET"])
def audit_logs():
    try:
        with open("audit_log.json") as f:
            logs = [line.strip() for line in f]
        return jsonify(logs)
    except:
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)