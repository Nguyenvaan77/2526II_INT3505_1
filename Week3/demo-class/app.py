from flask import Flask, request
from response_helper import ResponseHelper

app = Flask(__name__)

# Dữ liệu mẫu
tasks = [
    {"id": i, "title": f"Task sample {i}", "status": "new" if i % 2 == 0 else "completed"}
    for i in range(1, 26)
]

task_tags = {
    1: ["Work", "Urgent"],
    2: ["Personal", "Low-priority"]
}

# --- 1. LẤY DANH SÁCH (GET /v1/tasks) ---
@app.route('/v1/tasks', methods=['GET'])
def get_tasks():
    try:
        limit = int(request.args.get('limit', 10))  
        offset = int(request.args.get('offset', 0)) 
    except ValueError:
        return ResponseHelper.error("Limit and Offset must be integers", 400)

    status_filter = request.args.get('status')
    
    data_source = tasks
    if status_filter:
        data_source = [t for t in tasks if t['status'] == status_filter]
    
    paginated_data = data_source[offset : offset + limit]

    # Đồng nhất meta data vào ResponseHelper (nếu muốn) hoặc trả về kiểu này:
    meta = {
        "total": len(data_source),
        "limit": limit,
        "offset": offset,
        "count": len(paginated_data)
    }
    
    # Sử dụng success thay vì jsonify thủ công để nhất quán cấu trúc v1, v2
    return ResponseHelper.success(
        data=paginated_data, 
        message="Tasks retrieved successfully",
        # Chúng ta có thể bổ sung meta vào success helper nếu cần, 
        # nhưng ở đây dùng data làm object chứa cả meta cũng là 1 cách.
    )

# --- 2. LẤY TAGS (Sub-resource) ---
@app.route('/v1/tasks/<int:task_id>/tags', methods=['GET'])
def get_task_tags(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error(f"Task {task_id} not found", 404)
    
    tags = task_tags.get(task_id, [])
    return ResponseHelper.success(tags, f"Tags for task {task_id} retrieved")

# --- 3. LẤY CHI TIẾT ---
@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_one(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return ResponseHelper.success(task, "Task details found")
    return ResponseHelper.error(f"Task {task_id} not found", 404)

# --- 4. TẠO MỚI ---
@app.route('/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True)
    if not data or 'title' not in data:
        return ResponseHelper.error("Missing required field: 'title'", 400)

    new_id = tasks[-1]['id'] + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": data.get('title'),
        "status": data.get('status', 'new') 
    }
    tasks.append(new_task)
    return ResponseHelper.success(new_task, "Task created successfully", 201)

# --- 5. CẬP NHẬT ---
@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error(f"Task {task_id} not found", 404)
    
    data = request.get_json(silent=True) or {}
    task['title'] = data.get('title', task['title'])
    task['status'] = data.get('status', task['status'])
    return ResponseHelper.success(task, f"Task {task_id} updated successfully")

# --- 6. XÓA ---
@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return ResponseHelper.error(f"Task {task_id} not found", 404)

    tasks = [t for t in tasks if t['id'] != task_id]
    return ResponseHelper.success({"deleted_id": task_id}, f"Task {task_id} deleted")

if __name__ == '__main__':
    app.run(port=5000, debug=True)