from flask import Flask
from .config import Config
from .auth import auth_bp
from .query import query_bp
from .upload import main_bp
from .validusers import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/main')
    app.register_blueprint(query_bp,url_prefix='/query')
    with app.app_context():
        init_db()
    return app
