'''
Command                 Description
0x00 0x00 0x01 0x10     Login
0x00 0x00 0x01 0x11     Login Accepted
0x00 0x00 0x01 0xFF     Start Preview Stream
0x00 0x00 0x01 0x12     Alive Request
0x00 0x00 0x01 0x13     Alive Response
0x00 0x00 0xA0 0x34     Request Firmware Information
0x00 0x00 0xA0 0x35     Firmware Information Response
       1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64
admin: 61 64 6d 69 6e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
12345: 31 32 33 34 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
'''
import socket
import threading

host = '192.168.10.71'
port = 6666

controlSocket = socket.socket()
controlSocket.connect((host, port))

videoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
videoSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
videoSocket.bind(('0.0.0.0', 6840))

proxySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)


def login():
    print('Login!')
    controlSocket.send(bytes.fromhex('ab cd 00 81 00 00 01 10 61 64 6d 69 6e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 31 32 33 34 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'))
    print('Login Response:')
    print(controlSocket.recv(1024))
    print('Login Confirm!')
    controlSocket.send(bytes.fromhex('ab cd 00 00 00 00 01 13'))
    print('Confirm Response:')
    print(controlSocket.recv(1024))


def get_firmware_version():
    print('Request Firmware version!')
    controlSocket.send(bytes.fromhex('ab cd 00 00 00 00 a0 34'))
    print('Firmware version:')
    print(controlSocket.recv(1024))


def start_video_stream():
    print('Start video stream!')
    controlSocket.send(bytes.fromhex('ab cd 00 08 00 00 01 ff'))
    controlSocket.send(bytes.fromhex('ab cd 00 00 00 00 01 12'))


def ping():
    # print('Ping!')
    controlSocket.send(bytes.fromhex('ab cd 00 00 00 00 01 12'))
    # print('Pong:')
    # print(controlSocket.recv(1024))
    threading.Timer(3, ping).start()


def listen():
    print("Dump video stream:")
    while True:
        recvpack, payload = videoSocket.recvfrom(2048)
        control = recvpack.hex()[14:16]
        if control == "01":
            proxySocket.sendto(recvpack[8:], ('127.0.0.1', 8888))
        elif control == "02":
            continue


if __name__ == '__main__':
    login()
    get_firmware_version()
    start_video_stream()
    ping()
    listen()
