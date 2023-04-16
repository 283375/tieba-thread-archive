import os
from typing import Any, List, TypedDict, Union
from urllib.parse import urlparse

from .....models.content import *
from ._base import AV2Model, AV2TiebaAsset


class AV2ContentBase(AV2Model):
    class ArchivePart(TypedDict):
        type: Union[int, str]

    @staticmethod
    def archive_load(archive: ArchivePart) -> ContentBase:
        raise NotImplementedError()


class AV2ContentText(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentText(text=archive["text"])


class AV2ContentLink(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str
        link: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentLink(text=archive["text"], link=archive["link"])


class AV2ContentEmoticon(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str
        c: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentEmoticon(text=archive["text"], c=archive["c"])


class AV2ContentImage(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        size: Union[int, str]
        origin_src: str
        origin_size: Union[int, str]
        is_long_pic: Union[int, str]
        show_original_btn: Union[int, str]
        cdn_src: str
        cdn_src_active: str
        big_cdn_src: str
        pic_id: Union[int, str]
        is_native_app: Union[int, str]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentImage(
            origin_src=archive["origin_src"],
            origin_size=int(archive["origin_size"]),
            filename=f'{archive["pic_id"]}{os.path.splitext(os.path.basename(urlparse(archive["origin_src"]).path))[1]}',
        )

    @staticmethod
    def archive_load_from_av2_tieba_asset(archive: AV2TiebaAsset):
        return ContentImage(
            origin_src=archive["src"],
            origin_size=archive.get("size", 0),
            filename=archive["filename"],
        )


class AV2ContentAt(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str
        uid: int

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentAt(text=archive["text"], uid=archive["uid"])


class AV2ContentVideo(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str
        src: str
        bsize: str
        origin_size: Union[int, str]
        count: Union[int, str]
        link: str
        during_time: Union[int, str]
        width: Union[int, str]
        height: Union[int, str]
        is_native_app: Union[int, str]
        e_type: Union[int, str]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentVideo(
            text=archive["text"],
            filename=os.path.basename(urlparse(archive["link"]).path),
            link=archive["link"],
            src=archive["src"],
            bsize=tuple(int(v) for v in ",".split(archive["bsize"])),
            origin_size=int(archive["origin_size"]),
        )

    @staticmethod
    def archive_load_from_av2_tieba_asset(archive: AV2TiebaAsset):
        return ContentVideo(
            text="__V2_ABSENCE__",
            filename=archive["filename"],
            link="__V2_ABSENCE__",
            src=archive["src"],
            bsize=None,
            origin_size=archive.get("size"),
        )


class AV2ContentPhoneNumber(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentText(text=archive["text"])


class AV2ContentAudio(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        voice_md5: str
        during_time: Union[int, str]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentAudio(voice_md5=archive["voice_md5"])

    @staticmethod
    def archive_load_from_av2_tieba_asset(archive: AV2TiebaAsset):
        return ContentAudio(voice_md5=archive.get("md5", "__V2_ABSENCE__"))


class AV2ContentTopic(AV2ContentBase):
    class ArchivePart(AV2ContentBase.ArchivePart):
        text: str
        link: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentTopic(text=archive["text"], link=archive["link"])


class AV2ContentTypeMapping(dict):
    def __init__(self):
        self.update(
            {
                "0": AV2ContentText,
                "1": AV2ContentLink,
                "2": AV2ContentEmoticon,
                "3": AV2ContentImage,
                "4": AV2ContentAt,
                "5": AV2ContentVideo,
                "9": AV2ContentPhoneNumber,
                "10": AV2ContentAudio,
                "18": AV2ContentTopic,
            }
        )

    def get(self, __key: Any) -> AV2ContentBase:
        item = super().get(str(__key), None)
        if item is None:
            raise KeyError(f"Unknown content type {__key}.")
        return item

    def __getitem__(self, __key: Any):
        return self.get(__key)


class AV2ContentSegment:
    TYPE_MAPPING = AV2ContentTypeMapping()

    @classmethod
    def archive_load(cls, archive: AV2ContentBase.ArchivePart):
        content_type = archive["type"]
        constructor = cls.TYPE_MAPPING[content_type]
        return constructor.archive_load(archive)


class AV2Contents(List[AV2ContentBase]):
    ArchivePart = List[AV2ContentBase.ArchivePart]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Contents(AV2ContentSegment.archive_load(content) for content in archive)
