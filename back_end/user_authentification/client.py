import requests

BASE_URL = 'http://localhost:2005'


def register():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if len(password) < 8 and len(email) < 6:
        print('\nEmail must be at least 6 characters long, '
              'and password 8 or more')
        return

    data = {'email': email, 'password': password}
    response = requests.post(f"{BASE_URL}/register", json=data)

    if response.status_code == 201:
        print('\nRegistration successful.')
    else:
        print(f'\nRegistration failed: {response.json()["message"]}')


def login():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    data = {'email': email, 'password': password}
    response = requests.post(f'{BASE_URL}/login', json=data)

    if response.status_code == 200:
        print('\nLogin successful.')
    else:
        print(f'\nLogin failed: {response.json()["message"]}')


def logout():
    email = input('Enter your email: ')
    data = {'email': email}
    response = requests.post(f'{BASE_URL}/logout', json=data)

    if response.status_code == 200:
        print('\nLogout successful.')
    else:
        print('\nLogout failed. Status code:', response.status_code)
        # print(response)


# def request_password_reset():
#     email = input('Enter your email: ')
#     data = {'email': email}
#     response = requests.post(f'{BASE_URL}/password-reset-request', json=data)
#
#     if response.status_code == 200:
#         print('\nPassword reset link sent. Check your email for instructions.')
#     else:
#         print(f'\nPassword reset request failed: {response.json()["message"]}')

def request_password_reset():
    email = input('Enter your email: ')
    token = 'picsart academy'

    data = {'email': email, 'token': token}
    response = requests.post(f'{BASE_URL}/password-reset-request', json=data)

    if response.status_code == 200:
        print('\nPassword reset link sent. Check your email for instructions.')
    else:
        print(f'\nPassword reset request failed: {response.json()["message"]}')


def reset_password():
    email = input('Enter your email: ')
    token = input('Enter the password reset token: ')
    new_password = input('Enter your new password: ')

    data = {'email': email, 'token': token, 'new_password': new_password}
    response = requests.post(f'{BASE_URL}/password-reset', json=data)

    if response.status_code == 200:
        print('\nPassword reset successful. You can now log in with your new password.')
    else:
        print(f'\nPassword reset failed: {response.json()["message"]}')


def foo():
    while True:
        print('\nMenu:')
        print('1. Register')
        print('2. Login')
        print('3. Logout')
        print('4. Request Password Reset')
        print('5. Reset Password')
        print('6. Quit')

        choice = input('\nEnter your choice: ')

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            logout()
        elif choice == '4':
            request_password_reset()
        elif choice == '5':
            reset_password()
        elif choice == '6':
            break
        else:
            print('\nInvalid choice. Please try again.')


if __name__ == '__main__':
    foo()
