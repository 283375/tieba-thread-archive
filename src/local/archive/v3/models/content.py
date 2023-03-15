from typing import Any, List, TypedDict, Union

from .....models.content import *
from .....models.content import CONTENT_TYPE_TABLE


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


class AV3ContentAudio(AV3ContentBase):
    class ArchivePart(AV3ContentBase.ArchivePart):
        voice_md5: str

    @staticmethod
    def archive_dump(content: ContentAudio) -> ArchivePart:
        return {"type": content.type, "voice_md5": content.voice_md5}

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ContentAudio(voice_md5=archive["voice_md5"])


class AV3ContentTypeMapping(dict):
    def __init__(self):
        self |= {
            0: AV3ContentText,
            1: AV3ContentLink,
            2: AV3ContentEmoticon,
            3: AV3ContentImage,
            4: AV3ContentAt,
            10: AV3ContentAudio,
        }

    def get(self, __key: Any) -> AV3ContentBase:
        item = super().get(__key, None)
        if item is None:
            raise KeyError(f"Unknown content type {__key}.")
        return item

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
