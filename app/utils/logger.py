# FILE: app/utils/logger.py

import logging
import os

LOG_FILE_PATH = "logs/app.log"

# Create logs directory if missing
os.makedirs("logs", exist_ok=True)

# Configure logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def log_warning(message: str):
    logging.warning(message)
