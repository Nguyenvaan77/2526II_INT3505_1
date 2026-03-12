from flask import jsonify

class ResponseHelper:

    @staticmethod
    def success(data=None, message="OK", status=200, headers=None):
        response = jsonify({
            "status": status,
            "message": message,
            "data": data
        })

        response.status_code = status

        if headers:
            response.headers.extend(headers)

        return response


    @staticmethod
    def error(message="Bad Request", code=400, headers=None):
        response = jsonify({
            "code": code,
            "message": message
        })

        response.status_code = code

        if headers:
            response.headers.extend(headers)

        return response