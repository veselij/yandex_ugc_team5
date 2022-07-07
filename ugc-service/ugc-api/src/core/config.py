import os

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

SENTRY_DSN = os.getenv(
    "SENTRY_DSN",
    "https://7e6a809a189147aab1b45d6065372088@o1305980.ingest.sentry.io/6548342",
)

LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "logstash")
LOGSTASH_PORT = os.getenv("LOGSTASH_PORT", 5044)
