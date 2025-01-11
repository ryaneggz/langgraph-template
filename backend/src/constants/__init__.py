import os
import json
import base64
from dotenv import load_dotenv
load_dotenv()

# Server
HOST = str(os.getenv("HOST", "0.0.0.0"))
PORT = int(os.getenv("PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# App
DEFAULT_VECTOR_STORE_PATH = './sandbox/db/vectorstore.json'
DEFAULT_APP_USER_LIST = '[{"username": "admin", "password": "test1234", "name": "Admin User", "email": "admin@example.com"}]'
APP_USER_LIST = json.loads(base64.b64decode(os.getenv("APP_USER_LIST", DEFAULT_APP_USER_LIST)).decode('utf-8') + b'==')
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO").upper()

# Database
DB_URI = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable")
DB_URI_SANDBOX = os.getenv("POSTGRES_CONNECTION_STRING_SANDBOX", "postgresql://admin:test1234@localhost:5432/lg_template_agent?sslmode=disable")
CONNECTION_POOL_KWARGS = {
    "autocommit": True,
    "prepare_threshold": 0,
}

# LLM API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
