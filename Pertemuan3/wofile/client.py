import socket
import time

server_addr = ('127.0.0.1', 5005)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
angka = 0
while True:
    angka = angka + 1
    msg = "ini angka {} " . format(angka)
    print(msg)
    sock.sendto(msg.encode(), (server_addr))
    # msg = " ini angka " + str(angka)
    # print (msg)
    # sock.sendto(msg, (server_addr))
    time.sleep(1)
