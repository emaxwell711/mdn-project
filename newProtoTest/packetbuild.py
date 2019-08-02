from myproto import * 
conf.L3socket = L3RawSocket
p = my_packet(var=[1, 3, 5])
p.show2()
send(IP(dst="127.0.0.1")/UDP(dport=10000)/p)

