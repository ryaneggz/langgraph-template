import os
from dotenv import load_dotenv
load_dotenv()

HOST = str(os.getenv("HOST", "0.0.0.0"))
PORT = int(os.getenv("PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

DB_URI = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable")
DB_URI_SANDBOX = os.getenv("POSTGRES_CONNECTION_STRING_SANDBOX", "postgresql://admin:test1234@localhost:5432/lg_template_agent?sslmode=disable")
CONNECTION_POOL_KWARGS = {
    "autocommit": True,
    "prepare_threshold": 0,
}
DEFAULT_VECTOR_STORE_PATH = './sandbox/db/vectorstore.json'
APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "test1234")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO").upper()
APP_PORTAL_ENABLED = os.getenv("APP_PORTAL_ENABLED")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
