from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

WEBHOOK_SECRET = "super-secret-key"

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

@app.route("/webhooks/events", methods=["POST"])
def receive_webhook():

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

    print("\nEVENT RECEIVED")
    print(event)

    return jsonify({
        "status": "ok"
    }), 200

if __name__ == "__main__":
    app.run(port=6000)