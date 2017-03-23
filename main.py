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
import signal
import sys
import struct

host = '192.168.10.65'
port = 6666

controlSocket = socket.socket()
controlSocket.connect((host, port))

videoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
videoSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
videoSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)
videoSocket.bind(('0.0.0.0', 6840))

proxySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)

__response = ''


def login():
    # print('Login!')
    controlSocket.send(struct.pack('>8s64s64s', b'\xAB\xCD\x00\x81\x00\x00\x01\x10', b'admin', b'12345'))
    __response = controlSocket.recv(1024)
    # print('Login Response:')
    # print(controlSocket.recv(1024))
    # print('Login Confirm!')
    controlSocket.send(b'\xAB\xCD\x00\x00\x00\x00\x01\x13')
    __response = controlSocket.recv(1024)
    # print('Confirm Response:')
    # print(controlSocket.recv(1024))


def get_firmware_version():
    # print('Request Firmware version!')
    controlSocket.send(b'\xAB\xCD\x00\x00\x00\x00\xA0\x34')
    __response = controlSocket.recv(1024)
    # print('Firmware version:')
    # print(controlSocket.recv(1024))


def start_video_stream():
    # print('Start video stream!')
    controlSocket.send(b'\xAB\xCD\x00\x08\x00\x00\x01\xFF')
    controlSocket.send(b'\xAB\xCD\x00\x00\x00\x00\x01\x12')
    __response = controlSocket.recv(1024)


def ping():
    # print('Ping!')
    controlSocket.send(b'\xAB\xCD\x00\x00\x00\x00\x01\x12')
    __response = controlSocket.recv(1024)
    # print('Pong:')
    # print(controlSocket.recv(1024))
    threading.Timer(10, ping).start()


def listen():
    print("Dump video stream:")
    __seq = 0
    __fb = b''
    __el = 0
    while True:
        signal.signal(signal.SIGINT, exit)
        recvpack, payload = videoSocket.recvfrom(1024)
        control = recvpack[7]
        if control == 1:
            __fb += recvpack[8:]
        elif control == 2:
            __el = ord(recvpack[20])
            __rtp = struct.pack('>2shi4x', b'\x80\x63', __seq, (__el * 90)) + __fb
            proxySocket.sendto(__rtp, ('127.0.0.1', 8888))
            __fb = b''
            __seq += 1


def exit(signal, frame):
    print('Bye!')
    sys.exit(0)


if __name__ == '__main__':
    login()
    get_firmware_version()
    start_video_stream()
    ping()
    listen()
