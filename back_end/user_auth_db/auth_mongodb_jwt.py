from flask import Flask, request, jsonify
import pymongo
import jwt
import bcrypt
import enum
import secrets
from jsonschema import validate, ValidationError

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['secret_db']

user_schema = {
    'type': 'object',
    'properties': {
        'full_name': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'},
        'role': {'type': 'string', 'enum': ['new', 'standard', 'banned', 'admin']}
    },
    'required': ['email', 'password']
}

secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key


class UserRole(enum.Enum):
    NEW = 'new'
    STANDARD = 'standard'
    BANNED = 'banned'
    ADMIN = 'admin'


def initialize_admin_user():
    admin_user = db.users.find_one({'email': 'admin@example.com'})
    if admin_user is None:
        admin_user = {
            'full_name': 'admin admin',
            'email': 'admin@example.com',
            'password': bcrypt.hashpw('11111111'.encode('utf-8'), bcrypt.gensalt()),
            'role': UserRole.ADMIN.value
        }
        db.users.insert_one(admin_user)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        validate(data, user_schema)
    except ValidationError:
        return jsonify({'message': 'Invalid data format', 'statusCode': 400}), 400

    full_name = data.get('full_name', '')
    email = data['email']
    password = data['password']
    role = data.get('role', 'new')

    existing_user = db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'This email is already in use', 'statusCode': 409}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        'full_name': full_name,
        'email': email,
        'password': hashed_password,
        'role': role
    }
    db.users.insert_one(new_user)

    return jsonify({'message': 'Successfully added', 'statusCode': 201}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = db.users.find_one({'email': email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid credentials', 'statusCode': 401}), 401

    token = jwt.encode({'email': user['email'], 'role': user['role']}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify(
        {'token': token, 'user_data': {'full_name': user['full_name'], 'email': user['email'], 'role': user['role']}}
    )


@app.route('/change-role/<user_email>', methods=['PUT'])
def change_role(user_email):
    data = request.get_json()
    new_role = data.get('new_role', '').lower()

    if new_role not in [UserRole.STANDARD.value, UserRole.BANNED.value]:
        return jsonify({'message': 'Invalid role change', 'statusCode': 400}), 400

    admin_user = db.users.find_one({'email': user_email})
    if not admin_user or admin_user['role'] != UserRole.ADMIN.value:
        return jsonify({'message': 'Unauthorized', 'statusCode': 403}), 403

    user_to_update = db.users.find_one({'email': data['email']})
    if not user_to_update:
        return jsonify({'message': 'User not found', 'statusCode': 404}), 404

    if new_role == UserRole.BANNED.value and user_to_update['role'] == UserRole.NEW.value:
        return jsonify({'message': 'Cannot ban a new user', 'statusCode': 400}), 400

    db.users.update_one({'email': data['email']}, {'$set': {'role': new_role}})
    return jsonify({'message': 'Role changed successfully', 'statusCode': 200}), 200


@app.route('/get-all-users', methods=['GET'])
def get_all_users():
    admin_user = db.users.find_one({'email': request.json.get('email')})
    if not admin_user or admin_user['role'] != UserRole.ADMIN.value:
        return jsonify({'message': 'Unauthorized', 'statusCode': 403}), 403

    users = list(db.users.find({}, {'_id': False, 'password': False}))
    return jsonify(users)


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    # Check if admin
    admin_user = db.users.find_one({'email': request.json.get('email')})
    if not admin_user or admin_user['role'] != UserRole.ADMIN.value:
        return jsonify({'message': 'Unauthorized', 'statusCode': 403}), 403

    full_name = data.get('full_name', '')
    email = data['email']
    password = data['password']
    role = data.get('role', 'new')

    existing_user = db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'This email is already in use', 'statusCode': 409}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        'full_name': full_name,
        'email': email,
        'password': hashed_password,
        'role': role
    }
    db.users.insert_one(new_user)

    return jsonify({'message': 'User added successfully', 'statusCode': 201}), 201


if __name__ == '__main__':
    initialize_admin_user()
    app.run(debug=True)
