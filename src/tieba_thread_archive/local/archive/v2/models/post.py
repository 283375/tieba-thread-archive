import warnings
from typing import Iterable, List, TypedDict, Union

from .....models.post import *
from .....models.user import User
from ._base import AV2Model, av2_absence_user
from .agree import AV2Agree
from .content import AV2Contents
from .user import AV2User

__all__ = ("AV2SubPost", "AV2SubPosts", "AV2Post", "AV2Posts")


class AV2SubPost(AV2Model):
    class ArchivePart(TypedDict):
        id: Union[int, str]
        content: AV2Contents.ArchivePart
        time: Union[int, str]
        agree: AV2Agree.ArchivePart
        author: AV2User.ArchivePart

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        author_id = int(archive["author"].get("id", -1))
        author = av2_absence_user(author_id)
        for user in user_list:
            if user.id == author_id:
                author = user
                break
        else:
            warnings.warn(f"User {author_id} not found in provided user list.")

        return SubPost(
            id=int(archive["id"]),
            agree=AV2Agree.archive_load(archive["agree"]),
            author=author,
            time=int(archive["time"]),
            contents=AV2Contents.archive_load(archive["content"]),
        )


class AV2SubPosts(AV2Model):
    ArchivePart = List[AV2SubPost.ArchivePart]

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        return SubPosts(
            AV2SubPost.archive_load(subpost, user_list) for subpost in archive
        )


class AV2Post(AV2Model):
    class ArchivePart(TypedDict):
        id: int
        title: str
        floor: int
        time: int
        content: AV2Contents.ArchivePart
        agree: AV2Agree.ArchivePart
        sub_post_number: int
        sub_post_list: AV2SubPosts.ArchivePart
        author_id: int

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        author_id = archive["author_id"]
        author = av2_absence_user(author_id)
        for user in user_list:
            if user.id == author_id:
                author = user
                break
        else:
            warnings.warn(f"User {author_id} not found in provided user list.")

        return Post(
            floor=archive["floor"],
            id=archive["id"],
            title=archive["title"],
            agree=AV2Agree.archive_load(archive["agree"]),
            author=author,
            time=archive["time"],
            subpost_num=int(archive["sub_post_number"]),
            contents=AV2Contents.archive_load(archive["content"]),
        )


class AV2Posts(AV2Model):
    ArchivePart = List[AV2Post.ArchivePart]

    @staticmethod
    def archive_load(archive: ArchivePart, user_list: Iterable[User]):
        return Posts(AV2Post.archive_load(post, user_list) for post in archive)
