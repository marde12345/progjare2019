import socket
import time

ip = "10.151.253.180"
port = 5030
target = (ip,port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
i = 0

while True:
    i = i + 1
    msg = "Angka {}". format(i)

    print (msg)
    sock.sendto(msg.encode('utf-8'),target)
    time.sleep(1)