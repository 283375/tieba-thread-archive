import random
import secrets
from typing import Dict, Optional, Tuple, TypedDict

from src.tieba_thread_archive.models.post import Post, Posts, SubPost, SubPosts
from src.tieba_thread_archive.models.user import User

from .agree import MockAgree
from .common import mock_timestamp, mock_timestamp_later_than
from .content import MockContents
from .user import MockUser


def mock_post_id():
    return random.randint(120000000000, 150000000000)


class MockSubPost(SubPost):
    def __init__(self, *, spid: int, timestamp: int):
        super().__init__(
            id=spid,
            agree=MockAgree(),
            author=MockUser(),
            time=timestamp or mock_timestamp(),
            contents=MockContents(),
        )


class MockSubPosts(SubPosts):
    def __init__(
        self,
        start_spid: int = mock_post_id(),
        start_timestamp: int = mock_timestamp(),
        subpost_num: int = random.randint(1, 10),
    ):
        spid = start_spid
        timestamp = start_timestamp
        mock_subpost_number = subpost_num

        mock_subposts = []
        for _ in range(mock_subpost_number):
            mock_subposts.append(MockSubPost(spid=spid, timestamp=timestamp))
            spid += random.randint(100, 200)
            timestamp = mock_timestamp_later_than(timestamp)

        super().__init__(mock_subposts)


class MockPost(Post):
    def __init__(
        self,
        *,
        pid: int,
        floor: int,
        timestamp: int,
        author: Optional[User] = None,
        subpost_num: int,
    ):
        super().__init__(
            floor=floor,
            id=pid,
            title=secrets.token_urlsafe(10),
            agree=MockAgree(),
            author=author or MockUser(),
            time=timestamp,
            subpost_num=subpost_num,
            contents=MockContents(),
        )


class MockPosts(Posts):
    __slots__ = ("post_subpost_num",)

    def __init__(
        self,
        start_pid: int = mock_post_id(),
        start_timestamp: int = mock_timestamp(),
        lz: User = MockUser(),
        post_num: int = random.randint(3, 25),
    ):
        timestamp = start_timestamp
        pid = start_pid

        self.post_subpost_num = {}

        mock_posts = []
        for i in range(post_num):
            floor = i + 1
            subpost_num = random.randint(0, 5)
            self.post_subpost_num.setdefault(pid, subpost_num)
            mock_posts.append(
                MockPost(
                    pid=pid,
                    floor=floor,
                    timestamp=timestamp,
                    author=random.choices([lz, MockUser()], weights=(20, 80))[0],
                    subpost_num=subpost_num,
                )
            )
            timestamp = mock_timestamp_later_than(timestamp)
            pid += random.randint(20, 50)

        super().__init__(mock_posts)


def mock_posts_and_subposts(lz: User = MockUser()) -> Tuple[Posts, Dict[int, SubPosts]]:
    posts = MockPosts(lz=lz)
    subposts: Dict[int, SubPosts] = {
        post.id: MockSubPosts(
            start_spid=post.id + random.randint(100, 200),
            start_timestamp=mock_timestamp_later_than(post.time),
            subpost_num=post.subpost_num,
        )
        for post in posts
        if post.subpost_num > 0
    }
    return (posts, subposts)
