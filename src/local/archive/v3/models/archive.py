from typing import Dict, List, TypedDict, Union

from .....models import *
from .content import AV3ContentAudio, AV3ContentImage
from .post import AV3Posts, AV3SubPosts
from .user import AV3User


class AV3ThreadInfo:
    class ArchivePart(TypedDict):
        id: int
        title: str
        author: AV3User.ArchivePart
        create_time: int

    @staticmethod
    def archive_title():
        return "thread_info"

    @staticmethod
    def archive_dump(thread_info: ThreadInfo) -> ArchivePart:
        return {
            "id": thread_info.id,
            "title": thread_info.title,
            "author": AV3User.archive_dump(thread_info.author),
            "create_time": thread_info.create_time,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ThreadInfo(
            id=archive["id"],
            title=archive["title"],
            author=AV3User.archive_load(archive["author"]),
            create_time=archive["create_time"],
        )


class AV3ArchiveInfo:
    class ArchivePart(TypedDict):
        lz_only: bool
        images: bool
        audios: bool
        videos: bool
        portraits: bool

    @staticmethod
    def archive_title():
        return "archive_info"

    @staticmethod
    def archive_dump(archive_info: ArchiveInfo) -> ArchivePart:
        return {
            "lz_only": archive_info.lz_only,
            "images": archive_info.images,
            "audios": archive_info.audios,
            "videos": archive_info.videos,
            "portraits": archive_info.portraits,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveInfo(
            lz_only=archive["lz_only"],
            images=archive["images"],
            audios=archive["audios"],
            videos=archive["videos"],
            portraits=archive["portraits"],
        )


class AV3ArchiveUpdateInfo:
    class ArchivePart(TypedDict):
        store_time: int
        last_update_time: Union[int, None]

    @staticmethod
    def archive_title():
        return "archive_update_info"

    @staticmethod
    def archive_dump(archive_update_info: ArchiveUpdateInfo) -> ArchivePart:
        return {
            "store_time": archive_update_info.store_time,
            "last_update_time": archive_update_info.last_update_time,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveUpdateInfo(
            store_time=archive["store_time"],
            last_update_time=archive["last_update_time"],
        )


class AV3ArchiveThread:
    class ArchivePart(TypedDict):
        thread_info: AV3ThreadInfo.ArchivePart
        archive_info: AV3ArchiveInfo.ArchivePart
        posts: AV3Posts.ArchivePart
        subposts: Dict[int, AV3SubPosts.ArchivePart]
        users: List[AV3User.ArchivePart]
        images: List[AV3ContentImage.ArchivePart]
        audios: List[AV3ContentAudio.ArchivePart]

    @staticmethod
    def archive_dump(archive_thread: ArchiveThread) -> ArchivePart:
        return {
            "thread_info": AV3ThreadInfo.archive_dump(archive_thread.thread_info),
            "archive_info": AV3ArchiveInfo.archive_dump(archive_thread.archive_info),
            "posts": AV3Posts.archive_dump(archive_thread.posts),
            "subposts": {
                id: AV3SubPosts.archive_dump(subpost)
                for id, subpost in archive_thread.subposts.items()
            },
            "users": [AV3User.archive_dump(user) for user in archive_thread.users],
            "images": [
                AV3ContentImage.archive_dump(image) for image in archive_thread.images
            ],
            "audios": [
                AV3ContentAudio.archive_dump(audio) for audio in archive_thread.audios
            ],
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveThread(
            thread_info=AV3ThreadInfo.archive_load(archive["thread_info"]),
            archive_info=AV3ArchiveInfo.archive_load(archive["archive_info"]),
            posts=AV3Posts.archive_load(archive["posts"]),
            subposts={
                id: AV3SubPosts.archive_load(subpost)
                for id, subpost in archive["subposts"].items()
            },
            users=[AV3User.archive_load(user) for user in archive["users"]],
            images=[AV3ContentImage.archive_load(image) for image in archive["images"]],
            audios=[AV3ContentAudio.archive_load(audio) for audio in archive["audios"]],
        )
