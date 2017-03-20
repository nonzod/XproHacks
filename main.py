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
import time
import threading

host = '192.168.100.1'
port = 6666

mySocket = socket.socket()
mySocket.connect((host, port))


def login():
    mySocket.send(bytes.fromhex('ab cd 00 81 00 00 01 10 61 64 6d 69 6e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 31 32 33 34 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'))
    mySocket.send(bytes.fromhex('ab cd 00 00 00 00 01 12'))
    print(mySocket.recv(1024))
    print(mySocket.recv(1024))



def boh():
    mySocket.send(bytes.fromhex('AB CD 00 04 00 00 a0 3e 01 00 00 00'))
    mySocket.send(bytes.fromhex('AB CD 00 00 00 00 a0 34'))  # request_firmware_info
    print(mySocket.recv(1024))


def ping():
    mySocket.send(bytes.fromhex('AB CD 00 00 00 00 01 12'))  # Alive Request
    print(mySocket.recv(1024))
    threading.Timer(10, ping).start()


def start_video():
    mySocket.send(bytes.fromhex('AB CD 00 00 00 00 01 FF 00 00 00 00 00 00 00 00'))  # Start Preview Stream
    mySocket.send(bytes.fromhex('AB CD 00 24 00 00 a0 11 28 00 00 00 03 00 00 00 13 00 00 00 12 00 00 00 03 00 00 00 e1 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00'))
    mySocket.send(bytes.fromhex('AB CD 00 00 00 00 a0 34 ab cd 00000000 a0 2a'))
    print(mySocket.recv(1024))


def boh2():
    mySocket.send(bytes.fromhex('AB CD 00 00 00 00 A0 2a'))
    print(mySocket.recv(1024))


def boh3():
    mySocket.send(bytes.fromhex('AB CD 00 08 00 00 02 ff 00 00 00 00 00 00 00 00'))
    print(mySocket.recv(1024))


if __name__ == '__main__':
    login()
    boh()
    # request_firmware_info()
    start_video()
    boh2()
    boh2()
    boh2()
    boh2()
    boh2()
    boh2()
    boh2()
    boh3()
    ping()
    # data = mySocket.recv(1024)
    # mySocket.close()
