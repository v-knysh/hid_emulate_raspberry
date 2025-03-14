import argparse
import signal
import getpass


from transport import ReportSender, ReportReceiver
from security import PasswordReportApplier, PasswordReportSender 


def prompt_password():
    print("input_password")
    password = getpass.getpass("> ")
    return password

def signal_handler(sig, frame):
    print("KeyboardInterrupt ignored. Use End button to stop")


def udp_client(ip, port, password):
    # used this so there is no need to install keyboard library in raspberry
    from keyboard_input import EventListener

    print(f"Started UDP client on {ip}:{port}...")
    report_sender = ReportSender(ip, port)
    password_report_sender = PasswordReportSender(password, report_sender)
    event_listener = EventListener(password_report_sender)
    event_listener.run()


def udp_server(ip, port, password):
    from hid import PlainReportApplier

    print(f"Started UDP server on {ip}:{port}...")
    plain_report_applier = PlainReportApplier()
    password_report_applier = PasswordReportApplier(password, plain_report_applier)
    report_receiver = ReportReceiver(ip, port, password_report_applier)
    report_receiver.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="UDP Client/Server")
    parser.add_argument("UDP_IP", type=str, help="IP address to send/receive UDP packets")
    parser.add_argument("UDP_PORT", type=int, help="Port number for UDP communication")
    parser.add_argument("--mode", "-m", type=str, choices=['server', 'client'], default='client', help="Server mode for raspberry, client mode for pc")
    
    args = parser.parse_args()

    password = prompt_password()

    if args.mode == "server":
        udp_server(args.UDP_IP, args.UDP_PORT, password)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        udp_client(args.UDP_IP, args.UDP_PORT, password)
