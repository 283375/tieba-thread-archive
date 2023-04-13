import random
import secrets
from typing import Dict, Iterable, Union, overload

from src.tieba_thread_archive.models import (
    Agree,
    Contents,
    DictSubPosts,
    Post,
    Posts,
    SubPost,
    SubPosts,
    User,
)

from .agree import MockAgree
from .common import mock_timestamp, mock_timestamp_later_than
from .content import MockContents
from .user import MockUser

__all__ = (
    "mock_post_id",
    "MockSubPost",
    "MockSubPosts",
    "MockPost",
    "MockPosts",
    "MockDictSubPosts",
)


def mock_post_id():
    return random.randint(120000000000, 150000000000)


class MockSubPost:
    @staticmethod
    def mock(
        *,
        id: int = mock_post_id(),
        agree: Agree = MockAgree.mock(),
        author: User = MockUser.mock(),
        time: int = mock_timestamp(),
        contents: Contents = MockContents.mock(subpost_contents=True),
    ):
        return SubPost(
            id=id,
            agree=agree,
            author=author,
            time=time,
            contents=contents,
        )


class MockSubPosts:
    @overload
    @staticmethod
    def mock(__iterable: Iterable[SubPost], /) -> SubPosts:
        ...

    @overload
    @staticmethod
    def mock(
        *,
        start_spid: int = mock_post_id(),
        start_timestamp: int = mock_timestamp(),
        subpost_num: int = random.randint(1, 10),
    ) -> SubPosts:
        ...

    @staticmethod
    def mock(*args, **kwargs):
        if (
            len(args) == 1
            and args[0]
            and isinstance(args[0], Iterable)
            and all(isinstance(item, SubPost) for item in args[0])
        ):
            return SubPosts(args[0])

        spid = kwargs.get("spid", mock_post_id())
        timestamp = kwargs.get("start_timestamp", mock_timestamp())
        mock_subpost_number = kwargs.get("subpost_num", random.randint(1, 10))

        mock_subposts = []
        for _ in range(mock_subpost_number):
            mock_subposts.append(MockSubPost.mock(id=spid, time=timestamp))
            spid += random.randint(100, 200)
            timestamp = mock_timestamp_later_than(timestamp)

        return SubPosts(mock_subposts)


class MockPost:
    @staticmethod
    def mock(
        *,
        floor: int = random.randint(1, 50),
        id: int = mock_post_id(),
        title: str = secrets.token_urlsafe(10),
        agree: Agree = MockAgree.mock(),
        author: User = MockUser.mock(),
        time: int = mock_timestamp(),
        subpost_num: int = random.randint(1, 10),
        contents: Contents = MockContents.mock(),
    ):
        return Post(
            floor=floor,
            id=id,
            title=title,
            agree=agree,
            author=author,
            time=time,
            subpost_num=subpost_num,
            contents=contents,
        )


class MockPosts:
    @overload
    @staticmethod
    def mock(__iterable: Iterable[Post], /) -> Posts:
        ...

    @overload
    @staticmethod
    def mock(
        *,
        start_pid: int = mock_post_id(),
        start_timestamp: int = mock_timestamp(),
        author: User = MockUser.mock(),
        post_num: int = random.randint(3, 25),
    ) -> Posts:
        ...

    @staticmethod
    def mock(*args, **kwargs):
        if (
            len(args) == 1
            and args[0]
            and isinstance(args[0], Iterable)
            and all(isinstance(item, Post) for item in args[0])
        ):
            return Posts(args[0])

        pid = kwargs.get("start_pid", mock_post_id())
        timestamp = kwargs.get(" start_timestamp", mock_timestamp())
        author = kwargs.get("author", MockUser.mock())
        post_num = kwargs.get("post_num", random.randint(3, 25))

        mock_posts = []
        for i in range(post_num):
            floor = i + 1
            subpost_num = random.randint(0, 5)
            mock_posts.append(
                MockPost.mock(
                    id=pid,
                    floor=floor,
                    time=timestamp,
                    author=author if random.random() < 0.2 else MockUser.mock(),
                    subpost_num=subpost_num,
                )
            )
            timestamp = mock_timestamp_later_than(timestamp)
            pid += random.randint(20, 50)

        return Posts(mock_posts)


class MockDictSubPosts:
    @overload
    @staticmethod
    def mock(
        dict_subposts: Union[DictSubPosts, Dict[int, SubPosts]], /
    ) -> DictSubPosts:
        ...

    @overload
    @staticmethod
    def mock(posts: Posts, /) -> DictSubPosts:
        ...

    @staticmethod
    def mock(pos_arg, /):
        if isinstance(pos_arg, (dict, DictSubPosts)):
            return DictSubPosts(pos_arg)  # type: ignore , DictSubPosts would do type check
        elif isinstance(pos_arg, Posts):
            return DictSubPosts(
                {
                    post.id: MockSubPosts.mock(
                        start_spid=post.id + random.randint(100, 200),
                        start_timestamp=mock_timestamp_later_than(post.time),
                        subpost_num=post.subpost_num,
                    )
                    for post in pos_arg
                    if post.subpost_num > 0
                }
            )

    @staticmethod
    def slice(dict_subposts: DictSubPosts, posts: Posts):
        return DictSubPosts(
            {
                pid: subposts
                for pid, subposts in dict_subposts.items()
                if pid in [post.id for post in posts]
            }
        )
