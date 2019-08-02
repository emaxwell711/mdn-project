from scapy.all import *
class my_packet(Packet):
    name = "my_packet"
    fields_desc=[ByteField("value", 0),
    FieldLenField("len", None, count_of="var"),
    FieldListField("var", [1] , IntField("", 1), count_from=lambda pkt:pkt.len)

            ]

    
