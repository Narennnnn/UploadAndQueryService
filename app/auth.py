from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from clickhouse_driver import Client
from .config import Config
from .utils import check_password
from .usersSchema import insert_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

client = Client(
    host=Config.CLICKHOUSE_HOST,
    user=Config.CLICKHOUSE_USER,
    password=Config.CLICKHOUSE_PASSWORD,
    secure=True,
    verify=False
)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if user already exists
    query = f"SELECT password FROM users WHERE username='{username}'"
    try:
        result = client.execute(query)
        if result:
            stored_password = result[0][0]
            if check_password(stored_password, password):
                return jsonify({'message': 'User already registered. Try to login.'}), 400
            else:
                return jsonify({'message': 'Username already taken with a different password. Try a different username or reset your password.'}), 400

        # If user does not exist, insert the new user
        insert_user(username, password)
        return jsonify({'message': 'User registered successfully.'}), 200
    except Exception as e:
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    query = f"SELECT password FROM users WHERE username='{username}'"

    try:
        result = client.execute(query)
        if result:
            stored_password = result[0][0]
            if check_password(stored_password, password):
                token = jwt.encode({'exp': datetime.utcnow() + timedelta(hours=1)}, Config.JWT_SECRET, algorithm='HS256')
                print("Login Successfully!")
                return jsonify({'token': token}), 200
            else:
                print("Incorrect password!")
        else:
            print("Username not found!")
    except Exception as e:
        print(f"Failed to execute query: {str(e)}")

    return jsonify({'message': 'Invalid Credentials'}), 401
