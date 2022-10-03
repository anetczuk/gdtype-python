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
    return deserialize_data( data )


def serialize( data ) -> bytes:
    return serialize_data( data )


def get_message_length( data: bytes ):
    container = BytesContainer( data )
    if container.size() < 4:
        _LOGGER.error( "message is too short: %s", data )
        return None
    return container.popInt()


## ======================================================================


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


## ======================================================================


@unique
class GodotType( IntEnum ):
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
        return GodotType( value )


## ======================================================================


def deserialize_data( message: bytes ):
    data = BytesContainer( message )
    data_len = data.size()
    if data_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", data )
        raise ValueError( "invalid packet -- too short: %s" % data )

    packet_size = data.popInt()
    data_size   = data.size()
    if data_size != packet_size:
        _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", data )
        raise ValueError( "packet isze mismatch: %s" % data )

    return deserialize_type( data )

def deserialize_none( data_flags: int, data: BytesContainer ):
    return None

def deserialize_bool( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", data )
        raise ValueError( "invalid packet -- too short: %s" % data )
    data_value = data.popInt()
    proper_data = data_value > 0
    return proper_data

def deserialize_int( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: %s" % data )
    proper_data = data.popInt()
    if proper_data & 0x80000000:
        ## got negative number
        neg_val = proper_data & 0x7FFFFFFF
        return -0x80000000 + neg_val
#         return proper_data & 0x7FFFFFFF | ~0x7FFFFFFF
    else:
        ## positive number
        return proper_data

def deserialize_float( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    encoded_64 = (data_flags & 1) == 1
    if encoded_64:
        if data_len < 8:
            raise ValueError( "invalid packet -- too short: %s" % data )
        proper_data = data.popFloat64()
        return proper_data
    ## 32 bit variant
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: %s" % data )
    proper_data = data.popFloat32()
    return proper_data

def deserialize_string( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: %s" % data )
    string_len = data.popInt()
    if string_len < 1:
        return ""
    proper_data = data.popString( string_len )
    return proper_data

def deserialize_dict( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: %s" % data )
    data_header = data.popInt()
    list_size   = data_header & 0x7FFFFFFF
#         shared_flag = data_header & 0x80000000
    if list_size < 1:
        return {}

    proper_data = {}
    for _ in range(0, list_size):
        key_value  = deserialize_type( data )
        item_value = deserialize_type( data )
        proper_data[ key_value ] = item_value
    return proper_data

def deserialize_list( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: %s" % data )
    data_header = data.popInt()
    list_size   = data_header & 0x7FFFFFFF
#         shared_flag = data_header & 0x80000000
    if list_size < 1:
        return []

    proper_data = []
    for _ in range(0, list_size):
        item_value = deserialize_type( data )
        proper_data.append( item_value )
    return proper_data


## ======================================================================


def serialize_data( value ) -> bytes:
    data = BytesContainer()
    serialize_type( value, data )
    if data.size() < 1:
        ## failed to serialize data -- send NULL data
        data.pushFlagsType( 0, GodotType.NULL )
    message = BytesContainer()
    header_size = data.size()
    message.pushInt( header_size )
    message.push( data.data )
    return message.data  
    
def serialize_none( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 0, data_type_id )

def serialize_bool( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 0, data_type_id )
    data.pushInt( value )

def serialize_int( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 0, data_type_id )
    if value & 0x80000000:
        ## got negative number
        pos_val = value & 0x7FFFFFFF
        out = 0x80000000 + pos_val
        data.pushInt( out )
    else:
        ## positive number
        data.pushInt( value )

def serialize_float( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 1, data_type_id )
    data.pushFloat64( value )

def serialize_string( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 0, data_type_id )
    str_len = len( value )
    data.pushInt( str_len )
    data.pushString( value )
    remaining = str_len % 4
    padding = 4 - remaining
    if padding < 4:
        data.pushZeros( padding )

def serialize_dict( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 0, data_type_id )
    dict_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = dict_size & 0x7FFFFFFF
    data.pushInt( data_header )
    for key in value:
        serialize_type( key, data )
        sub_value = value[ key ]
        serialize_type( sub_value, data )
    
def serialize_list( data_type_id, value, data: BytesContainer ):
    data.pushFlagsType( 0, data_type_id )
    list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = list_size & 0x7FFFFFFF
    data.pushInt( data_header )
    for i in range(0, list_size):
        sub_value = value[ i ]
        serialize_type( sub_value, data )


## ======================================================================


"""
types configuration for serialization and deserialization
<deserialize_function> converts given Godot type in form of binary array into Python equivalent
<serialize_function>   converts Python value into binary array representing Godot type
"""
CONFIG_LIST = [
    ( GodotType.NULL,   type(None), deserialize_none,   serialize_none ),
    ( GodotType.BOOL,   bool,       deserialize_bool,   serialize_bool ),
    ( GodotType.INT,    int,        deserialize_int,    serialize_int ),
    ( GodotType.FLOAT,  float,      deserialize_float,  serialize_float ),
    ( GodotType.STRING, str,        deserialize_string, serialize_string ),
    ( GodotType.DICT,   dict,       deserialize_dict,   serialize_dict ),
    ( GodotType.LIST,   list,       deserialize_list,   serialize_list )
]


## ======================================================================


## calculate proper maps and validate configuration
DESERIALIZATION_MAP = {}        ## map GodotType to deserialization function
SERIALIZATION_MAP   = {}

for config in CONFIG_LIST:
    ## deserialization map
    config_gd_type = config[0]
    if config_gd_type in DESERIALIZATION_MAP:
        raise ValueError( "invalid CONFIG_LIST: Godot type %s already defined" % config_gd_type )
    DESERIALIZATION_MAP[ config_gd_type ] = config[2]
    
    ## serialization map
    config_py_type = config[1]
    if config_py_type in SERIALIZATION_MAP:
        raise ValueError( "invalid CONFIG_LIST: Python type %s already defined" % config_py_type )
    SERIALIZATION_MAP[ config_py_type ] = ( config_gd_type, config[3] )


## ======================================================================


## returns Python equivalent of given data
def deserialize_type( data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: %s" % data )

    data_flags, data_type = data.popFlagsType()
    data_type_id          = GodotType.fromInt( data_type )
    
    deserialize_function = DESERIALIZATION_MAP.get( data_type_id, None )
    if deserialize_function is None:
        _LOGGER.error( "unhandled data type %s %s", data_type, data_type_id )
        raise ValueError( "invalid CONFIG_LIST: missing entry for GodotType %s" % data_type_id )

    return deserialize_function( data_flags, data )
    
#     for config in CONFIG_LIST:
#         config_gd_type = config[0]
#         if data_type_id is config_gd_type:
#             deserialize_function = config[2]
#             proper_data = deserialize_function( data_flags, data )
#             return ( data_type_id, proper_data )
# 
#     ## unhandled case
#     _LOGGER.error( "unhandled data type %s %s", data_type, data_type_id )
#     return ( data_type_id, None )


## serialize into 'data' given Python 'value' as binary representation of Godot equivalent
def serialize_type( value, data: BytesContainer ):
    value_type = type( value )
    
    serialize_config = SERIALIZATION_MAP.get( value_type, None )
    if serialize_config is None:
        #_LOGGER.warning( "unable to serialize data: %s %s", value, type(value) )
        raise ValueError( "unable to serialize data: %s %s" % ( value, type(value) ) )
    
    data_type_id       = serialize_config[0]
    serialize_function = serialize_config[1]

    serialize_function( data_type_id, value, data )
    
#     for config in CONFIG_LIST:
#         config_py_type = config[1]
#         ## if isinstance(value, config_py_type):
#         if value_type is config_py_type:
#             serialize_function = config[3]
#             data_type_id       = config[0]
#             serialize_function( data_type_id, value, data )
#             return
# 
#     raise ValueError( "unable to serialize data: %s %s" % ( value, type(value) ) )
#     #_LOGGER.warning( "unable to serialize data: %s %s", value, type(value) )
