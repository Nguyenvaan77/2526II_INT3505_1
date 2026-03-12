from flask import Flask, jsonify, request
from response_helper import ResponseHelper

app = Flask(__name__)

# Dữ liệu lộn xộn, trộn lẫn tiếng Anh và tiếng Việt
tasks = [
    {"id": 1, "title": "Learn REST Consistency", "status": "new"},
    {"id": 2, "title": "Write report", "status": "done"}
]

# 1. LẤY TẤT CẢ (GET /tasks)
@app.route('/tasks', methods=['GET'])
def get_all():
    return ResponseHelper.success(tasks, "Get all tasks successfully", 200)

# 2. Lấy một cái (Sai: Tên lộn xộn, cấu trúc ID kiểu query string)
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_one(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return ResponseHelper.success(task, "Task found", 200)
    return ResponseHelper.error("Task not found", 404)

# 3.
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data:
        return ResponseHelper.error("Title is required", 400)
        
    new_task = {
        "id": len(tasks) + 1,
        "title": data.get('title'),
        "status": "new"
    }
    tasks.append(new_task)
    return ResponseHelper.success(new_task, "Task created successfully", 201)

# 4. SỬA (PUT /tasks/<id>)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error("Task not found to update", 404)
    
    data = request.json
    task['title'] = data.get('title', task['title'])
    task['status'] = data.get('status', task['status'])
    return ResponseHelper.success(task, "Task updated successfully", 200)

# 5. XÓA (DELETE /tasks/<id>)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error("Task not found to delete", 404)

    tasks = [t for t in tasks if t['id'] != task_id]
    return ResponseHelper.success(None, "Task deleted successfully", 200)

if __name__ == '__main__':
    app.run(port=5000)