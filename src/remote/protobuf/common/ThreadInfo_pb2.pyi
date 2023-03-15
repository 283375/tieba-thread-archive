from . import User_pb2 as _User_pb2
from . import PollInfo_pb2 as _PollInfo_pb2
from . import PbContent_pb2 as _PbContent_pb2
from . import Agree_pb2 as _Agree_pb2
from . import Media_pb2 as _Media_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThreadInfo(_message.Message):
    __slots__ = ["agree", "author", "author_id", "create_time", "custom_figure", "custom_state", "fid", "first_post_content", "first_post_id", "fname", "id", "is_ad", "is_deleted", "is_frs_mask", "is_godthread_recommend", "is_good", "is_livepost", "is_share_thread", "is_top", "is_voice_thread", "last_time_int", "origin_thread_info", "poll_info", "post_id", "reply_num", "share_num", "tab_id", "thread_type", "title", "view_num"]
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
    class OriginThreadInfo(_message.Message):
        __slots__ = ["content", "fid", "fname", "media", "pid", "poll_info", "tid", "title", "voice_info"]
        class Voice(_message.Message):
            __slots__ = ["type"]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            type: int
            def __init__(self, type: _Optional[int] = ...) -> None: ...
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        FID_FIELD_NUMBER: _ClassVar[int]
        FNAME_FIELD_NUMBER: _ClassVar[int]
        MEDIA_FIELD_NUMBER: _ClassVar[int]
        PID_FIELD_NUMBER: _ClassVar[int]
        POLL_INFO_FIELD_NUMBER: _ClassVar[int]
        TID_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        VOICE_INFO_FIELD_NUMBER: _ClassVar[int]
        content: _containers.RepeatedCompositeFieldContainer[_PbContent_pb2.PbContent]
        fid: int
        fname: str
        media: _containers.RepeatedCompositeFieldContainer[_Media_pb2.Media]
        pid: int
        poll_info: _PollInfo_pb2.PollInfo
        tid: str
        title: str
        voice_info: _containers.RepeatedCompositeFieldContainer[ThreadInfo.OriginThreadInfo.Voice]
        def __init__(self, title: _Optional[str] = ..., media: _Optional[_Iterable[_Union[_Media_pb2.Media, _Mapping]]] = ..., fname: _Optional[str] = ..., tid: _Optional[str] = ..., fid: _Optional[int] = ..., voice_info: _Optional[_Iterable[_Union[ThreadInfo.OriginThreadInfo.Voice, _Mapping]]] = ..., content: _Optional[_Iterable[_Union[_PbContent_pb2.PbContent, _Mapping]]] = ..., poll_info: _Optional[_Union[_PollInfo_pb2.PollInfo, _Mapping]] = ..., pid: _Optional[int] = ...) -> None: ...
    AGREE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIGURE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_STATE_FIELD_NUMBER: _ClassVar[int]
    FID_FIELD_NUMBER: _ClassVar[int]
    FIRST_POST_CONTENT_FIELD_NUMBER: _ClassVar[int]
    FIRST_POST_ID_FIELD_NUMBER: _ClassVar[int]
    FNAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_AD_FIELD_NUMBER: _ClassVar[int]
    IS_DELETED_FIELD_NUMBER: _ClassVar[int]
    IS_FRS_MASK_FIELD_NUMBER: _ClassVar[int]
    IS_GODTHREAD_RECOMMEND_FIELD_NUMBER: _ClassVar[int]
    IS_GOOD_FIELD_NUMBER: _ClassVar[int]
    IS_LIVEPOST_FIELD_NUMBER: _ClassVar[int]
    IS_SHARE_THREAD_FIELD_NUMBER: _ClassVar[int]
    IS_TOP_FIELD_NUMBER: _ClassVar[int]
    IS_VOICE_THREAD_FIELD_NUMBER: _ClassVar[int]
    LAST_TIME_INT_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_THREAD_INFO_FIELD_NUMBER: _ClassVar[int]
    POLL_INFO_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_NUM_FIELD_NUMBER: _ClassVar[int]
    SHARE_NUM_FIELD_NUMBER: _ClassVar[int]
    TAB_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    VIEW_NUM_FIELD_NUMBER: _ClassVar[int]
    agree: _Agree_pb2.Agree
    author: _User_pb2.User
    author_id: int
    create_time: int
    custom_figure: ThreadInfo.CustomFigure
    custom_state: ThreadInfo.CustomState
    fid: int
    first_post_content: _containers.RepeatedCompositeFieldContainer[_PbContent_pb2.PbContent]
    first_post_id: int
    fname: str
    id: int
    is_ad: int
    is_deleted: int
    is_frs_mask: int
    is_godthread_recommend: int
    is_good: int
    is_livepost: int
    is_share_thread: int
    is_top: int
    is_voice_thread: int
    last_time_int: int
    origin_thread_info: ThreadInfo.OriginThreadInfo
    poll_info: _PollInfo_pb2.PollInfo
    post_id: int
    reply_num: int
    share_num: int
    tab_id: int
    thread_type: int
    title: str
    view_num: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., reply_num: _Optional[int] = ..., view_num: _Optional[int] = ..., last_time_int: _Optional[int] = ..., is_top: _Optional[int] = ..., is_good: _Optional[int] = ..., is_voice_thread: _Optional[int] = ..., author: _Optional[_Union[_User_pb2.User, _Mapping]] = ..., thread_type: _Optional[int] = ..., fid: _Optional[int] = ..., fname: _Optional[str] = ..., is_livepost: _Optional[int] = ..., first_post_id: _Optional[int] = ..., create_time: _Optional[int] = ..., post_id: _Optional[int] = ..., author_id: _Optional[int] = ..., is_ad: _Optional[int] = ..., poll_info: _Optional[_Union[_PollInfo_pb2.PollInfo, _Mapping]] = ..., is_godthread_recommend: _Optional[int] = ..., agree: _Optional[_Union[_Agree_pb2.Agree, _Mapping]] = ..., share_num: _Optional[int] = ..., origin_thread_info: _Optional[_Union[ThreadInfo.OriginThreadInfo, _Mapping]] = ..., first_post_content: _Optional[_Iterable[_Union[_PbContent_pb2.PbContent, _Mapping]]] = ..., is_share_thread: _Optional[int] = ..., tab_id: _Optional[int] = ..., is_deleted: _Optional[int] = ..., is_frs_mask: _Optional[int] = ..., custom_figure: _Optional[_Union[ThreadInfo.CustomFigure, _Mapping]] = ..., custom_state: _Optional[_Union[ThreadInfo.CustomState, _Mapping]] = ...) -> None: ...
