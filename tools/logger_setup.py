import logging
from logging.handlers import RotatingFileHandler
import os
from  tools.config_reader import ConfigurationReader

def setup_logger(name=None):
    config = ConfigurationReader().get_logging_config()

    log_dir = config.get("log_dir", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, config.get("log_filename", "app.log"))

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.get("log_level", "INFO").upper()))

    handler = RotatingFileHandler(
        log_path,
        maxBytes=config.get("max_bytes", 2048),
        backupCount=config.get("backup_count", 5)
    )

    formatter = logging.Formatter(
        config.get("log_format"),
        config.get("time_format")
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# logger = setup_logger()
# logger.info("hi this is testing")