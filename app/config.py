import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST')
    CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER')
    CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')
    JWT_SECRET = os.getenv('JWT_SECRET')
