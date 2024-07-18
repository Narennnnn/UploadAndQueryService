import sys
import os
import pytest
import jwt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config
from datetime import datetime, timedelta


class TestConfig(Config):
    TESTING = True
    CLICKHOUSE_HOST =Config.CLICKHOUSE_HOST
    CLICKHOUSE_USER = Config.CLICKHOUSE_USER
    CLICKHOUSE_PASSWORD = Config.CLICKHOUSE_PASSWORD
    JWT_SECRET = Config.JWT_SECRET


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token():
    token = jwt.encode({'exp': datetime.utcnow() + timedelta(hours=1)}, TestConfig.JWT_SECRET, algorithm='HS256')
    return token
