from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ["BDUSS", "bawu_type", "concern_num", "fans_num", "gender", "id", "intro", "ip_address", "is_bawu", "is_coreuser", "is_default_avatar", "is_fans", "is_friend", "is_guanfang", "level_id", "likeForum", "name", "name_show", "new_god_data", "new_tshow_icon", "portrait", "post_num", "priv_sets", "sex", "tb_age", "tieba_uid", "user_growth", "vipInfo", "virtual_image_info"]
    class LikeForumInfo(_message.Message):
        __slots__ = ["forum_id", "forum_name"]
        FORUM_ID_FIELD_NUMBER: _ClassVar[int]
        FORUM_NAME_FIELD_NUMBER: _ClassVar[int]
        forum_id: int
        forum_name: str
        def __init__(self, forum_name: _Optional[str] = ..., forum_id: _Optional[int] = ...) -> None: ...
    class NewGodInfo(_message.Message):
        __slots__ = ["field_id", "field_name", "status"]
        FIELD_ID_FIELD_NUMBER: _ClassVar[int]
        FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        field_id: int
        field_name: str
        status: int
        def __init__(self, status: _Optional[int] = ..., field_id: _Optional[int] = ..., field_name: _Optional[str] = ...) -> None: ...
    class PrivSets(_message.Message):
        __slots__ = ["bazhu_show_inside", "bazhu_show_outside", "friend", "group", "like", "live", "location", "post", "reply"]
        BAZHU_SHOW_INSIDE_FIELD_NUMBER: _ClassVar[int]
        BAZHU_SHOW_OUTSIDE_FIELD_NUMBER: _ClassVar[int]
        FRIEND_FIELD_NUMBER: _ClassVar[int]
        GROUP_FIELD_NUMBER: _ClassVar[int]
        LIKE_FIELD_NUMBER: _ClassVar[int]
        LIVE_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        POST_FIELD_NUMBER: _ClassVar[int]
        REPLY_FIELD_NUMBER: _ClassVar[int]
        bazhu_show_inside: int
        bazhu_show_outside: int
        friend: int
        group: int
        like: int
        live: int
        location: int
        post: int
        reply: int
        def __init__(self, location: _Optional[int] = ..., like: _Optional[int] = ..., group: _Optional[int] = ..., post: _Optional[int] = ..., friend: _Optional[int] = ..., live: _Optional[int] = ..., reply: _Optional[int] = ..., bazhu_show_inside: _Optional[int] = ..., bazhu_show_outside: _Optional[int] = ...) -> None: ...
    class TshowInfo(_message.Message):
        __slots__ = ["name"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        name: str
        def __init__(self, name: _Optional[str] = ...) -> None: ...
    class UserGrowth(_message.Message):
        __slots__ = ["level_id"]
        LEVEL_ID_FIELD_NUMBER: _ClassVar[int]
        level_id: int
        def __init__(self, level_id: _Optional[int] = ...) -> None: ...
    class UserVipInfo(_message.Message):
        __slots__ = ["v_level", "v_status"]
        V_LEVEL_FIELD_NUMBER: _ClassVar[int]
        V_STATUS_FIELD_NUMBER: _ClassVar[int]
        v_level: int
        v_status: int
        def __init__(self, v_status: _Optional[int] = ..., v_level: _Optional[int] = ...) -> None: ...
    class VirtualImageInfo(_message.Message):
        __slots__ = ["isset_virtual_image", "personal_state"]
        class StateInfo(_message.Message):
            __slots__ = ["text"]
            TEXT_FIELD_NUMBER: _ClassVar[int]
            text: str
            def __init__(self, text: _Optional[str] = ...) -> None: ...
        ISSET_VIRTUAL_IMAGE_FIELD_NUMBER: _ClassVar[int]
        PERSONAL_STATE_FIELD_NUMBER: _ClassVar[int]
        isset_virtual_image: int
        personal_state: User.VirtualImageInfo.StateInfo
        def __init__(self, isset_virtual_image: _Optional[int] = ..., personal_state: _Optional[_Union[User.VirtualImageInfo.StateInfo, _Mapping]] = ...) -> None: ...
    BAWU_TYPE_FIELD_NUMBER: _ClassVar[int]
    BDUSS: str
    BDUSS_FIELD_NUMBER: _ClassVar[int]
    CONCERN_NUM_FIELD_NUMBER: _ClassVar[int]
    FANS_NUM_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INTRO_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IS_BAWU_FIELD_NUMBER: _ClassVar[int]
    IS_COREUSER_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_AVATAR_FIELD_NUMBER: _ClassVar[int]
    IS_FANS_FIELD_NUMBER: _ClassVar[int]
    IS_FRIEND_FIELD_NUMBER: _ClassVar[int]
    IS_GUANFANG_FIELD_NUMBER: _ClassVar[int]
    LEVEL_ID_FIELD_NUMBER: _ClassVar[int]
    LIKEFORUM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_SHOW_FIELD_NUMBER: _ClassVar[int]
    NEW_GOD_DATA_FIELD_NUMBER: _ClassVar[int]
    NEW_TSHOW_ICON_FIELD_NUMBER: _ClassVar[int]
    PORTRAIT_FIELD_NUMBER: _ClassVar[int]
    POST_NUM_FIELD_NUMBER: _ClassVar[int]
    PRIV_SETS_FIELD_NUMBER: _ClassVar[int]
    SEX_FIELD_NUMBER: _ClassVar[int]
    TB_AGE_FIELD_NUMBER: _ClassVar[int]
    TIEBA_UID_FIELD_NUMBER: _ClassVar[int]
    USER_GROWTH_FIELD_NUMBER: _ClassVar[int]
    VIPINFO_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    bawu_type: str
    concern_num: int
    fans_num: int
    gender: int
    id: int
    intro: str
    ip_address: str
    is_bawu: int
    is_coreuser: int
    is_default_avatar: int
    is_fans: int
    is_friend: int
    is_guanfang: int
    level_id: int
    likeForum: _containers.RepeatedCompositeFieldContainer[User.LikeForumInfo]
    name: str
    name_show: str
    new_god_data: User.NewGodInfo
    new_tshow_icon: _containers.RepeatedCompositeFieldContainer[User.TshowInfo]
    portrait: str
    post_num: int
    priv_sets: User.PrivSets
    sex: int
    tb_age: str
    tieba_uid: str
    user_growth: User.UserGrowth
    vipInfo: User.UserVipInfo
    virtual_image_info: User.VirtualImageInfo
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., name_show: _Optional[str] = ..., portrait: _Optional[str] = ..., is_coreuser: _Optional[int] = ..., level_id: _Optional[int] = ..., is_bawu: _Optional[int] = ..., bawu_type: _Optional[str] = ..., BDUSS: _Optional[str] = ..., fans_num: _Optional[int] = ..., concern_num: _Optional[int] = ..., sex: _Optional[int] = ..., intro: _Optional[str] = ..., post_num: _Optional[int] = ..., tb_age: _Optional[str] = ..., gender: _Optional[int] = ..., priv_sets: _Optional[_Union[User.PrivSets, _Mapping]] = ..., is_friend: _Optional[int] = ..., likeForum: _Optional[_Iterable[_Union[User.LikeForumInfo, _Mapping]]] = ..., is_guanfang: _Optional[int] = ..., vipInfo: _Optional[_Union[User.UserVipInfo, _Mapping]] = ..., new_tshow_icon: _Optional[_Iterable[_Union[User.TshowInfo, _Mapping]]] = ..., is_fans: _Optional[int] = ..., new_god_data: _Optional[_Union[User.NewGodInfo, _Mapping]] = ..., is_default_avatar: _Optional[int] = ..., tieba_uid: _Optional[str] = ..., ip_address: _Optional[str] = ..., virtual_image_info: _Optional[_Union[User.VirtualImageInfo, _Mapping]] = ..., user_growth: _Optional[_Union[User.UserGrowth, _Mapping]] = ...) -> None: ...
