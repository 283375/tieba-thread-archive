from typing import Iterable, List, Optional, Union

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

from ..remote.protobuf.common import Post_pb2, SubPostList_pb2, User_pb2
from .agree import Agree
from .content import Contents
from .user import User

__all__ = ("SubPost", "SubPosts", "Post", "Posts")


class SubPost:
    __slots__ = ("id", "agree", "author", "time", "contents")

    def __init__(
        self, *, id: int, agree: Agree, author: User, time: int, contents: Contents
    ):
        self.id = id
        self.agree = agree
        self.author = author
        self.time = time
        self.contents = contents

    @classmethod
    def from_protobuf(cls, pb: SubPostList_pb2.SubPostList):
        return cls(
            id=pb.id,
            agree=Agree.from_protobuf(pb.agree),
            author=User.from_protobuf(pb.author),
            contents=Contents.from_protobuf(pb.content),
            time=pb.time,
        )

    def __repr__(self):
        return f"SubPost({self.id})"

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.time < other.time

    def __le__(self, other):
        return isinstance(other, self.__class__) and self.time <= other.time

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id


class SubPosts(List[SubPost]):
    def __init__(self, /, __iterable: Optional[Iterable[SubPost]] = None):
        if __iterable is not None:
            self.clear()
            self.extend(__iterable)
            self.sort()

    @classmethod
    def from_protobuf(
        cls,
        pb: Union[
            SubPostList_pb2.SubPost,
            RepeatedCompositeFieldContainer[SubPostList_pb2.SubPostList],
        ],
    ):
        subposts_pb = (
            pb.sub_post_list if isinstance(pb, SubPostList_pb2.SubPost) else pb
        )
        subposts = [SubPost.from_protobuf(pb) for pb in subposts_pb]

        return cls(subposts)

    def sort(self):
        self = sorted(self, key=lambda x: x.id)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            subposts = {subpost.id: subpost for subpost in self} | {
                subpost.id: subpost for subpost in other
            }
            subposts = [v for i, v in sorted(subposts.items(), key=lambda kv: kv[0])]
            self.clear()
            self.extend(subposts)
            return self
        else:
            raise TypeError(
                "SubPosts can only be added to another instance of SubPosts."
            )

    def __repr__(self):
        display_subposts = self[:3]
        rest_subposts = len(self) - 3

        insert_str = ", ".join(repr(sp) for sp in display_subposts)
        if rest_subposts > 0:
            insert_str += f", ...{rest_subposts}"
        return f"[{insert_str}]"


class Post:
    __slots__ = (
        "floor",
        "id",
        "title",
        "agree",
        "author_id",
        "author",
        "time",
        "subpost_num",
        "contents",
    )

    def __init__(
        self,
        *,
        floor: int,
        id: int,
        title: str,
        agree: Agree,
        author: User,
        time: int,
        subpost_num: int,
        contents: Contents,
    ):
        self.floor = floor
        self.id = id
        self.title = title
        self.agree = agree
        self.author = author
        self.author_id = author.id
        self.subpost_num = subpost_num
        self.time = time
        self.contents = contents

    @classmethod
    def from_protobuf(
        cls,
        pb: Post_pb2.Post,
        user_list: Union[RepeatedCompositeFieldContainer[User_pb2.User], None] = None,
    ):
        return cls(
            floor=pb.floor,
            id=pb.id,
            title=pb.title,
            agree=Agree.from_protobuf(pb.agree),
            author=User.from_protobuf(pb.author),
            time=pb.time,
            subpost_num=pb.sub_post_number,
            contents=Contents.from_protobuf(pb.content),
        )

    def __repr__(self):
        return f"Post({self.id}, {self.floor}L)"

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.floor < other.floor

    def __le__(self, other):
        return isinstance(other, self.__class__) and self.floor <= other.floor

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id


class Posts(List[Post]):
    def __init__(self, /, __iterable: Optional[Iterable[Post]] = None):
        if __iterable is not None:
            self.clear()
            self.extend(__iterable)
            self.sort()

    @classmethod
    def from_protobuf(
        cls,
        pb: RepeatedCompositeFieldContainer[Post_pb2.Post],
        user_list: Union[RepeatedCompositeFieldContainer[User_pb2.User], None] = None,
    ):
        posts = [Post.from_protobuf(_pb, user_list) for _pb in pb]
        return cls(posts)

    def sort(self):
        self = sorted(self, key=lambda x: x.id)

    def __repr__(self):
        display_posts = self[:3]
        rest_posts = len(self) - 3

        insert_str = ", ".join(repr(p) for p in display_posts)
        if rest_posts > 0:
            insert_str += f", ...{rest_posts}"
        return f"[{insert_str}]"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            posts = {post.id: post for post in self} | {post.id: post for post in other}
            posts = [v for i, v in sorted(posts.items(), key=lambda kv: kv[0])]
            self.clear()
            self.extend(posts)
            return self
        else:
            raise TypeError("Posts can only be added to another instance of Posts.")

    def __radd__(self, other):
        return self.__add__(other)
