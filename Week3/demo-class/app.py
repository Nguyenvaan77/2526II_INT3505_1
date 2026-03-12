from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu lộn xộn, trộn lẫn tiếng Anh và tiếng Việt
data_list = [
    {"id": 1, "task_name": "Học REST v0", "trang_thai": "moi"},
    {"id": 2, "task_name": "Viết báo cáo", "trang_thai": "xong"}
]

# 1. Lấy tất cả (Sai: Dùng động từ, CamelCase, trả về list thô)
@app.route('/getAllTasks', methods=['GET'])
def get_all():
    return jsonify(data_list)

# 2. Lấy một cái (Sai: Tên lộn xộn, cấu trúc ID kiểu query string)
@app.route('/xemChiTiet', methods=['GET'])
def get_one():
    task_id = int(request.args.get('id'))
    item = next((t for t in data_list if t['id'] == task_id), None)
    return jsonify(item) # Trả về null nếu không thấy (không có báo lỗi)

# 3. Thêm mới (Sai: Tên tiếng Việt có dấu gạch ngang, trả về string thô)
@app.route('/them-moi-nhiem-vu', methods=['POST'])
def add_task():
    new_data = request.json
    data_list.append({"id": 3, "task_name": new_data.get('name'), "trang_thai": "moi"})
    return "Đã lưu vào máy chủ thành công!" 

# 4. Sửa (Sai: Dùng POST để sửa thay vì PUT/PATCH, tên lộn xộn)
@app.route('/UpdateCongViec', methods=['POST'])
def edit_task():
    task_id = int(request.args.get('id'))
    for t in data_list:
        if t['id'] == task_id:
            t['task_name'] = request.json.get('name')
    return jsonify({"mess": "update xong", "code": 1})

# 5. Xóa (Sai: Dùng GET để xóa - lỗi bảo mật nghiêm trọng)
@app.route('/removeTaskNow', methods=['GET'])
def delete_it():
    task_id = int(request.args.get('id'))
    global data_list
    data_list = [t for t in data_list if t['id'] != task_id]
    return "Xóa rồi nhé"

if __name__ == '__main__':
    app.run(port=5000, debug=True)