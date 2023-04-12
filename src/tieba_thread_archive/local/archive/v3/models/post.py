from typing import Dict, Iterable, List, TypedDict

from .....models.post import *
from .....models.user import User
from .agree import AV3Agree
from .content import AV3Contents

__all__ = ("AV3SubPost", "AV3SubPosts", "AV3DictSubPosts", "AV3Post", "AV3Posts")


class AV3SubPost:
    class ArchivePart(TypedDict):
        id: int
        agree: AV3Agree.ArchivePart
        author_id: int
        time: int
        contents: AV3Contents.ArchivePart

    @staticmethod
    def archive_dump(subpost: SubPost) -> ArchivePart:
        return {
            "id": subpost.id,
            "agree": AV3Agree.archive_dump(subpost.agree),
            "author_id": subpost.author.id,
            "time": subpost.time,
            "contents": AV3Contents.archive_dump(subpost.contents),
        }

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        author_id = archive["author_id"]
        author = None
        for user in user_list:
            if user.id == author_id:
                author = user
                break
        else:
            raise ValueError(f"User {author_id} not found in provided user list.")

        return SubPost(
            id=archive["id"],
            agree=AV3Agree.archive_load(archive["agree"]),
            author=author,
            time=archive["time"],
            contents=AV3Contents.archive_load(archive["contents"]),
        )


class AV3SubPosts:
    ArchivePart = List[AV3SubPost.ArchivePart]

    @staticmethod
    def archive_dump(subposts: SubPosts) -> ArchivePart:
        return [AV3SubPost.archive_dump(subpost) for subpost in subposts]

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        return SubPosts(
            AV3SubPost.archive_load(subpost, user_list) for subpost in archive
        )


class AV3DictSubPosts:
    ArchivePart = Dict[int, AV3SubPosts.ArchivePart]

    @staticmethod
    def archive_dump(dict_subposts: DictSubPosts) -> ArchivePart:
        return {
            pid: AV3SubPosts.archive_dump(subposts)
            for pid, subposts in dict_subposts.items()
        }

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        dict_subposts = DictSubPosts()

        for pid, subposts_archive in archive.items():
            dict_subposts.update_id(
                pid, AV3SubPosts.archive_load(subposts_archive, user_list)
            )

        return dict_subposts


class AV3Post:
    class ArchivePart(TypedDict):
        floor: int
        id: int
        title: str
        agree: AV3Agree.ArchivePart
        author_id: int
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
            "time": post.time,
            "subpost_num": post.subpost_num,
            "contents": AV3Contents.archive_dump(post.contents),
        }

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        author_id = archive["author_id"]
        author = None
        for user in user_list:
            if user.id == author_id:
                author = user
                break
        else:
            raise ValueError(f"User {author_id} not found in provided user list.")

        return Post(
            floor=archive["floor"],
            id=archive["id"],
            title=archive["title"],
            agree=AV3Agree.archive_load(archive["agree"]),
            author=author,
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
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        return Posts(AV3Post.archive_load(post, user_list) for post in archive)
