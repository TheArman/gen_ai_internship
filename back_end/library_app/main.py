from flask import Flask, request, jsonify, render_template, make_response
import pymongo
import jwt
import bcrypt
import enum
import secrets
from jsonschema import validate, ValidationError

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['book_db']

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
        'required': ['filename', 'originalName', 'contentType'],
    }
}

secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key


class UserRole(enum.Enum):
    NEW = 'new'
    STANDARD = 'standard'
    BANNED = 'banned'
    ADMIN = 'admin'


book_id_counter = 1


@app.route('/', methods=['GET'])
def blank_page():
    return 'blank page'


@app.route('/register', methods=['GET'])
def render_registration_form():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()

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


@app.route('/login', methods=['GET'])
def render_login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()

    email = data['email']
    password = data['password']

    user = db.users.find_one({'email': email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid credentials', 'statusCode': 401}), 401

    token = jwt.encode({'email': user['email'], 'role': user['role']}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify(
        {'token': token, 'user_data': {'full_name': user['full_name'], 'email': user['email'], 'role': user['role']}}
    )


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

    global book_id_counter
    data['book_id'] = book_id_counter
    book_id_counter += 1

    data['file'] = file_data

    try:
        db.books.insert_one(data)
        return jsonify({'message': 'Book added successfully', 'statusCode': 201}), 201
    except Exception as e:
        print(f'Database insertion error: {e}')
        return jsonify({'message': 'Failed to add book', 'statusCode': 500}), 500


@app.route('/update-book/<string:book_id>', methods=['GET'])
def render_update_book_form(book_id):
    existing_book = db.books.find_one({'book_id': int(book_id)})
    if not existing_book:
        return jsonify({'message': 'Book not found', 'statusCode': 404}), 404
    return render_template('update-book.html', book=existing_book)  # Pass the book data to the template


@app.route('/update-book/<string:book_id>', methods=['POST'])
def update_existing_book(book_id):
    data = request.form.to_dict()

    try:
        validate(data, book_schema)
    except ValidationError:
        return jsonify({'message': 'Invalid data format', 'statusCode': 400}), 400

    existing_book = db.books.find_one({'book_id': int(book_id)})
    if not existing_book:
        return jsonify({'message': 'Book not found', 'statusCode': 404}), 404

    db.books.update_one({'book_id': int(book_id)}, {'$set': data})
    return jsonify({'message': 'Book updated successfully', 'statusCode': 200}), 200


@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
        delete in browser don't working

        for delete book, in terminal write this line`
            ➔ curl -X DELETE http://127.0.0.1:9271/delete-book/1

    """

    book = db.books.find_one({'book_id': book_id})

    if book is None:
        return jsonify({'message': 'Book not found', 'statusCode': 404}), 404

    result = db.books.delete_one({'book_id': book_id})

    if result.deleted_count == 1:
        return jsonify({'message': 'Book deleted successfully', 'statusCode': 200}), 200
    else:
        return jsonify({'message': 'Failed to delete book', 'statusCode': 500}), 500


@app.route('/book/<int:book_id>', methods=['GET'])
def view_book(book_id):
    book = db.books.find_one({'book_id': book_id})

    if book is None:
        return jsonify({'message': 'Book not found', 'statusCode': 404}), 404

    return render_template('book-details.html', book=book)


@app.route('/download/<int:book_id>', methods=['GET'])
def download_book(book_id):
    book = db.books.find_one({'book_id': book_id})

    if book is None:
        return jsonify({'message': 'Book not found', 'statusCode': 404}), 404

    book_data = book.get('file', {})

    if not book_data:
        return jsonify({'message': 'Book file not found', 'statusCode': 404}), 404

    response = make_response(book_data['data'])
    response.headers['Content-Type'] = book_data['contentType']
    response.headers['Content-Disposition'] = f'attachment; filename={book_data["filename"]}'
    return response


@app.route('/books', methods=['GET'])
def get_all_books():
    books = list(db.books.find())

    if not books:
        return jsonify({'message': 'No books found', 'statusCode': 404}), 404

    books_data = [{'book_id': book['book_id'], 'name': book.get('name', ''), 'author_name': book.get('author_name', ''),
                   'label': book.get('label', '')} for book in books]

    return jsonify(books_data), 200


if __name__ == '__main__':
    app.run(debug=True, port=9271)
