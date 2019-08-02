class Butts(Packet):
    name = "ButtsPacket "
    fields_desc=[
		ByteField("butt", 0),	# this is 8 bits long (i.e. 1 byte)
		ShortField("butt",0),	# this is 16 bits long (i.e. 2 bytes)
		IntField("butt",0),		# this is 32 bits long (i.e. 4 bytes)
    ]

class DSCP_Discover(Packet):
    name = "DSCP_DiscPacket"
    fields_desc=[
                ByteField("Msg_Type", 0),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Capab", 0),
    ]
    
class DSCP_Offer(Packet):
    name = "DSCP_OffPacket"
    fields_desc=[
                ByteField("Msg_Type", 0),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Lease_Time", 0),
                ShortField("Elem_Type", 0),
                ShortField("Elem_Len", 0),
    ]
    
class DSCP_Req(Packet):
    name = "DSCP_ReqPacket"
    fields_desc=[
                ByteField("Msg_Type", 0),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Lease_Time", 0),
                ShortField("Elem_Type", 0),
                ShortField("Elem_Len", 0),
                IntField("Elem_Value" , 0 ,
                      { 4: "Phys_Dom", 5: "Capab" , 23: "Signal" } )
    ]
                
class DSCP_ACK(Packet):
    name = "DSCP_ACKPacket"
    fields_desc=[
                ByteField("Msg_Type", 0),
                ByteField("Version", 0),
                ShortField("Phys_Dom", 0),
                IntField("Sess_Id", 0),
                IntField("Play_Id", 0),
                IntField("Cond_Id", 0),
                IntField("Lease_Time", 0),
                ShortField("Elem_Type", 0),
                ShortField("Elem_Len", 0),
                IntField("Elem_Value" , 0 ,
                        { 4: "Phys_Dom", 5: "Capab" , 23: "Signal" } )
]
                
        
                
