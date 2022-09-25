# MIT License
#
# Copyright (c) 2020 Arkadiusz Netczuk <dev.arnet@gmail.com>
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

from gdtype.binaryapi import deserialize, GodotType


# b'\x0c\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00aaa2' 16
# b'\x08\x00\x00\x00\x02\x00\x00\x00{\x00\x00\x00' 12

# b'\x0c\x00\x00\x00\x03\x00\x01\x00Zd;\xdfO\xd5^@' 16
# b'\x08\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00' 12
# b'\x08\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00' 12


class DeserializeTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        pass

    def tearDown(self):
        ## Called after testfunction was executed
        pass

    def test_bool_true(self):
        raw_bytes = b'\x08\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.BOOL )
        self.assertEqual( type(data_value), bool )
        self.assertEqual( data_value, True )

    def test_int(self):
        raw_bytes = b'\x08\x00\x00\x00\x02\x00\x00\x00{\x00\x00\x00'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.INT )
        self.assertEqual( type(data_value), int )
        self.assertEqual( data_value, 123 )

    def test_float64(self):
        raw_bytes = b'\x0c\x00\x00\x00\x03\x00\x01\x00Zd;\xdfO\xd5^@'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.FLOAT )
        self.assertEqual( type(data_value), float )
        self.assertEqual( data_value, 123.333 )

    def test_string_nonempty(self):
        raw_bytes = b'\x0c\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00aaa2'
        data = deserialize( raw_bytes )

        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.STRING )
        self.assertEqual( type(data_value), str )
        self.assertEqual( data_value, "aaa2" )

    def test_string_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'
        data = deserialize( raw_bytes )

        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.STRING )
        self.assertEqual( type(data_value), str )
        self.assertEqual( data_value, "" )

    def test_list_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.LIST )
        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, [] )

    def test_list_int(self):
        raw_bytes = b' \x00\x00\x00\x1c\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.LIST )
        self.assertEqual( type(data_value), list )
        self.assertEqual( data_value, [1, 2, 3] )

    def test_dict_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.DICT )
        self.assertEqual( type(data_value), dict )
        self.assertEqual( data_value, {} )

    def test_dict_int_str(self):
        raw_bytes =  b'\x1c\x00\x00\x00\x1b\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00bbc\x00'
        data = deserialize( raw_bytes )
        
        data_type  = data[0]
        data_value = data[1]
        self.assertEqual( data_type, GodotType.DICT )
        self.assertEqual( type(data_value), dict )
        self.assertEqual( data_value, {5: "bbc"} )

#     def test_PackedColorArray(self):
#         ## two RGBA items
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
