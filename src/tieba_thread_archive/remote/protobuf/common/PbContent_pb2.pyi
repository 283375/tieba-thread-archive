from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class PbContent(_message.Message):
    __slots__ = [
        "_static",
        "big_cdn_src",
        "big_size",
        "big_src",
        "bsize",
        "btn_type",
        "c",
        "cdn_src",
        "cdn_src_active",
        "count",
        "during_time",
        "dynamic",
        "e_type",
        "graffiti_info",
        "height",
        "high_together",
        "imgtype",
        "is_long_pic",
        "is_native_app",
        "is_sub",
        "item",
        "item_forum_name",
        "item_id",
        "link",
        "media_subtitle",
        "meme_info",
        "native_app",
        "origin_size",
        "origin_src",
        "packet_name",
        "phonetype",
        "pic_id",
        "show_original_btn",
        "src",
        "text",
        "tiebaplus_info",
        "topic_special_icon",
        "type",
        "uid",
        "url_type",
        "voice_md5",
        "width",
    ]

    class GraffitiInfo(_message.Message):
        __slots__ = ["gid", "url"]
        GID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        gid: int
        url: str
        def __init__(
            self, url: _Optional[str] = ..., gid: _Optional[int] = ...
        ) -> None: ...

    class Item(_message.Message):
        __slots__ = [
            "apk_name",
            "button_link",
            "button_link_type",
            "button_name",
            "category_id",
            "forum_name",
            "icon_size",
            "icon_url",
            "item_appid",
            "item_id",
            "item_name",
            "score",
            "star",
            "tags",
        ]
        APK_NAME_FIELD_NUMBER: _ClassVar[int]
        BUTTON_LINK_FIELD_NUMBER: _ClassVar[int]
        BUTTON_LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
        BUTTON_NAME_FIELD_NUMBER: _ClassVar[int]
        CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
        FORUM_NAME_FIELD_NUMBER: _ClassVar[int]
        ICON_SIZE_FIELD_NUMBER: _ClassVar[int]
        ICON_URL_FIELD_NUMBER: _ClassVar[int]
        ITEM_APPID_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_NAME_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        STAR_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        apk_name: str
        button_link: str
        button_link_type: int
        button_name: str
        category_id: int
        forum_name: str
        icon_size: float
        icon_url: str
        item_appid: str
        item_id: int
        item_name: str
        score: float
        star: int
        tags: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            item_id: _Optional[int] = ...,
            item_name: _Optional[str] = ...,
            icon_size: _Optional[float] = ...,
            icon_url: _Optional[str] = ...,
            tags: _Optional[_Iterable[str]] = ...,
            score: _Optional[float] = ...,
            star: _Optional[int] = ...,
            button_name: _Optional[str] = ...,
            button_link: _Optional[str] = ...,
            item_appid: _Optional[str] = ...,
            category_id: _Optional[int] = ...,
            button_link_type: _Optional[int] = ...,
            apk_name: _Optional[str] = ...,
            forum_name: _Optional[str] = ...,
        ) -> None: ...

    class MemeInfo(_message.Message):
        __slots__ = [
            "detail_link",
            "height",
            "pck_id",
            "pic_id",
            "pic_url",
            "thumbnail",
            "width",
        ]
        DETAIL_LINK_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        PCK_ID_FIELD_NUMBER: _ClassVar[int]
        PIC_ID_FIELD_NUMBER: _ClassVar[int]
        PIC_URL_FIELD_NUMBER: _ClassVar[int]
        THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        detail_link: str
        height: int
        pck_id: int
        pic_id: int
        pic_url: str
        thumbnail: str
        width: int
        def __init__(
            self,
            pck_id: _Optional[int] = ...,
            pic_id: _Optional[int] = ...,
            pic_url: _Optional[str] = ...,
            thumbnail: _Optional[str] = ...,
            width: _Optional[int] = ...,
            height: _Optional[int] = ...,
            detail_link: _Optional[str] = ...,
        ) -> None: ...

    class NativeApp(_message.Message):
        __slots__ = ["download_and", "download_ios", "jump_and", "jump_ios"]
        DOWNLOAD_AND_FIELD_NUMBER: _ClassVar[int]
        DOWNLOAD_IOS_FIELD_NUMBER: _ClassVar[int]
        JUMP_AND_FIELD_NUMBER: _ClassVar[int]
        JUMP_IOS_FIELD_NUMBER: _ClassVar[int]
        download_and: str
        download_ios: str
        jump_and: str
        jump_ios: str
        def __init__(
            self,
            jump_and: _Optional[str] = ...,
            jump_ios: _Optional[str] = ...,
            download_and: _Optional[str] = ...,
            download_ios: _Optional[str] = ...,
        ) -> None: ...

    class TiebaPlusInfo(_message.Message):
        __slots__ = [
            "app_company",
            "app_icon",
            "app_id",
            "app_package",
            "app_power",
            "app_privacy",
            "app_version",
            "button_desc",
            "desc",
            "download_url",
            "forum_name",
            "h5_jump_number",
            "h5_jump_param",
            "h5_jump_type",
            "is_appoint",
            "item_id",
            "jump_setting",
            "jump_type",
            "jump_url",
            "plugin_user",
            "target_type",
            "title",
            "wx_thumbnail",
        ]

        class PluginUser(_message.Message):
            __slots__ = [
                "is_download_card_whiteuser",
                "user_id",
                "user_name_show",
                "user_photo",
                "user_type",
            ]
            IS_DOWNLOAD_CARD_WHITEUSER_FIELD_NUMBER: _ClassVar[int]
            USER_ID_FIELD_NUMBER: _ClassVar[int]
            USER_NAME_SHOW_FIELD_NUMBER: _ClassVar[int]
            USER_PHOTO_FIELD_NUMBER: _ClassVar[int]
            USER_TYPE_FIELD_NUMBER: _ClassVar[int]
            is_download_card_whiteuser: int
            user_id: int
            user_name_show: str
            user_photo: str
            user_type: int
            def __init__(
                self,
                user_id: _Optional[int] = ...,
                user_name_show: _Optional[str] = ...,
                user_type: _Optional[int] = ...,
                user_photo: _Optional[str] = ...,
                is_download_card_whiteuser: _Optional[int] = ...,
            ) -> None: ...
        APP_COMPANY_FIELD_NUMBER: _ClassVar[int]
        APP_ICON_FIELD_NUMBER: _ClassVar[int]
        APP_ID_FIELD_NUMBER: _ClassVar[int]
        APP_PACKAGE_FIELD_NUMBER: _ClassVar[int]
        APP_POWER_FIELD_NUMBER: _ClassVar[int]
        APP_PRIVACY_FIELD_NUMBER: _ClassVar[int]
        APP_VERSION_FIELD_NUMBER: _ClassVar[int]
        BUTTON_DESC_FIELD_NUMBER: _ClassVar[int]
        DESC_FIELD_NUMBER: _ClassVar[int]
        DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
        FORUM_NAME_FIELD_NUMBER: _ClassVar[int]
        H5_JUMP_NUMBER_FIELD_NUMBER: _ClassVar[int]
        H5_JUMP_PARAM_FIELD_NUMBER: _ClassVar[int]
        H5_JUMP_TYPE_FIELD_NUMBER: _ClassVar[int]
        IS_APPOINT_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        JUMP_SETTING_FIELD_NUMBER: _ClassVar[int]
        JUMP_TYPE_FIELD_NUMBER: _ClassVar[int]
        JUMP_URL_FIELD_NUMBER: _ClassVar[int]
        PLUGIN_USER_FIELD_NUMBER: _ClassVar[int]
        TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        WX_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
        app_company: str
        app_icon: str
        app_id: str
        app_package: str
        app_power: str
        app_privacy: str
        app_version: str
        button_desc: str
        desc: str
        download_url: str
        forum_name: str
        h5_jump_number: str
        h5_jump_param: str
        h5_jump_type: int
        is_appoint: int
        item_id: str
        jump_setting: int
        jump_type: int
        jump_url: str
        plugin_user: PbContent.TiebaPlusInfo.PluginUser
        target_type: int
        title: str
        wx_thumbnail: str
        def __init__(
            self,
            title: _Optional[str] = ...,
            desc: _Optional[str] = ...,
            jump_url: _Optional[str] = ...,
            download_url: _Optional[str] = ...,
            app_id: _Optional[str] = ...,
            app_icon: _Optional[str] = ...,
            app_package: _Optional[str] = ...,
            app_version: _Optional[str] = ...,
            app_privacy: _Optional[str] = ...,
            app_power: _Optional[str] = ...,
            app_company: _Optional[str] = ...,
            target_type: _Optional[int] = ...,
            h5_jump_type: _Optional[int] = ...,
            h5_jump_number: _Optional[str] = ...,
            h5_jump_param: _Optional[str] = ...,
            jump_type: _Optional[int] = ...,
            item_id: _Optional[str] = ...,
            is_appoint: _Optional[int] = ...,
            plugin_user: _Optional[
                _Union[PbContent.TiebaPlusInfo.PluginUser, _Mapping]
            ] = ...,
            forum_name: _Optional[str] = ...,
            jump_setting: _Optional[int] = ...,
            wx_thumbnail: _Optional[str] = ...,
            button_desc: _Optional[str] = ...,
        ) -> None: ...

    class TogetherHi(_message.Message):
        __slots__ = [
            "album_id",
            "album_name",
            "end_time",
            "location",
            "num_join",
            "num_signup",
            "pic_urls",
            "potraits",
            "start_time",
        ]
        ALBUM_ID_FIELD_NUMBER: _ClassVar[int]
        ALBUM_NAME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        NUM_JOIN_FIELD_NUMBER: _ClassVar[int]
        NUM_SIGNUP_FIELD_NUMBER: _ClassVar[int]
        PIC_URLS_FIELD_NUMBER: _ClassVar[int]
        POTRAITS_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        album_id: int
        album_name: str
        end_time: int
        location: str
        num_join: int
        num_signup: int
        pic_urls: _containers.RepeatedScalarFieldContainer[str]
        potraits: _containers.RepeatedScalarFieldContainer[str]
        start_time: int
        def __init__(
            self,
            album_name: _Optional[str] = ...,
            album_id: _Optional[int] = ...,
            start_time: _Optional[int] = ...,
            end_time: _Optional[int] = ...,
            location: _Optional[str] = ...,
            num_signup: _Optional[int] = ...,
            potraits: _Optional[_Iterable[str]] = ...,
            num_join: _Optional[int] = ...,
            pic_urls: _Optional[_Iterable[str]] = ...,
        ) -> None: ...
    BIG_CDN_SRC_FIELD_NUMBER: _ClassVar[int]
    BIG_SIZE_FIELD_NUMBER: _ClassVar[int]
    BIG_SRC_FIELD_NUMBER: _ClassVar[int]
    BSIZE_FIELD_NUMBER: _ClassVar[int]
    BTN_TYPE_FIELD_NUMBER: _ClassVar[int]
    CDN_SRC_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    CDN_SRC_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    C_FIELD_NUMBER: _ClassVar[int]
    DURING_TIME_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_FIELD_NUMBER: _ClassVar[int]
    E_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRAFFITI_INFO_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HIGH_TOGETHER_FIELD_NUMBER: _ClassVar[int]
    IMGTYPE_FIELD_NUMBER: _ClassVar[int]
    IS_LONG_PIC_FIELD_NUMBER: _ClassVar[int]
    IS_NATIVE_APP_FIELD_NUMBER: _ClassVar[int]
    IS_SUB_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    ITEM_FORUM_NAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    MEDIA_SUBTITLE_FIELD_NUMBER: _ClassVar[int]
    MEME_INFO_FIELD_NUMBER: _ClassVar[int]
    NATIVE_APP_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SIZE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_SRC_FIELD_NUMBER: _ClassVar[int]
    PACKET_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONETYPE_FIELD_NUMBER: _ClassVar[int]
    PIC_ID_FIELD_NUMBER: _ClassVar[int]
    SHOW_ORIGINAL_BTN_FIELD_NUMBER: _ClassVar[int]
    SRC_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TIEBAPLUS_INFO_FIELD_NUMBER: _ClassVar[int]
    TOPIC_SPECIAL_ICON_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    URL_TYPE_FIELD_NUMBER: _ClassVar[int]
    VOICE_MD5_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    _STATIC_FIELD_NUMBER: _ClassVar[int]
    _static: str
    big_cdn_src: str
    big_size: str
    big_src: str
    bsize: str
    btn_type: int
    c: str
    cdn_src: str
    cdn_src_active: str
    count: int
    during_time: int
    dynamic: str
    e_type: int
    graffiti_info: PbContent.GraffitiInfo
    height: int
    high_together: PbContent.TogetherHi
    imgtype: str
    is_long_pic: int
    is_native_app: int
    is_sub: int
    item: PbContent.Item
    item_forum_name: str
    item_id: int
    link: str
    media_subtitle: str
    meme_info: PbContent.MemeInfo
    native_app: PbContent.NativeApp
    origin_size: int
    origin_src: str
    packet_name: str
    phonetype: str
    pic_id: int
    show_original_btn: int
    src: str
    text: str
    tiebaplus_info: PbContent.TiebaPlusInfo
    topic_special_icon: str
    type: int
    uid: int
    url_type: int
    voice_md5: str
    width: int
    def __init__(
        self,
        type: _Optional[int] = ...,
        text: _Optional[str] = ...,
        link: _Optional[str] = ...,
        src: _Optional[str] = ...,
        bsize: _Optional[str] = ...,
        big_src: _Optional[str] = ...,
        big_size: _Optional[str] = ...,
        cdn_src: _Optional[str] = ...,
        big_cdn_src: _Optional[str] = ...,
        imgtype: _Optional[str] = ...,
        c: _Optional[str] = ...,
        voice_md5: _Optional[str] = ...,
        during_time: _Optional[int] = ...,
        is_sub: _Optional[int] = ...,
        uid: _Optional[int] = ...,
        dynamic: _Optional[str] = ...,
        _static: _Optional[str] = ...,
        width: _Optional[int] = ...,
        height: _Optional[int] = ...,
        packet_name: _Optional[str] = ...,
        phonetype: _Optional[str] = ...,
        is_native_app: _Optional[int] = ...,
        native_app: _Optional[_Union[PbContent.NativeApp, _Mapping]] = ...,
        e_type: _Optional[int] = ...,
        origin_src: _Optional[str] = ...,
        btn_type: _Optional[int] = ...,
        origin_size: _Optional[int] = ...,
        count: _Optional[int] = ...,
        graffiti_info: _Optional[_Union[PbContent.GraffitiInfo, _Mapping]] = ...,
        high_together: _Optional[_Union[PbContent.TogetherHi, _Mapping]] = ...,
        media_subtitle: _Optional[str] = ...,
        url_type: _Optional[int] = ...,
        meme_info: _Optional[_Union[PbContent.MemeInfo, _Mapping]] = ...,
        is_long_pic: _Optional[int] = ...,
        show_original_btn: _Optional[int] = ...,
        cdn_src_active: _Optional[str] = ...,
        topic_special_icon: _Optional[str] = ...,
        item_id: _Optional[int] = ...,
        item_forum_name: _Optional[str] = ...,
        tiebaplus_info: _Optional[_Union[PbContent.TiebaPlusInfo, _Mapping]] = ...,
        item: _Optional[_Union[PbContent.Item, _Mapping]] = ...,
        pic_id: _Optional[int] = ...,
    ) -> None: ...
