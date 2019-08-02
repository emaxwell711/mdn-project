from myproto import *
import socket
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind(("127.0.0.1", 10000))
data, addr = receive_sock.recvfrom(1024)
p = my_packet(data)
p.show2()

