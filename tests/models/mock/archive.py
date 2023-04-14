import random
import secrets
from typing import Tuple, overload

from src.tieba_thread_archive.models import ArchiveThread, ThreadInfo, User

from .post import MockDictSubPosts, MockPosts
from .user import MockUser

__all__ = ("MockArchiveThread",)


class MockArchiveThread(ArchiveThread):
    @overload
    def mock(*, post_num: int = random.randint(3, 25)) -> ArchiveThread:
        ...

    @overload
    @staticmethod
    def mock(
        author: User, /, *, post_num: int = random.randint(3, 25)
    ) -> ArchiveThread:
        ...

    @overload
    @staticmethod
    def mock(slice: Tuple[ArchiveThread, int, int], /) -> ArchiveThread:
        """This overload is for slicing"""
        ...

    @staticmethod
    def mock(pos_arg=None, /, *, post_num: int = random.randint(3, 25)):
        if isinstance(pos_arg, User) or pos_arg is None:
            author = pos_arg or MockUser.mock()
            posts = MockPosts.mock(author=author, post_num=post_num)
            dict_subposts = MockDictSubPosts.mock(posts)

            return ArchiveThread(
                archive_time=posts[0].time + random.randint(3375, 283375),
                thread_info=ThreadInfo(
                    id=random.randint(7000000000, 8000000000),
                    title=f"__TEST_ONLY_{secrets.token_hex(8)}__",
                    author=author,
                    create_time=posts[0].time,
                ),
                posts=posts,
                dict_subposts=dict_subposts,
                users=dict_subposts.users() | posts.users(),
            )
        else:
            raise ValueError("Unsupported call params.")

    @staticmethod
    def slice(
        archive_thread: ArchiveThread, start_floor: int, end_floor: int
    ) -> ArchiveThread:
        orig_archive_thread = archive_thread

        sliced_posts = orig_archive_thread.posts.slice(start_floor, end_floor)
        sliced_dict_subposts = MockDictSubPosts.slice(
            orig_archive_thread.dict_subposts, sliced_posts
        )

        return ArchiveThread(
            archive_time=orig_archive_thread.archive_time
            + random.randint(3375, 283375),
            thread_info=orig_archive_thread.thread_info,
            posts=sliced_posts,
            dict_subposts=sliced_dict_subposts,
            users=sliced_dict_subposts.users() | sliced_posts.users(),
        )
