from scapy.all import *

class DSCP_Discover(Packet):
    name = "DSCP_DiscPacket"
    fields_desc=[
                ByteField("Msg_Type", 1),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Capab", 0),
    ]
    
class DSCP_Offer(Packet):
    name = "DSCP_OffPacket"
    fields_desc=[
                ByteField("Msg_Type", 2),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Lease_Time", 0),
                ShortField("Elem_Type", 0),
                FieldLenField("Elem_Len", None, count_of="signals"),
                FieldListField("signals", None, IntField("", 1), count_from=lambda pkt:pkt.Elem_Len)
    ]
    
class DSCP_Req(Packet):
    name = "DSCP_ReqPacket"
    fields_desc=[
                ByteField("Msg_Type", 3),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Lease_Time", 0),
                ShortField("Elem_Type", 0),
                FieldLenField("Elem_Len", None, count_of="signals"),
                FieldListField("signals", None, IntField("", 1), count_from=lambda pkt:pkt.Elem_Len)

    ]
                
class DSCP_ACK(Packet):
    name = "DSCP_ACKPacket"
    fields_desc=[
                ByteField("Msg_Type", 4),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Lease_Time", 0),
                ShortField("Elem_Type", 0),
                FieldLenField("Elem_Len", None, count_of="signals"),
                FieldListField("signals", None, IntField("", 1), count_from=lambda pkt:pkt.Elem_Len)


]
                
        
                
