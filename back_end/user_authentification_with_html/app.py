from flask import Flask, request, render_template, session
import json
import bcrypt
import time

app = Flask(__name__)

app.secret_key = 'secret_key'

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
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return render_template('index.html', message='Email and password are required')

    if user_exists(email):
        return render_template('index.html', message='This email is already used')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users.append({'email': email, 'password': hashed_password})
    save_users()

    return render_template('index.html', message='Registration successful')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return render_template('index.html', message='Email and password are required'), 400

    user = next((user for user in users if user['email'] == email), None)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        existing_user = next((au for au in authorized_users if au['email'] == email), None)
        if existing_user:
            authorized_users.remove(existing_user)

        session['email'] = email
        authorized_users.append({'email': email})
        save_authorized_users()

        return render_template('index.html', message='Logged in')

    return render_template('index.html', message='Authentication failed'), 401


@app.route('/logout', methods=['POST'])
def logout():
    email = request.form.get('email')

    global authorized_users

    if any(user['email'] == email for user in authorized_users):
        authorized_users = [user for user in authorized_users if user['email'] != email]
        save_authorized_users()
        session.pop('email', None)
        message = 'Logged out successfully'
    else:
        message = 'Not logged in'

    return render_template('index.html', message=message)


@app.route('/password-reset-request', methods=['POST'])
def password_reset_request():
    email = request.form.get('email')

    user = next((user for user in users if user['email'] == email), None)

    if not user:
        return render_template('index.html', message='Email not found'), 404

    # Set a fixed token value of "picsart academy"
    token = 'picsart academy'

    password_reset_tokens[email] = {
        'token': token,
        'expiration_time': time.time() + 3600
    }

    return render_template('index.html', message='Password reset link sent')


@app.route('/password-reset', methods=['POST'])
def password_reset():
    email = request.form.get('email')
    token = request.form.get('token')
    new_password = request.form.get('new_password')

    user = next((user for user in users if user['email'] == email), None)

    if not user:
        return render_template('index.html', message='Email not found'), 404

    token_info = password_reset_tokens.get(email)
    if not token_info or token_info['token'] != token or time.time() > token_info['expiration_time']:
        return render_template('index.html', message='Invalid or expired token'), 401

    for existing_user in authorized_users:
        if existing_user['email'] == email:
            authorized_users.remove(existing_user)
            break

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user['password'] = hashed_password
    save_users()
    save_authorized_users()

    del password_reset_tokens[email]

    return render_template('index.html', message='Password reset successful')


if __name__ == '__main__':
    app.run(debug=True, port=2005)
