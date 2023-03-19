from ..common import CommonReq_pb2 as _CommonReq_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PbFloorReqIdl(_message.Message):
    __slots__ = ["data"]
    class DataReq(_message.Message):
        __slots__ = ["common", "pid", "pn", "spid", "tid"]
        COMMON_FIELD_NUMBER: _ClassVar[int]
        PID_FIELD_NUMBER: _ClassVar[int]
        PN_FIELD_NUMBER: _ClassVar[int]
        SPID_FIELD_NUMBER: _ClassVar[int]
        TID_FIELD_NUMBER: _ClassVar[int]
        common: _CommonReq_pb2.CommonReq
        pid: int
        pn: int
        spid: int
        tid: int
        def __init__(self, common: _Optional[_Union[_CommonReq_pb2.CommonReq, _Mapping]] = ..., tid: _Optional[int] = ..., pid: _Optional[int] = ..., spid: _Optional[int] = ..., pn: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: PbFloorReqIdl.DataReq
    def __init__(self, data: _Optional[_Union[PbFloorReqIdl.DataReq, _Mapping]] = ...) -> None: ...
