import purchaser_client
from supervisor_service import process_order
from purchasing_dept_service import verify_final

message = purchaser_client.message

approved = process_order(message)

verify_final(approved)