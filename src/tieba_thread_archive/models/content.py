from typing import Any, Dict, Iterable, List, Optional, Tuple, Type

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from yarl import URL

from ..remote.protobuf.common import PbContent_pb2
from ..utils import truncate_text

__all__ = (
    "ContentBase",
    "ContentText",
    "ContentLink",
    "ContentEmoticon",
    "ContentImage",
    "ContentAt",
    "ContentVideo",
    "ContentPhoneNumber",
    "ContentAudio",
    "ContentTopic",
    "ContentItem",
    "ContentUnknown",
    "ContentSegment",
    "Contents",
)


class ContentBase:
    __slots__ = ()
    type: int

    def __init__(self):
        if self.__class__ == ContentBase:
            raise NotImplementedError("ContentBase is not meant to be used directly.")

    @classmethod
    def from_protobuf(cls, pb: PbContent_pb2.PbContent):
        raise NotImplementedError("ContentBase is not meant to be used directly.")

    def __hash__(self):
        raise NotImplementedError("ContentBase is not meant to be used directly.")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__hash__() == other.__hash__()


class ContentText(ContentBase):
    __slots__ = ("text",)
    type = 0

    def __init__(self, *, text: str):
        self.text = text

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text)

    def __repr__(self):
        return f"ContentText({truncate_text(self.text, 5)})"

    def __hash__(self):
        return hash(self.text)


class ContentLink(ContentBase):
    __slots__ = ("text", "link")
    type = 1

    def __init__(self, *, text: str, link: str):
        self.text = text
        self.link = link

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text, link=pb.link)

    def __repr__(self):
        return f"ContentLink({truncate_text(self.link, 50)})"

    def __hash__(self):
        return hash(f"{hash(self.text)}{self.text}{hash(self.link)}{self.link}")


class ContentEmoticon(ContentBase):
    __slots__ = ("text", "c")
    type = 2

    def __init__(self, *, text: str, c: str):
        self.text = text
        self.c = c

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text, c=pb.c)

    def __repr__(self):
        return f"ContentEmoticon({self.c}:{self.text})"

    def __hash__(self):
        return hash(f"{self.text}{self.c}")


class ContentImage(ContentBase):
    __slots__ = ("origin_src", "origin_size", "filename")
    type = 3

    def __init__(self, *, origin_src: str, origin_size: int, filename: str):
        self.origin_src = origin_src
        self.origin_size = origin_size
        self.filename = filename

    @classmethod
    def from_protobuf(cls, pb):
        return cls(
            origin_src=pb.origin_src,
            origin_size=pb.origin_size,
            filename=URL(pb.origin_src).name,
        )

    def __hash__(self):
        return hash(f"{self.origin_src}{self.filename}")

    def __repr__(self):
        return f"ContentImage({self.filename})"


class ContentAt(ContentBase):
    __slots__ = ("text", "uid")
    type = 4

    def __init__(self, *, text: str, uid: int):
        self.text = text
        self.uid = uid

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text, uid=pb.uid)

    def __hash__(self):
        return hash(f"{self.text}{self.uid}")

    def __repr__(self):
        return f"ContentAt(@{self.text}:{self.uid})"


class ContentVideo(ContentBase):
    __slots__ = ("text", "link", "src", "bsize", "origin_size", "filename")
    type = 5

    def __init__(
        self,
        *,
        text: str,
        filename: Optional[str] = None,
        link: Optional[str] = None,
        src: Optional[str] = None,
        bsize: Optional[Tuple[int, int]] = None,
        origin_size: Optional[int] = None,
    ):
        self.text = text
        self.filename = filename
        self.link = link
        self.src = src
        self.bsize = bsize
        self.origin_size = origin_size

    @classmethod
    def from_protobuf(cls, pb):
        return cls(
            text=pb.text,
            filename=URL(pb.link).name if pb.link else None,
            link=pb.link or None,
            src=pb.src or None,
            bsize=tuple(int(v) for v in pb.bsize.split(",")) if pb.bsize else None,
            origin_size=pb.origin_size or None,
        )

    def __hash__(self):
        return hash(f"{self.text}{self.link}")

    def __repr__(self):
        return f"ContentVideo({self.filename or self.text})"


class ContentPhoneNumber(ContentBase):
    __slots__ = ("text",)
    type = 9

    def __init__(self, *, text: str):
        self.text = text

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text)

    def __hash__(self):
        return hash(self.text)

    def __repr__(self):
        return f"ContentPhoneNumber({self.text})"


class ContentAudio(ContentBase):
    __slots__ = ("voice_md5", "filename")
    type = 10

    def __init__(self, *, voice_md5: str):
        self.voice_md5 = voice_md5
        self.filename = f"{voice_md5}.amr"

    @property
    def src(self):
        return f"https://tiebac.baidu.com/c/p/voice?voice_md5={self.voice_md5}&play_from=pb_voice_play"

    @classmethod
    def from_protobuf(cls, pb):
        return cls(voice_md5=pb.voice_md5)

    def __hash__(self):
        return hash(self.voice_md5)

    def __repr__(self):
        return f"ContentAudio({self.voice_md5})"


class ContentTopic(ContentBase):
    __slots__ = ("text", "link")
    type = 18

    def __init__(self, *, text: str, link: str):
        self.text = text
        self.link = link

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text, link=pb.link)

    def __hash__(self):
        return hash(self.text)

    def __repr__(self):
        return f"ContentTopic({self.text})"


class ContentItem(ContentBase):
    __slots__ = ("text", "item_id")
    type = 27

    def __init__(self, *, text: str, item_id: int):
        self.text = text
        self.item_id = item_id

    @classmethod
    def from_protobuf(cls, pb):
        return cls(text=pb.text, item_id=pb.item_id)

    def __hash__(self):
        return hash(f"__TIEBA_ITEM_{self.item_id}")

    def __repr__(self):
        return f"ContentItem({self.text}, {self.item_id})"


class ContentUnknown(ContentBase):
    __slots__ = ("type", "dict")

    def __init__(self, dict: Dict[str, Any], /):
        self.type = dict["type"]
        self.dict = dict

    @classmethod
    def from_protobuf(cls, pb):
        return cls({k.name: v for k, v in pb.ListFields()})


class ContentTypeMapping(dict):
    def __init__(self):
        self.update(
            {
                0: ContentText,
                1: ContentLink,
                2: ContentEmoticon,
                3: ContentImage,
                4: ContentAt,
                5: ContentVideo,
                9: ContentPhoneNumber,
                10: ContentAudio,
                18: ContentTopic,
                27: ContentItem,
            }
        )

    def get(self, __key: int) -> Type[ContentBase]:
        # raise KeyError(f"Unknown content type {__key}")
        return super().get(__key, ContentUnknown)

    def __getitem__(self, __key: int):
        return self.get(__key)


CONTENT_TYPE_TABLE = ContentTypeMapping()


class ContentSegment:
    @staticmethod
    def from_protobuf(pb: PbContent_pb2.PbContent):
        content = CONTENT_TYPE_TABLE[pb.type]
        content_class = content.from_protobuf(pb)
        if isinstance(content_class, ContentUnknown):
            print(f"Unknown content type {content_class.type}")
            print(content_class.dict)
        return content_class


class Contents(List[ContentBase]):
    def __init__(self, __iterable: Optional[Iterable[ContentBase]] = None, /):
        if __iterable is not None:
            self.clear()
            self.extend(__iterable)

    @classmethod
    def from_protobuf(
        cls, pb: RepeatedCompositeFieldContainer[PbContent_pb2.PbContent]
    ):
        return cls(ContentSegment.from_protobuf(content) for content in pb)

    def __repr__(self):
        return f"Contents(...{len(self)})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return (
            all(self[i] == other[i] for i in range(len(self)))
            if len(self) == len(other)
            else False
        )
