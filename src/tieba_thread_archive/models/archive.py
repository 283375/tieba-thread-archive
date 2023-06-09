from typing import Any, Optional, Set

from ..remote.protobuf.response.PbPageResIdl_pb2 import PbPageResIdl
from .content import ContentAudio, ContentImage, ContentVideo
from .forum import Forum
from .post import DictSubPosts, Posts
from .user import User

__all__ = ("ThreadInfo", "ArchiveOptions", "ArchiveUpdateInfo", "ArchiveThread")


class ThreadInfo:
    __slots__ = ("id", "title", "author", "forum", "create_time")

    def __init__(
        self, *, id: int, title: str, author: User, forum: Forum, create_time: int
    ):
        self.id = id
        self.title = title
        self.author = author
        self.forum = forum
        self.create_time = create_time

    @classmethod
    def from_protobuf(cls, pb: PbPageResIdl):
        return cls(
            id=pb.data.thread.id,
            title=pb.data.thread.title,
            author=User.from_protobuf(pb.data.thread.author),
            forum=Forum.from_protobuf(pb.data.forum),
            create_time=pb.data.thread.create_time,
        )

    def __repr__(self):
        return f"ThreadInfo({self.id}:{self.title}@{self.author.name})"

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.author.id == other.author.id
            and self.forum.id == other.forum.id
            and self.create_time == other.create_time
            if isinstance(other, self.__class__)
            else False
        )


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
        "posts",
        "dict_subposts",
        "users",
    )

    archive_time: int
    thread_info: ThreadInfo
    posts: Posts
    dict_subposts: DictSubPosts
    users: Set[User]

    def __init__(
        self,
        *,
        archive_time: int,
        thread_info: ThreadInfo,
        posts: Posts,
        dict_subposts: DictSubPosts,
        users: Set[User],
    ):
        self.archive_time = archive_time
        self.thread_info = thread_info
        self.posts = posts
        self.dict_subposts = dict_subposts
        self.users = users

    def __setattr__(self, name: str, value: Any):
        if name == "time":
            assert isinstance(value, int)
        elif name == "thread_info":
            assert isinstance(value, ThreadInfo)
        elif name == "archive_info":
            assert isinstance(value, ArchiveOptions)
        elif name == "posts":
            assert isinstance(value, Posts)
        elif name == "dict_subposts":
            assert isinstance(value, DictSubPosts)
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
        self.posts = self.posts | other.posts
        self.dict_subposts = self.dict_subposts | other.dict_subposts
        self.users = other.users | self.users
        return self

    def images(self):
        return self.posts.images()

    def audios(self):
        return self.dict_subposts.audios() | self.posts.audios()

    def videos(self):
        return self.posts.videos()

    def __or__(self, other):
        return self.update(other)

    def __eq__(self, other):
        return (
            (
                self.thread_info == other.thread_info
                and self.posts == other.posts
                and self.dict_subposts == other.dict_subposts
                and self.users == other.users
            )
            if isinstance(other, self.__class__)
            else False
        )
