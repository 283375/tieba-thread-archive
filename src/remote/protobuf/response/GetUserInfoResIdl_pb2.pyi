from ..common import Error_pb2 as _Error_pb2
from ..common import User_pb2 as _User_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserInfoResIdl(_message.Message):
    __slots__ = ["data", "error"]
    class DataRes(_message.Message):
        __slots__ = ["user"]
        USER_FIELD_NUMBER: _ClassVar[int]
        user: _User_pb2.User
        def __init__(self, user: _Optional[_Union[_User_pb2.User, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    data: GetUserInfoResIdl.DataRes
    error: _Error_pb2.Error
    def __init__(self, error: _Optional[_Union[_Error_pb2.Error, _Mapping]] = ..., data: _Optional[_Union[GetUserInfoResIdl.DataRes, _Mapping]] = ...) -> None: ...
