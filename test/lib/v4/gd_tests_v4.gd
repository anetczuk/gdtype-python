## 
##

extends MainLoop

func _initialize():
    execute()
func _process( delta ):
    return true


## =========================================================================


const Utils = preload( "utilsv4.gd" )


## Godot 4.0 does not allow to access "Variant.Type" and enumerate it's items
## so all constants have to be stored within dict
const TYPE_DICT = {
    TYPE_NIL: "TYPE_NIL",                                           ## 0 0x00
    TYPE_BOOL: "TYPE_BOOL",
    TYPE_INT: "TYPE_INT",
    TYPE_FLOAT: "TYPE_FLOAT",
    TYPE_STRING: "TYPE_STRING",
    TYPE_VECTOR2: "TYPE_VECTOR2",
    TYPE_VECTOR2I: "TYPE_VECTOR2I",
    TYPE_RECT2: "TYPE_RECT2",
    TYPE_RECT2I: "TYPE_RECT2I",
    TYPE_VECTOR3: "TYPE_VECTOR3",
    TYPE_VECTOR3I: "TYPE_VECTOR3I",                                 ## 10 0x0A
    TYPE_TRANSFORM2D: "TYPE_TRANSFORM2D",
    TYPE_VECTOR4: "TYPE_VECTOR4",
    TYPE_VECTOR4I: "TYPE_VECTOR4I",
    TYPE_PLANE: "TYPE_PLANE",
    TYPE_QUATERNION: "TYPE_QUATERNION",
    TYPE_AABB: "TYPE_AABB",
    TYPE_BASIS: "TYPE_BASIS",
    TYPE_TRANSFORM3D: "TYPE_TRANSFORM3D",
    TYPE_PROJECTION: "TYPE_PROJECTION",
    TYPE_COLOR: "TYPE_COLOR",                                       ## 20 0x14
    TYPE_STRING_NAME: "TYPE_STRING_NAME",
    TYPE_NODE_PATH: "TYPE_NODE_PATH",
    TYPE_RID: "TYPE_RID",
    TYPE_OBJECT: "TYPE_OBJECT",
    TYPE_CALLABLE: "TYPE_CALLABLE",
    TYPE_SIGNAL: "TYPE_SIGNAL",
    TYPE_DICTIONARY: "TYPE_DICTIONARY",                             ## 27 0x1B
    TYPE_ARRAY: "TYPE_ARRAY",                                       ## 28 0x1C
    TYPE_PACKED_BYTE_ARRAY: "TYPE_PACKED_BYTE_ARRAY",
    TYPE_PACKED_INT32_ARRAY: "TYPE_PACKED_INT32_ARRAY",             ## 30 0x1E
    TYPE_PACKED_INT64_ARRAY: "TYPE_PACKED_INT64_ARRAY",
    TYPE_PACKED_FLOAT32_ARRAY: "TYPE_PACKED_FLOAT32_ARRAY",
    TYPE_PACKED_FLOAT64_ARRAY: "TYPE_PACKED_FLOAT64_ARRAY",
    TYPE_PACKED_STRING_ARRAY: "TYPE_PACKED_STRING_ARRAY",
    TYPE_PACKED_VECTOR2_ARRAY: "TYPE_PACKED_VECTOR2_ARRAY",
    TYPE_PACKED_VECTOR3_ARRAY: "TYPE_PACKED_VECTOR3_ARRAY",         ## 36 0x24
    TYPE_PACKED_COLOR_ARRAY: "TYPE_PACKED_COLOR_ARRAY",
    TYPE_MAX: "TYPE_MAX"                                            ## 38 0x26
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
    var handler_path = curr_dir + "./lib/v4/handle_data.sh"

    var tmp_in  = curr_dir + "./tmp/data_in_v4.bin"
    var tmp_out = curr_dir + "./tmp/data_out_v4.bin"

    var data_out = File.new()
    data_out.open( tmp_in, File.WRITE )
    data_out.store_var( input_data )
    data_out.close()

    var output = []
    var exit_code = OS.execute( handler_path, [ "-if=" + tmp_in, "-of=" + tmp_out ], output, true, true )

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
    
    ## vector2i
    data = Vector2i( 5, 1 )
    test_data( data )
    
    ## Rect2
    data = Rect2( 0.5, 1.0, 3.0, 2.5 )
    test_data( data )
    
    ## Rect2i
    data = Rect2i( 0, 1, 3, 2 )
    test_data( data )

    ## vector3
    data = Vector3( 0.5, 0.0, 1.0 )
    test_data( data )
    
    ## Vector3i
    data = Vector3i( 5, 0, 1 )
    test_data( data )

    ## Transform2D
    data = Transform2D()
    data = data.translated( Vector2( 0.5, 1.0 ) )
    test_data( data )
    
    ## vector4
    data = Vector4( 0.5, 0.0, 1.0, 2.2 )
    test_data( data )
    
    ## Vector4i
    data = Vector4i( 5, 0, 1, 2 )
    test_data( data )

    ## Plane
    data = Plane( 1.1, 2.2, 3.3, 4.4 )
    test_data( data )

    ## Quaternion
    data = Quaternion( 1.1, 2.2, 3.3, 4.4 )
    test_data( data )

    ## AABB
    data = AABB( Vector3(1.1, 2.2, 3.3), Vector3(4.1, 5.2, 6.3) )
    test_data( data )

    ## Basis
    data = Basis( Vector3(1.0, 0.0, 0.0), 0.5 )
    test_data( data )
    
    ## Transform3D
    data = Transform3D()
    data = data.translated( Vector3( 0.5, 0.0, 1.0 ) )
    test_data( data )
    
    ## Projection
    data = Projection()
    test_data( data )
    
    ## Color
    data = Color( 0.5, 0.0, 1.0 )
    test_data( data )

    ## list with string
    data = [ "aaaa2" ]
    test_data( data )
    
    data = [ "REG_RESP", "a" ]
    test_data( data )
    
    ## StringName
    data = StringName( "333" )
    test_data( data )
    
    data = StringName( "4444" )
    test_data( data )
    
    data = StringName( "55555" )
    test_data( data )

    ### NodePath new format
    #data = NodePath( "aaa/bbb" )
    #test_data( data )

    ## RID
    data = RID()
    test_data( data )

    ## PackedByteArray
    data = PackedByteArray( [1, 2, 3] )
    test_data( data )
    
    ## PackedInt32Array
    data = PackedInt32Array( [1, 2, 3] )
    test_data( data )
    
    ## PackedInt64Array
    data = PackedInt64Array( [31, 32, 33] )
    test_data( data )
    
    ## PackedFloat32Array
    data = PackedInt32Array( [1.1, 2.2, 3.3] )
    test_data( data )
    
    ## PackedFloat64Array
    data = PackedFloat64Array( [31.3, 32.4, 33.5] )
    test_data( data )
    
    ## PackedStringArray
    data = PackedStringArray( ["333", "4444", "55555"] )
    test_data( data )

    ## PackedVector2Array
    data = PackedVector2Array()
    data.append( Vector2( 0.5, 0.0 ) )
    data.append( Vector2( 0.6, 0.1 ) )
    test_data( data )

    ## PackedVector3Array
    data = PackedVector3Array()
    data.append( Vector3( 0.5, 0.0, 1.0 ) )
    data.append( Vector3( 0.6, 0.1, 1.1 ) )
    test_data( data )
    
    ## packed Color array
    data = PackedColorArray()
    data.append( Color( 0.5, 0.0, 1.0 ) )
    data.append( Color( 0.6, 0.1, 1.1 ) )
    test_data( data )
    
    if valid:
        print( "tests passed" )
    else:
        print( "some tests failed" )
