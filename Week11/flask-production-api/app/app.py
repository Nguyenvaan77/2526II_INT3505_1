from flask import Flask, jsonify, request
from .logger import logger
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
import time

app = Flask(__name__)

# Setup Rate Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)

# Setup Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('flask_app_info', 'Flask Production API', version='1.0.0')

# Custom metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Duration',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP Requests'
)

RATE_LIMIT_EXCEEDED = Counter(
    'rate_limit_exceeded_total',
    'Total Rate Limit Exceeded',
    ['endpoint']
)


@app.before_request
def before_request():
    """Log incoming requests and track active requests"""
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()
    logger.info(
        f"[REQUEST] {request.method} {request.path} from {request.remote_addr}"
    )


@app.after_request
def after_request(response):
    """Log response and update metrics"""
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.path
        ).observe(duration)
        ACTIVE_REQUESTS.dec()
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    
    logger.info(
        f"[RESPONSE] {request.method} {request.path} - Status: {response.status_code}"
    )
    return response


@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    """Handle rate limit exceeded"""
    RATE_LIMIT_EXCEEDED.labels(endpoint=request.path).inc()
    logger.warning(
        f"[RATE LIMIT] {request.remote_addr} exceeded limit on {request.path}"
    )
    return jsonify({
        "error": "Rate limit exceeded",
        "message": str(e.description)
    }), 429


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Flask Production API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    }), 200


@app.route('/api/users')
@limiter.limit("10 per minute")
def users():
    """Get users list (limited to 10 requests per minute)"""
    logger.info("Fetching users list")
    return jsonify([
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]), 200


@app.route('/api/users/<int:user_id>')
@limiter.limit("15 per minute")
def get_user(user_id):
    """Get specific user (limited to 15 requests per minute)"""
    logger.info(f"Fetching user {user_id}")
    users_data = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
        3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    }
    
    if user_id in users_data:
        return jsonify(users_data[user_id]), 200
    else:
        logger.warning(f"User {user_id} not found")
        return jsonify({"error": "User not found"}), 404


@app.route('/metrics')
def metrics_endpoint():
    """Metrics endpoint for Prometheus"""
    return generate_latest(), 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    logger.info("Starting Flask Production API...")
    app.run(host='0.0.0.0', port=3000, debug=False)