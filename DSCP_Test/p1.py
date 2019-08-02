from DSCP_classes import * 
from random import randint, choice
from time import sleep
import sys
from time import time

# add socket
import socket
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock.bind(("127.0.0.1", 10001))

# socket timeout
receive_sock.settimeout(1)

# config scapy to send packets over loopback
conf.L3socket = L3RawSocket

# player parameters
player_version = 1
player_physdom = 0b1000000000000001

# initialize list of received DSCP-Offers packets
offer_list = []

# initialize counter of DSCP-Discovers sent
discover_count = 0

# initialize counter of DSCP-Offers received
offer_count = 0

# initialize counter of DSCP-Requests sent
request_count = 0

# initialize time
start_lease_time = 0

# initialize state
state = 1

# set maximum number of DSCP Requests
max_req = 3

input('Press Enter to Start')

# build DSCP-Discover packet
discover_p = DSCP_Discover(Version= player_version, Phys_Dom= player_physdom)
print('DSCP-Discover packet built')
discover_p.show2()
send(IP(dst="127.0.0.1")/UDP(dport=10000)/discover_p)
print('DSCP-Discover packet sent')
discover_count += 1

while True:

    ### STATE = OFFER COLLECTION ###

    while state == 1:
      # listen for incoming DSCP-O packets for number of socket timeouts
      for i in range(10):
          try:
              data, addr = receive_sock.recvfrom(1024)
          except:
              print('Socket Timeout')
              continue
      
          # parse received data into a DSCP-O packet
          offer_p = DSCP_Offer(data)
          # check message type
          if offer_p.Msg_Type == 2:
              print('Received DSCP-O')
              offer_p.show2()
              offer_list.append(offer_p)
      
      # check if offer_list is empty
      if not offer_list:
          send(IP(dst="127.0.0.1")/UDP(dport=10000)/discover_p)
          print('DSCP-Discover packet sent')
          discover_count += 1
      else:
          state = 2
          break

    # choose offer
    # for offer_p in offer_list:
    # for the moment, choose offer randomly
    offer_p = choice(offer_list)
    print('Chosen DSCP-Offer:')
    offer_p.show2()

    session_id = offer_p.Sess_Id
    player_id = offer_p.Play_Id
    conductor_id = offer_p.Cond_Id
    lease_time =  offer_p.Lease_Time
    signals = offer_p.signals
    
    # build request packet
    request_p = DSCP_Req(
            Version = player_version, 
            Phys_Dom = player_physdom, 
            Sess_Id = session_id, 
            Play_Id = player_id, 
            Cond_Id = conductor_id, 
            Lease_Time = lease_time, 
            signals = signals
            )
    
    print('DSCP-Request sent')
    request_p.show2()
    send(IP(dst="127.0.0.1")/UDP(dport=10000)/request_p)
    request_count += 1

    ### STATE = WAIT FOR ACK ###

    receive_sock.settimeout(10)

    while state == 2:
      # listen for incoming DSCP-ACK packet
      try:
          data, addr = receive_sock.recvfrom(1024)
      except:
          print('Socket Timeout')
          send(IP(dst="127.0.0.1")/UDP(dport=10000)/request_p)
          request_count += 1
          if request_count > max_req:
              send(IP(dst="127.0.0.1")/UDP(dport=10000)/discover_p)
              print('DSCP-Discover packet sent')
              discover_count += 1
              state = 1
              break
          continue

      ack_p = DSCP_ACK(data)
      if ack_p.Msg_Type == 4:
        print('DSCP-ACK received')
        ack_p.show2()
        start_lease_time = time()
        state = 3
        break
    
    ### STATE = PERFORMANCE ### 
    
    while state == 3:
        # check if half of lease_time is expired
        if time()-start_lease_time == int(lease_time/2):
            send(IP(dst="127.0.0.1")/UDP(dport=10000)/request_p)
            request_count += 1
            receive_sock.settimeout(1)
            for i in range(int(lease_time/2)):
                try: 
                    data, addr = receive_sock.recvfrom(1024)
                except:
                    continue
                ack_p = DSCP_ACK(data)
                if ack_p.Msg_Type == 4:
                    print('DSCP-ACK received')
                    ack_p.show2()
                    start_lease_time = start_lease_time + lease_time
                    break
           # TODO handle case of lease time expiration with no ACK 



          

        

