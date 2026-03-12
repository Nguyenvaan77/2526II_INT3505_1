from flask import jsonify

class ResponseHelper:
    @staticmethod
    def success(data=None, message="OK", status=200):
        # Cấu trúc đồng nhất cho phản hồi thành công
        return jsonify({
            "status": status,
            "message": message,
            "data": data
        }), status

    @staticmethod
    def error(message="Bad Request", code=400):
        # Cấu trúc đồng nhất cho phản hồi lỗi
        return jsonify({
            "code": code,
            "message": message
        }), code