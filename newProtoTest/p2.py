from myproto import *
from random import randint
from time import sleep
import sys 

#add socket
import socket
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind(("127.0.0.1", 10000))

#config scapy to send packets over loopback
conf.L3socket = L3RawSocket

#timeout 
receive_sock.settimeout(3)

while True:

    input('Press Enter to Start')
    
    #listen for incoming packets
    try:
        data, addr = receive_sock.recvfrom(1024)
        p1 = my_packet(data)
    except: 
        print('Socket Timeout')
        continue
    
    print('first received packet')
    p1.show2()
    
    #wait
    sleep(randint(1, 9))
    
    #check value of p1 packet
    if p1.value == 1:
        reply_list = p1.var
        reply_list.append(randint(1, 9))
        p2 = my_packet(value=2,var= reply_list)  #build reply packet
        
        print('first reply sent')
        p2.show2()
        send(IP(dst="127.0.0.1")/UDP(dport=10001)/p2) #send reply packet
    
    #timeout
    receive_sock.settimeout(3)
    
    #listen for incoming reply packet
    try:
        data, addr = receive_sock.recvfrom(1024)
        p3 = my_packet(data)
    except:
        print('Socket Timeout')
        continue
    
    print('second received packet')
    p3.show2()
    
    #wait
    sleep(randint(1, 9))
    
    #check value of p1 reply packet
    if p3.value == 3:
        reply_list = p3.var
        reply_list.append(randint(1, 9))
        p4 = my_packet(value=4,var= reply_list) #build another reply
    
        print('second reply sent')
        p4.show2()
        send(IP(dst="127.0.0.1")/UDP(dport=10001)/p4) #send another reply
    
