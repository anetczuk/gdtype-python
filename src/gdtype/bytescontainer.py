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

import logging
import struct
from typing import List


_LOGGER = logging.getLogger(__name__)


## mutable wrapper for bytes
class BytesContainer:

    def __init__(self, data: bytes = None):
        self.data = data
        if self.data is None:
            self.data = bytes()

    def size(self):
        return len( self.data )

    ## =====================================================

    ## pop front
    def pop(self, size):
        ret_data  = self.data[ :size ]
        self.data = self.data[ size: ]
        return ret_data

    ## pop int from front
    def popInt(self):
        raw = self.pop(4)
        return int.from_bytes( raw, byteorder='little' )

    def popFloat32(self):
        raw = self.pop(4)
        proper_data = struct.unpack( "<f", raw )
        proper_data = proper_data[0]
        return proper_data

    def popFloat32Items(self, items):
        retList = []
        for _ in range(0, items):
            value = self.popFloat32()
            retList.append( value )
        return retList

    def popFloat64(self):
        raw = self.pop(8)
        proper_data = struct.unpack( "<d", raw )
        proper_data = proper_data[0]
        return proper_data

    def popString(self, string_len: int):
        data_string = self.pop( string_len )
        return data_string.decode("utf-8")

    ## pop from front
    def popFlagsType(self):
        raw = self.popInt()
        data_type  = raw & 0xFF
        data_flags = (raw >> 16) & 0xFF
        return ( data_flags, data_type )

    ## =====================================================

    def push( self, value: bytes ):
        self.data = self.data + value

    def pushZeros( self, number: int ):
        if number < 1:
            return
        zeros = bytes()
        for _ in range( 0, number ):
            zeros = zeros + b'\x00'
        self.data = self.data + zeros

    ## push back value
    def pushInt( self, value: int ):
        raw = value.to_bytes( 4,  byteorder='little' )
        self.push( raw )

    def pushFloat32(self, value: float):
        raw = struct.pack( "<f", value )
        self.push( raw )

    def pushFloat32Items(self, value_array: List[float] ):
        for item in value_array:
            self.pushFloat32( item )

    def pushFloat64(self, value: float):
        raw = struct.pack( "<d", value )
        self.push( raw )

    def pushString(self, value: str):
        raw = value.encode("utf-8")
        self.push( raw )

    ## push back value
    def pushFlagsType( self, flags: int, data_type: int ):
        value = ((flags & 0xFF) << 16) | ( data_type & 0xFF )
        self.pushInt( value )

    ## =====================================================

    def __str__(self):
        return str( self.data )
