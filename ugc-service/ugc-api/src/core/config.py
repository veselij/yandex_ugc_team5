import logging
import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "API film watch timestamp")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

AUTH_URL = os.getenv("AUTH_URL", "http://127.0.0.1:82/api/v1/roles/user/check")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILENAME = os.getenv("LOG_FILENAME", "backoff.log")

KAFKA_BROKER_HOST = os.getenv("KAFKA_BROKER_HOST", "127.0.0.1")
KAFKA_BROKER_PORT = int(os.getenv("KAFKA_BROKER_PORT", 29092))
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "movies")

NO_AUTH = os.getenv("NO_AUTH", "True") == "True"
TEST_UUID = "1ef50a24-dff0-4b69-9351-2936f098825d"

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler(filename=LOG_FILENAME)
fh.setFormatter(formatter)
logger.addHandler(fh)
