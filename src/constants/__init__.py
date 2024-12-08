import os

DB_URI = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable")
DB_URI_SANDBOX = os.getenv("POSTGRES_CONNECTION_STRING_SANDBOX", "postgresql://admin:test1234@localhost:5432/lg_template_agent?sslmode=disable")
CONNECTION_POOL_KWARGS = {
    "autocommit": True,
    "prepare_threshold": 0,
}
DEFAULT_VECTOR_STORE_PATH = './sandbox/db/vectorstore.json'
APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "test1234")
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
