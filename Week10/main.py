from flask import Flask, request, jsonify, make_response
from datetime import datetime

app = Flask(__name__)

# =========================================================
# Fake Database
# =========================================================

payments_v1 = []
payments_v2 = []

# =========================================================
# VERSION 1 API
# URL Versioning
# =========================================================

@app.route("/api/v1/payments", methods=["POST"])
def create_payment_v1():

    """
    API v1:
    - amount dùng string
    - gửi full card number
    - response đơn giản
    """

    data = request.get_json()

    # Validate
    required_fields = ["amount", "card_number"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    payment = {
        "id": len(payments_v1) + 1,
        "amount": data["amount"],
        "card_number": data["card_number"],
        "status": "success",
        "created_at": datetime.now().isoformat()
    }

    payments_v1.append(payment)

    # Deprecation Header
    response = make_response(jsonify(payment), 201)

    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "2026-12-01"
    response.headers["X-API-Warning"] = (
        "API v1 will be removed soon. Please migrate to v2."
    )

    return response


@app.route("/api/v1/payments", methods=["GET"])
def get_all_payments_v1():

    """
    API v1:
    Không phân trang
    """

    return jsonify(payments_v1)


# =========================================================
# VERSION 2 API
# URL Versioning
# =========================================================

@app.route("/api/v2/payments", methods=["POST"])
def create_payment_v2():

    """
    API v2:
    - amount dùng integer
    - có currency
    - chỉ lưu 4 số cuối thẻ
    - response chuẩn hơn
    """

    data = request.get_json()

    required_fields = [
        "amount",
        "currency",
        "card_last4"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    payment = {
        "payment_id": len(payments_v2) + 1,
        "amount": data["amount"],
        "currency": data["currency"],
        "card_last4": data["card_last4"],
        "status": "completed",
        "created_at": datetime.now().isoformat()
    }

    payments_v2.append(payment)

    return jsonify({
        "data": payment,
        "meta": {
            "api_version": "v2"
        }
    }), 201


@app.route("/api/v2/payments", methods=["GET"])
def get_all_payments_v2():

    """
    API v2:
    Có phân trang
    """

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    start = (page - 1) * limit
    end = start + limit

    result = payments_v2[start:end]

    return jsonify({
        "data": result,
        "meta": {
            "page": page,
            "limit": limit,
            "total": len(payments_v2)
        }
    })


# =========================================================
# HEADER VERSIONING DEMO
# =========================================================

@app.route("/api/products", methods=["GET"])
def get_products():

    """
    Header Versioning:
    X-API-Version: 1 hoặc 2
    """

    version = request.headers.get("X-API-Version", "1")

    products = [
        {
            "id": 1,
            "name": "Laptop",
            "price": 2000
        },
        {
            "id": 2,
            "name": "Phone",
            "price": 1000
        }
    ]

    if version == "2":

        return jsonify({
            "data": products,
            "meta": {
                "version": "2"
            }
        })

    return jsonify(products)


# =========================================================
# QUERY PARAM VERSIONING DEMO
# =========================================================

@app.route("/api/orders", methods=["GET"])
def get_orders():

    """
    Query Param Versioning:
    /api/orders?version=1
    /api/orders?version=2
    """

    version = request.args.get("version", "1")

    orders = [
        {
            "id": "ORD001",
            "total": 500
        },
        {
            "id": "ORD002",
            "total": 1000
        }
    ]

    if version == "2":

        return jsonify({
            "data": orders,
            "api_version": "2"
        })

    return jsonify(orders)


# =========================================================
# MIGRATION GUIDE
# =========================================================

@app.route("/api/migration-guide", methods=["GET"])
def migration_guide():

    """
    Hướng dẫn migrate từ v1 -> v2
    """

    return jsonify({
        "message": "Migration Guide v1 -> v2",

        "breaking_changes": [

            {
                "field": "amount",
                "v1": "string",
                "v2": "integer"
            },

            {
                "field": "card_number",
                "v1": "full card",
                "v2": "last 4 digits only"
            },

            {
                "field": "currency",
                "v1": "not supported",
                "v2": "required"
            }

        ],

        "timeline": [

            {
                "date": "2026-06-01",
                "event": "Release API v2"
            },

            {
                "date": "2026-09-01",
                "event": "Deprecate API v1"
            },

            {
                "date": "2026-12-01",
                "event": "Shutdown API v1"
            }

        ]
    })


# =========================================================
# ROOT
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Payment API Demo",
        "versions": [
            "/api/v1/payments",
            "/api/v2/payments"
        ]
    })


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)