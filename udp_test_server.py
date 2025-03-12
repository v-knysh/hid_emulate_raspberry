import socket

# Set up the UDP socket
UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 5005  # Choose any port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")




while True:
    data, addr = sock.recvfrom(1024)  # Receive up to 1024 bytes
    print(f"Received from {addr}: {data}")
    write_report(data)
