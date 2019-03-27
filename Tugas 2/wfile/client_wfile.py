# PYTHON2 ONLY

import socket
import os

server_addr = ('127.0.0.1', 5005)
filename = 'wp1935737.jpeg'
size = os.stat(filename).st_size

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fp = open(filename, 'rb')
k = fp.read()
sent = 0
for x in k:
    sock.sendto(x, server_addr)
    sent += 1
    print "\r sent {} of {} " . format(sent, size)
