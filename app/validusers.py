from clickhouse_driver import Client
from .config import Config

client = Client(
    host=Config.CLICKHOUSE_HOST,
    user=Config.CLICKHOUSE_USER,
    password=Config.CLICKHOUSE_PASSWORD,
    secure=True,
    verify=False
)

def init_db():
    create_users_table()

def create_users_table():
    client.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id UUID,
        username String,
        password String
    ) ENGINE = MergeTree()
    ORDER BY (username)
    ''')

def insert_user(username, password):
    from .utils import hash_password
    hashed_password = hash_password(password)
    import uuid
    user_id = str(uuid.uuid4())
    client.execute(
        f"INSERT INTO users (id, username, password) VALUES ('{user_id}', '{username}', '{hashed_password.decode('utf-8')}')"
    )

def add_sample_users():
    insert_user("narendrr", "script#Testing123.")
    insert_user("shobhit", "shobhit@segwise")
