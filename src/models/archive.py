from typing import Any, Dict, Iterable, Optional, TypedDict

from ..remote.api.base.get_posts import RESPONSE_PROTOBUF
from .content import ContentAudio, ContentImage
from .post import Posts, SubPosts
from .user import User

__all__ = ("ThreadInfo", "ArchiveInfo", "ArchiveUpdateInfo", "ArchiveThread")


class ThreadInfo:
    __slots__ = ("id", "title", "author", "create_time")

    def __init__(self, *, id: int, title: str, author: User, create_time: int):
        self.id = id
        self.title = title
        self.author = author
        self.create_time = create_time

    @classmethod
    def from_protobuf(cls, pb: RESPONSE_PROTOBUF):
        return cls(
            id=pb.data.thread.id,
            title=pb.data.thread.title,
            author=User.from_protobuf(pb.data.thread.author),
            create_time=pb.data.thread.create_time,
        )

    def __repr__(self):
        return f"ThreadInfo({self.id}:{self.title}@{self.author.name})"


class ArchiveInfo:
    __slots__ = ("lz_only", "images", "audios", "videos", "portraits")

    def __init__(
        self,
        *,
        lz_only: bool,
        images: bool,
        audios: bool,
        videos: bool,
        portraits: bool,
    ):
        self.lz_only = lz_only
        self.images = images
        self.audios = audios
        self.videos = videos
        self.portraits = portraits


class ArchiveUpdateInfo:
    __slots__ = ("store_time", "last_update_time")

    def __init__(self, *, store_time: int, last_update_time: Optional[int]):
        self.store_time = store_time
        self.last_update_time = last_update_time


class ArchiveThread:
    __slots__ = (
        "thread_info",
        "archive_info",
        "posts",
        "subposts",
        "users",
        "images",
        "audios",
        "videos",
    )

    thread_info: ThreadInfo
    archive_info: ArchiveInfo
    posts: Posts
    subposts: Dict[int, SubPosts]
    users: Iterable[User]
    images: Iterable[ContentImage]
    audios: Iterable[ContentAudio]

    def __init__(
        self,
        *,
        thread_info: ThreadInfo,
        archive_info: ArchiveInfo,
        posts: Posts,
        subposts: Dict[int, SubPosts],
        users: Iterable[User],
        images: Iterable[ContentImage],
        audios: Iterable[ContentAudio],
    ):
        self.thread_info = thread_info
        self.archive_info = archive_info
        self.posts = posts
        self.subposts = subposts
        self.users = users
        self.images = images
        self.audios = audios

    def __setattr__(self, name: str, value: Any):
        if name == "thread_info":
            assert isinstance(value, ThreadInfo)
        elif name == "archive_info":
            assert isinstance(value, ArchiveInfo)
        elif name == "posts":
            assert isinstance(value, Posts)
        elif name == "subposts":
            assert isinstance(value, dict) and all(
                isinstance(v, SubPosts) for v in value.values()
            )
        elif name == "users":
            assert all(isinstance(v, User) for v in value)
        elif name == "images":
            assert all(isinstance(v, ContentImage) for v in value)
        elif name == "audios":
            assert all(isinstance(v, ContentAudio) for v in value)

        return super().__setattr__(name, value)
