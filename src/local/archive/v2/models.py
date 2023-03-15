from typing import Iterable, List, Optional, TypedDict

from ....models import *

__all__ = ("AV2User", "AV2Asset", "AV2Content", "AV2Agree", "AV2SubPost", "AV2Post")


class AV2User:
    __slots__ = ("id", "name", "name_show", "portrait", "level_id")

    class ArchivePart(TypedDict, total=False):
        id: str
        name: Optional[str]
        name_show: Optional[str]
        portrait: Optional[str]
        level_id: Optional[str]

    def __init__(
        self,
        *,
        id: int,
        name: str,
        name_show: str,
        portrait: str,
        level_id: int,
    ):
        self.id = id
        self.name = name or ""
        self.name_show = name_show or ""
        self.portrait = portrait or ""
        self.level_id = level_id or -1

    @staticmethod
    def archive_load(archive: ArchivePart):
        return User(
            id=int(archive.get("id", 0) or 0),
            name=archive.get("name") or "",
            name_show=archive.get("name_show") or "",
            portrait=archive.get("portrait") or "",
            level_id=int(archive.get("level_id", -1) or -1),
        )


class AV2Asset:
    __slots__ = ("type", "src", "filename", "id", "size", "md5", "portrait")

    class ArchivePart(TypedDict):
        type: str
        src: str
        filename: str
        id: Optional[str]
        size: Optional[str]
        md5: Optional[str]
        portrait: Optional[str]

    @staticmethod
    def archive_load(archive: ArchivePart):
        if archive["type"] == "image":
            origin_src = archive.get("src")
            origin_size = archive.get("size")
            filename = archive.get("filename")
            assert origin_src and origin_size and filename is not None
            assert origin_src != "" and origin_size != "" and filename != ""
            return ContentImage(
                origin_src=origin_src,
                origin_size=int(origin_size),
                filename=filename,
            )
        elif archive["type"] == "audio":
            voice_md5 = archive.get("md5")
            assert voice_md5 is not None and voice_md5 != ""
            return ContentAudio(voice_md5=voice_md5)


class AV2Content:
    class ArchivePart(TypedDict, total=False):
        type: str

        text: Optional[str]
        link: Optional[str]
        c: Optional[str]
        uid: Optional[str]

        origin_src: Optional[str]
        origin_size: Optional[str]
        pic_id: Optional[str]

        voice_md5: Optional[str]

    @staticmethod
    def archive_load(archive: ArchivePart) -> ContentBase:
        content_type = int(archive.get("type", "-1"))

        if content_type == 0:
            return ContentText(text=archive.get("text", "") or "")
        elif content_type == 1:
            return ContentLink(
                text=archive.get("text", "") or "",
                link=archive.get("link", "") or "",
            )
        elif content_type == 2:
            return ContentEmoticon(
                text=archive.get("text", "") or "",
                c=archive.get("c", "") or "",
            )
        elif content_type == 3:
            return ContentImage(
                origin_src=archive.get("origin_src", "") or "",
                origin_size=int(archive.get("origin_size", 0) or 0),
                filename=f"{archive.get('pic_id')}.jpg",
            )
        elif content_type == 4:
            return ContentAt(
                text=archive.get("text", "") or "",
                uid=int(archive.get("uid", 0) or 0),
            )
        elif content_type == 10:
            return ContentAudio(
                voice_md5=archive.get("voice_md5", "") or "",
            )
        else:
            return ContentBase()


class AV2Agree:
    class ArchivePart(TypedDict):
        agree_num: str
        disagree_num: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Agree(
            agree_num=int(archive["agree_num"]),
            disagree_num=int(archive["disagree_num"]),
        )


class AV2SubPost:
    class ArchivePart(TypedDict):
        id: str
        content: List[AV2Content.ArchivePart]
        time: str
        agree: AV2Agree.ArchivePart
        author: AV2User.ArchivePart

    @staticmethod
    def archive_load(archive: ArchivePart):
        return SubPost(
            id=int(archive["id"]),
            agree=AV2Agree.archive_load(archive["agree"]),
            author=AV2User.archive_load(archive["author"]),
            time=int(archive["time"]),
            contents=Contents(
                AV2Content.archive_load(content) for content in archive["content"]
            ),
        )


class AV2Post:
    class ArchivePart(TypedDict):
        id: str
        title: str
        floor: str
        time: str
        author_id: str
        agree: AV2Agree.ArchivePart
        content: List[AV2Content.ArchivePart]
        sub_post_number: str
        sub_post_list: List[AV2SubPost.ArchivePart]

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        author = User(id=0, name="", name_show="", portrait="", level_id=-1)
        for user in user_list:
            if user.id == int(archive["author_id"]):
                author = user

        return Post(
            floor=int(archive["floor"]),
            id=int(archive["id"]),
            title=archive["title"],
            agree=AV2Agree.archive_load(archive["agree"]),
            author=author,
            time=int(archive["time"]),
            subpost_num=int(archive["sub_post_number"]),
            contents=Contents(
                AV2Content.archive_load(content) for content in archive["content"]
            ),
        )
