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
from enum import IntEnum, unique


_LOGGER = logging.getLogger(__name__)


@unique
class GodotType( IntEnum ):
    UNKNOWN             = -1
    BOOL                = 1
    INT                 = 2
    FLOAT               = 3
    STRING              = 4
    DICT                = 27
    LIST                = 28
#     PackedColorArray    = 37

    @classmethod
    def from_int(cls, value):
        try:
            return GodotType( value )
        except ValueError:
            return GodotType.UNKNOWN


def deserialize( data: bytes ):
    deserializer = Deserializer( data )
    return deserializer.deserialize()


## ===========================================================


## mutable wrapper for bytes
class BytesContainer:
    
    def __init__(self, data: bytes = None):
        self.data = data

    def size(self):
        return len( self.data )

    def pop(self, size):
        ret_data = self.data[ :size ]
        self.data = self.data[ size: ]
        return ret_data
    
    def pop_int(self):
        raw = self.pop(4)
        return int.from_bytes( raw, byteorder='little' )
    
    def __str__(self):
        return str( self.data )


## 
class Deserializer:
    
    def __init__(self, data: bytes = None):
        self.data = BytesContainer( data )

    def deserialize(self):
        data_len = self.data.size()
        if data_len < 4:
            _LOGGER.error( "invalid packet -- too short: %s", self.data )
            return ( None, None )

        packet_size = self.data.pop_int()
        data_size = self.data.size()
        if data_size != packet_size:
            _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", self.data )
            return ( None, None )
        
        result = self._pop_type()
        return ( result[0], result[1] )
    
    def _pop_type( self ):
        data_len = self.data.size()
        if data_len < 4:
            _LOGGER.error( "invalid packet -- too short: ", self.data )
            return ( None, None )
    
        data_header  = self.data.pop_int()
        data_type    =  data_header & 0xFF
        data_flags   = (data_header >> 16) & 0xFF
        return self._convert_type( data_type, data_flags )
    
    
    def _convert_type( self, data_type: int, data_flags: int ):
        data_type_id = GodotType.from_int( data_type )
        
        if data_type_id == GodotType.UNKNOWN:
            _LOGGER.error( "unknown data type %s", data_type )
            return ( data_type_id, None )
    
        if data_type_id == GodotType.BOOL:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: ", self.data )
                return ( None, None )
            data_value = self.data.pop_int()
            proper_data = data_value > 0
            return ( data_type_id, proper_data )
    
        if data_type_id == GodotType.INT:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: ", self.data )
                return ( None, None )
            proper_data = self.data.pop_int()
            return ( data_type_id, proper_data )
        
        if data_type_id == GodotType.FLOAT:
            data_len = self.data.size()
            encoded_64 = (data_flags & 1) == 1
            if encoded_64:
                if data_len < 8:
                    _LOGGER.error( "invalid packet -- too short: ", self.data )
                    return ( None, None )
    #             _LOGGER.info( "remaining float data: %s", data[4:12] )
                proper_data = struct.unpack( "<d", self.data.pop(8) )
                proper_data = proper_data[0]
                return ( data_type_id, proper_data )
            else:
                if data_len < 4:
                    _LOGGER.error( "invalid packet -- too short: ", self.data )
                    return ( None, None )
    #             _LOGGER.info( "remaining float data: %s", data[4:8] )
                proper_data = struct.unpack( "<d", self.data.pop(4) )
                proper_data = proper_data[0]
                return ( data_type_id, proper_data )
    
        if data_type_id == GodotType.STRING:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: ", self.data )
                return ( None, None )
            string_len = self.data.pop_int()
            if string_len < 1:
                return ( data_type_id, "" )
            data_string = self.data.pop( string_len )
            proper_data = data_string.decode("utf-8") 
            return ( data_type_id, proper_data )
    
        if data_type_id == GodotType.DICT:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: ", self.data )
                return ( None, None )
            data_header = self.data.pop_int()
            list_size   = data_header & 0x7FFFFFFF
    #         shared_flag = data_header & 0x80000000
            if list_size < 1:
                return ( data_type_id, {} )
    
            proper_data = {}
            for _ in range(0, list_size):
                key_result = self._pop_type()
                key_result_type = key_result[0]
                if key_result_type is GodotType.UNKNOWN:
                    _LOGGER.error( "invalid dict key" )
                    return ( None, None )
                key_result_value = key_result[1]
    
                item_result = self._pop_type()
                item_result_type = item_result[0]
                if item_result_type is GodotType.UNKNOWN:
                    _LOGGER.error( "invalid dict value" )
                    return ( None, None )
                item_result_value = item_result[1]
                
                proper_data[ key_result_value ] = item_result_value
            return ( data_type_id, proper_data )
    
        if data_type_id == GodotType.LIST:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: ", self.data )
                return ( None, None )
            data_header = self.data.pop_int()
            list_size   = data_header & 0x7FFFFFFF
    #         shared_flag = data_header & 0x80000000
            if list_size < 1:
                return ( data_type_id, [] )
    
            proper_data = []
            for _ in range(0, list_size):
                result = self._pop_type()
                result_type = result[0]
                if result_type is GodotType.UNKNOWN:
                    _LOGGER.error( "invalid list item" )
                    return ( None, None )
                proper_data.append( result[1] )
            return ( data_type_id, proper_data )

        ## unhandled case
        _LOGGER.error( "unhandled data type %s %s", data_type, data_type_id )
        return ( data_type_id, None )
