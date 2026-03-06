from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Cho phép Client-Server tách biệt gọi nhau

# Database của bạn
db_users = [
    {"id": "2", "name": "Trần Thị Bình", "email": "binh.tran@example.com", "phoneNumber": "0912345678"},
    {"id": "3", "name": "Lê Hoàng Cường", "email": "cuong.le@example.com", "phoneNumber": "0923456789"},
    {"id": "4", "name": "Phạm Minh Đức", "email": "duc.pham@example.com", "phoneNumber": "0934567890"},
    {"id": "5", "name": "Hoàng Lan Anh", "email": "anh.hoang@example.com", "phoneNumber": "0945678901"},
    {"id": "6", "name": "Vũ Văn Phương", "email": "phuong.vu@example.com", "phoneNumber": "0956789012"},
    {"id": "7", "name": "Đặng Thu Thảo", "email": "thao.dang@example.com", "phoneNumber": "0967890123"},
    {"id": "8", "name": "Bùi Tiến Dũng", "email": "dung.bui@example.com", "phoneNumber": "0978901234"},
    {"id": "9", "name": "Đỗ Mỹ Linh", "email": "linh.do@example.com", "phoneNumber": "0989012345"},
    {"id": "10", "name": "Ngô Gia Bảo", "email": "bao.ngo@example.com", "phoneNumber": "0990123456"},
    {"id": "11", "name": "Lý Thanh Tùng", "email": "tung.ly@example.com", "phoneNumber": "0812345678"},
    {"id": "12", "name": "Dương Ngọc Hải", "email": "hai.duong@example.com", "phoneNumber": "0823456789"},
    {"id": "13", "name": "Trịnh Kim Chi", "email": "chi.trinh@example.com", "phoneNumber": "0834567890"},
    {"id": "14", "name": "Mai Xuân Trường", "email": "truong.mai@example.com", "phoneNumber": "0845678901"},
    {"id": "15", "name": "Đinh Quang Khải", "email": "khai.dinh@example.com", "phoneNumber": "0856789012"},
    {"id": "16", "name": "Hồ Bích Ngọc", "email": "ngoc.ho@example.com", "phoneNumber": "0867890123"},
    {"id": "17", "name": "Phan Văn Hậu", "email": "hau.phan@example.com", "phoneNumber": "0878901234"},
    {"id": "18", "name": "Cao Thùy Trang", "email": "trang.cao@example.com", "phoneNumber": "0889012345"},
    {"id": "19", "name": "Tạ Đình Phong", "email": "phong.ta@example.com", "phoneNumber": "0890123456"},
    {"id": "20", "name": "Lương Gia Huy", "email": "huy.luong@example.com", "phoneNumber": "0701234567"},
    {"id": "21", "name": "Test User", "email": "test@example.com", "phoneNumber": "0987654321"},
    {"id": "22", "name": "Ngô Văn E", "email": "e.ngo@example.com", "phoneNumber": "0989012345"}
]

# 1. GET: Lấy toàn bộ danh sách
@app.route('/api/users', methods=['GET'])
def get_all_users():
    return jsonify(db_users), 200

# 2. GET: Lấy thông tin 1 user cụ thể (Dựa vào ID trên URL)
@app.route('/api/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in db_users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Không tìm thấy user"}), 404

# 3. POST: Thêm user mới
@app.route('/api/users', methods=['POST'])
def create_user():
    new_data = request.json
    # Tạo ID tự động (giả lập)
    new_data['id'] = str(len(db_users) + 2) 
    db_users.append(new_data)
    return jsonify(new_data), 201

# 4. PUT: Cập nhật thông tin user
@app.route('/api/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in db_users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Không tìm thấy"}), 404
    
    update_data = request.json
    user.update(update_data) # Cập nhật dữ liệu mới vào user cũ
    return jsonify(user), 200

# 5. DELETE: Xóa user
@app.route('/api/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global db_users
    db_users = [u for u in db_users if u['id'] != user_id]
    return '', 204 # No Content: Xóa thành công nhưng không cần trả về dữ liệu

if __name__ == '__main__':
    app.run(port=5000, debug=True)