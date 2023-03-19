from . import PbContent_pb2 as _PbContent_pb2
from . import User_pb2 as _User_pb2
from . import Agree_pb2 as _Agree_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubPost(_message.Message):
    __slots__ = ["pid", "sub_post_list"]
    PID_FIELD_NUMBER: _ClassVar[int]
    SUB_POST_LIST_FIELD_NUMBER: _ClassVar[int]
    pid: int
    sub_post_list: _containers.RepeatedCompositeFieldContainer[SubPostList]
    def __init__(self, pid: _Optional[int] = ..., sub_post_list: _Optional[_Iterable[_Union[SubPostList, _Mapping]]] = ...) -> None: ...

class SubPostList(_message.Message):
    __slots__ = ["agree", "author", "author_id", "content", "floor", "id", "time", "title"]
    AGREE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FLOOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    agree: _Agree_pb2.Agree
    author: _User_pb2.User
    author_id: int
    content: _containers.RepeatedCompositeFieldContainer[_PbContent_pb2.PbContent]
    floor: int
    id: int
    time: int
    title: str
    def __init__(self, id: _Optional[int] = ..., content: _Optional[_Iterable[_Union[_PbContent_pb2.PbContent, _Mapping]]] = ..., time: _Optional[int] = ..., author_id: _Optional[int] = ..., title: _Optional[str] = ..., floor: _Optional[int] = ..., author: _Optional[_Union[_User_pb2.User, _Mapping]] = ..., agree: _Optional[_Union[_Agree_pb2.Agree, _Mapping]] = ...) -> None: ...
