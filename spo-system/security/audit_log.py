import json, time

def log_event(event_type, data):

    record = {
        "event": event_type,
        "timestamp": int(time.time()),
        "data": data
    }

    with open("audit_log.json", "a") as f:
        f.write(json.dumps(record) + "\n")