from flask import Flask, jsonify, request
from response_helper import ResponseHelper

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn REST Consistency", "status": "new"},
    {"id": 2, "title": "Clean up code", "status": "completed"}
]

# --- 1. LẤY DANH SÁCH (Sử dụng Query Params để lọc) ---
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Clarity: Dùng tham số ?status=... để lọc dữ liệu minh bạch
    status_filter = request.args.get('status')
    
    if status_filter:
        filtered = [t for t in tasks if t['status'] == status_filter]
        return ResponseHelper.success(
            filtered, 
            f"Retrieved tasks with status: {status_filter}"
        )
    
    return ResponseHelper.success(tasks, "All tasks retrieved successfully")

# --- 2. LẤY CHI TIẾT (Thông báo lỗi chi tiết) ---
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_one(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return ResponseHelper.success(task, "Task details found")
    
    # Clarity: Chỉ rõ ID không tồn tại giúp Client dễ debug
    return ResponseHelper.error(f"Task with ID {task_id} not found in our system", 404)

# --- 3. TẠO MỚI (Validation dữ liệu đầu vào) ---
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True)
    
    # Clarity: Kiểm tra kỹ body và cung cấp lý do lỗi cụ thể
    if data is None:
        return ResponseHelper.error("Request body is missing or not a valid JSON", 400)
    
    if 'title' not in data:
        return ResponseHelper.error("Field 'title' is mandatory to create a task", 400)

    new_id = tasks[-1]['id'] + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": data.get('title'),
        "status": "new"
    }
    tasks.append(new_task)
    return ResponseHelper.success(new_task, "Task created successfully", 201)

# --- 4. CẬP NHẬT (Sử dụng PUT) ---
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error(f"Cannot update: Task {task_id} does not exist", 404)
    
    data = request.get_json(silent=True) or {}
    
    # Cập nhật thông tin
    task['title'] = data.get('title', task['title'])
    task['status'] = data.get('status', task['status'])
    
    return ResponseHelper.success(task, f"Task {task_id} updated successfully")

# --- 5. XÓA (Sử dụng DELETE) ---
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return ResponseHelper.error(f"Cannot delete: Task {task_id} was not found", 404)

    tasks = [t for t in tasks if t['id'] != task_id]
    return ResponseHelper.success(None, f"Task {task_id} has been permanently removed")

if __name__ == '__main__':
    app.run(port=5000, debug=True)