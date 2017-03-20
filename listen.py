import socket
UDP_IP = "0.0.0.0"
UDP_PORT = 6669

videoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
videoSocket.bind((UDP_IP, UDP_PORT))
# sock.settimeout(1)

while True:
    recvpack, payload = videoSocket.recvfrom(4096)
    print(recvpack)
