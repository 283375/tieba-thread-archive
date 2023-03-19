from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Page(_message.Message):
    __slots__ = ["current_page", "has_more", "has_prev", "page_size", "total_count", "total_page"]
    CURRENT_PAGE_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    HAS_PREV_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGE_FIELD_NUMBER: _ClassVar[int]
    current_page: int
    has_more: int
    has_prev: int
    page_size: int
    total_count: int
    total_page: int
    def __init__(self, page_size: _Optional[int] = ..., current_page: _Optional[int] = ..., total_count: _Optional[int] = ..., total_page: _Optional[int] = ..., has_more: _Optional[int] = ..., has_prev: _Optional[int] = ...) -> None: ...
