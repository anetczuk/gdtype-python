## 
##


static func serialized_representation( data ):
    var buff   = StreamPeerBuffer.new()
    var packet = PacketPeerStream.new()
    packet.set_stream_peer( buff )
    packet.put_var( data )
    return print_hex( buff.data_array )


##
## print bytes array to python string: b'\x04\x00\x00\x00\x00\x00\x00\x00'
##
static func print_hex( data_bytes: PoolByteArray ):
    var python_repr = ""
    for item in data_bytes:
        python_repr += "\\x" + to_hex_string( item )
    return "b'" + python_repr + "'"


static func to_hex_string( value: int ):
    if value < 10:
        return "0" + String( value )
    match value:
        10: return "0a"
        11: return "0b"
        12: return "0c"
        13: return "0d"
        14: return "0e"
        15: return "0f"
    return ""
