from typing import Iterable, Literal, TypedDict, Union

from .....models import *
from ._base import AV2Model, av2_absence_user
from .forum import AV2Forum

__all__ = (
    "AV2ThreadInfo",
    "AV2ArchiveOptions",
    "AV2ArchiveUpdateInfo",
)


class AV2ArchiveOptions(AV2Model):
    class ArchivePart(TypedDict):
        __VERSION__: Literal[2]
        lzOnly: bool
        assets: bool
        portraits: bool

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveOptions(
            images=archive["assets"],
            audios=archive["assets"],
            videos=archive["assets"],
            portraits=archive["portraits"],
        )


class AV2ArchiveUpdateInfo(AV2Model):
    class ArchivePart(TypedDict):
        storeTime: int
        updateTime: Union[int, None]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveUpdateInfo(
            archive_time=archive["storeTime"],
            last_update_time=archive["updateTime"],
        )


class AV2ThreadInfoAuthor:
    class ArchivePart(TypedDict):
        id: Union[int, str]
        origName: str
        displayName: str

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        author_id = int(archive["id"])
        return next(
            (user for user in user_list if user.id == author_id),
            av2_absence_user(author_id),
        )


class AV2ThreadInfo(AV2Model):
    class ArchivePart(TypedDict):
        id: Union[int, str]
        title: str
        createTime: Union[int, str]
        author: AV2ThreadInfoAuthor.ArchivePart
        forum: AV2Forum.ArchivePart
        storeOptions: AV2ArchiveOptions.ArchivePart
        updateInfo: AV2ArchiveUpdateInfo.ArchivePart

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        return ThreadInfo(
            id=int(archive["id"]),
            title=archive["title"],
            author=AV2ThreadInfoAuthor.archive_load(archive["author"], user_list),
            forum=AV2Forum.archive_load(archive["forum"]),
            create_time=int(archive["createTime"]),
        )
