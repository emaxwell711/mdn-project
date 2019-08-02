from DSCP_classes import *
from random import randint
from time import sleep
import sys 

# add socket
import socket
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind(("127.0.0.1", 10000))

# config scapy to send packets over loopback
conf.L3socket = L3RawSocket

# timeout 
# receive_sock.settimeout(5)

while True:

    input('Press Enter to Start')
    
    ### STATE = LISTEN FOR DISCOVERS ###

    while state == 1:
      # listen for incoming packets
      try:
          data, addr = receive_sock.recvfrom(1024)
      except: 
          print('Socket Timeout')
          continue

      discover_p = DSCP_Discover(data)
      if discover_p.Msg_Type == 1:
        print('Received DSCP-D packet')
        discover_p.show2()
        break
   
    # parse values from Discover packet
    player_version = discover_p.Version
    player_physdom = discover_p.Phys_Dom
    # create IDs
    session_id = randint(1, 2**32-1)
    player_id = randint(1, 2**32-1)
    conductor_id = 100
    # set signals and lease time for the player
    lease_time = 86400
    signals = [1, 2, 3]

    # build offer packet
    offer_p = DSCP_Offer(      
            Version = player_version,
            Phys_Dom = player_physdom,
            Sess_Id = session_id,
            Play_Id = player_id,
            Cond_Id = conductor_id,
            Lease_Time = lease_time, 
            signals = signals
            )  

    print('DSCP-Offer built')
    offer_p.show2()
    send(IP(dst="127.0.0.1")/UDP(dport=10001)/offer_p)
    print('DSCP-Offer sent')

    ### STATE = WAIT FOR REQUEST ###

    # set socket timeout
    receive_sock.settimeout(10)

    #listen for incoming request packet
    try:
        data, addr = receive_sock.recvfrom(1024)
        request_p = DSCP_Req(data)
    except:
        print('Socket Timeout')
        continue
    
    print('request packet received')
    request_p.show2()
    
    #wait
    sleep(1)
    
    #check value of request packet
    if request_p.Msg_Type == 3:
        session_id = request_p.Sess_Id
        player_id = request_p.Play_Id
        conductor_id = request_p.Cond_Id
        lease_time =  request_p.Lease_Time
        signals = request_p.signals
        
        #build ACK 
        ack_p = DSCP_ACK(
                Version = player_version,
                Phys_Dom = player_physdom, 
                Sess_Id = session_id,
                Play_Id = player_id, 
                Cond_Id = conductor_id,
                Lease_Time = lease_time,
                signals = signals
                ) 
 
        print('ACK sent')
        ack_p.show2()
        send(IP(dst="127.0.0.1")/UDP(dport=10001)/ack_p) #send ACK
    
    ### STATE = PERFORMANCE ###
