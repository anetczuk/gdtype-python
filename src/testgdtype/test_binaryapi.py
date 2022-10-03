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

from gdtype.binaryapi import deserialize, serialize, Transform3D


#TODO: add tests for invalid input (check exceptions)
#TODO: add test for CONFIG_LIST: serialize and deserialize and compare results
#TODO: add tests inside GDScript (call python code from gdsript)


class Transform3DTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        pass

    def tearDown(self):
        ## Called after testfunction was executed
        pass

    def test_indexing_1d(self):
        raw_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        data = Transform3D( raw_data )
        
        self.assertEqual( data[0], 1 )
        self.assertEqual( data.get(0, 0), 1 )
        
        self.assertEqual( data[1], 2 )
        self.assertEqual( data.get(0, 1), 2 )
        
        self.assertEqual( data[2], 3 )
        self.assertEqual( data.get(0, 2), 3 )


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

    def test_string_empty(self):
        raw_bytes = b'\x08\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'
        data_value = deserialize( raw_bytes )
        self.assertEqual( type(data_value), str )
        self.assertEqual( data_value, "" )

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
