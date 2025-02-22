import socket
import re

# Define the target IP and correct port sequence
TARGET_IP = "ctf.securi-tay.co.uk"  # Change this to the actual server IP

# Regex to capture the next port from the server's message
PORT_PATTERN = r"knock on port (\d+)"

def knock_port(ip, port):
    """Attempts to connect to a port, then extracts the port to knock on next."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Increase timeout to handle faster connections
            s.connect((ip, port))
            response = s.recv(1024).decode().strip()
            print(f"[+] Knocked on {port}: {response}")

            # Use regex to determine the next port
            match = re.search(PORT_PATTERN, response)
            if match:
                next_port = int(match.group(1))
                print(f"[+] Next port to knock: {next_port}")
                return next_port
            else:
                print("[!] No further ports specified in the message.")
                # If no further port, check for flag port in the response
                flag_match = re.search(r"connect to port (\d+) for the flag", response)
                if flag_match:
                    flag_port = int(flag_match.group(1))
                    print(f"[+] Flag port found: {flag_port}")
                    return flag_port
                return None
    except Exception as e:
        print(f"[-] Failed to knock on {port}: {e}")
        return None

def get_flag(ip, port):
    """Connects to the flag port and prints the flag."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, port))
            flag = s.recv(1024).decode().strip()
            print(f"[🏁] Flag: {flag}")
    except Exception as e:
        print(f"[-] Failed to retrieve flag: {e}")

def solve_ctf():
    """Performs the full port knocking sequence and dynamically finds the flag port."""
    print("[*] Starting port knocking sequence...")

    current_port = 17751  # Starting port for the first knock

    while current_port is not None:
        current_port = knock_port(TARGET_IP, current_port)

        # If the flag port is found, break out of the loop and retrieve the flag
        if current_port == 9999:
            break

    print("[*] Knocking complete! Connecting to flag port...")
    get_flag(TARGET_IP, current_port)

if __name__ == "__main__":
    solve_ctf()
