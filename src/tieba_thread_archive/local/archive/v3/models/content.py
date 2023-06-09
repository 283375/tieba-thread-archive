from typing import Any, Dict, List, Optional, Tuple, TypedDict

from .....models.content import *

__all__ = (
    "AV3ContentBase",
    "AV3ContentText",
    "AV3ContentLink",
    "AV3ContentEmoticon",
    "AV3ContentImage",
    "AV3ContentAt",
    "AV3ContentVideo",
    "AV3ContentPhoneNumber",
    "AV3ContentAudio",
    "AV3ContentTopic",
    "AV3ContentUnknown",
    "AV3ContentTypeMapping",
    "AV3ContentSegment",
    "AV3Contents",
)


class AV3ContentBase:
    class ArchivePart(TypedDict):
        type: int

    @staticmethod
    def archive_dump(dump_cls: ContentBase) -> ArchivePart:
        raise NotImplementedError()

    @staticmethod
    def archive_load(archive: ArchivePart) -> ContentBase:
        raise NotImplementedError()


class AV3ContentText(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str

    @staticmethod
    def archive_dump(content: ContentText) -> ArchivePart:
        return {"type": content.type, "text": content.text}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentText(text=archive["text"])


class AV3ContentLink(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str
        link: str

    @staticmethod
    def archive_dump(content: ContentLink) -> ArchivePart:
        return {"type": content.type, "text": content.text, "link": content.link}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentLink(text=archive["text"], link=archive["link"])


class AV3ContentEmoticon(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str
        c: str

    @staticmethod
    def archive_dump(content: ContentEmoticon) -> ArchivePart:
        return {"type": content.type, "text": content.text, "c": content.c}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentEmoticon(text=archive["text"], c=archive["c"])


class AV3ContentImage(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        origin_src: str
        origin_size: int
        filename: str

    @staticmethod
    def archive_dump(content: ContentImage) -> ArchivePart:
        return {
            "type": content.type,
            "origin_src": content.origin_src,
            "origin_size": content.origin_size,
            "filename": content.filename,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentImage(
            origin_src=archive["origin_src"],
            origin_size=archive["origin_size"],
            filename=archive["filename"],
        )


class AV3ContentAt(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str
        uid: int

    @staticmethod
    def archive_dump(content: ContentAt) -> ArchivePart:
        return {"type": content.type, "text": content.text, "uid": content.uid}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentAt(text=archive["text"], uid=archive["uid"])


class AV3ContentVideo(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str
        filename: Optional[str]
        link: Optional[str]
        src: Optional[str]
        bsize: Optional[Tuple[int, int]]
        origin_size: Optional[int]

    @staticmethod
    def archive_dump(content: ContentVideo) -> ArchivePart:
        return {
            "type": content.type,
            "text": content.text,
            "filename": content.filename,
            "link": content.link,
            "src": content.src,
            "bsize": content.bsize,
            "origin_size": content.origin_size,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentVideo(
            text=archive["text"],
            filename=archive["filename"],
            link=archive["link"],
            src=archive["src"],
            bsize=archive["bsize"],
            origin_size=archive["origin_size"],
        )


class AV3ContentPhoneNumber(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str

    @staticmethod
    def archive_dump(content: ContentText) -> ArchivePart:
        return {"type": content.type, "text": content.text}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentText(text=archive["text"])


class AV3ContentAudio(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        voice_md5: str

    @staticmethod
    def archive_dump(content: ContentAudio) -> ArchivePart:
        return {"type": content.type, "voice_md5": content.voice_md5}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentAudio(voice_md5=archive["voice_md5"])


class AV3ContentTopic(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str
        link: str

    @staticmethod
    def archive_dump(content: ContentTopic) -> ArchivePart:
        return {"type": content.type, "text": content.text, "link": content.link}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentTopic(text=archive["text"], link=archive["link"])


class AV3ContentItem(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        text: str
        item_id: int

    @staticmethod
    def archive_dump(content: ContentItem) -> ArchivePart:
        return {"type": content.type, "text": content.text, "item_id": content.item_id}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentItem(text=archive["text"], item_id=archive["item_id"])


class AV3ContentUnknown(AV3ContentBase):
    @staticmethod
    def archive_dump(content: ContentUnknown) -> Dict[str, Any]:
        return content.dict

    @staticmethod
    def archive_load(archive: Dict[str, Any]):
        return ContentUnknown(archive)


class AV3ContentTypeMapping(dict):
    def __init__(self):
        self.update(
            {
                0: AV3ContentText,
                1: AV3ContentLink,
                2: AV3ContentEmoticon,
                3: AV3ContentImage,
                4: AV3ContentAt,
                5: AV3ContentVideo,
                9: AV3ContentPhoneNumber,
                10: AV3ContentAudio,
                18: AV3ContentTopic,
                27: AV3ContentItem,
            }
        )

    def get(self, __key: Any) -> AV3ContentBase:
        return super().get(__key, AV3ContentUnknown)

    def __getitem__(self, __key: int):
        return self.get(__key)


class AV3ContentSegment:
    TYPE_MAPPING = AV3ContentTypeMapping()

    @classmethod
    def archive_dump(cls, content: ContentBase):
        constructor = cls.TYPE_MAPPING[content.type]
        return constructor.archive_dump(content)

    @classmethod
    def archive_load(cls, archive: AV3ContentBase.ArchivePart):
        content_type = archive["type"]
        constructor = cls.TYPE_MAPPING[content_type]
        return constructor.archive_load(archive)


class AV3Contents(List[AV3ContentBase]):
    ArchivePart = List[AV3ContentBase.ArchivePart]

    @staticmethod
    def archive_dump(contents: Contents):
        return [AV3ContentSegment.archive_dump(content) for content in contents]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Contents(AV3ContentSegment.archive_load(content) for content in archive)
