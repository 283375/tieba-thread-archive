from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ["errmsg", "errorno"]
    ERRMSG_FIELD_NUMBER: _ClassVar[int]
    ERRORNO_FIELD_NUMBER: _ClassVar[int]
    errmsg: str
    errorno: int
    def __init__(self, errorno: _Optional[int] = ..., errmsg: _Optional[str] = ...) -> None: ...
