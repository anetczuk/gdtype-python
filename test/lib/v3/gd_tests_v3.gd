## 
##

extends MainLoop

func _initialize():
    execute()
func _process( delta ):
    return true


## =========================================================================


const Utils = preload( "utilsv3.gd" )


## Godot 4.0 does not allow to access "Variant.Type" and enumerate it's items
## so all constants have to be stored within dict
var TYPE_DICT = {
    TYPE_NIL: "TYPE_NIL",                                           ## 0 0x00
    TYPE_BOOL: "TYPE_BOOL",
    TYPE_INT: "TYPE_INT",
    TYPE_REAL: "TYPE_REAL",
    TYPE_STRING: "TYPE_STRING",
    TYPE_VECTOR2: "TYPE_VECTOR2",
    TYPE_RECT2: "TYPE_RECT2",
    TYPE_VECTOR3: "TYPE_VECTOR3",
    TYPE_TRANSFORM2D: "TYPE_TRANSFORM2D",
    TYPE_PLANE: "TYPE_PLANE",
    TYPE_QUAT: "TYPE_QUAT",                                         ## 10 0x0a
    TYPE_AABB: "TYPE_AABB",
    TYPE_BASIS: "TYPE_BASIS",
    TYPE_TRANSFORM: "TYPE_TRANSFORM",
    TYPE_COLOR: "TYPE_COLOR",
    TYPE_NODE_PATH: "TYPE_NODE_PATH",
    TYPE_RID: "TYPE_RID",
    TYPE_OBJECT: "TYPE_OBJECT",
    TYPE_DICTIONARY: "TYPE_DICTIONARY",
    TYPE_ARRAY: "TYPE_ARRAY",
    TYPE_RAW_ARRAY: "TYPE_RAW_ARRAY",                               ## 20 0x14
    TYPE_INT_ARRAY: "TYPE_INT_ARRAY",
    TYPE_REAL_ARRAY: "TYPE_REAL_ARRAY",
    TYPE_STRING_ARRAY: "TYPE_STRING_ARRAY",
    TYPE_VECTOR2_ARRAY: "TYPE_VECTOR2_ARRAY",
    TYPE_VECTOR3_ARRAY: "TYPE_VECTOR3_ARRAY",
    TYPE_COLOR_ARRAY: "TYPE_COLOR_ARRAY",
    TYPE_MAX: "TYPE_MAX"                                            ## 27 0x1b
}


var valid: bool = true


func type_name( data ):
    var type_id = typeof( data )
    return TYPE_DICT[ type_id ]


func read_file( file_path: String ):
    var data_in = File.new()
    data_in.open( file_path, File.READ )
    var buffer = data_in.get_buffer( 9999 )
    data_in.close()
    return buffer


func test_data( input_data ):
    var curr_dir = ProjectSettings.globalize_path("res://")
    var handler_path = curr_dir + "./lib/v3/handle_data.sh"

    var tmp_in  = curr_dir + "./tmp/data_in_v3.bin"
    var tmp_out = curr_dir + "./tmp/data_out_v3.bin"

    var data_out = File.new()
    data_out.open( tmp_in, File.WRITE )
    data_out.store_var( input_data )
    data_out.close()

    var output = []
    var args = PoolStringArray( [ "-if=" + tmp_in, "-of=" + tmp_out ] )
    var exit_code = OS.execute( handler_path, args, true, output, true )

    if exit_code != OK:
        var words = output[0].replace( "\n", "\n")
        print( "error occur during serialization/deserialization of godot type: ", type_name(input_data) )
        print( "exit code: ", exit_code )
        print( "output:\n", words )
        valid = false
        return false

    var data_in = File.new()
    data_in.open( tmp_out, File.READ )
    var test_data = data_in.get_var()
    data_in.close()
    
    if test_data != input_data:
        var input_buffer  = read_file( tmp_in )
        var output_buffer = read_file( tmp_out )
        print( "invalid serialization/deserialization of ", type_name( input_data ), " ", input_data, " received ", type_name( input_data ), " ", test_data )
        print( "input data:  ", Utils.print_hex( input_buffer ) )
        print( "output data: ", Utils.print_hex( output_buffer ) )
        valid = false
        return false

    return true


func execute():
    var data = null
    
    ## null
    data = null
    test_data( data )
    
    ## bool
    data = true
    test_data( data )
    
    ## positive integer
    data = 321
    test_data( data )
    
    ## negative integer
    data = -321
    test_data( data )

    ## float
    data = float( 123.321 )
    test_data( data )

    ## string
    data = "qwer1"
    test_data( data )
    
    ## vector2
    data = Vector2( 0.5, 1.0 )
    test_data( data )
    
    ## Rect2
    data = Rect2( 0.5, 1.0, 3.0, 2.5 )
    test_data( data )

    ## vector3
    data = Vector3( 0.5, 0.0, 1.0 )
    test_data( data )

    ## Transform2D
    data = Transform2D()
    data = data.translated( Vector2( 0.5, 1.0 ) )
    test_data( data )

    ## Plane
    data = Plane( 1.1, 2.2, 3.3, 4.4 )
    test_data( data )

    ## Quat
    data = Quat( 1.1, 2.2, 3.3, 4.4 )
    test_data( data )

    ## AABB
    data = AABB( Vector3(1.1, 2.2, 3.3), Vector3(4.1, 5.2, 6.3) )
    test_data( data )

    ## Basis
    data = Basis( Vector3(1.0, 0.0, 0.0), 0.5 )
    test_data( data )
    
    ## Transform
    data = Transform()
    test_data( data )
    
    ## Color
    data = Color( 0.5, 0.0, 1.0 )
    test_data( data )

    ## list with string
    data = [ "aaaa2" ]
    test_data( data )
    
    data = [ "REG_RESP", "a" ]
    test_data( data )

    ### NodePath new format
    #data = NodePath( "aaa/bbb" )
    #test_data( data )

    ## RID
    data = RID()
    test_data( data )

    ## PoolByteArray
    data = PoolByteArray( [1, 2, 3] )
    test_data( data )
    
    ## PoolIntArray
    data = PoolIntArray( [1, 2, 3] )
    test_data( data )
    
    ## PoolRealArray
    data = PoolRealArray( [1.1, 2.2, 3.3] )
    test_data( data )
    
    ## PoolStringArray
    data = PoolStringArray( ["333", "4444", "55555"] )
    test_data( data )

    ## PoolVector2Array
    data = PoolVector2Array()
    data.append( Vector2( 0.5, 0.0 ) )
    data.append( Vector2( 0.6, 0.1 ) )
    test_data( data )

    ## PoolVector3Array
    data = PoolVector3Array()
    data.append( Vector3( 0.5, 0.0, 1.0 ) )
    data.append( Vector3( 0.6, 0.1, 1.1 ) )
    test_data( data )
    
    ## packed Color array
    data = PoolColorArray()
    data.append( Color( 0.5, 0.0, 1.0 ) )
    data.append( Color( 0.6, 0.1, 1.1 ) )
    test_data( data )
    
    if valid:
        print( "tests passed" )
    else:
        print( "some tests failed" )
