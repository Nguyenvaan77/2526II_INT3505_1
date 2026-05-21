from flask import Flask, request, jsonify
import hashlib
import hmac
import time
app = Flask(__name__)

WEBHOOK_SECRET = "email-secret-key"

processed_events = set()


def verify_signature(payload, signature):

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


@app.route("/webhooks/email", methods=["POST"])
def receive_email_webhook():
    print("Email Service ĐÃ NHẬN ĐƯỢC EMAIL")

    payload = request.data

    signature = request.headers.get(
        "X-Webhook-Signature"
    )

    if not verify_signature(payload, signature):
        return jsonify({
            "error": "Invalid signature"
        }), 401

    event = request.json

    event_id = event["event_id"]

    if event_id in processed_events:
        return jsonify({
            "message": "Duplicate ignored"
        }), 200

    processed_events.add(event_id)

    event_type = event["event_type"]

    user = event["user"]
    task = event["task"]

    print("ĐỢI 10S")


    time.sleep(10)

    print("HẾT THỜI GIAN ĐỢI 10S")

    print("\n========================")
    print("EMAIL SERVICE")
    print("========================")

    print("TO:", user["email"])

    if event_type == "task_created":
        print(f"EMAIL: Task created -> {task['title']}")

    elif event_type == "task_updated":
        print(f"EMAIL: Task updated -> {task['title']}")

    elif event_type == "task_deleted":
        print(f"EMAIL: Task deleted -> {task['title']}")

    return jsonify({
        "status": "email processed"
    }), 200


if __name__ == "__main__":
    app.run(port=7000, debug=True)