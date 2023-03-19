from ..common import CommonReq_pb2 as _CommonReq_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PbPageReqIdl(_message.Message):
    __slots__ = ["data"]
    class DataReq(_message.Message):
        __slots__ = ["comment_rn", "comment_sort_by_agree", "common", "is_fold", "only_thread_author", "pid", "pn", "rn", "sort", "tid", "with_comments"]
        COMMENT_RN_FIELD_NUMBER: _ClassVar[int]
        COMMENT_SORT_BY_AGREE_FIELD_NUMBER: _ClassVar[int]
        COMMON_FIELD_NUMBER: _ClassVar[int]
        IS_FOLD_FIELD_NUMBER: _ClassVar[int]
        ONLY_THREAD_AUTHOR_FIELD_NUMBER: _ClassVar[int]
        PID_FIELD_NUMBER: _ClassVar[int]
        PN_FIELD_NUMBER: _ClassVar[int]
        RN_FIELD_NUMBER: _ClassVar[int]
        SORT_FIELD_NUMBER: _ClassVar[int]
        TID_FIELD_NUMBER: _ClassVar[int]
        WITH_COMMENTS_FIELD_NUMBER: _ClassVar[int]
        comment_rn: int
        comment_sort_by_agree: int
        common: _CommonReq_pb2.CommonReq
        is_fold: int
        only_thread_author: int
        pid: int
        pn: int
        rn: int
        sort: int
        tid: int
        with_comments: int
        def __init__(self, common: _Optional[_Union[_CommonReq_pb2.CommonReq, _Mapping]] = ..., tid: _Optional[int] = ..., only_thread_author: _Optional[int] = ..., sort: _Optional[int] = ..., pid: _Optional[int] = ..., with_comments: _Optional[int] = ..., comment_rn: _Optional[int] = ..., rn: _Optional[int] = ..., pn: _Optional[int] = ..., comment_sort_by_agree: _Optional[int] = ..., is_fold: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: PbPageReqIdl.DataReq
    def __init__(self, data: _Optional[_Union[PbPageReqIdl.DataReq, _Mapping]] = ...) -> None: ...
