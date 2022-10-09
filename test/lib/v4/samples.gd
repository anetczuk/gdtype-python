## 
##

extends MainLoop
func _initialize():
    execute()
func _process( delta ):
    return true

## =========================================================================


const Utils = preload( "utilsv4.gd" )


func execute():
    var data = 0
    
    data = "aaa2"
    print( "string ", data, "\n", Utils.serialized_representation( data ) )
    
    data = "ab"
    print( "string ", data, "\n", Utils.serialized_representation( data ) )
    
    data = "DO_STEP"
    print( "string ", data, "\n", Utils.serialized_representation( data ) )

    data = ""
    print( "string ", data, "\n", Utils.serialized_representation( data ) )

    data = true
    print( "bool ", data, "\n", Utils.serialized_representation( data ) )

    data = 123
    print( "int ", data, "\n", Utils.serialized_representation( data ) )

    data = -1
    print( "-int ", data, "\n", Utils.serialized_representation( data ) )

    data = -2147483648
    print( "-int ", data, "\n", Utils.serialized_representation( data ) )

    #data = -123
    #print( "-int ", data, "\n", Utils.serialized_representation( data ) )

    data = 123.333
    print( "float ", data, "\n", Utils.serialized_representation( data ) )

    data = []
    print( "list ", data, "\n", Utils.serialized_representation( data ) )

    data = [1, 2, 3]
    print( "list ", data, "\n", Utils.serialized_representation( data ) )

    data = {}
    print( "dict ", data, "\n", Utils.serialized_representation( data ) )

    data = {}
    data[5] = "bbc"
    print( "dict ", data, "\n", Utils.serialized_representation( data ) )

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
