from Crypto.Cipher import ChaCha20
import os

NONCE_LENGTH = 12


def encrypt_chacha20(password: bytes, data: bytes):
    key = password.ljust(32, b'\x00')[:32]  # Ensure 32-byte key
    nonce = os.urandom(NONCE_LENGTH)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    encrypted_data = cipher.encrypt(data)
    return nonce + encrypted_data  # Send nonce with ciphertext

def decrypt_chacha20(password: bytes, encrypted_data: bytes):
    key = password.ljust(32, b'\x00')[:32]  # Ensure 32-byte key
    nonce = encrypted_data[:NONCE_LENGTH]  # 12-byte random nonce
    cipher = ChaCha20.new(key=key, nonce=nonce)
    decrypted_data = cipher.decrypt(encrypted_data[NONCE_LENGTH:])
    return decrypted_data


class PasswordReportApplier():
    def __init__(self, password_str, report_applier):
        self._password = password_str.encode('utf-8')
        self._report_applier = report_applier
    
    def apply(self, data):
        decrypted_report = decrypt_chacha20(self._password, data)
        print(f"decrypted_report: {decrypted_report}")
        self._report_applier.apply(decrypted_report)


class PasswordReportSender():
    def __init__(self, password_str, report_sender):
        self._password = password_str.encode('utf-8')
        self._report_sender = report_sender

    def apply(self, report):
        encrypted_report = encrypt_chacha20(self._password, report)
        self._report_sender.apply(encrypted_report)

if __name__ == "__main__":
    packet = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    password = b'1234'
    for i in range(2):

        print("password:         ", password)
        print('packet:           ', packet.hex())
        encrypted_packet = encrypt_chacha20(password, packet)
        print("encrypted_packet: ", encrypted_packet.hex())
        dectypted_packet = decrypt_chacha20(password, encrypted_packet)
        print("decrypted_packet: ", dectypted_packet.hex())
        print()
        


