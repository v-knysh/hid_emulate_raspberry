import socket


class ReportSender:
    def __init__(self, udp_ip, udp_port):
        self._udp_ip = udp_ip
        self._udp_port = udp_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def apply(self, data):
        print(f"Sending to {self._udp_ip}: {data.hex()}")
        return self._sock.sendto(data, (self._udp_ip, self._udp_port))


class ReportReceiver:
    def __init__(self, udp_ip, udp_port, report_appllier):
        self._udp_ip = udp_ip
        self._udp_port = udp_port
        self._report_applier = report_appllier
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def run(self):
        self._sock.bind((self._udp_ip, self._udp_port))
        while True:
            data, addr = self._sock.recvfrom(1024)  # Receive up to 1024 bytes
            print(f"Received from {addr}: {data.hex()}")
            self._report_applier.apply(data)
            
            
