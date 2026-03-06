from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
CORS(app) # Cho phép Client-Server tách biệt gọi nhau

# Secret key cho JWT
SECRET_KEY = "your-secret-key-here"

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

# ===== MIDDLEWARE =====
# Decorator kiểm tra Token trước khi truy cập
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Thiếu Token"}), 401
        
        try:
            token = auth_header.split(" ")[1]  # Lấy token từ "Bearer <token>"
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded['user_id']  # Lưu user_id vào request
            request.user_name = decoded['user_name']
        except:
            return jsonify({"error": "Token không hợp lệ hoặc hết hạn"}), 401
        
        return f(*args, **kwargs)
    return decorated

# ===== AUTHENTICATION =====
# 1. LOGIN: Nhận Token
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    
    # Tìm user (demo đơn giản)
    user = next((u for u in db_users if u['id'] == user_id), None)
    if not user or password != "123456":  # Password demo
        return jsonify({"error": "Thông tin đăng nhập sai"}), 401
    
    # Tạo JWT Token (hết hạn sau 1 giờ)
    token = jwt.encode({
        'user_id': user_id,
        'user_name': user['name'],
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        "message": "Đăng nhập thành công",
        "token": token,
        "user": user
    }), 200

# ===== USER CRUD API (Đã bảo vệ với Token) =====
# 1. GET: Lấy toàn bộ danh sách
@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users():
    return jsonify(db_users), 200

# 2. GET: Lấy thông tin 1 user cụ thể
@app.route('/api/users/<string:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = next((u for u in db_users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Không tìm thấy user"}), 404

# 3. POST: Thêm user mới
@token_required
@app.route('/api/users', methods=['POST'])
def create_user():
    new_data = request.json
    # Tạo ID tự động (giả lập)
    new_data['id'] = str(len(db_users) + 2) 
    db_users.append(new_data)
    return jsonify(new_data), 201

# 4. PUT: Cập nhật thông tin user
@token_required
def update_user(user_id):
    user = next((u for u in db_users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Không tìm thấy"}), 404
    
    update_data = request.json
    user.update(update_data)
    user.update(update_data) # Cập nhật dữ liệu mới vào user cũ
    return jsonify(user), 200

@token_required
def delete_user(user_id):
    global db_users
    db_users = [u for u in db_users if u['id'] != user_id]
    return '', 204

# 6. GET: Lấy hồ sơ người dùng hiện tại (dựa trên JWT)
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    user = next((u for u in db_users if u['id'] == request.user_id), None)
    return jsonify({
        "message": "Server không nhớ bạn, nhưng JWT Token cho phép tôi biết bạn là ai",
        "data": user
    }), 200
    # Nếu không có token hoặc token sai
    return jsonify({"error": "Bạn là ai? Tôi không giữ Session, hãy gửi Token!"}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)