import json

from flask import Flask, request, jsonify, render_template, send_from_directory
import pymongo
import jwt
import bcrypt
import enum
import secrets
from jsonschema import validate, ValidationError
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB setup
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['book_db']

# JSON schemas
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

book_schema = {
    'file': {
        'type': 'object',
        'properties': {
            'filename': {'type': 'string'},
            'originalName': {'type': 'string'},
            'contentType': {'type': 'string'},
            'data': {'type': 'string'},
        },
        'required': ['filename', 'originalName', 'contentType'],  # Remove 'data' from required
    }
}
# Upload folder for images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Secret key for JWT
secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key




class UserRole(enum.Enum):
    NEW = 'new'
    STANDARD = 'standard'
    BANNED = 'banned'
    ADMIN = 'admin'


# Function to initialize admin user
# def initialize_admin_user():
#     admin_user = db.users.find_one({'email': 'admin@example.com'})
#     if admin_user is None:
#         admin_user = {
#             'full_name': 'admin admin',
#             'email': 'admin@example.com',
#             'password': bcrypt.hashpw('11111111'.encode('utf-8'), bcrypt.gensalt()),
#             'role': UserRole.ADMIN.value
#         }
#         db.users.insert_one(admin_user)


# Function to check if the uploaded file is allowed (e.g., images)
def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


@app.route('/', methods=['GET'])
def blank_page():
    return 'blank page'


# Route to render the registration form
@app.route('/register', methods=['GET'])
def render_registration_form():
    return render_template('registration.html')


# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()  # Extract form data

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


# Route to render the login form
@app.route('/login', methods=['GET'])
def render_login_form():
    return render_template('login.html')


# Route to handle user login
@app.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()  # Extract form data

    email = data['email']
    password = data['password']

    user = db.users.find_one({'email': email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid credentials', 'statusCode': 401}), 401

    token = jwt.encode({'email': user['email'], 'role': user['role']}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify(
        {'token': token, 'user_data': {'full_name': user['full_name'], 'email': user['email'], 'role': user['role']}}
    )


# # Route to get all books
# @app.route('/books', methods=['GET'])
# def get_all_books():
#     books = list(db.books.find())
#     return jsonify(books), 200


# # Route to filter books by author or label
# @app.route('/books/filter', methods=['POST'])
# def filter_books():
#     data = request.get_json()
#     author = data.get('author')
#     label = data.get('label')
#     query = {}
#     if author:
#         query['author_name'] = author
#     if label:
#         query['label'] = label
#
#     books = list(db.books.find(query))
#     return jsonify(books), 200


# # Route to get book details by ID
# @app.route('/books/<book_id>', methods=['GET'])
# def get_book_details(book_id):
#     existing_book = db.books.find_one({'_id': ObjectId(book_id)})
#     if not existing_book:
#         return jsonify({'message': 'Book not found', 'statusCode': 404}), 404
#     return jsonify(existing_book), 200


# # Route to create a new book
# @app.route('/books', methods=['POST'])
# def create_book():
#     data = request.get_json()
#
#     try:
#         validate(data, book_schema)
#     except ValidationError:
#         return jsonify({'message': 'Invalid data format', 'statusCode': 400}), 400
#
#     db.books.insert_one(data)
#     return jsonify({'message': 'Book created successfully', 'statusCode': 201}), 201


# # Route to update book by ID
# @app.route('/books/<book_id>', methods=['PUT'])
# def update_book(book_id):
#     data = request.get_json()
#
#     try:
#         validate(data, book_schema)
#     except ValidationError:
#         return jsonify({'message': 'Invalid data format', 'statusCode': 400}), 400
#
#     db.books.update_one({'_id': ObjectId(book_id)}, {'$set': data})
#     return jsonify({'message': 'Book updated successfully', 'statusCode': 200}), 200


# # Route to delete book by ID using /delete-book endpoint
# @app.route('/delete-book/<book_id>', methods=['DELETE'])
# def delete_book(book_id):
#     try:
#         result = db.books.delete_one({'_id': ObjectId(book_id)})
#         if result.deleted_count == 1:
#             return jsonify({'message': 'Book deleted successfully', 'statusCode': 200}), 200
#         else:
#             return jsonify({'message': 'Book not found', 'statusCode': 404}), 404
#     except Exception as e:
#         print(f'Database deletion error: {e}')
#         return jsonify({'message': 'Failed to delete book', 'statusCode': 500}), 500


# Route to delete book by ID
@app.route('/delete-book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        result = db.books.delete_one({'_id': ObjectId(book_id)})

        if result.deleted_count == 1:
            return jsonify({'message': 'Book deleted successfully', 'statusCode': 200}), 200
        else:
            return jsonify({'message': 'Book not found', 'statusCode': 404}), 404

    except pymongo.errors.ServerSelectionTimeoutError as server_error:
        print(f'MongoDB server selection error: {server_error}')
        return jsonify({'message': 'Database server selection error', 'statusCode': 500}), 500

    except Exception as e:
        print(f'Database deletion error: {e}')
        return jsonify({'message': 'Failed to delete book', 'statusCode': 500}), 500


# Route to render the add book form
@app.route('/add-book', methods=['GET'])
def render_add_book_form():
    return render_template('add-book.html')


@app.route('/add-book', methods=['POST'])
def add_book():
    data = request.form.to_dict()

    if 'file' not in request.files:
        return jsonify({'message': 'No file part', 'statusCode': 400}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file', 'statusCode': 400}), 400

    try:
        validate(data, book_schema)
    except ValidationError as e:
        print(f'Validation error: {e}')
        return jsonify({'message': 'Invalid data format', 'statusCode': 400}), 400

    file_data = {
        'filename': file.filename,
        'originalName': file.filename,
        'contentType': file.content_type,
        'data': file.read()
    }

    data['file'] = file_data

    try:
        db.books.insert_one(data)
        return jsonify({'message': 'Book added successfully', 'statusCode': 201}), 201
    except Exception as e:
        print(f'Database insertion error: {e}')
        return jsonify({'message': 'Failed to add book', 'statusCode': 500}), 500


# Route to render the update book form
@app.route('/update-book/<book_id>', methods=['GET'])
def render_update_book_form(book_id):
    existing_book = db.books.find_one({'_id': ObjectId(book_id)})
    if not existing_book:
        return jsonify({'message': 'Book not found', 'statusCode': 404}), 404
    return render_template('update-book.html', book=existing_book)


# Route to handle updating a book
@app.route('/update-book/<book_id>', methods=['POST'])
def update_existing_book(book_id):
    data = request.form.to_dict()  # Extract form data

    try:
        validate(data, book_schema)
    except ValidationError:
        return jsonify({'message': 'Invalid data format', 'statusCode': 400}), 400

    db.books.update_one({'_id': ObjectId(book_id)}, {'$set': data})
    return jsonify({'message': 'Book updated successfully', 'statusCode': 200}), 200


if __name__ == '__main__':
    # initialize_admin_user()
    app.run(debug=True, port=9271)