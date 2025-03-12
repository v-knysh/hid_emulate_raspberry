import argparse
import logging

logger = logging.getLogger(__name__)

from transport import PlainReportSender, PlainReportReceiver

def udp_client(ip, port):
    from keyboard_input import EventListener

    logger.info(f"Started UDP client on {ip}:{port}...")
    report_sender = PlainReportSender(ip, port)
    event_listener = EventListener(report_sender)
    event_listener.run()


def udp_server(ip, port):
    from hid import PlainReportApplier

    logger.info(f"Started UDP server on {ip}:{port}...")
    plain_report_applier = PlainReportApplier()
    report_receiver = PlainReportReceiver(ip, port, plain_report_applier)
    report_receiver.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Client/Server")
    parser.add_argument("UDP_IP", type=str, help="IP address to send/receive UDP packets")
    parser.add_argument("UDP_PORT", type=int, help="Port number for UDP communication")
    parser.add_argument("--mode", "-m", type=str, choices=['server', 'client'], default='client', help="Server mode for raspberry, client mode for pc")
    
    args = parser.parse_args()

    if args.mode == "server":
        udp_server(args.UDP_IP, args.UDP_PORT)
    else:
        udp_client(args.UDP_IP, args.UDP_PORT)
