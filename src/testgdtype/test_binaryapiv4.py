# MIT License
#
# Copyright (c) 2022 Arkadiusz Netczuk <dev.arnet@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import unittest

import numpy

from gdtype.binaryapiv4 import deserialize, serialize
from gdtype.commontypes import Vector3, deserialize_custom, deserialize_type, serialize_custom, serialize_type,\
    Int32Array, Int64Array, Vector2Array, Vector3Array


#TODO: add tests for invalid input (check exceptions)
#TODO: add test for CONFIG_LIST: serialize and deserialize and compare results
#TODO: add tests inside GDScript (call python code from gdsript)


##
class DeserializeTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        pass

    def tearDown(self):
        ## Called after testfunction was executed
        pass

    def test_none(self):
        raw_bytes = b'\x04\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( data_value, None )

    def test_bool_true(self):
        raw_bytes = b'\x08\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), bool )
        self.assertEqual( data_value, True )

    def test_int(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00{\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), int )
        self.assertEqual( data_value, 123 )

    def test_int_negative_1(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), int )
        self.assertEqual( data_value, -1 )

    def test_int_negative_max(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x80'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), int )
        self.assertEqual( data_value, -2147483648 )

    def test_float64(self):
        raw_bytes = b'\x0c\x00\x00\x00\x03\x00\x01\x00Zd;\xdfO\xd5^@'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), float )
        self.assertEqual( data_value, 123.333 )

    def test_string_nonempty(self):
        raw_bytes = b'\x0c\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00aaa2'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), str )
        self.assertEqual( data_value, "aaa2" )

    def test_string_DO_STEP(self):
        raw_bytes = b'\x10\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00DO_STEP\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), str )
        self.assertEqual( data_value, "DO_STEP" )

    def test_string_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), str )
        self.assertEqual( data_value, "" )

    def test_Vector3(self):
        raw_bytes = b'\x10\x00\x00\x00\x09\x00\x00\x00\x9a\x99\x31\x41\x9a\x99\xb1\x41\x33\x33\x05\x42'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), Vector3 )
        self.assertAlmostEqual( data_value.x, 11.1, 5 )
        self.assertAlmostEqual( data_value.y, 22.2, 5 )
        self.assertAlmostEqual( data_value.z, 33.3, 5 )

    def test_list_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, [] )

    def test_list_int(self):
        # pylint: disable=C0301
        raw_bytes = b'\x20\x00\x00\x00\x1c\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, [1, 2, 3] )

    def test_list_string_01(self):
        # pylint: disable=C0301
        raw_bytes = b'\x24\x00\x00\x00\x1c\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x08\x00\x00\x00REG_RESP\x04\x00\x00\x00\x01\x00\x00\x00\x61\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, [ 'REG_RESP', 'a' ] )

    def test_list_string_02(self):
        # pylint: disable=C0301
        raw_bytes = b'D\x00\x00\x00\x1c\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x08\x00\x00\x00REG_RESP\x04\x00\x00\x00$\x00\x00\x002e0434f5-6755-4460-b860-5ea50fbf6640'
        data_value = deserialize( raw_bytes )

        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, ['REG_RESP', '2e0434f5-6755-4460-b860-5ea50fbf6640'] )

    def test_list_string_03(self):
        # pylint: disable=C0301
        raw_bytes = b',\x00\x00\x00\x1c\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\t\x00\x00\x00VEH_STATE\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00player1\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, [ 'VEH_STATE', 'player1' ] )

    def test_dict_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), dict )
        self.assertEqual( data_value, {} )

    def test_dict_int_str(self):
        # pylint: disable=C0301
        raw_bytes = b'\x1c\x00\x00\x00\x1b\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00bbc\x00'
        data_value = deserialize( raw_bytes )

        self.assertEqual( type(data_value), dict )
        self.assertEqual( data_value, {5: "bbc"} )

#     def test_PackedColorArray(self):
#         ## two RGBA items
#         # pylint: disable=C0301
#         raw_bytes = b'(\x00\x00\x00%\x00\x00\x00\x02\x00\x00\x00\xcd\xcc\xcc=\xcd\xccL>\x9a\x99\x99>\xcd\xcc\xcc>\xcd\xcc\xcc>\x00\x00\x00?\x9a\x99\x19?333?'
#         data = deserialize( raw_bytes )
#
#         data_type  = data[0]
#         data_value = data[1]
#         self.assertEqual( data_type, GodotType.PackedColorArray )
#         self.assertEqual( type(data_value), dict )
#         data_dict = { "type": "PackedColorArray"
#                     }
#         self.assertEqual( data_value, data_dict )

    def test_int_custom(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00{\x00\x00\x00'
        data_value = deserialize_custom( raw_bytes, deserialize_type )
        self.assertEqual( type(data_value), int )
        self.assertEqual( data_value, 123 )

    def test_Int32Array(self):
        raw_bytes = b'\x14\x00\x00\x00\x1e\x00\x00\x00\x03\x00\x00\x00\x1f\x00\x00\x00\xe0\xff\xff\xff\x21\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), Int32Array )
        self.assertEqual( data_value.values, [31, -32, 33] )

    def test_Int64Array(self):
        raw_bytes = b'\x20\x00\x00\x00\x1f\x00\x00\x00\x03\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\xe0\xff\xff\xff\xff\xff\xff\xff\x21\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), Int64Array )
        self.assertEqual( data_value.values, [31, -32, 33] )

    def test_Int64Array_numpy(self):
        raw_bytes = b'\x20\x00\x00\x00\x1f\x00\x00\x00\x03\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\xe0\xff\xff\xff\xff\xff\xff\xff\x21\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        data_value = data_value.toNumpy()
        data_list  = data_value.tolist()
        self.assertEqual( type(data_value), numpy.ndarray )
        self.assertEqual( int, data_value.dtype )
        self.assertEqual( data_list, [31, -32, 33] )

    def test_Vector2Array(self):
        Vector2Array
        raw_bytes = b' \x00\x00\x00#\x00\x00\x00\x03\x00\x00\x00\xcd\xcc\xcc=\x9a\x99\x99?33S@\x9a\x99\x19@\x00\x00\xf0\xc0\x9a\x99\x19\xc1'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), Vector2Array )
        self.assertAlmostEqual( data_value.items[0][0], 0.1, 4 ) 
        self.assertAlmostEqual( data_value.items[2][1], -9.6, 4 ) 

    def test_Vector2Array_numpy(self):
        raw_bytes = b' \x00\x00\x00#\x00\x00\x00\x03\x00\x00\x00\xcd\xcc\xcc=\x9a\x99\x99?33S@\x9a\x99\x19@\x00\x00\xf0\xc0\x9a\x99\x19\xc1'
        data_value = deserialize( raw_bytes )
        data_value = data_value.toNumpy()
        data_list  = data_value.tolist()
        self.assertEqual( type(data_value), numpy.ndarray )
        self.assertEqual( float, data_value.dtype )
        self.assertEqual( len(data_value), 3 )
        self.assertAlmostEqual( data_list[0][0], 0.1, 4 ) 
        self.assertAlmostEqual( data_list[2][1], -9.6, 4 ) 

    def test_Vector3Array(self):
        raw_bytes = b'\x20\x00\x00\x00\x24\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x00\x00\x00\x00\x80\x3f\x9a\x99\x19\x3f\xcd\xcc\xcc\x3d\xcd\xcc\x8c\xbf'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), Vector3Array )
        self.assertAlmostEqual( data_value.items[0][0], 0.5, 4 ) 
        self.assertAlmostEqual( data_value.items[1][2], -1.1, 4 ) 

    def test_Vector3Array_numpy(self):
        raw_bytes = b'\x20\x00\x00\x00\x24\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x00\x00\x00\x00\x80\x3f\x9a\x99\x19\x3f\xcd\xcc\xcc\x3d\xcd\xcc\x8c\xbf'
        data_value = deserialize( raw_bytes )
        data_value = data_value.toNumpy()
        data_list  = data_value.tolist()
        self.assertEqual( type(data_value), numpy.ndarray )
        self.assertEqual( float, data_value.dtype )
        self.assertEqual( len(data_value), 2 )
        self.assertAlmostEqual( data_list[0][0], 0.5, 4 ) 
        self.assertAlmostEqual( data_list[1][2], -1.1, 4 ) 


##
class SerializeTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        pass

    def tearDown(self):
        ## Called after testfunction was executed
        pass

    def test_bool_true(self):
        raw_bytes = b'\x08\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00'
        data_value = True
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_int(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00{\x00\x00\x00'
        data_value = 123
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_int_negative(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00\xf7\xff\xff\xff'
        data_value = -9
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_float64(self):
        raw_bytes = b'\x0c\x00\x00\x00\x03\x00\x01\x00Zd;\xdfO\xd5^@'
        data_value = 123.333
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_string_nonempty(self):
        raw_bytes = b'\x0c\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00aaa2'
        data_value = "aaa2"
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_string_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'
        data_value = ""
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Vector3(self):
        # pylint: disable=C0301
        raw_bytes = b'\x10\x00\x00\x00\x09\x00\x00\x00\x9a\x99\x31\x41\x9a\x99\xb1\x41\x33\x33\x05\x42'
        data_value = Vector3( [11.1, 22.2, 33.3] )
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Vector3_alias(self):
        # pylint: disable=C0301
        raw_bytes = b'\x10\x00\x00\x00\x09\x00\x00\x00\x9a\x99\x31\x41\x9a\x99\xb1\x41\x33\x33\x05\x42'
        data_value = Vector3( [11.1, 22.2, 33.3] )
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_list_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00'
        data_value = []
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_list_int(self):
        # pylint: disable=C0301
        raw_bytes = b'\x20\x00\x00\x00\x1c\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
        data_value = [1, 2, 3]
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_dict_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00'
        data_value = {}
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_dict_int_str(self):
        # pylint: disable=C0301
        raw_bytes = b'\x1c\x00\x00\x00\x1b\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00bbc\x00'
        data_value = {5: "bbc"}
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_int_custom(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00{\x00\x00\x00'
        data_value = 123
        data = serialize_custom( data_value, serialize_type )
        self.assertEqual( data, raw_bytes )

    def test_Int32Array(self):
        raw_bytes = b'\x14\x00\x00\x00\x1e\x00\x00\x00\x03\x00\x00\x00\x1f\x00\x00\x00\xe0\xff\xff\xff\x21\x00\x00\x00'
        data_value = Int32Array([31, -32, 33])
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Int64Array(self):
        raw_bytes = b'\x20\x00\x00\x00\x1f\x00\x00\x00\x03\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\xe0\xff\xff\xff\xff\xff\xff\xff\x21\x00\x00\x00\x00\x00\x00\x00'
        data_value = Int64Array([31, -32, 33])
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Int64Array_numpy(self):
        raw_bytes = b'\x20\x00\x00\x00\x1f\x00\x00\x00\x03\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\xe0\xff\xff\xff\xff\xff\xff\xff\x21\x00\x00\x00\x00\x00\x00\x00'
        data_value = numpy.array([31, -32, 33])
        data_value = Int64Array.fromNumpy( data_value )
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Vector2Array(self):
        raw_bytes = b' \x00\x00\x00#\x00\x00\x00\x03\x00\x00\x00\xcd\xcc\xcc=\x9a\x99\x99?33S@\x9a\x99\x19@\x00\x00\xf0\xc0\x9a\x99\x19\xc1'
        data_value = Vector2Array([[0.1, 1.2], [3.3, 2.4], [-7.5, -9.6]])
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Vector2Array_numpy(self):
        raw_bytes = b' \x00\x00\x00#\x00\x00\x00\x03\x00\x00\x00\xcd\xcc\xcc=\x9a\x99\x99?33S@\x9a\x99\x19@\x00\x00\xf0\xc0\x9a\x99\x19\xc1'
        data_value = numpy.array([[0.1, 1.2], [3.3, 2.4], [-7.5, -9.6]])
        data_value = Vector2Array.fromNumpy( data_value )
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Vector3Array(self):
        raw_bytes = b'\x20\x00\x00\x00\x24\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x00\x00\x00\x00\x80\x3f\x9a\x99\x19\x3f\xcd\xcc\xcc\x3d\xcd\xcc\x8c\xbf'
        data_value = Vector3Array([[0.5, 0.0, 1.0], [0.6, 0.1, -1.1]])
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )

    def test_Vector3Array_numpy(self):
        raw_bytes = b'\x20\x00\x00\x00\x24\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x00\x00\x00\x00\x80\x3f\x9a\x99\x19\x3f\xcd\xcc\xcc\x3d\xcd\xcc\x8c\xbf'
        data_value = numpy.array([[0.5, 0.0, 1.0], [0.6, 0.1, -1.1]])
        data_value = Vector3Array.fromNumpy( data_value )
        data = serialize( data_value )
        self.assertEqual( data, raw_bytes )
