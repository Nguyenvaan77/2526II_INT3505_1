from flask import jsonify

class ResponseHelper:
    @staticmethod
    def success(data=None, message="OK", status=200):
        """Phản hồi khi thành công"""
        return jsonify({
            "status": status,
            "message": message,
            "data": data
        }), status

    @staticmethod
    def error(message="Bad Request", code=400):
        """Phản hồi khi có lỗi"""
        return jsonify({
            "code": code,
            "message": message
        }), code