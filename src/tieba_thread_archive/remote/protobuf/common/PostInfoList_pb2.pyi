from . import Media_pb2 as _Media_pb2
from . import PollInfo_pb2 as _PollInfo_pb2
from . import PbContent_pb2 as _PbContent_pb2
from . import Agree_pb2 as _Agree_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostInfoList(_message.Message):
    __slots__ = ["agree", "content", "create_time", "first_post_content", "forum_id", "forum_name", "freq_num", "is_share_thread", "media", "name_show", "poll_info", "post_id", "reply_num", "share_num", "thread_id", "thread_type", "title", "user_id", "user_name", "user_portrait"]
    class PostInfoContent(_message.Message):
        __slots__ = ["create_time", "post_content", "post_id", "post_type"]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        POST_CONTENT_FIELD_NUMBER: _ClassVar[int]
        POST_ID_FIELD_NUMBER: _ClassVar[int]
        POST_TYPE_FIELD_NUMBER: _ClassVar[int]
        create_time: int
        post_content: _containers.RepeatedCompositeFieldContainer[_PbContent_pb2.PbContent]
        post_id: int
        post_type: int
        def __init__(self, post_content: _Optional[_Iterable[_Union[_PbContent_pb2.PbContent, _Mapping]]] = ..., create_time: _Optional[int] = ..., post_type: _Optional[int] = ..., post_id: _Optional[int] = ...) -> None: ...
    AGREE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    FIRST_POST_CONTENT_FIELD_NUMBER: _ClassVar[int]
    FORUM_ID_FIELD_NUMBER: _ClassVar[int]
    FORUM_NAME_FIELD_NUMBER: _ClassVar[int]
    FREQ_NUM_FIELD_NUMBER: _ClassVar[int]
    IS_SHARE_THREAD_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    NAME_SHOW_FIELD_NUMBER: _ClassVar[int]
    POLL_INFO_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_NUM_FIELD_NUMBER: _ClassVar[int]
    SHARE_NUM_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_PORTRAIT_FIELD_NUMBER: _ClassVar[int]
    agree: _Agree_pb2.Agree
    content: _containers.RepeatedCompositeFieldContainer[PostInfoList.PostInfoContent]
    create_time: int
    first_post_content: _containers.RepeatedCompositeFieldContainer[_PbContent_pb2.PbContent]
    forum_id: int
    forum_name: str
    freq_num: int
    is_share_thread: int
    media: _containers.RepeatedCompositeFieldContainer[_Media_pb2.Media]
    name_show: str
    poll_info: _PollInfo_pb2.PollInfo
    post_id: int
    reply_num: int
    share_num: int
    thread_id: int
    thread_type: int
    title: str
    user_id: int
    user_name: str
    user_portrait: str
    def __init__(self, forum_id: _Optional[int] = ..., thread_id: _Optional[int] = ..., post_id: _Optional[int] = ..., create_time: _Optional[int] = ..., forum_name: _Optional[str] = ..., title: _Optional[str] = ..., content: _Optional[_Iterable[_Union[PostInfoList.PostInfoContent, _Mapping]]] = ..., user_name: _Optional[str] = ..., media: _Optional[_Iterable[_Union[_Media_pb2.Media, _Mapping]]] = ..., reply_num: _Optional[int] = ..., user_id: _Optional[int] = ..., user_portrait: _Optional[str] = ..., thread_type: _Optional[int] = ..., poll_info: _Optional[_Union[_PollInfo_pb2.PollInfo, _Mapping]] = ..., freq_num: _Optional[int] = ..., name_show: _Optional[str] = ..., share_num: _Optional[int] = ..., agree: _Optional[_Union[_Agree_pb2.Agree, _Mapping]] = ..., is_share_thread: _Optional[int] = ..., first_post_content: _Optional[_Iterable[_Union[_PbContent_pb2.PbContent, _Mapping]]] = ...) -> None: ...
