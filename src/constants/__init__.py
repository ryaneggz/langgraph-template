import os

DB_URI = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql://admin:test1234@localhost:5432/postgres?sslmode=disable")
CONNECTION_POOL_KWARGS = {
    "autocommit": True,
    "prepare_threshold": 0,
}
DEFAULT_VECTOR_STORE_PATH = './sandbox/db/vectorstore.json'
