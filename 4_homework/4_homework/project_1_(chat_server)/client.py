"""Client module"""

import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))


def receive_messages():
    """
        Receives and displays messages from the chat server.
    """

    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except Exception('client_disconnected') as e:
            print(e)
            break


def send_message():
    """
        Sends messages to the chat server.
    """

    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode())

        if message.lower() == 'exit':
            break

    client_socket.close()


if __name__ == "__main__":
    print('Connected to the chat server.')
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_message()
