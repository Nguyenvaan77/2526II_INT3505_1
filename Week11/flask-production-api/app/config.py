import os
from datetime import timedelta


class Config:
    """Application configuration from environment variables"""
    
    # Flask
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Server
    PORT = int(os.getenv('PORT', 3000))
    HOST = os.getenv('HOST', '0.0.0.0')
    WORKERS = int(os.getenv('WORKERS', 4))
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
    REDIS_TIMEOUT = int(os.getenv('REDIS_TIMEOUT', 5))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    JSON_LOGS = os.getenv('JSON_LOGS', 'False').lower() == 'true'
    
    # API
    API_VERSION = os.getenv('API_VERSION', '1.0.0')
    API_NAME = os.getenv('API_NAME', 'Flask Production API')
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '100 per hour')
    
    # Graceful shutdown timeout (seconds)
    GRACEFUL_SHUTDOWN_TIMEOUT = int(os.getenv('GRACEFUL_SHUTDOWN_TIMEOUT', 30))
    
    # Health check timeout
    HEALTH_CHECK_TIMEOUT = int(os.getenv('HEALTH_CHECK_TIMEOUT', 5))
