# docker build -t rpsk .
# docker run -d -p 38172:38172 --name rpsk rpsk
import ctypes
import random
import socket
import time

HOST = "0.0.0.0"
PORT = 38172

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Listen for up to 5 connections
print(f"Listening for connections on {HOST}:{PORT}...")

class CTFChallenge:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.secret_value = ctypes.c_int(0)  # 32-bit signed integer

    def send(self, message):
        """Send a message to the client."""
        try:
            self.client_socket.sendall(message.encode() + b"\n")
        except:
            self.client_socket.close()
    def receive(self):
        """Receive input from the client."""
        try:
            return self.client_socket.recv(1024).decode().strip()
        except:
            self.client_socket.close()

    def add_points(self, points):
        self.secret_value.value += points 
        if self.secret_value.value < -10000000:  # Overflowed into negative
            self.send("SECURI-TAY{315cd75e7e1a5c34918b402851e3ebda}")
        else:
            self.send(f"Current points: {self.secret_value.value}")

    def show_points(self):
        self.send(f"You have {self.secret_value.value} points!")

    def menu(self):
        self.send("""
Welcome to my Rock Paper Scissors Game.
0. Shop
1. Play
2. View Points
3. Quit
4. Developer Mode 
5. Dev Mode (REMOVED)
6. Super Duper Secret Dev Mode (NOT WORKING)
Enter your choice:""")
        return self.receive()

    def shop(self):
        self.send("Welcome to my shop!\nYou want the flag... well luckily for you, I have it.")
        time.sleep(2)
        self.send("Prove to me computers are superior and lose 10,000,000 points, then I'll give you it.")

    def rps(self):
        options = ["r", "p", "s"]
        self.send("Please choose: Rock (R), Paper (P) or Scissors (S)")
        choice = self.receive().lower()
        comp_choice = random.choice(options)

        if choice == "r":
            if comp_choice == "r":
                self.send("You both chose Rock! No points added.")
            elif comp_choice == "p":
                self.secret_value.value -= 3
                self.send(f"Computer chose Paper, you lose 3 points! You now have: {self.secret_value.value} points")
            elif comp_choice == "s":
                self.secret_value.value += 3
                self.send(f"Computer chose Scissors, you win 3 points! You now have: {self.secret_value.value} points")

        elif choice == "p":
            if comp_choice == "p":
                self.send("You both chose Paper! No points added.")
            elif comp_choice == "r":
                self.secret_value.value += 3
                self.send(f"Computer chose Rock, you win 3 points! You now have: {self.secret_value.value} points")
            elif comp_choice == "s":
                self.secret_value.value -= 3
                self.send(f"Computer chose Scissors, you lose 3 points! You now have: {self.secret_value.value} points")

        elif choice == "s":
            if comp_choice == "s":
                self.send("You both chose Scissors! No points added.")
            elif comp_choice == "p":
                self.secret_value.value += 3
                self.send(f"Computer chose Paper, you win 3 points! You now have: {self.secret_value.value} points")
            elif comp_choice == "r":
                self.secret_value.value -= 3
                self.send(f"Computer chose Rock, you lose 3 points! You now have: {self.secret_value.value} points")
        else:
            self.send("Invalid choice. Please enter R, P, or S.")

    def special_rps(self):
        self.send(""">>> DEVELOPER MODE EXCLUSIVE <<<
New version of Rock Paper Scissors that includes a new move! Doesn't handle integers nicely so make sure to input correctly!""")
        options = ["r", "p", "s"]
        self.send("Please choose: Rock (R), Paper (P), Scissors (S) or Karate Chop (K)")
        choice = self.receive().lower()
        comp_choice = random.choice(options)

        if choice == "r":
            if comp_choice == "r":
                self.send("You both chose Rock! No points added.")
            elif comp_choice == "p":
                self.secret_value.value -= 3
                self.send(f"Computer chose Paper, you lose 3 points! You now have: {self.secret_value.value} points")
            elif comp_choice == "s":
                self.secret_value.value += 3
                self.send(f"Computer chose Scissors, you win 3 points! You now have: {self.secret_value.value} points")

        elif choice == "p":
            if comp_choice == "p":
                self.send("You both chose Paper! No points added.")
            elif comp_choice == "r":
                self.secret_value.value += 3
                self.send(f"Computer chose Rock, you win 3 points! You now have: {self.secret_value.value} points")
            elif comp_choice == "s":
                self.secret_value.value -= 3
                self.send(f"Computer chose Scissors, you lose 3 points! You now have: {self.secret_value.value} points")

        elif choice == "s":
            if comp_choice == "s":
                self.send("You both chose Scissors! No points added.")
            elif comp_choice == "p":
                self.secret_value.value += 3
                self.send(f"Computer chose Paper, you win 3 points! You now have: {self.secret_value.value} points")
            elif comp_choice == "r":
                self.secret_value.value -= 3
                self.send(f"Computer chose Rock, you lose 3 points! You now have: {self.secret_value.value} points")

        elif choice == "k":
            self.send("You might have won, you might have lost. Who knows.")
        else:
            try:
                temp = int(choice)
                if temp < 0:
                    self.send("Invalid Input.")
                else:
                    self.add_points(temp)
            except ValueError:
                self.send("Invalid Input.")

# Handle multiple clients
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    challenge = CTFChallenge(client_socket)

    try:
        while True:
            choice = challenge.menu()
            if choice is None:
                break
            if choice == "0":
                challenge.shop()
            elif choice == "1":
                challenge.rps()
            elif choice == "2":
                challenge.show_points()
            elif choice == "3":
                client_socket.close()
                break
            elif choice == "5":
                challenge.special_rps()
            else:
                challenge.send("Invalid option. You have lost one point.")
                challenge.add_points(-1)
    except (ValueError, ConnectionResetError):
        challenge.send("Connection closed.")
        client_socket.close()
