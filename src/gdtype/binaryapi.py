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
from enum import IntEnum, unique
from typing import Dict, Tuple, Callable, Any
from dataclasses import dataclass

from gdtype.bytescontainer import BytesContainer


_LOGGER = logging.getLogger(__name__)


def deserialize( message: bytes ):
    data = BytesContainer( message )
    data_len = data.size()
    if data_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", data )
        raise ValueError( f"invalid packet -- too short: {data}" % data )

    packet_size = data.popInt()
    data_size   = data.size()
    if data_size != packet_size:
        _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", data )
        raise ValueError( f"packet isze mismatch: {data}" )

    return deserialize_type( data )


def serialize( value ) -> bytes:
    data = BytesContainer()
    serialize_type( value, data )
    if data.size() < 1:
        ## failed to serialize data
        raise ValueError( "failed to serialize: empty output data" )
    message = BytesContainer()
    header_size = data.size()
    message.pushInt( header_size )
    message.push( data.data )
    return message.data


def get_message_length( data: bytes ):
    container = BytesContainer( data )
    if container.size() < 4:
        _LOGGER.error( "message is too short: %s", data )
        return None
    return container.popInt()


## ======================================================================
## ======================================================================


## returns Python equivalent of given data
def deserialize_type( data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )

    data_flags, gd_type_id = data.popFlagsType()

    deserialize_function = get_deserialization_function( gd_type_id )
    if deserialize_function is None:
        raise ValueError( f"unable to get deserialization info for Godot type {gd_type_id}" )

    return deserialize_function( data_flags, data )

#     for config in CONFIG_LIST:
#         config_gd_type = config[0]
#         if gd_type_id is config_gd_type:
#             deserialize_function = config[2]
#             proper_data = deserialize_function( data_flags, data )
#             return ( gd_type_id, proper_data )
#
#     ## unhandled case
#     _LOGGER.error( "unhandled data type %s %s", data_type, gd_type_id )
#     return ( gd_type_id, None )


## serialize into 'data' given Python 'value' as binary representation of Godot equivalent
def serialize_type( value, data: BytesContainer ):
    value_type = type( value )

    serialize_config = get_serialization_config( value_type )
#     serialize_config = SERIALIZATION_MAP.get( value_type, None )
    if serialize_config is None:
        #_LOGGER.warning( "unable to serialize data: %s %s", value, type(value) )
        raise ValueError( f"unable to serialize data: {value} {type(value)}" )

    gd_type_id         = serialize_config[0]
    serialize_function = serialize_config[1]

    serialize_function( gd_type_id, value, data )

#     for config in CONFIG_LIST:
#         config_py_type = config[1]
#         ## if isinstance(value, config_py_type):
#         if value_type is config_py_type:
#             serialize_function = config[3]
#             gd_type_id         = config[0]
#             serialize_function( gd_type_id, value, data )
#             return
#
#     raise ValueError( "unable to serialize data: %s %s" % ( value, type(value) ) )
#     #_LOGGER.warning( "unable to serialize data: %s %s", value, type(value) )


## =========================================================

# def get_deserialization_function( gd_type_id: int ):
#     raise NotImplementedError( "stub function: implement and import proper function" )
#
# def get_serialization_config( py_type: type ):
#     raise NotImplementedError( "stub function: implement and import proper function" )

## =========================================================


def deserialize_uninplemented( data_flags: int, data: BytesContainer ):
    raise NotImplementedError( "stub deserialization used: implement/use proper function" )


def serialize_uninplemented( gd_type_id: int, value, data: BytesContainer ):
    raise NotImplementedError( "stub serialization used: implement/use proper function" )


## =========================================================


def deserialize_none( _: int, _2: BytesContainer ):
    return None


def serialize_none( gd_type_id: int, _, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )


## =========================================================


# def deserialize_bool( data_flags: int, data: BytesContainer ):
def deserialize_bool( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", data )
        raise ValueError( f"invalid packet -- too short: {data}" )
    data_value = data.popInt()
    proper_data = data_value > 0
    return proper_data


def serialize_bool( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data.pushInt( value )


## =========================================================


# def deserialize_int( data_flags: int, data: BytesContainer ):
def deserialize_int( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    proper_data = data.popInt()
    if proper_data & 0x80000000:
        ## got negative number
        neg_val = proper_data & 0x7FFFFFFF
        return -0x80000000 + neg_val
#         return proper_data & 0x7FFFFFFF | ~0x7FFFFFFF

    ## positive number
    return proper_data


def serialize_int( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    if value & 0x80000000:
        ## got negative number
        pos_val = value & 0x7FFFFFFF
        out = 0x80000000 + pos_val
        data.pushInt( out )
    else:
        ## positive number
        data.pushInt( value )


## =========================================================


def deserialize_float( data_flags: int, data: BytesContainer ):
    data_len = data.size()
    encoded_64 = (data_flags & 1) == 1
    if encoded_64:
        if data_len < 8:
            raise ValueError( f"invalid packet -- too short: {data}" )
        proper_data = data.popFloat64()
        return proper_data
    ## 32 bit variant
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    proper_data = data.popFloat32()
    return proper_data


def serialize_float( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 1, gd_type_id )
    data.pushFloat64( value )


## =========================================================


# def deserialize_string( data_flags: int, data: BytesContainer ):
def deserialize_string( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    string_len = data.popInt()
    if string_len < 1:
        return ""
    proper_data = data.popString( string_len )
    return proper_data


def serialize_string( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    str_len = len( value )
    data.pushInt( str_len )
    data.pushString( value )
    remaining = str_len % 4
    padding = 4 - remaining
    if padding < 4:
        data.pushZeros( padding )


## =========================================================


@dataclass
class Vector3():
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __init__( self, data_array = None ):
        if data_array is None:
            return
        if len(data_array) != 3:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]
        self.z = data_array[2]

    def getDataArray(self):
        return [ self.x, self.y, self.z ]


# def deserialize_vector3( data_flags: int, data: BytesContainer ):
def deserialize_vector3( _: int, data: BytesContainer ) -> Vector3:
    ## XYZ
    data = data.popFloat32Items(3)
    return Vector3( data )


def serialize_vector3( gd_type_id: int, value: Vector3, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    ## XYZ
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Transform3D():
    ## has 3 rows and 4 columns
    values: list
    
    def __init__( self, data_array = None ):
        if data_array is None:
            self.values: list = [ 0.0 ] * 12
            return
        if len(data_array) != 12:
            raise ValueError( f"invalid array size: {data_array}" )
        self.values = list( data_array )    ## copy

    def __getitem__( self, key ):
        return self.values[ key ]

    def get( self, row, col ):
        return self.values[ col + row * 3 ]

    def getDataArray(self):
        return list( self.values )


# def deserialize_vector3( data_flags: int, data: BytesContainer ):
def deserialize_transform3d( _: int, data: BytesContainer ) -> Transform3D:
    data = data.popFloat32Items(12)
    return Transform3D( data )


def serialize_transform3d( gd_type_id: int, value: Transform3D, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Color():
    red: float   = 0.0
    green: float = 0.0
    blue: float  = 0.0
    alpha: float = 0.0

    def __init__( self, data_array = None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.red   = data_array[0]
        self.green = data_array[1]
        self.blue  = data_array[2]
        self.alpha = data_array[3]

    def getDataArray(self):
        return [ self.red, self.green, self.blue, self.alpha ]


# def deserialize_color( data_flags: int, data: BytesContainer ):
def deserialize_color( _: int, data: BytesContainer ) -> Color:
    ## RGBA
    data = data.popFloat32Items(4)
    return Color( data )


def serialize_color( gd_type_id: int, value: Color, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    ## RGBA
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class StringName():
    value: str


# def deserialize_color( data_flags: int, data: BytesContainer ):
def deserialize_stringname( _: int, data: BytesContainer ) -> StringName:
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    string_len = data.popInt()
    if string_len < 1:
        return ""
    proper_data = data.popString( string_len )
    return StringName( proper_data )


def serialize_stringname( gd_type_id: int, value: StringName, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    raw_value = value.value
    str_len = len( raw_value )
    data.pushInt( str_len )
    data.pushString( raw_value )
    remaining = str_len % 4
    padding = 4 - remaining
    if padding < 4:
        data.pushZeros( padding )


## =========================================================


# def deserialize_dict( data_flags: int, data: BytesContainer ):
def deserialize_dict( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
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


def serialize_dict( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    dict_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = dict_size & 0x7FFFFFFF
    data.pushInt( data_header )
    for key in value:
        serialize_type( key, data )
        sub_value = value[ key ]
        serialize_type( sub_value, data )


## =========================================================

# def deserialize_list( data_flags: int, data: BytesContainer ):
def deserialize_list( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
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


def serialize_list( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = list_size & 0x7FFFFFFF
    data.pushInt( data_header )
    for i in range(0, list_size):
        sub_value = value[ i ]
        serialize_type( sub_value, data )


## ======================================================================


@unique
class GodotType( IntEnum ):
    NULL                = 0
    BOOL                = 1
    INT                 = 2
    FLOAT               = 3
    STRING              = 4
    VECTOR3             = 9
    TRANSFORM3D         = 18
    COLOR               = 20
    STRINGNAME          = 21
    DICT                = 27
    LIST                = 28
#     PackedColorArray    = 37

    @classmethod
    def fromInt(cls, value):
        try:
            return GodotType( value )
        except ValueError as ex:
            raise ValueError( f"unsupported Godot type: {value}" ) from ex


## types configuration for serialization and deserialization
## <deserialize_function> converts given Godot type in form of binary array into Python equivalent
## <serialize_function>   converts Python value into binary array representing Godot type
CONFIG_LIST = [
    ( GodotType.NULL,          type(None),   deserialize_none,         serialize_none ),
    ( GodotType.BOOL,          bool,         deserialize_bool,         serialize_bool ),
    ( GodotType.INT,           int,          deserialize_int,          serialize_int ),
    ( GodotType.FLOAT,         float,        deserialize_float,        serialize_float ),
    ( GodotType.STRING,        str,          deserialize_string,       serialize_string ),
    ( GodotType.VECTOR3,       Vector3,      deserialize_vector3,      serialize_vector3 ),
    ( GodotType.TRANSFORM3D,   Transform3D,  deserialize_transform3d,  serialize_transform3d ),
    ( GodotType.COLOR,         Color,        deserialize_color,        serialize_color ),
    ( GodotType.STRINGNAME,    StringName,   deserialize_stringname,   serialize_stringname ),
    ( GodotType.DICT,          dict,         deserialize_dict,         serialize_dict ),
    ( GodotType.LIST,          list,         deserialize_list,         serialize_list )

    # ( GodotType.BOOL,  bool,        deserialize_uninplemented,  serialize_uninplemented ),
]


## ======================================================================


## calculate proper maps and validate configuration
DESERIALIZATION_MAP: Dict[ GodotType, Callable[[int, BytesContainer], Any] ] = {}
SERIALIZATION_MAP: Dict[ object, Tuple[GodotType, Callable[[int, Any, BytesContainer], Any]] ] = {}

for config in CONFIG_LIST:
    ## deserialization map
    gd_type: GodotType = config[0]
    if gd_type in DESERIALIZATION_MAP:
        raise ValueError( f"invalid CONFIG_LIST: Godot type {gd_type} already defined" )
    DESERIALIZATION_MAP[ gd_type ] = config[2]

    ## serialization map
    config_py_type: object = config[1]
    if config_py_type in SERIALIZATION_MAP:
        raise ValueError( f"invalid CONFIG_LIST: Python type {config_py_type} already defined" )
    func_ptr = config[3]
    SERIALIZATION_MAP[ config_py_type ] = ( gd_type, func_ptr )


def get_deserialization_function( gd_type_id: int ):
    data_type = GodotType.fromInt( gd_type_id )
    deserialize_function = DESERIALIZATION_MAP.get( data_type, None )
    if deserialize_function is None:
        raise ValueError( f"invalid CONFIG_LIST: unsupported Godot type {gd_type_id}" )
    return deserialize_function


def get_serialization_config( py_type: type ):
    return SERIALIZATION_MAP.get( py_type, None )
