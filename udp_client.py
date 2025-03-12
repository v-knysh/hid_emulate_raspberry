import socket
import time 

# Set the Raspberry Pi's IP and port
UDP_IP = "192.168.1.220"  # Replace with the Raspberry Pi's actual IP
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    message = input("Enter message: ")
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"Sent: {message}")
