import hashlib
from flask_cors import CORS
import jwt
import datetime
from flask import Flask, json, jsonify, request
from api.response_helper import ResponseHelper
from functools import wraps
from flasgger import Swagger
import yaml
import os

app = Flask(__name__)
CORS(app)

# Load file YAML đúng path trong serverless
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(BASE_DIR, "openapi.yaml")

with open(yaml_path, "r", encoding="utf-8") as f:
    template = yaml.safe_load(f)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
    "openapi": "3.0.0", # Ép buộc giao diện sử dụng chuẩn 3.0
}

# Khởi tạo Swagger với template đã load từ file yaml
swagger = Swagger(app, template=template, config=swagger_config)

SECRET_KEY = "my-super-secret-key"

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Giả lập kiểm tra user (thực tế sẽ query DB)
    if username == "admin" and password == "123456":

        payload = {
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return ResponseHelper.success(
            {"token": token},
            "Login successful",
            200
        )

    return ResponseHelper.error("Invalid username or password", 401)

# Giả lập một Database API Keys (Thực tế sẽ lưu trong DB)
VALID_API_KEYS = ["gemini-secret-key-123", "user-token-abc"]

def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return ResponseHelper.error("Token missing", 401)

        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = decoded["user"]

        except jwt.ExpiredSignatureError:
            return ResponseHelper.error("Token expired", 401)

        except jwt.InvalidTokenError:
            return ResponseHelper.error("Invalid token", 401)

        return f(*args, **kwargs)

    return decorated_function

# --- 🛡️ BỘ LỌC STATELESS (Decorator) ---
def require_api_key(f):  
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Lấy token từ Header 'X-API-KEY'
        api_key = request.headers.get('X-API-KEY')
        
        # Nguyên tắc Stateless: Kiểm tra danh tính TRÊN MỖI request
        if api_key and api_key in VALID_API_KEYS:
            return f(*args, **kwargs)
        
        # Nếu không có token hoặc token sai -> Trả về 401
        return ResponseHelper.error("Unauthorized: Invalid or missing API Key", 401)
    return decorated_function

# Dữ liệu nằm ở Server
tasks = [
    {"id": 1, "name": "Học nguyên tắc Client-Server", "status": "Doing"},
    {"id": 2, "name": "Viết báo cáo Ver 1", "status": "Pending"}
]

# Helper tạo ETag
def generate_etag(data):
    return hashlib.md5(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()

@app.route('/')
def home():
    return "Flask API running on Vercel"

# --- 1. LẤY DANH SÁCH (GET /tasks) ---
@app.route('/tasks', methods=['GET'])
@require_jwt
def get_tasks():
    etag = generate_etag(tasks)

    if request.headers.get("If-None-Match") == etag:
        return "", 304

    headers = {
        "Cache-Control": "public, max-age=60",
        "ETag": etag
    }
    # Trả về mã 200 OK
    return ResponseHelper.success(tasks,"OK", 200, headers)

# --- 2. LẤY CHI TIẾT 1 TASK (GET /tasks/<id>) ---
@app.route('/tasks/<int:task_id>', methods=['GET'])
@require_jwt
def get_one_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        return ResponseHelper.error("Task not found", 404)

    etag = generate_etag(task)

    if request.headers.get("If-None-Match") == etag:
        return "", 304

    headers = {
        "Cache-Control": "public, max-age=120",
        "ETag": etag
    }

    return ResponseHelper.success(task, "Task retrieved successfully", 200, headers)

# --- 3. TẠO MỚI (POST /tasks) ---
@app.route('/tasks', methods=['POST'])
@require_jwt
def create_task():
    # Lấy dữ liệu từ body của request
    data = request.get_json()

    new_task = {
        "id": len(tasks) + 1,
        "name": data.get("name"),
        "status": "Pending"
    }
    tasks.append(new_task)

    return ResponseHelper.success(new_task, "Created successfully", 201)

# --- 4. CẬP NHẬT (PUT /tasks/<id>) ---
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@require_jwt
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error("Task not found", 404)
    
    data = request.get_json() or {}
    task['name'] = data.get('name', task['name'])
    task['status'] = data.get('status', task['status'])

    return ResponseHelper.success(task, "Task updated successfully", 200)

# --- 5. XÓA (DELETE /tasks/<id>) ---
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@require_jwt
def delete_task(task_id):
    # Tìm task
    task = next((t for t in tasks if t['id'] == task_id), None)

    # Nếu không tồn tại
    if not task:
        return ResponseHelper.error("Task not found", 404)

    # Nếu tồn tại thì xóa
    tasks.remove(task)

    return ResponseHelper.success(None, "Deleted successfully", 200)

# if __name__ == '__main__':
#     app.run(port=5000)