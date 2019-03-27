import socket

server_addr = ('127.0.0.1', 5005)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_addr))

while True:
    data, addr = sock.recvfrom(1024) # buffer size 1024 bytes
    print("diterima ", data)
    print("dikirim oleh ", addr)
