import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Create logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.DEBUG)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Enhanced formatter with more details
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler with rotation
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=5000000,  # 5MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler for real-time logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Additional file for errors
error_file_handler = RotatingFileHandler(
    'logs/error.log',
    maxBytes=5000000,  # 5MB
    backupCount=3
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
logger.addHandler(error_file_handler)

logger.info(f"Logger initialized at {datetime.now()}")