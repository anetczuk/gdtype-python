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

from typing import List, Tuple

from . import commontypes as ct


_LOGGER = logging.getLogger(__name__)


##
## interface functions
##
deserialize        = ct.deserialize
serialize          = ct.serialize
get_message_length = ct.get_message_length
check_message_size = ct.check_message_size


## ============================================================


@unique
class GodotType( IntEnum ):
    NULL                = 0
    BOOL                = 1
    INT                 = 2
    FLOAT               = 3
    STRING              = 4
    VECTOR2             = 5
    RECT2               = 6
    VECTOR3             = 7
    TRANSFORM2D         = 8
    PLANE               = 9
    QUAT                = 10
    AABB                = 11
    BASIS               = 12
    TRANSFORM           = 13
    COLOR               = 14
    NODEPATH            = 15
    RID                 = 16
#     OBJECT              = 17
    DICT                = 18
    LIST                = 19
    POOLBYTEARRAY       = 20
    POOLINT32ARRAY      = 21
    POOLFLOAT32ARRAY    = 22
    POOLSTRINGARRAY     = 23
    POOLVECTOR2ARRAY    = 24
    POOLVECTOR3ARRAY    = 25
    POOLCOLORARRAY      = 26

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
    ( GodotType.NULL.value,                 type(None),       ct.deserialize_none,         ct.serialize_none ),
    ( GodotType.BOOL.value,                 bool,             ct.deserialize_bool,         ct.serialize_bool ),
    ( GodotType.INT.value,                  int,              ct.deserialize_int,          ct.serialize_int ),
    ( GodotType.FLOAT.value,                float,            ct.deserialize_float,        ct.serialize_float ),
    ( GodotType.STRING.value,               str,              ct.deserialize_string,       ct.serialize_string ),
    ( GodotType.VECTOR2.value,              ct.Vector2 ),
    ( GodotType.RECT2.value,                ct.Rect2 ),
    ( GodotType.VECTOR3.value,              ct.Vector3 ),
    ( GodotType.TRANSFORM2D.value,          ct.Transform2D ),
    ( GodotType.PLANE.value,                ct.Plane ),
    ( GodotType.QUAT.value,                 ct.Quaternion ),
    ( GodotType.AABB.value,                 ct.AABB ),
    ( GodotType.BASIS.value,                ct.Basis ),
    ( GodotType.TRANSFORM.value,            ct.Transform3D ),
    ( GodotType.COLOR.value,                ct.Color ),
    ( GodotType.NODEPATH.value,             ct.NodePath ),
    ( GodotType.RID.value,                  ct.RID ),
    ( GodotType.DICT.value,                 dict,             ct.deserialize_dict,         ct.serialize_dict ),
    ( GodotType.LIST.value,                 list,             ct.deserialize_list,         ct.serialize_list ),
    ( GodotType.POOLBYTEARRAY.value,        ct.ByteArray ),
    ( GodotType.POOLINT32ARRAY.value,       ct.Int32Array ),
    ( GodotType.POOLFLOAT32ARRAY.value,     ct.Float32Array ),
    ( GodotType.POOLSTRINGARRAY.value,      ct.StringArray ),
    ( GodotType.POOLVECTOR2ARRAY.value,     ct.Vector2Array ),
    ( GodotType.POOLVECTOR3ARRAY.value,     ct.Vector3Array ),
    ( GodotType.POOLCOLORARRAY.value,       ct.ColorArray )

    # ( GodotType.BOOL.value,  bool,        deserialize_uninplemented,  serialize_uninplemented ),
]


## ======================================================================


DESERIALIZATION_MAP, SERIALIZATION_MAP = ct.prepare_config_dicts( CONFIG_LIST, ct )


def get_deserialization_function_v3( gd_type_id: int ):
    deserialize_function = DESERIALIZATION_MAP.get( gd_type_id, None )
    if deserialize_function is None:
        raise ValueError( f"invalid CONFIG_LIST: unsupported Godot type {gd_type_id}" )
    return deserialize_function


def get_serialization_config_v3( py_type: type ):
    return SERIALIZATION_MAP.get( py_type, None )


## override 'abstract' functions
ct.get_deserialization_function = get_deserialization_function_v3
ct.get_serialization_config     = get_serialization_config_v3
