from psycopg import Connection
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

DB_URI = "postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable"
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}
pool = ConnectionPool(DB_URI, min_size=1, max_size=10)

def get_checkpointer():
    with Connection.connect(DB_URI, **connection_kwargs) as conn:
        checkpointer = PostgresSaver(conn)
        # NOTE: you need to call .setup() the first time you're using your checkpointer
        checkpointer.setup()
        return checkpointer
    
def get_db_checkpointer():
    conn = pool.getconn()
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()
    return checkpointer