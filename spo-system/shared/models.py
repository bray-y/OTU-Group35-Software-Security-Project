import uuid, json, time

def create_order():

    order = {
        "order_id": str(uuid.uuid4()),
        "item": "Laptop",
        "quantity": 5,
        "price": 1200,
        "department": "IT",
        "justification": "New employee onboarding",
        "timestamp": int(time.time())
    }

    return order


def to_json(data):
    return json.dumps(data, sort_keys=True)