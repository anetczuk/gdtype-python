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


def deserialize( data: bytes ):
    deserializer = Deserializer( data )
    return deserializer.deserialize()


def serialize( data ) -> bytes:
    serializer = Serializer()
    return serializer.serialize( data )


## ===========================================================


@unique
class GodotType( IntEnum ):
    UNKNOWN             = -1
    NULL                = 0
    BOOL                = 1
    INT                 = 2
    FLOAT               = 3
    STRING              = 4
    DICT                = 27
    LIST                = 28
#     PackedColorArray    = 37

    @classmethod
    def fromInt(cls, value):
        try:
            return GodotType( value )
        except ValueError:
            return GodotType.UNKNOWN


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


##
class Deserializer:

    def __init__(self, data: bytes = None):
        self.data = BytesContainer( data )

    def deserialize(self):
        data_len = self.data.size()
        if data_len < 4:
            _LOGGER.error( "invalid packet -- too short: %s", self.data )
            return ( None, None )

        packet_size = self.data.popInt()
        data_size = self.data.size()
        if data_size != packet_size:
            _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", self.data )
            return ( None, None )

        result = self._popType()
        return ( result[0], result[1] )

    def _popType( self ):
        data_len = self.data.size()
        if data_len < 4:
            _LOGGER.error( "invalid packet -- too short: %s", self.data )
            return ( None, None )

        data_flags, data_type = self.data.popFlagsType()

        data_type_id = GodotType.fromInt( data_type )

        if data_type_id == GodotType.UNKNOWN:
            _LOGGER.error( "unknown data type %s", data_type )
            return ( data_type_id, None )

        if data_type_id == GodotType.NULL:
            return ( data_type_id, None )

        if data_type_id == GodotType.BOOL:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: %s", self.data )
                return ( None, None )
            data_value = self.data.popInt()
            proper_data = data_value > 0
            return ( data_type_id, proper_data )

        if data_type_id == GodotType.INT:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: %s", self.data )
                return ( None, None )
            proper_data = self.data.popInt()
            return ( data_type_id, proper_data )

        if data_type_id == GodotType.FLOAT:
            data_len = self.data.size()
            encoded_64 = (data_flags & 1) == 1
            if encoded_64:
                if data_len < 8:
                    _LOGGER.error( "invalid packet -- too short: %s", self.data )
                    return ( None, None )
    #             _LOGGER.info( "remaining float data: %s", data[4:12] )
                proper_data = self.data.popFloat64()
                return ( data_type_id, proper_data )
            ## 32 bit variant
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: %s", self.data )
                return ( None, None )
#             _LOGGER.info( "remaining float data: %s", data[4:8] )
            proper_data = self.data.popFloat32()
            return ( data_type_id, proper_data )

        if data_type_id == GodotType.STRING:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: %s", self.data )
                return ( None, None )
            string_len = self.data.popInt()
            if string_len < 1:
                return ( data_type_id, "" )
            proper_data = self.data.popString( string_len )
            return ( data_type_id, proper_data )

        if data_type_id == GodotType.DICT:
            data_len = self.data.size()
            if data_len < 4:
                _LOGGER.error( "invalid packet -- too short: %s", self.data )
                return ( None, None )
            data_header = self.data.popInt()
            list_size   = data_header & 0x7FFFFFFF
    #         shared_flag = data_header & 0x80000000
            if list_size < 1:
                return ( data_type_id, {} )

            proper_data = {}
            for _ in range(0, list_size):
                key_result = self._popType()
                key_result_type = key_result[0]
                if key_result_type is GodotType.UNKNOWN:
                    _LOGGER.error( "invalid dict key" )
                    return ( None, None )
                key_result_value = key_result[1]

                item_result = self._popType()
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
                _LOGGER.error( "invalid packet -- too short: %s", self.data )
                return ( None, None )
            data_header = self.data.popInt()
            list_size   = data_header & 0x7FFFFFFF
    #         shared_flag = data_header & 0x80000000
            if list_size < 1:
                return ( data_type_id, [] )

            proper_data = []
            for _ in range(0, list_size):
                result = self._popType()
                result_type = result[0]
                if result_type is GodotType.UNKNOWN:
                    _LOGGER.error( "invalid list item" )
                    return ( None, None )
                proper_data.append( result[1] )
            return ( data_type_id, proper_data )

        ## unhandled case
        _LOGGER.error( "unhandled data type %s %s", data_type, data_type_id )
        return ( data_type_id, None )
    
    @classmethod
    def get_message_length(cls, data: bytes):
        container = BytesContainer( data )
        if container.size() < 4:
            return None
        return container.popInt()


## ===========================================================


##
class Serializer:

    def __init__(self):
        self.data = None

    def serialize(self, value = None) -> bytes:
        self.data = BytesContainer()
        self._pushType( value )
        if self.data.size() < 1:
            ## failed to serialize data -- send NULL data
            self.data.pushFlagsType( 0, GodotType.NULL )
        header = BytesContainer()
        header_size = self.data.size()
        header.pushInt( header_size )
        header.push( self.data.data )
        self.data = header
        return self.data.data

    def _pushType(self, value = None ):
        if value is None:
            data_type_id = GodotType.NULL
            self.data.pushFlagsType( 0, data_type_id )
            return

        if isinstance(value, bool):
            data_type_id = GodotType.BOOL
            self.data.pushFlagsType( 0, data_type_id )
            self.data.pushInt( value )
            return

        if isinstance(value, int):
            data_type_id = GodotType.INT
            self.data.pushFlagsType( 0, data_type_id )
            self.data.pushInt( value )
            return

        if isinstance(value, float):
            data_type_id = GodotType.FLOAT
            self.data.pushFlagsType( 1, data_type_id )
            self.data.pushFloat64( value )
            return

        if isinstance(value, str):
            data_type_id = GodotType.STRING
            self.data.pushFlagsType( 0, data_type_id )
            str_len = len( value )
            self.data.pushInt( str_len )
            self.data.pushString( value )
            remaining = str_len % 4
            padding = 4 - remaining
            if padding < 4:
                self.data.pushZeros( padding )
            return

        if isinstance(value, dict):
            data_type_id = GodotType.DICT
            self.data.pushFlagsType( 0, data_type_id )
            dict_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
            data_header = dict_size & 0x7FFFFFFF
            self.data.pushInt( data_header )
            for key in value:
                self._pushType( key )
                sub_value = value[ key ]
                self._pushType( sub_value )
            return

        if isinstance(value, list):
            data_type_id = GodotType.LIST
            self.data.pushFlagsType( 0, data_type_id )
            list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
            data_header = list_size & 0x7FFFFFFF
            self.data.pushInt( data_header )
            for i in range(0, list_size):
                sub_value = value[ i ]
                self._pushType( sub_value )
            return

        _LOGGER.warning( "unable to serialize data: %s %s", value, type(value) )
