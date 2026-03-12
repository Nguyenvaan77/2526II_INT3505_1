from flask import Flask, jsonify, request
from response_helper import ResponseHelper
from functools import wraps # Dùng để tạo decorator
import hashlib
import json

app = Flask(__name__)

# Giả lập một Database API Keys (Thực tế sẽ lưu trong DB)
VALID_API_KEYS = ["gemini-secret-key-123", "user-token-abc"]

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


# --- 1. LẤY DANH SÁCH (GET /tasks) ---
@app.route('/tasks', methods=['GET'])
@require_api_key #Phải có key mới truy cập được 
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
@require_api_key
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
@require_api_key
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
@require_api_key
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json() or {}
    task['name'] = data.get('name', task['name'])
    task['status'] = data.get('status', task['status'])

    return ResponseHelper.success(task, "Task updated successfully", 200)

# --- 5. XÓA (DELETE /tasks/<id>) ---
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@require_api_key
def delete_task(task_id):
    # Tìm task
    task = next((t for t in tasks if t['id'] == task_id), None)

    # Nếu không tồn tại
    if not task:
        return ResponseHelper.error("Task not found", 404)

    # Nếu tồn tại thì xóa
    tasks.remove(task)

    return ResponseHelper.success(None, "Deleted successfully", 200)

if __name__ == '__main__':
    app.run(port=5000)