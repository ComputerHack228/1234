import socket
import threading

def handle_client(client_socket, address):
    print(f"New connection from {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{address}: {message}")
            broadcast(message, client_socket)
        except ConnectionResetError:
            break
    print(f"Connection from {address} closed.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Use public IP for external connections
    server.listen(5)
    print("Server started on port 5555...")
    
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

def start_client(server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 5555))
    
    def receive_messages():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                print(message)
            except ConnectionResetError:
                break
    
    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()
    
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break
        client.send(message.encode('utf-8'))
    client.close()

clients = []

if __name__ == "__main__":
    choice = input("Start as (server/client): ").strip().lower()
    if choice == "server":
        start_server()
    elif choice == "client":
        server_ip = input("Enter server IP: ").strip()
        start_client(server_ip)
    else:
        print("Invalid choice. Exiting.")
