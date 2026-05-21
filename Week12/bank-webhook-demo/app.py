from flask import Flask, request, jsonify
from tasks import send_email_webhook_task
import uuid
from datetime import datetime

app = Flask(__name__)

users = {}
tasks_db = {}

# =========================
# USER APIs
# =========================

@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    user_id = str(uuid.uuid4())

    user = {
        "user_id": user_id,
        "name": data["name"],
        "email": data["email"]
    }

    users[user_id] = user

    return jsonify(user), 201


# =========================
# TASK APIs
# =========================

@app.route("/tasks", methods=["POST"])
def create_task():

    data = request.json

    user_id = data["user_id"]

    if user_id not in users:
        return jsonify({
            "error": "User not found"
        }), 404

    task_id = str(uuid.uuid4())

    task = {
        "task_id": task_id,
        "title": data["title"],
        "status": "TODO",
        "user_id": user_id
    }

    tasks_db[task_id] = task

    print("Created New Task Successfully")

    # =========================
    # EVENT
    # =========================

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task_created",
        "timestamp": datetime.utcnow().isoformat(),
        "user": users[user_id],
        "task": task
    }

    # =========================
    # ASYNC TASK
    # =========================

    send_email_webhook_task.delay(event)

    return jsonify(task), 201


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):

    if task_id not in tasks_db:
        return jsonify({
            "error": "Task not found"
        }), 404

    data = request.json

    tasks_db[task_id]["title"] = data.get(
        "title",
        tasks_db[task_id]["title"]
    )

    tasks_db[task_id]["status"] = data.get(
        "status",
        tasks_db[task_id]["status"]
    )

    task = tasks_db[task_id]

    user = users[task["user_id"]]

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task_updated",
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "task": task
    }

    send_email_webhook_task.delay(event)

    return jsonify(task)


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    if task_id not in tasks_db:
        return jsonify({
            "error": "Task not found"
        }), 404

    task = tasks_db[task_id]

    user = users[task["user_id"]]

    del tasks_db[task_id]

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task_deleted",
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "task": task
    }

    send_email_webhook_task.delay(event)

    return jsonify({
        "message": "Task deleted"
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)