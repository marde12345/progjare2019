import socket
import time

ip = "127.0.0.1"
port = 5005
server = (ip,port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server)

while True:
    data, addr = sock.recvfrom(1024)

    print("Pesan :", data)
    print("Dari ->", addr)