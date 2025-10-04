import logging
import logging.config
from pythonjsonlogger import jsonlogger
import os


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    logHandler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(logHandler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.info("Logging initialized", extra={"level": log_level})
