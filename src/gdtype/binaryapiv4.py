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

from typing import List, Dict, Tuple, Callable, Any
from types import FunctionType

from .bytescontainer import BytesContainer
from . import commontypes as ct


_LOGGER = logging.getLogger(__name__)


def deserialize( message: bytes ):
    mess_len = len( message )
    if mess_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", message )
        raise ValueError( f"invalid packet -- too short: {mess_len} < 4 for {message!r}" )

    data = BytesContainer( message )
    expected_size = data.popInt32()
    message_size  = data.size()
    if message_size != expected_size:
        _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", data )
        raise ValueError( f"message size mismatch: {message_size} != {expected_size} for {data}" )

    return ct.deserialize_type( data )


def serialize( value ) -> bytes:
    data = BytesContainer()
    ct.serialize_type( value, data )
    data_size = data.size()
    if data_size < 1:
        ## failed to serialize data
        raise ValueError( "failed to serialize: empty output data" )
    message = BytesContainer()
    message.pushInt32( data_size )        ## set header
    message.push( data.data )
    return message.data


## read header value of message and return it
def get_message_length( data: bytes ):
    container = BytesContainer( data )
    if container.size() < 4:
        _LOGGER.error( "message is too short: %s", data )
        return None
    return container.popInt32()


## return:
##        0         if buffer contains full message without additional bytes
##        negative  if there is missing data (how many bytes are missing)
##        positive  if there are additional bytes (part of next message in case of TCP/IP)
##
## whole message consists of header and remaining data
## header is 4 bytes integer containing size of remaining data
## so whole message is sum of value in header increased by size of header itself
def check_message_size( buffer: bytes ):
    curr_size = len( buffer )
    if curr_size < 4:
        return -4 + curr_size
    expected_size = get_message_length( buffer )
    expected_size += 4                              ## increase by message header
    return curr_size - expected_size


## ======================================================================
## ======================================================================


@unique
class GodotType( IntEnum ):
    NULL                = 0
    BOOL                = 1
    INT                 = 2
    FLOAT               = 3
    STRING              = 4
    VECTOR2             = 5
    VECTOR2I            = 6
    RECT2               = 7
    RECT2I              = 8
    VECTOR3             = 9
    VECTOR3I            = 10
    TRANSFORM2D         = 11
    VECTOR4             = 12
    VECTOR4I            = 13
    PLANE               = 14
    QUATERNION          = 15
    AABB                = 16
    BASIS               = 17
    TRANSFORM3D         = 18
    PROJECTION          = 19
    COLOR               = 20
    STRINGNAME          = 21
    NODEPATH            = 22
    RID                 = 23
#     OBJECT              = 24
#     CALLABLE            = 25
#     SIGNAL              = 26
    DICT                = 27
    LIST                = 28
    PACKEDBYTEARRAY     = 29
    PACKEDINT32ARRAY    = 30
    PACKEDINT64ARRAY    = 31
    PACKEDFLOAT32ARRAY  = 32
    PACKEDFLOAT64ARRAY  = 33
    PACKEDSTRINGARRAY   = 34
    PACKEDVECTOR2ARRAY  = 35
    PACKEDVECTOR3ARRAY  = 36
    PACKEDCOLORARRAY    = 37

    @classmethod
    def fromInt(cls, value):
        try:
            return GodotType( value )
        except ValueError as ex:
            raise ValueError( f"unsupported Godot type: {value}" ) from ex


## types configuration for serialization and deserialization
## <deserialize_function> converts given Godot type in form of binary array into Python equivalent
## <serialize_function>   converts Python value into binary array representing Godot type
## configuration accepts two formats"
##     explicit: ( Godot_Type_Id, Python_Type, <deserialize_function>, <serialize_function> )
##     implicit: ( Godot_Type_Id, Python_Type )
##                where <deserialize_function> is "deserialize_Python_Type"
##                where <serialize_function>   is "serialize_Python_Type"
CONFIG_LIST: List[ Tuple ] = [
    ( GodotType.NULL.value,                 type(None),     ct.deserialize_none,         ct.serialize_none ),
    ( GodotType.BOOL.value,                 bool,           ct.deserialize_bool,         ct.serialize_bool ),
    ( GodotType.INT.value,                  int,            ct.deserialize_int,          ct.serialize_int ),
    ( GodotType.FLOAT.value,                float,          ct.deserialize_float,        ct.serialize_float ),
    ( GodotType.STRING.value,               str,            ct.deserialize_string,       ct.serialize_string ),
    ( GodotType.VECTOR2.value,              ct.Vector2,        ct.deserialize_vector2,      ct.serialize_vector2 ),
    ( GodotType.VECTOR2I.value,             ct.Vector2i,       ct.deserialize_vector2i,     ct.serialize_vector2i ),
    ( GodotType.RECT2.value,                ct.Rect2,          ct.deserialize_Rect2,        ct.serialize_Rect2 ),
    ( GodotType.RECT2I.value,               ct.Rect2i,         ct.deserialize_Rect2i,       ct.serialize_Rect2i ),
    ( GodotType.VECTOR3.value,              ct.Vector3,        ct.deserialize_vector3,      ct.serialize_vector3 ),
    ( GodotType.VECTOR3I.value,             ct.Vector3i,       ct.deserialize_vector3i,     ct.serialize_vector3i ),
    ( GodotType.TRANSFORM2D.value,          ct.Transform2D ),
    ( GodotType.VECTOR4.value,              ct.Vector4 ),
    ( GodotType.VECTOR4I.value,             ct.Vector4i ),
    ( GodotType.PLANE.value,                ct.Plane ),
    ( GodotType.QUATERNION.value,           ct.Quaternion ),
    ( GodotType.AABB.value,                 ct.AABB ),
    ( GodotType.BASIS.value,                ct.Basis ),
    ( GodotType.TRANSFORM3D.value,          ct.Transform3D ),
    ( GodotType.PROJECTION.value,           ct.Projection ),
    ( GodotType.COLOR.value,                ct.Color ),
    ( GodotType.STRINGNAME.value,           ct.StringName ),
    ( GodotType.NODEPATH.value,             ct.NodePath ),
    ( GodotType.RID.value,                  ct.RID ),
    ( GodotType.DICT.value,                 dict,           ct.deserialize_dict,         ct.serialize_dict ),
    ( GodotType.LIST.value,                 list,           ct.deserialize_list,         ct.serialize_list ),
    ( GodotType.PACKEDBYTEARRAY.value,      ct.ByteArray ),
    ( GodotType.PACKEDINT32ARRAY.value,     ct.Int32Array ),
    ( GodotType.PACKEDINT64ARRAY.value,     ct.Int64Array ),
    ( GodotType.PACKEDFLOAT32ARRAY.value,   ct.Float32Array ),
    ( GodotType.PACKEDFLOAT64ARRAY.value,   ct.Float64Array ),
    ( GodotType.PACKEDSTRINGARRAY.value,    ct.StringArray ),
    ( GodotType.PACKEDVECTOR2ARRAY.value,   ct.Vector2Array ),
    ( GodotType.PACKEDVECTOR3ARRAY.value,   ct.Vector3Array ),
    ( GodotType.PACKEDCOLORARRAY.value,     ct.ColorArray )

    # ( GodotType.BOOL.value,  bool,        deserialize_uninplemented,  serialize_uninplemented ),
]


## ======================================================================


## calculate proper maps and validate configuration
DESERIALIZATION_MAP: Dict[ int, Callable[[int, BytesContainer], Any] ] = {}
SERIALIZATION_MAP: Dict[ object, Tuple[int, FunctionType] ] = {}
# SERIALIZATION_MAP: Dict[ object, Tuple[int, Callable[[int, Any, BytesContainer], Any]] ] = {}

for config in CONFIG_LIST:
    ## deserialization map
    config_gd_type: int  = config[0]
    config_py_type: type = config[1]

    if len( config ) == 4:
        deserialize_func: FunctionType = config[2]
        serialize_func: FunctionType   = config[3]
    else:
        ## find serialization/deserialization functions by name
        py_type_name = config_py_type.__name__
        deserialize_func = getattr( ct, f"deserialize_{py_type_name}" )
        serialize_func   = getattr( ct, f"serialize_{py_type_name}" )
#         mod_vars = vars()
#         deserialize_func = mod_vars[ f"deserialize_{py_type_name}" ]
#         serialize_func   = mod_vars[ f"serialize_{py_type_name}" ]

    if config_gd_type in DESERIALIZATION_MAP:
        raise ValueError( f"invalid CONFIG_LIST: Godot type {config_gd_type} already defined" )
    DESERIALIZATION_MAP[ config_gd_type ] = deserialize_func

    ## serialization map
    if config_py_type in SERIALIZATION_MAP:
        raise ValueError( f"invalid CONFIG_LIST: Python type {config_py_type} already defined" )
    SERIALIZATION_MAP[ config_py_type ] = ( config_gd_type, serialize_func )


def get_deserialization_function_v4( gd_type_id: int ):
    deserialize_function = DESERIALIZATION_MAP.get( gd_type_id, None )
    if deserialize_function is None:
        raise ValueError( f"invalid CONFIG_LIST: unsupported Godot type {gd_type_id}" )
    return deserialize_function


def get_serialization_config_v4( py_type: type ):
    return SERIALIZATION_MAP.get( py_type, None )


ct.get_deserialization_function = get_deserialization_function_v4
ct.get_serialization_config     = get_serialization_config_v4
