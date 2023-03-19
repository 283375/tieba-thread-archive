from typing import List, TypedDict

from .....models.post import *
from .agree import AV3Agree
from .content import AV3Contents
from .user import AV3User


__all__ = ("AV3SubPost", "AV3SubPosts", "AV3Post", "AV3Posts")


class AV3SubPost:
    class ArchivePart(TypedDict):
        id: int
        agree: AV3Agree.ArchivePart
        author: AV3User.ArchivePart
        time: int
        contents: AV3Contents.ArchivePart

    @staticmethod
    def archive_dump(subpost: SubPost) -> ArchivePart:
        return {
            "id": subpost.id,
            "agree": AV3Agree.archive_dump(subpost.agree),
            "author": AV3User.archive_dump(subpost.author),
            "time": subpost.time,
            "contents": AV3Contents.archive_dump(subpost.contents),
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return SubPost(
            id=archive["id"],
            agree=AV3Agree.archive_load(archive["agree"]),
            author=AV3User.archive_load(archive["author"]),
            time=archive["time"],
            contents=AV3Contents.archive_load(archive["contents"]),
        )


class AV3SubPosts:
    ArchivePart = List[AV3SubPost.ArchivePart]

    @staticmethod
    def archive_dump(subposts: SubPosts) -> ArchivePart:
        return [AV3SubPost.archive_dump(subpost) for subpost in subposts]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return SubPosts(AV3SubPost.archive_load(subpost) for subpost in archive)


class AV3Post:
    class ArchivePart(TypedDict):
        floor: int
        id: int
        title: str
        agree: AV3Agree.ArchivePart
        author_id: int
        author: AV3User.ArchivePart
        time: int
        subpost_num: int
        contents: AV3Contents.ArchivePart

    @staticmethod
    def archive_dump(post: Post) -> ArchivePart:
        return {
            "floor": post.floor,
            "id": post.id,
            "title": post.title,
            "agree": AV3Agree.archive_dump(post.agree),
            "author_id": post.author_id,
            "author": AV3User.archive_dump(post.author),
            "time": post.time,
            "subpost_num": post.subpost_num,
            "contents": AV3Contents.archive_dump(post.contents),
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Post(
            floor=archive["floor"],
            id=archive["id"],
            title=archive["title"],
            agree=AV3Agree.archive_load(archive["agree"]),
            author=AV3User.archive_load(archive["author"]),
            time=archive["time"],
            subpost_num=archive["subpost_num"],
            contents=AV3Contents.archive_load(archive["contents"]),
        )


class AV3Posts:
    ArchivePart = List[AV3Post.ArchivePart]

    @staticmethod
    def archive_dump(posts: Posts) -> ArchivePart:
        return [AV3Post.archive_dump(post) for post in posts]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Posts(AV3Post.archive_load(post) for post in archive)
