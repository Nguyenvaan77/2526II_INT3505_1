from flask import Flask, request, jsonify
from tasks import send_webhook_task
import uuid
from datetime import datetime

app = Flask(__name__)

customers = {}
accounts = {}

@app.route("/customers", methods=["POST"])
def create_customer():

    data = request.json

    customer_id = str(uuid.uuid4())

    customer = {
        "customer_id": customer_id,
        "name": data["name"],
        "email": data["email"]
    }

    customers[customer_id] = customer

    # =========================
    # Create Event
    # =========================

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "customer_registered",
        "timestamp": datetime.utcnow().isoformat(),
        "data": customer
    }

    # =========================
    # PUSH TO QUEUE
    # =========================

    send_webhook_task.delay(event)

    return jsonify(customer), 201


@app.route("/accounts", methods=["POST"])
def create_account():

    data = request.json

    customer_id = data["customer_id"]

    account_id = str(uuid.uuid4())

    account = {
        "account_id": account_id,
        "customer_id": customer_id,
        "balance": 0
    }

    accounts[account_id] = account

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "account_created",
        "timestamp": datetime.utcnow().isoformat(),
        "data": account
    }

    send_webhook_task.delay(event)

    return jsonify(account), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)