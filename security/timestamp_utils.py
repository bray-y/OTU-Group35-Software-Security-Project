from datetime import datetime

processed_orders = set()


def validate_timestamp(ts):

    now = datetime.utcnow()

    msg_time = datetime.fromisoformat(ts)

    if abs((now - msg_time).seconds) > 120:

        raise Exception("Replay attack suspected")


def check_replay(order_id):

    if order_id in processed_orders:

        raise Exception("Duplicate order detected")

    processed_orders.add(order_id)