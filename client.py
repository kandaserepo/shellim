import socket
from cryptography.fernet import Fernet
import threading

# Load encryption key
with open("server_key.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

def receive_messages(client_socket):
    """Handle incoming messages"""
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
            print(f"\nReceived message: {decrypted_message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def connect_to_server():
    """Connect to chat server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('tcp.cloudpub.ru', 57547))  # Для чата

    # Authentication
    user_id = input("Enter your ID: ")
    client_socket.send(cipher_suite.encrypt(user_id.encode()))

    password = input("Enter your password: ")
    client_socket.send(cipher_suite.encrypt(password.encode()))

    response = cipher_suite.decrypt(client_socket.recv(1024)).decode()
    print(response)

    if "Error" in response:
        client_socket.close()
        return

    # Start message receiving thread
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Message sending loop
    while True:
        receiver_id = input("Enter recipient ID: ")
        message = input("Enter message: ")

        full_message = f"{receiver_id}:{message}"
        encrypted_message = cipher_suite.encrypt(full_message.encode())
        client_socket.send(encrypted_message)

if __name__ == "__main__":
    connect_to_server()