from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PbContent(_message.Message):
    __slots__ = ["big_cdn_src", "bsize", "c", "cdn_src", "item", "link", "origin_size", "origin_src", "src", "text", "tiebaplus_info", "type", "uid", "voice_md5"]
    class Item(_message.Message):
        __slots__ = ["item_name"]
        ITEM_NAME_FIELD_NUMBER: _ClassVar[int]
        item_name: str
        def __init__(self, item_name: _Optional[str] = ...) -> None: ...
    class TiebaPlusInfo(_message.Message):
        __slots__ = ["app_icon", "button_desc", "desc", "h5_jump_number", "h5_jump_param", "h5_jump_type", "jump_type", "jump_url", "target_type", "title"]
        APP_ICON_FIELD_NUMBER: _ClassVar[int]
        BUTTON_DESC_FIELD_NUMBER: _ClassVar[int]
        DESC_FIELD_NUMBER: _ClassVar[int]
        H5_JUMP_NUMBER_FIELD_NUMBER: _ClassVar[int]
        H5_JUMP_PARAM_FIELD_NUMBER: _ClassVar[int]
        H5_JUMP_TYPE_FIELD_NUMBER: _ClassVar[int]
        JUMP_TYPE_FIELD_NUMBER: _ClassVar[int]
        JUMP_URL_FIELD_NUMBER: _ClassVar[int]
        TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        app_icon: str
        button_desc: str
        desc: str
        h5_jump_number: str
        h5_jump_param: str
        h5_jump_type: int
        jump_type: int
        jump_url: str
        target_type: int
        title: str
        def __init__(self, title: _Optional[str] = ..., desc: _Optional[str] = ..., jump_url: _Optional[str] = ..., app_icon: _Optional[str] = ..., target_type: _Optional[int] = ..., h5_jump_type: _Optional[int] = ..., h5_jump_number: _Optional[str] = ..., h5_jump_param: _Optional[str] = ..., jump_type: _Optional[int] = ..., button_desc: _Optional[str] = ...) -> None: ...
    BIG_CDN_SRC_FIELD_NUMBER: _ClassVar[int]
    BSIZE_FIELD_NUMBER: _ClassVar[int]
    CDN_SRC_FIELD_NUMBER: _ClassVar[int]
    C_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SIZE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SRC_FIELD_NUMBER: _ClassVar[int]
    SRC_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TIEBAPLUS_INFO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    VOICE_MD5_FIELD_NUMBER: _ClassVar[int]
    big_cdn_src: str
    bsize: str
    c: str
    cdn_src: str
    item: PbContent.Item
    link: str
    origin_size: int
    origin_src: str
    src: str
    text: str
    tiebaplus_info: PbContent.TiebaPlusInfo
    type: int
    uid: int
    voice_md5: str
    def __init__(self, type: _Optional[int] = ..., text: _Optional[str] = ..., link: _Optional[str] = ..., src: _Optional[str] = ..., bsize: _Optional[str] = ..., cdn_src: _Optional[str] = ..., big_cdn_src: _Optional[str] = ..., c: _Optional[str] = ..., voice_md5: _Optional[str] = ..., uid: _Optional[int] = ..., origin_src: _Optional[str] = ..., origin_size: _Optional[int] = ..., tiebaplus_info: _Optional[_Union[PbContent.TiebaPlusInfo, _Mapping]] = ..., item: _Optional[_Union[PbContent.Item, _Mapping]] = ...) -> None: ...
