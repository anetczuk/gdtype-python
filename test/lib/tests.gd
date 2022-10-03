## 
##

extends MainLoop
func _initialize():
    execute()
func _process( delta ):
    return true


## =========================================================================


const Utils = preload( "utils.gd" )


## Godot 4.0 does not allow to access "Variant.Type" and enumerate it's items
## so all constants have to be stored within dict
const TYPE_DICT = {
    TYPE_NIL: "TYPE_NIL",
    TYPE_BOOL: "TYPE_BOOL",
    TYPE_INT: "TYPE_INT",
    TYPE_FLOAT: "TYPE_FLOAT",
    TYPE_STRING: "TYPE_STRING",
    TYPE_VECTOR2: "TYPE_VECTOR2",
    TYPE_VECTOR2I: "TYPE_VECTOR2I",
    TYPE_RECT2: "TYPE_RECT2",
    TYPE_RECT2I: "TYPE_RECT2I",
    TYPE_VECTOR3: "TYPE_VECTOR3",
    TYPE_VECTOR3I: "TYPE_VECTOR3I",
    TYPE_TRANSFORM2D: "TYPE_TRANSFORM2D",
    TYPE_VECTOR4: "TYPE_VECTOR4",
    TYPE_VECTOR4I: "TYPE_VECTOR4I",
    TYPE_PLANE: "TYPE_PLANE",
    TYPE_QUATERNION: "TYPE_QUATERNION",
    TYPE_AABB: "TYPE_AABB",
    TYPE_BASIS: "TYPE_BASIS",
    TYPE_TRANSFORM3D: "TYPE_TRANSFORM3D",
    TYPE_PROJECTION: "TYPE_PROJECTION",
    TYPE_COLOR: "TYPE_COLOR",
    TYPE_STRING_NAME: "TYPE_STRING_NAME",
    TYPE_NODE_PATH: "TYPE_NODE_PATH",
    TYPE_RID: "TYPE_RID",
    TYPE_OBJECT: "TYPE_OBJECT",
    TYPE_CALLABLE: "TYPE_CALLABLE",
    TYPE_SIGNAL: "TYPE_SIGNAL",
    TYPE_DICTIONARY: "TYPE_DICTIONARY",
    TYPE_ARRAY: "TYPE_ARRAY",
    TYPE_PACKED_BYTE_ARRAY: "TYPE_PACKED_BYTE_ARRAY",
    TYPE_PACKED_INT32_ARRAY: "TYPE_PACKED_INT32_ARRAY",
    TYPE_PACKED_INT64_ARRAY: "TYPE_PACKED_INT64_ARRAY",
    TYPE_PACKED_FLOAT32_ARRAY: "TYPE_PACKED_FLOAT32_ARRAY",
    TYPE_PACKED_FLOAT64_ARRAY: "TYPE_PACKED_FLOAT64_ARRAY",
    TYPE_PACKED_STRING_ARRAY: "TYPE_PACKED_STRING_ARRAY",
    TYPE_PACKED_VECTOR2_ARRAY: "TYPE_PACKED_VECTOR2_ARRAY",
    TYPE_PACKED_VECTOR3_ARRAY: "TYPE_PACKED_VECTOR3_ARRAY",
    TYPE_PACKED_COLOR_ARRAY: "TYPE_PACKED_COLOR_ARRAY",
    TYPE_MAX: "TYPE_MAX"
}


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
    var handler_path = curr_dir + "./lib/handle_data.sh"

    var tmp_in  = curr_dir + "./tmp/data_in.bin"
    var tmp_out = curr_dir + "./tmp/data_out.bin"

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
        return false

    return true


func execute():
    var data = null
    
    ## positive integer
    data = 321
    test_data( data )
    
    ## negative integer
    data = -321
    test_data( data )
    
    ## list with string
    data = [ "aaaa2" ]
    test_data( data )
    
    ## color
    data = Color( 0.5, 0.0, 1.0 )
    test_data( data )
    
    ## vector3
    data = Vector3( 0.5, 0.0, 1.0 )
    test_data( data )
    
    # Transform
    data = Transform3D()
    data = data.translated( Vector3( 0.5, 0.0, 1.0 ) )
    test_data( data )
    
    # string name
    data = StringName( "asdfg" )
    test_data( data )
