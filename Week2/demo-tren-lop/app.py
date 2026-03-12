from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu nằm ở Server
tasks = [
    {"id": 1, "name": "Học nguyên tắc Client-Server", "status": "Doing"},
    {"id": 2, "name": "Viết báo cáo Ver 1", "status": "Pending"}
]

# --- 1. LẤY DANH SÁCH (GET /tasks) ---
@app.route('/get-all-tasks-now', methods=['GET']) #Url chứa động từ thay vì danh từ
def get_tasks():
    #Trả về JSON thay vì HTML
    #Biến Object List thành JSON để trả về Client
    return jsonify(tasks)

# --- 2. LẤY CHI TIẾT 1 TASK (GET /tasks/<id>) ---
@app.route('/get-one-task/<int:task_id>', methods=['GET'])
def get_one_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"})

# --- 3. TẠO MỚI (POST /create-task) --- nhẽ ra là PUT 
@app.route('/create-task', methods=['POST'])
def create_task():
    # Lấy dữ liệu từ body của request
    data = request.get_json()

    new_task = {
        "id": len(tasks) + 1,
        "name": data.get("name"),
        "status": "Pending"
    }
    tasks.append(new_task)

    return jsonify(new_task)

# --- 4. CẬP NHÂT (PUT /update-task-by-id?id=1) ---
@app.route('/update-task-by-id/<int:task_id>', methods=['PUT']) 
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"})
    
    data = request.get_json() or {}
    task['name'] = data.get('name', task['name'])
    task['status'] = data.get('status', task['status'])
    return jsonify(task)

# --- 5. XÓA (DELETE /delete-task-by-id/<id>) ---
@app.route('/delete-task-by-id/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Tìm task
    task = next((t for t in tasks if t['id'] == task_id), None)

    # Nếu không tồn tại
    if not task:
        return jsonify({"error": "Task not found"})

    # Nếu tồn tại thì xóa
    tasks.remove(task)

    return jsonify({
        "message": "Task deleted successfully",
        "deleted_task": task
    })

if __name__ == '__main__':
    app.run(port=5000)