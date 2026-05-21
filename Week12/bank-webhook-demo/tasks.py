from celery import Celery
import requests
import json
import hmac
import hashlib

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)

WEBHOOK_URL = "http://localhost:7000/webhooks/email"
WEBHOOK_SECRET = "email-secret-key"


def generate_signature(payload):

    return hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=5
)
def send_email_webhook_task(self, event):

    payload = json.dumps(event)

    signature = generate_signature(payload)

    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": signature
    }

    response = requests.post(
        WEBHOOK_URL,
        data=payload,
        headers=headers,
        timeout=5
    )

    print("\nWebhook Email Sent")
    print(response.status_code)

    return response.status_code