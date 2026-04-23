from flask import request, jsonify
from app.services import create_user, get_users, create_task, get_tasks

def register_routes(app):
    @app.route("/", methods=["GET"])
    def home():
        return {"message": "Welcome to Week9 API"}

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "healthy"}

    @app.route("/reset", methods=["POST"])
    def reset():
        from app.services import users, tasks
        users.clear()
        tasks.clear()
        return {"message": "reset done"}

    @app.route("/users", methods=["POST"])
    def add_user():
        try:
            if(data := request.json) is None:
                raise ValueError("Invalid JSON payload")
            user = create_user(data.get("name"))
            return jsonify(user), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/users", methods=["GET"])
    def list_users():
        return jsonify(get_users())

    @app.route("/tasks", methods=["POST"])
    def add_task():
        try:
            data = request.json
            task = create_task(data.get("title"), data.get("user_id"))
            return jsonify(task), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/tasks", methods=["GET"])
    def list_tasks():
        return jsonify(get_tasks())