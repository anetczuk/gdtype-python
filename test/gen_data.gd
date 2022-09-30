## 
##

extends MainLoop

func _initialize():
    execute()

func _process(delta):
    return true

## =========================================================================

func serialized_representation( data: Variant ):
    var buff   = StreamPeerBuffer.new()
    var packet = PacketPeerStream.new()
    packet.set_stream_peer( buff )
    packet.put_var( data )
    return print_hex( buff.data_array )

##
## print bytes array to python string: b'\x04\x00\x00\x00\x00\x00\x00\x00'
##
func print_hex( data_bytes: PackedByteArray ):
    var python_repr = ""
    for item in data_bytes:
        python_repr += "\\x" + to_hex_string( item )
    return "b'" + python_repr + "'"

func to_hex_string( value: int ):
    if value > 15:
        return String.num_uint64( value, 16 )
    return "0" + String.num_uint64( value, 16 )

## =========================================================================

func execute():
    var data = 0
    
    data = "aaa2"
    print( "string ", data, "\n", serialized_representation( data ) )
    
    data = "ab"
    print( "string ", data, "\n", serialized_representation( data ) )

    data = ""
    print( "string ", data, "\n", serialized_representation( data ) )

    data = true
    print( "bool ", data, "\n", serialized_representation( data ) )

    data = 123
    print( "int ", data, "\n", serialized_representation( data ) )

    data = 123.333
    print( "float ", data, "\n", serialized_representation( data ) )

    data = []
    print( "list ", data, "\n", serialized_representation( data ) )

    data = [1, 2, 3]
    print( "list ", data, "\n", serialized_representation( data ) )

    data = {}
    print( "dict ", data, "\n", serialized_representation( data ) )

    data = {}
    data[5] = "bbc"
    print( "dict ", data, "\n", serialized_representation( data ) )

#       data = PackedColorArray()
#       data.append( Color( 0.1, 0.2, 0.3, 0.4 ) )
#       data.append( Color( 0.4, 0.5, 0.6, 0.7 ) )
#       tcp_stream.put_var( data )
#       OS.delay_msec(500)

#       var data_dict = 321
#       var data_dict = {}
#       data_dict["method"] = "aaa1"
#       data_dict["int"] = 123543
#       data_dict["float"] = 43242.777
#       data_dict["list"] = [1,2,3,4]
#       tcp_stream.put_var( data_dict )