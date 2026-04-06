from datetime import datetime

def log_event(user, action, order_id):

    with open("audit_log.txt", "a") as f:

        f.write(

            f"{datetime.utcnow()} | {user} | {action} | {order_id}\n"
        )