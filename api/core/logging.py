import logging
import sys
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Logging configuration
LOG_FILE = os.path.join(LOG_DIR, "api.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging():
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
        ]
    )

    # Disable excessive logging from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logger = logging.getLogger("quantai-api")
    logger.info("Logging initialized successfully.")
    return logger

# Create a global logger instance
logger = logging.getLogger("quantai-api")
