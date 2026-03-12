from flask import Flask, jsonify, request
from response_helper import ResponseHelper

app = Flask(__name__)

# Dùng Danh từ (Resources): Tất cả URL chỉ xoay quanh danh từ /tasks. Hành động được xác định bằng phương thức HTTP (GET, POST, PUT, DELETE).
# Đúng mã HTTP Status Code: Trả về 201 khi tạo mới thành công, 404 khi không tìm thấy tài nguyên thay vì chỉ trả về text thông thường.
# Cấu trúc URL chuẩn: /tasks/<id> dùng cho cả lấy chi tiết, cập nhật và xóa.

# Dữ liệu nằm ở Server
tasks = [
    {"id": 1, "name": "Học nguyên tắc Client-Server", "status": "Doing"},
    {"id": 2, "name": "Viết báo cáo Ver 1", "status": "Pending"}
]

# --- 1. LẤY DANH SÁCH (GET /tasks) ---
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Trả về mã 200 OK
    return ResponseHelper.success(tasks,"OK", 200)

# --- 2. LẤY CHI TIẾT 1 TASK (GET /tasks/<id>) ---
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_one_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return ResponseHelper.success(task, "Found task", 200)
    return ResponseHelper.error("Task not found", 404)

# --- 3. TẠO MỚI (POST /tasks) ---
@app.route('/tasks', methods=['POST'])
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
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json() or {}
    task['name'] = data.get('name', task['name'])
    task['status'] = data.get('status', task['status'])
    return jsonify(task), 200

# --- 5. XÓA (DELETE /tasks/<id>) ---
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Tìm task
    task = next((t for t in tasks if t['id'] == task_id), None)

    # Nếu không tồn tại
    if not task:
        return ResponseHelper.error("Task not found", 404)

    # Nếu tồn tại thì xóa
    tasks.remove(task)

    return ResponseHelper.error(None, "Deleted successfully")

if __name__ == '__main__':
    app.run(port=5000)