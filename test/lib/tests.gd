## 
##

extends MainLoop
func _initialize():
    execute()
func _process( delta ):
    return true

## =========================================================================

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
        print( "exit code: ", exit_code )
        print( "output:\n", words )
        return false

    var data_in = File.new()
    data_in.open( tmp_out, File.READ )
    var test_data = data_in.get_var()
    data_in.close()
    
    if test_data != input_data:
        print( "invalid conversion of ", input_data, " to ", test_data )
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
