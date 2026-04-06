import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(BASE_DIR, "security_tests", "outputs", "processed_orders.txt")


def is_duplicate(order_id):
    if not os.path.exists(FILE):
        return False

    with open(FILE) as f:
        return order_id in f.read().splitlines()


def mark_processed(order_id):
    with open(FILE, "a") as f:
        f.write(order_id + "\n")


def reset():
    if os.path.exists(FILE):
        os.remove(FILE)