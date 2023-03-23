from typing import Dict, List, TypedDict, Union

from .....models import *
from .content import AV3ContentAudio, AV3ContentImage, AV3ContentVideo
from .post import AV3Posts, AV3SubPosts
from .user import AV3User

__all__ = (
    "AV3ThreadInfo",
    "AV3ArchiveOptions",
    "AV3ArchiveUpdateInfo",
    "AV3ArchiveThread",
)


class AV3ThreadInfo:
    class ArchivePart(TypedDict):
        id: int
        title: str
        author: AV3User.ArchivePart
        create_time: int

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


class AV3ArchiveOptions:
    class ArchivePart(TypedDict):
        images: bool
        audios: bool
        videos: bool
        portraits: bool

    @staticmethod
    def archive_dump(archive_info: ArchiveOptions) -> ArchivePart:
        return {
            "images": archive_info.images,
            "audios": archive_info.audios,
            "videos": archive_info.videos,
            "portraits": archive_info.portraits,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveOptions(
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
    def archive_dump(archive_update_info: ArchiveUpdateInfo) -> ArchivePart:
        return {
            "store_time": archive_update_info.archive_time,
            "last_update_time": archive_update_info.last_update_time,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return ArchiveUpdateInfo(
            archive_time=archive["store_time"],
            last_update_time=archive["last_update_time"],
        )


class AV3ArchiveThread:
    class ArchivePart(TypedDict):
        archive_time: int
        thread_info: AV3ThreadInfo.ArchivePart
        posts: AV3Posts.ArchivePart
        subposts: Dict[int, AV3SubPosts.ArchivePart]
        users: List[AV3User.ArchivePart]
        images: List[AV3ContentImage.ArchivePart]
        audios: List[AV3ContentAudio.ArchivePart]
        videos: List[AV3ContentVideo.ArchivePart]

    @staticmethod
    def archive_dump(archive_thread: ArchiveThread) -> ArchivePart:
        return {
            "archive_time": archive_thread.archive_time,
            "thread_info": AV3ThreadInfo.archive_dump(archive_thread.thread_info),
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
            "videos": [
                AV3ContentVideo.archive_dump(video) for video in archive_thread.videos
            ],
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        users = {AV3User.archive_load(user) for user in archive["users"]}

        return ArchiveThread(
            archive_time=archive["archive_time"],
            thread_info=AV3ThreadInfo.archive_load(archive["thread_info"]),
            posts=AV3Posts.archive_load(archive["posts"], users),
            subposts={
                id: AV3SubPosts.archive_load(subpost, users)
                for id, subpost in archive["subposts"].items()
            },
            users=users,
            images={AV3ContentImage.archive_load(image) for image in archive["images"]},
            audios={AV3ContentAudio.archive_load(audio) for audio in archive["audios"]},
            videos={AV3ContentVideo.archive_load(video) for video in archive["videos"]},
        )
