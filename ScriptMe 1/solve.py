import socket
import re

HOST = '127.0.0.1'  # Server IP (change if needed)
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive the question from the server
question = client_socket.recv(1024).decode()
print("Server:", question)

# Extract numbers from the question (e.g., "What is 3x4?")
match = re.search(r'(\d+)x(\d+)', question)
if match:
    num1, num2 = int(match.group(1)), int(match.group(2))
    answer = str(num1 * num2)  # Solve the multiplication
    client_socket.sendall(answer.encode())  # Send answer immediately

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print("Server response:", response)

client_socket.close()
