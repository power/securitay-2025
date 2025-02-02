import socket
import select
import random
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345      # Port to listen on
TIMEOUT = 0.1       # Timeout in seconds
FLAG = 'SECURI-TAY{e73d93c13ccbc2ebd1907eee8e01bed6}'

# Create and configure the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Listen for up to 5 connections
print(f"Listening for connections on {HOST}:{PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")


    
    rand1 = random.randint(1,10)
    rand2 = random.randint(1,10)
    ans = rand1 * rand2
    question = f"What is {rand1}x{rand2}?"
    client_socket.sendall(question.encode())
    # Use select to wait for input with a timeout
    ready, _, _ = select.select([client_socket], [], [], TIMEOUT)
    if ready:
        data = client_socket.recv(1024).decode().strip()
        if data:
            print(f"Received: {data}")
            if (int(data) == ans):
                client_socket.sendall(FLAG.encode())
            else:
                client_socket.sendall(f"Echo: {data}\n".encode())
        else:
            print("Client sent empty data, closing connection.")
    else:
        print("No input received within the timeout. Closing connection.")
        client_socket.close()
    
