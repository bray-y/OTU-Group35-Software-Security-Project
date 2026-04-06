import json
from uuid import uuid4
from datetime import datetime

def create_order():

    order = {

        "order_id": str(uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "item": "Laptop",
        "quantity": 2,
        "price": 1200,
        "department": "IT",
        "justification": "Developer machines"
    }

    return order


def to_json(data):
    return json.dumps(data, sort_keys=True)