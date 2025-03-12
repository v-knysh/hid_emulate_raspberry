
import socket
import logging

logger = logging.getLogger(__name__)


class PlainReportSender:
    def __init__(self, udp_ip, udp_port):
        self._udp_ip = udp_ip
        self._udp_port = udp_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def apply(self, report):
        logger.debug(f"Sending to {self._udp_ip}: {report}")
        return self._sock.sendto(bytes(report), (self._udp_ip, self._udp_port))


class PlainReportReceiver:
    def __init__(self, udp_ip, udp_port, report_appllier):
        self._udp_ip = udp_ip
        self._udp_port = udp_port
        self._report_applier = report_appllier
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def run(self):
        self._sock.bind((self._udp_ip, self._udp_port))
        while True:
            data, addr = self._sock.recvfrom(1024)  # Receive up to 1024 bytes
            logger.debug(f"Received from {addr}: {data}")
            self._report_applier.apply(data)
            
            
