## 
##


static func serialized_representation( data: Variant ):
    var buff   = StreamPeerBuffer.new()
    var packet = PacketPeerStream.new()
    packet.set_stream_peer( buff )
    packet.put_var( data )
    return print_hex( buff.data_array )


##
## print bytes array to python string: b'\x04\x00\x00\x00\x00\x00\x00\x00'
##
static func print_hex( data_bytes: PackedByteArray ):
    var python_repr = ""
    for item in data_bytes:
        python_repr += "\\x" + to_hex_string( item )
    return "b'" + python_repr + "'"


static func to_hex_string( value: int ):
    if value > 15:
        return String.num_uint64( value, 16 )
    return "0" + String.num_uint64( value, 16 )
