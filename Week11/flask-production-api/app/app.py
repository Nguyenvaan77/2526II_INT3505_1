import os
import signal
import sys
from threading import Event
from uuid import uuid4
from flask import Flask, jsonify, request, g
from .logger import logger
from .config import Config
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
import time

app = Flask(__name__)
app.config.from_object(Config)

# Graceful shutdown event
shutdown_event = Event()

# Setup Rate Limiter with Redis backend
try:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[Config.RATE_LIMIT_DEFAULT],
        storage_uri=Config.REDIS_URL,
        storage_options={"connection_pool_kwargs": {"max_connections": 50}}
    )
    logger.info(f"Rate limiter configured with Redis: {Config.REDIS_URL}")
    REDIS_AVAILABLE = True
except Exception as e:
    logger.warning(f"Redis rate limiter initialization failed: {e}. Using memory storage.")
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[Config.RATE_LIMIT_DEFAULT],
        storage_uri="memory://"
    )
    REDIS_AVAILABLE = False

# Setup Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('flask_app_info', Config.API_NAME, version=Config.API_VERSION)

RATE_LIMIT_EXCEEDED = Counter(
    'rate_limit_exceeded_total',
    'Total Rate Limit Exceeded',
    ['endpoint']
)

# Application state tracking
STARTUP_COMPLETE = False
DEPENDENCIES_OK = {'redis': REDIS_AVAILABLE}


def handle_sigterm(signum, frame):
    """Handle SIGTERM signal for graceful shutdown"""
    logger.info("SIGTERM received - initiating graceful shutdown")
    shutdown_event.set()


# Register signal handlers
signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


@app.before_request
def add_request_context():
    """Add request ID and check shutdown status"""
    # Add request ID for tracing
    g.request_id = str(uuid4())
    
    # Check if server is shutting down
    if shutdown_event.is_set():
        logger.warning(f"Request rejected - server shutting down: {request.method} {request.path}")
        return jsonify({
            "error": "Server shutting down",
            "message": "Server is in graceful shutdown mode"
        }), 503
    
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()
    logger.info(
        f"[REQUEST] {request.method} {request.path} from {request.remote_addr} [ID: {g.request_id}]"
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
        f"[RESPONSE] {request.method} {request.path} - Status: {response.status_code} [ID: {g.get('request_id', 'unknown')}]"
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
        "message": Config.API_NAME,
        "version": Config.API_VERSION,
        "status": "running",
        "redis": "connected" if DEPENDENCIES_OK['redis'] else "disconnected"
    })


@app.route('/health')
def health():
    """Health check endpoint - basic liveness check"""
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "version": Config.API_VERSION,
        "dependencies": DEPENDENCIES_OK
    }), 200


@app.route('/startup')
def startup_probe():
    """K8s startup probe - checks if app is initialized"""
    global STARTUP_COMPLETE
    if STARTUP_COMPLETE:
        return jsonify({"status": "ready", "message": "Application started"}), 200
    else:
        return jsonify({"status": "initializing", "message": "Application is initializing"}), 503


@app.route('/ready')
def readiness_probe():
    """K8s readiness probe - checks if ready for traffic"""
    if not STARTUP_COMPLETE:
        return jsonify({"status": "not_ready", "message": "Application not initialized"}), 503
    
    # All checks passed
    return jsonify({
        "status": "ready",
        "message": "Application is ready for traffic",
        "dependencies": DEPENDENCIES_OK
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


def initialize_app():
    """Initialize application - check dependencies"""
    global STARTUP_COMPLETE, DEPENDENCIES_OK
    
    logger.info("Initializing application...")
    
    # Check Redis connection if available
    if REDIS_AVAILABLE:
        try:
            import redis
            r = redis.Redis.from_url(Config.REDIS_URL, socket_connect_timeout=Config.REDIS_TIMEOUT)
            r.ping()
            DEPENDENCIES_OK['redis'] = True
            logger.info("Redis connection verified")
        except Exception as e:
            DEPENDENCIES_OK['redis'] = False
            logger.warning(f"Redis connection check failed: {e}")
    
    STARTUP_COMPLETE = True
    logger.info("Application startup complete")


# Initialize app on first request (Flask 2.0+)
@app.before_first_request
def on_first_request():
    initialize_app()


if __name__ == '__main__':
    logger.info(f"Starting {Config.API_NAME}...")
    logger.info(f"Config: HOST={Config.HOST}, PORT={Config.PORT}, DEBUG={Config.DEBUG}")
    
    # Initialize before running
    initialize_app()
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, threaded=True)