import socket

XPRO2_IP = '192.168.10.55'
CONTROL_PORT = 6666
VIDEO_PORT = 6669

client = socket.socket()
client.connect((XPRO2_IP, CONTROL_PORT))
