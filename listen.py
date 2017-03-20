import socket
UDP_IP = "0.0.0.0"
UDP_PORT = 6669
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.connect(("192.168.100.1", 6669))
while True:
    data, addr = sock.recvfrom(4096)
    print(data)
