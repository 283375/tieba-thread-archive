from typing import Iterable, List, Optional, TypedDict, TypeVar, Union

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
    "ContentAudio",
    "ContentSegment",
    "Contents",
)


class ContentBase:
    __slots__ = tuple()
    type: int

    def __init__(self):
        if self.__class__ == ContentBase:
            raise NotImplementedError("ContentBase is not meant to be used directly.")

    @classmethod
    def from_protobuf(cls, pb: PbContent_pb2.PbContent):
        raise NotImplementedError("ContentBase is not meant to be used directly.")


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
        return hash(self.origin_src)

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

    def __repr__(self):
        return f"ContentAt(@{self.text}:{self.uid})"


class ContentAudio(ContentBase):
    __slots__ = ("voice_md5",)
    type = 10

    def __init__(self, *, voice_md5: str):
        self.voice_md5 = voice_md5

    @classmethod
    def from_protobuf(cls, pb):
        return cls(voice_md5=pb.voice_md5)

    def __hash__(self):
        return hash(self.voice_md5)

    def __repr__(self):
        return f"ContentAudio({self.voice_md5}.mp3)"


K = TypeVar("K", bound=int)
CB = TypeVar("CB", bound=ContentBase, covariant=True)


class ContentTypeMapping(dict):
    def __init__(self):
        self |= {
            0: ContentText,
            1: ContentLink,
            2: ContentEmoticon,
            3: ContentImage,
            4: ContentAt,
            10: ContentAudio,
        }

    def get(self, __key: int) -> ContentBase:
        item = super().get(__key, None)
        if item is None:
            raise KeyError(f"Unknown content type {item}")
        return item

    def __getitem__(self, __key: int):
        return self.get(__key)


CONTENT_TYPE_TABLE = ContentTypeMapping()


class ContentSegment:
    @staticmethod
    def from_protobuf(pb: PbContent_pb2.PbContent):
        content = CONTENT_TYPE_TABLE[pb.type]
        return content.from_protobuf(pb)


class Contents(List[ContentBase]):
    def __init__(self, /, __iterable: Optional[Iterable[ContentBase]] = None):
        if __iterable is not None:
            self.clear()
            self.extend(__iterable)

    @classmethod
    def from_protobuf(
        cls, pb: RepeatedCompositeFieldContainer[PbContent_pb2.PbContent]
    ):
        self = cls()
        for content in pb:
            try:
                self.append(ContentSegment.from_protobuf(content))
            except KeyError as e:
                print(content)
                print(e)
        return self

    def __repr__(self):
        return f"Contents(...{len(self)})"
