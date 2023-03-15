from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Media(_message.Message):
    __slots__ = ["big_pic", "height", "origin_pic", "origin_size", "small_pic", "type", "water_pic", "width"]
    BIG_PIC_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_PIC_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SIZE_FIELD_NUMBER: _ClassVar[int]
    SMALL_PIC_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WATER_PIC_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    big_pic: str
    height: int
    origin_pic: str
    origin_size: int
    small_pic: str
    type: int
    water_pic: str
    width: int
    def __init__(self, type: _Optional[int] = ..., small_pic: _Optional[str] = ..., big_pic: _Optional[str] = ..., water_pic: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., origin_pic: _Optional[str] = ..., origin_size: _Optional[int] = ...) -> None: ...
