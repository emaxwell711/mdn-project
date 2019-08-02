from myproto import * 
from random import randint
from time import sleep
import sys

#add socket
import socket
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind(("127.0.0.1", 10001))

#config scapy to send packets over loopback
conf.L3socket = L3RawSocket

while True:
    input('Press Enter to Start')
    #build packet
    p1 = my_packet(value=1, var=[randint(1, 9)])
    
    print('first packet')
    p1.show2()
    send(IP(dst="127.0.0.1")/UDP(dport=10000)/p1)
    
    #timeout
    receive_sock.settimeout(3)
    
    #listen for incoming reply packet
    try:
        
        data, addr = receive_sock.recvfrom(1024)
        p2  = my_packet(data)
    except:
        print('Socket Timeout')
        continue
    
    print('first received packet')
    p2.show2()
    
    #wait
    sleep(randint(1, 9))
    
    #check value of p2 reply packet
    if p2.value == 2:
        reply_list = p2.var
        reply_list.append(randint(1, 9))
        p3 = my_packet(value=3, var= reply_list) #build reply packet
        
        print('first reply sent')
        p3.show2()
        send(IP(dst="127.0.0.1")/UDP(dport=10000)/p3) #send reply packet
    
    #timeout
    receive_sock.settimeout(3)
    
    #listen for incoming reply packet
    try:
        data, addr = receive_sock.recvfrom(1024)
        p4 = my_packet(data)
    except:
        print('Socket Timeout')
        continue
    
    print('second received packet')
    p4.show2()
