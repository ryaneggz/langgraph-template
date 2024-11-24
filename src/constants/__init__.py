

DB_URI = "postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable"
CONNECTION_POOL_KWARGS = {
    "autocommit": True,
    "prepare_threshold": 0,
}
DEFAULT_VECTOR_STORE_PATH = './sandbox/db/vectorstore.json'
