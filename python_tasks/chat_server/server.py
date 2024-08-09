"""Server module"""

import socket
import threading

clients = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))


def remove_client(client: socket.socket):
    """
         Removes a client's socket from the list of connected clients.
    """

    if client in clients:
        client.close()
        clients.remove(client)


def broadcast_message(message: str, sender: socket.socket):
    """
         Broadcasts a message to all connected clients except the sender.
    """

    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except Exception('Client disconnected') as e:
                print(e)
                remove_client(client)


def handle_client(client: socket.socket, address: tuple):
    """
        Handles communication with a client.
    """

    print(f'{address} connected')

    try:
        client.send("hi ".encode())

        while True:
            message = client.recv(1024).decode()
            if message.lower() == 'exit':
                break
            broadcast_message(f'{address}: {message}', client)

    except 'Client disconnected' as e:
        print(e)

    finally:
        remove_client(client)
        return True


def start_server():
    """
         Starts the chat server and listens for incoming connections.
    """

    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
