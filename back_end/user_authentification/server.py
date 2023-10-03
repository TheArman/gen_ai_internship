from flask import Flask, request, jsonify
import json
import bcrypt
import secrets
import time

app = Flask(__name__)

users = []
authorized_users = []
password_reset_tokens = {}

try:
    with open('users.json', 'r') as users_file:
        users = json.load(users_file)
except (FileNotFoundError, json.JSONDecodeError):
    users = []

try:
    with open('authorized.json', 'r') as authorized_file:
        authorized_users = json.load(authorized_file)
except (FileNotFoundError, json.JSONDecodeError):
    authorized_users = []


def save_users():
    with open('users.json', 'w') as users_file:
        json.dump(users, users_file, indent=4)


def save_authorized_users():
    with open('authorized.json', 'w') as authorized_file:
        json.dump(authorized_users, authorized_file, indent=4)


def user_exists(email):
    for user in users:
        if user['email'] == email:
            return True
    return False


@app.route('/')
def blank():
    return 'Blank'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'statusCode': 400, 'message': 'Email and password are required'}), 400

    if user_exists(email):
        return jsonify({'statusCode': 409, 'message': 'This email already used'}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users.append({'email': email, 'password': hashed_password})
    save_users()

    return jsonify({'statusCode': 201, 'message': 'Successfully added'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'statusCode': 400, 'message': 'Email and password are required'}), 400

    user = next((user for user in users if user['email'] == email), None)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        authorized_users.append({'email': email})
        save_authorized_users()
        return jsonify({'statusCode': 200, 'message': 'Logged in', 'user_data': {'email': email}}), 200

    return jsonify({'statusCode': 401, 'message': 'Authentication failed'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    email = data.get('email')

    global authorized_users

    if any(user['email'] == email for user in authorized_users):
        authorized_users = [user for user in authorized_users if user['email'] != email]
        save_authorized_users()
        return jsonify({'statusCode': 200, 'message': 'Logged out'}), 200
    return jsonify({'statusCode': 401, 'message': 'Not logged in'}), 401


# @app.route('/password-reset-request', methods=['POST'])
# def password_reset_request():
#     data = request.get_json()
#     email = data.get('email')
#
#     user = next((user for user in users if user['email'] == email), None)
#
#     if not user:
#         return jsonify({'statusCode': 404, 'message': 'Email not found'}), 404
#
#     token = secrets.token_hex(16)
#     password_reset_tokens[email] = {
#         'token': token,
#         'expiration_time': time.time() + 3600
#     }
#
#     return jsonify({'statusCode': 200, 'message': 'Password reset link sent'}), 200


@app.route('/password-reset-request', methods=['POST'])
def password_reset_request():
    data = request.get_json()
    email = data.get('email')

    user = next((user for user in users if user['email'] == email), None)

    if not user:
        return jsonify({'statusCode': 404, 'message': 'Email not found'}), 404

    # Set a fixed token value of "picsart academy"
    token = 'picsart academy'

    password_reset_tokens[email] = {
        'token': token,
        'expiration_time': time.time() + 3600
    }

    return jsonify({'statusCode': 200, 'message': 'Password reset link sent'}), 200


@app.route('/password-reset', methods=['POST'])
def password_reset():
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('new_password')

    user = next((user for user in users if user['email'] == email), None)

    if not user:
        return jsonify({'statusCode': 404, 'message': 'Email not found'}), 404

    token_info = password_reset_tokens.get(email)
    if not token_info or token_info['token'] != token or time.time() > token_info['expiration_time']:
        return jsonify({'statusCode': 401, 'message': 'Invalid or expired token'}), 401

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user['password'] = hashed_password
    save_users()

    del password_reset_tokens[email]

    return jsonify({'statusCode': 200, 'message': 'Password reset successful'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=2005)
