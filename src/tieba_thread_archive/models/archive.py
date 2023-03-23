from typing import Any, Dict, Optional, Set

from ..remote.protobuf.response.PbPageResIdl_pb2 import PbPageResIdl
from .content import ContentAudio, ContentImage, ContentVideo
from .post import Posts, SubPosts
from .user import User

__all__ = ("ThreadInfo", "ArchiveOptions", "ArchiveUpdateInfo", "ArchiveThread")


class ThreadInfo:
    __slots__ = ("id", "title", "author", "create_time")

    def __init__(self, *, id: int, title: str, author: User, create_time: int):
        self.id = id
        self.title = title
        self.author = author
        self.create_time = create_time

    @classmethod
    def from_protobuf(cls, pb: PbPageResIdl):
        return cls(
            id=pb.data.thread.id,
            title=pb.data.thread.title,
            author=User.from_protobuf(pb.data.thread.author),
            create_time=pb.data.thread.create_time,
        )

    def __repr__(self):
        return f"ThreadInfo({self.id}:{self.title}@{self.author.name})"


class ArchiveOptions:
    __slots__ = ("images", "audios", "videos", "portraits")

    def __init__(
        self,
        *,
        images: bool,
        audios: bool,
        videos: bool,
        portraits: bool,
    ):
        self.images = images
        self.audios = audios
        self.videos = videos
        self.portraits = portraits


class ArchiveUpdateInfo:
    __slots__ = ("archive_time", "last_update_time")

    def __init__(self, *, archive_time: int, last_update_time: Optional[int]):
        self.archive_time = archive_time
        self.last_update_time = last_update_time


class ArchiveThread:
    __slots__ = (
        "archive_time",
        "thread_info",
        "archive_options",
        "posts",
        "subposts",
        "users",
        "images",
        "audios",
        "videos",
    )

    archive_time: int
    thread_info: ThreadInfo
    posts: Posts
    subposts: Dict[int, SubPosts]
    users: Set[User]
    images: Set[ContentImage]
    audios: Set[ContentAudio]
    videos: Set[ContentVideo]

    def __init__(
        self,
        *,
        archive_time: int,
        thread_info: ThreadInfo,
        posts: Posts,
        subposts: Dict[int, SubPosts],
        users: Set[User],
        images: Set[ContentImage],
        audios: Set[ContentAudio],
        videos: Set[ContentVideo],
    ):
        self.archive_time = archive_time
        self.thread_info = thread_info
        self.posts = posts
        self.subposts = subposts
        self.users = users
        self.images = images
        self.audios = audios
        self.videos = videos

    def __setattr__(self, name: str, value: Any):
        if name == "time":
            assert isinstance(value, int)
        elif name == "thread_info":
            assert isinstance(value, ThreadInfo)
        elif name == "archive_info":
            assert isinstance(value, ArchiveOptions)
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
        elif name == "videos":
            assert all(isinstance(v, ContentVideo) for v in value)

        return super().__setattr__(name, value)

    def update(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Not ArchiveThread.")
        if self.thread_info.id != other.thread_info.id:
            raise ValueError("Different ArchiveThread (thread_info not match).")

        self.archive_time = other.archive_time
        self.thread_info = other.thread_info
        self.posts = other.posts | self.posts
        for id in self.subposts.keys():
            _other_subposts = other.subposts.get(id)
            if _other_subposts is not None:
                self.subposts[id] = _other_subposts | self.subposts[id]
        self.users = other.users | self.users
        self.images = other.images | self.images
        self.audios = other.audios | self.audios
        self.videos = other.videos | self.videos
        return self

    def __or__(self, other):
        return self.update(other)
