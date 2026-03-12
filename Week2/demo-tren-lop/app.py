from flask import Flask, jsonify

app = Flask(__name__)

# Dữ liệu nằm ở Server
tasks = [
    {"id": 1, "name": "Học nguyên tắc Client-Server", "status": "Doing"},
    {"id": 2, "name": "Viết báo cáo Ver 1", "status": "Pending"}
]

# Sai lầm 1: Url chứa động từ (Vi phạm nguyên tắc uniform interface) 
@app.route('/get-all-tasks-now', methods=['GET'])
def get_tasks():
    #Trả về JSON thay vì HTML
    #Biến Object List thành JSON để trả về Client
    return jsonify(tasks)

# Sai lầm 3: Dùng GET để cập nhật thay vì PUT
@app.route('/update-task-by-id?id=1', methods=['GET']) 
def update_task():
    tasks[0]['name'] = "Đã học xong REST"
    return jsonify(tasks[0])

if __name__ == '__main__':
    app.run(port=5000)