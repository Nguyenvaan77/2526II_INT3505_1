from flask import Flask

app = Flask(__name__)

# Dữ liệu giả lập
tasks = [
    {
        "id": 1,
        "name": "Học REST"
    }
]

# Sai lầm 1: Url chứa động từ (Vi phạm nguyên tắc uniform interface) 
@app.route('/get-all-tasks-now', methods=['GET'])
def get_tasks():
    # Sai lầm 2: Trả về HTML trực tiếp (vi phạm Client-Server)
    html = "<h1>Danh sách công việc</h1><ul>"
    for t in tasks:
        html += f"<li>{t['name']}</li>"
    html += "</ul>"
    return html

# Sai lầm 3: Dùng GET để cập nhật thay vì PUT
@app.route('/update-task-by-id?id=1', methods=['GET']) 
def update_task():
    tasks[0]['name'] = "Đã học xong REST"
    return "Xong rồi!"

if __name__ == '__main__':
    app.run(port=5000)