from ..common import Error_pb2 as _Error_pb2
from ..common import SimpleForum_pb2 as _SimpleForum_pb2
from ..common import Page_pb2 as _Page_pb2
from ..common import Post_pb2 as _Post_pb2
from ..common import ThreadInfo_pb2 as _ThreadInfo_pb2
from ..common import SubPostList_pb2 as _SubPostList_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PbFloorResIdl(_message.Message):
    __slots__ = ["data", "error"]
    class DataRes(_message.Message):
        __slots__ = ["forum", "page", "post", "subpost_list", "thread"]
        FORUM_FIELD_NUMBER: _ClassVar[int]
        PAGE_FIELD_NUMBER: _ClassVar[int]
        POST_FIELD_NUMBER: _ClassVar[int]
        SUBPOST_LIST_FIELD_NUMBER: _ClassVar[int]
        THREAD_FIELD_NUMBER: _ClassVar[int]
        forum: _SimpleForum_pb2.SimpleForum
        page: _Page_pb2.Page
        post: _Post_pb2.Post
        subpost_list: _containers.RepeatedCompositeFieldContainer[_SubPostList_pb2.SubPostList]
        thread: _ThreadInfo_pb2.ThreadInfo
        def __init__(self, page: _Optional[_Union[_Page_pb2.Page, _Mapping]] = ..., post: _Optional[_Union[_Post_pb2.Post, _Mapping]] = ..., subpost_list: _Optional[_Iterable[_Union[_SubPostList_pb2.SubPostList, _Mapping]]] = ..., thread: _Optional[_Union[_ThreadInfo_pb2.ThreadInfo, _Mapping]] = ..., forum: _Optional[_Union[_SimpleForum_pb2.SimpleForum, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    data: PbFloorResIdl.DataRes
    error: _Error_pb2.Error
    def __init__(self, error: _Optional[_Union[_Error_pb2.Error, _Mapping]] = ..., data: _Optional[_Union[PbFloorResIdl.DataRes, _Mapping]] = ...) -> None: ...
