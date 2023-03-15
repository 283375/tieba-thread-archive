from . import PbContent_pb2 as _PbContent_pb2
from . import SubPostList_pb2 as _SubPostList_pb2
from . import User_pb2 as _User_pb2
from . import Agree_pb2 as _Agree_pb2
from . import SimpleForum_pb2 as _SimpleForum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Post(_message.Message):
    __slots__ = ["agree", "author", "author_id", "content", "custom_figure", "custom_state", "floor", "from_forum", "id", "signature", "sub_post_list", "sub_post_number", "tid", "time", "title"]
    class CustomFigure(_message.Message):
        __slots__ = ["background_value"]
        BACKGROUND_VALUE_FIELD_NUMBER: _ClassVar[int]
        background_value: str
        def __init__(self, background_value: _Optional[str] = ...) -> None: ...
    class CustomState(_message.Message):
        __slots__ = ["content"]
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        content: str
        def __init__(self, content: _Optional[str] = ...) -> None: ...
    class SignatureData(_message.Message):
        __slots__ = ["content"]
        class SignatureContent(_message.Message):
            __slots__ = ["text", "type"]
            TEXT_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            text: str
            type: int
            def __init__(self, type: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        content: _containers.RepeatedCompositeFieldContainer[Post.SignatureData.SignatureContent]
        def __init__(self, content: _Optional[_Iterable[_Union[Post.SignatureData.SignatureContent, _Mapping]]] = ...) -> None: ...
    class SubPost(_message.Message):
        __slots__ = ["sub_post_list"]
        SUB_POST_LIST_FIELD_NUMBER: _ClassVar[int]
        sub_post_list: _containers.RepeatedCompositeFieldContainer[_SubPostList_pb2.SubPostList]
        def __init__(self, sub_post_list: _Optional[_Iterable[_Union[_SubPostList_pb2.SubPostList, _Mapping]]] = ...) -> None: ...
    AGREE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIGURE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_STATE_FIELD_NUMBER: _ClassVar[int]
    FLOOR_FIELD_NUMBER: _ClassVar[int]
    FROM_FORUM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    SUB_POST_LIST_FIELD_NUMBER: _ClassVar[int]
    SUB_POST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    agree: _Agree_pb2.Agree
    author: _User_pb2.User
    author_id: int
    content: _containers.RepeatedCompositeFieldContainer[_PbContent_pb2.PbContent]
    custom_figure: Post.CustomFigure
    custom_state: Post.CustomState
    floor: int
    from_forum: _SimpleForum_pb2.SimpleForum
    id: int
    signature: Post.SignatureData
    sub_post_list: Post.SubPost
    sub_post_number: int
    tid: int
    time: int
    title: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., floor: _Optional[int] = ..., time: _Optional[int] = ..., content: _Optional[_Iterable[_Union[_PbContent_pb2.PbContent, _Mapping]]] = ..., sub_post_number: _Optional[int] = ..., author_id: _Optional[int] = ..., sub_post_list: _Optional[_Union[Post.SubPost, _Mapping]] = ..., signature: _Optional[_Union[Post.SignatureData, _Mapping]] = ..., author: _Optional[_Union[_User_pb2.User, _Mapping]] = ..., agree: _Optional[_Union[_Agree_pb2.Agree, _Mapping]] = ..., from_forum: _Optional[_Union[_SimpleForum_pb2.SimpleForum, _Mapping]] = ..., tid: _Optional[int] = ..., custom_figure: _Optional[_Union[Post.CustomFigure, _Mapping]] = ..., custom_state: _Optional[_Union[Post.CustomState, _Mapping]] = ...) -> None: ...
