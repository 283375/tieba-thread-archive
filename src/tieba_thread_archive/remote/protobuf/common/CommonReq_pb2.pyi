from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommonReq(_message.Message):
    __slots__ = ["BDUSS", "_client_type", "_client_version"]
    BDUSS: str
    BDUSS_FIELD_NUMBER: _ClassVar[int]
    _CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    _CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    _client_type: int
    _client_version: str
    def __init__(self, _client_type: _Optional[int] = ..., _client_version: _Optional[str] = ..., BDUSS: _Optional[str] = ...) -> None: ...
