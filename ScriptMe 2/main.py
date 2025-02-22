import socket
import time
import threading
# docker build -t scriptme2 .
# docker run -d -p 17751:17751 -p 39112:39112 -p 36214:36214 -p 9999:9999 --name scriptme2 scriptme2




# Define the correct port sequence
CORRECT_SEQUENCE = [17751, 39112, 36214]
active_knocks = {}  # Stores { "IP": [knock sequence] }
knock_timestamps = {}  # Stores { "IP": last knock time }

# Time limit (seconds) between knocks before reset
TIMEOUT = 1

def handle_knock(client_socket, client_ip, port):
    current_time = time.time()

    # Reset if they took too long
    if client_ip in knock_timestamps and (current_time - knock_timestamps[client_ip] > TIMEOUT):
        #print(f"[-] {client_ip} took too long! Resetting sequence.")
        active_knocks[client_ip] = []
        send_message(client_socket, "Timeout! Start again.")
        client_socket.close()
        return

    # Initialize if first knock
    if client_ip not in active_knocks:
        active_knocks[client_ip] = []

    sequence = active_knocks[client_ip]

    # Check if the next port is correct
    if len(sequence) < len(CORRECT_SEQUENCE) and port == CORRECT_SEQUENCE[len(sequence)]:
        sequence.append(port)
        knock_timestamps[client_ip] = current_time  # Update timestamp
        #print(f"[+] {client_ip} knocked {port} correctly!")

        # Send progress message and close connection
        if len(sequence) < len(CORRECT_SEQUENCE):
            send_message(client_socket, f"Good! Now knock on port {CORRECT_SEQUENCE[len(sequence)]}.")
        else:
            #print(f"[+] {client_ip} unlocked the flag!")
            send_message(client_socket, "Correct sequence! Now connect to port 9999 for the flag.")
            send_flag(client_ip)
            del active_knocks[client_ip]  # Reset their state after success
            del knock_timestamps[client_ip]

    else:
        #print(f"[-] {client_ip} knocked {port} incorrectly. Resetting sequence.")
        send_message(client_socket, "Wrong port! Start over.")
        active_knocks[client_ip] = []  # Reset sequence on failure
        knock_timestamps[client_ip] = current_time  # Reset timestamp

    # Close the connection after handling the knock
    client_socket.close()

def send_message(client_socket, message):
    try:
        client_socket.sendall(message.encode() + b"\n")
    except Exception as e:
        print(f"[!] Failed to send message: {e}")

def send_flag(client_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as flag_server:
        flag_server.bind(("0.0.0.0", 9999))
        flag_server.listen(1)
        #print("[*] Waiting for player to connect on port 9999 for the flag...")

        conn, addr = flag_server.accept()
        if addr[0] == client_ip: # if the users address is the one passed from previous functions, send the flag
            conn.sendall(b"SECURI-TAY{b830f274b91316b09d6ac6ec658cc83d}\n")
        conn.close()

def start_knock_listener(): # handle connections
    server_sockets = {}
    
    for port in CORRECT_SEQUENCE:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port))
        s.listen(5)
        server_sockets[port] = s
        print(f"[*] Listening on port {port} for knocks...")

    try:
        while True:
            for port, server in server_sockets.items():
                client_socket, client_address = server.accept()
                threading.Thread(target=handle_knock, args=(client_socket, client_address[0], port)).start()
    except KeyboardInterrupt:
        #print("\n[!] Shutting down server.")
        for server in server_sockets.values():
            server.close()

if __name__ == "__main__":
    start_knock_listener()
