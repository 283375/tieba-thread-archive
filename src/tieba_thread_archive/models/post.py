from copy import deepcopy
from functools import reduce
from typing import Dict, Iterable, List, Optional, Set, Union

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from typing_extensions import Self

from ..remote.protobuf.common import Post_pb2, SubPostList_pb2, User_pb2
from .agree import Agree
from .content import ContentAudio, ContentImage, Contents, ContentVideo
from .user import User

__all__ = ("SubPost", "SubPosts", "DictSubPosts", "Post", "Posts")


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

    def audios(self):
        return {
            content for content in self.contents if isinstance(content, ContentAudio)
        }

    def __repr__(self):
        return f"SubPost({self.id})"

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.time < other.time

    def __le__(self, other):
        return isinstance(other, self.__class__) and self.time <= other.time

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
            and self.contents == other.contents
        )


class SubPosts(List[SubPost]):
    def __init__(self, __iterable: Optional[Iterable[SubPost]] = None, /):
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

    def users(self):
        return {subpost.author for subpost in self}

    def audios(self):
        return reduce(lambda c1, c2: c2 | c1, [subpost.audios() for subpost in self])

    def __add__(self, other):
        if isinstance(other, self.__class__):
            subposts = {subpost.id: subpost for subpost in self}
            subposts.update({subpost.id: subpost for subpost in other})
            subposts = [v for i, v in sorted(subposts.items(), key=lambda kv: kv[0])]
            self.clear()
            self.extend(subposts)
            return self
        else:
            raise TypeError(
                "SubPosts can only be added to another instance of SubPosts."
            )

    def __radd__(self, other):
        return self.__add__(other)

    def __or__(self, other):
        return self.__add__(other)

    def __repr__(self):
        display_subposts = self[:3]
        rest_subposts = len(self) - 3

        insert_str = ", ".join(repr(sp) for sp in display_subposts)
        if rest_subposts > 0:
            insert_str += f", ...{rest_subposts}"
        return f"[{insert_str}]"


class DictSubPosts:
    def __init__(
        self, dict_subposts: Optional[Union[Self, Dict[int, SubPosts]]] = None, /
    ):
        self.__dict: Dict[int, SubPosts] = {}

        if isinstance(dict_subposts, self.__class__):
            self += dict_subposts
        elif (
            isinstance(dict_subposts, dict)
            and all(isinstance(key, int) for key in dict_subposts.keys())
            and all(isinstance(value, SubPosts) for value in dict_subposts.values())
        ):
            self.__dict = deepcopy(dict_subposts)
        elif dict_subposts is not None:
            raise ValueError(
                f"Expect {self.__class__.__name__} or Dict[int, SubPosts]."
            )

    def __getitem__(self, key):
        return self.__dict.__getitem__(key)

    def update_id(self, id: int, subposts: SubPosts):
        if self.__dict.get(id):
            self.__dict[id] |= subposts
        else:
            self.__dict.setdefault(id, subposts)

    def users(self) -> Set[User]:
        user_list = [subposts.users() for subposts in self.__dict.values()]
        return reduce(lambda u1, u2: u1 | u2, user_list) if user_list else set()

    def audios(self):
        audio_list = [subposts.audios() for subposts in self.__dict.values()]
        return reduce(lambda a1, a2: a1 | a2, audio_list) if audio_list else set()

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def items(self):
        return self.__dict.items()

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected instance of {self.__class__}.")

        for pid in other.keys():
            self.update_id(pid, other[pid])
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __or__(self, other):
        return self.__add__(other)

    def __eq__(self, other):
        return (
            self.__dict == other.__dict if isinstance(other, self.__class__) else False
        )


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
        user_list: RepeatedCompositeFieldContainer[User_pb2.User],
    ):
        for user_pb in user_list:
            if pb.author_id == user_pb.id:
                author = User.from_protobuf(user_pb)
                break
        else:
            raise ValueError(f"Cannot find author (id {pb.author_id}) in user list.")

        return cls(
            floor=pb.floor,
            id=pb.id,
            title=pb.title,
            agree=Agree.from_protobuf(pb.agree),
            author=author,
            time=pb.time,
            subpost_num=pb.sub_post_number,
            contents=Contents.from_protobuf(pb.content),
        )

    def images(self):
        return {
            content for content in self.contents if isinstance(content, ContentImage)
        }

    def audios(self):
        return {
            content for content in self.contents if isinstance(content, ContentAudio)
        }

    def videos(self):
        return {
            content for content in self.contents if isinstance(content, ContentVideo)
        }

    def __repr__(self):
        return f"Post({self.id}, {self.floor}L)"

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.floor < other.floor

    def __le__(self, other):
        return isinstance(other, self.__class__) and self.floor <= other.floor

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
            and self.contents == other.contents
        )


class Posts(List[Post]):
    def __init__(self, __iterable: Optional[Iterable[Post]] = None, /):
        if __iterable is not None:
            self.clear()
            self.extend(__iterable)
            self.sort_self()

    @classmethod
    def from_protobuf(
        cls,
        pb: RepeatedCompositeFieldContainer[Post_pb2.Post],
        user_list: RepeatedCompositeFieldContainer[User_pb2.User],
    ):
        posts = [Post.from_protobuf(_pb, user_list) for _pb in pb]
        return cls(posts)

    def __sort(self, posts: Iterable[Post]):
        return sorted(posts, key=lambda x: x.id)

    def sort(self) -> Self:
        return Posts(self.__sort(self))

    def sort_self(self):
        sorted_posts = self.__sort(self)
        self.clear()
        self.extend(sorted_posts)

    def __slice(self, posts: Iterable[Post], start_floor: int, end_floor: int):
        if start_floor > end_floor:
            raise ValueError("start_floor must be less than or equal to end_floor")
        start_floor = max(1, start_floor)
        end_floor = min(len(self), end_floor)
        return [post for post in self if start_floor <= post.floor <= end_floor]

    def slice(self, start_floor: int, end_floor: int) -> Self:
        return Posts(self.__slice(self, start_floor, end_floor))

    def slice_self(self, start_floor: int, end_floor: int):
        sliced_posts = self.__slice(self, start_floor, end_floor)
        self.clear()
        self.extend(sliced_posts)

    def users(self):
        return {post.author for post in self}

    def images(self):
        return reduce(lambda c1, c2: c2 | c1, [post.images() for post in self])

    def audios(self):
        return reduce(lambda c1, c2: c2 | c1, [post.audios() for post in self])

    def videos(self):
        return reduce(lambda c1, c2: c2 | c1, [post.videos() for post in self])

    def __repr__(self):
        display_posts = self[:3]
        rest_posts = len(self) - 3

        insert_str = ", ".join(repr(p) for p in display_posts)
        if rest_posts > 0:
            insert_str += f", ...{rest_posts}"
        return f"[{insert_str}]"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            posts = {post.id: post for post in self}
            posts.update({post.id: post for post in other})
            posts = [v for i, v in sorted(posts.items(), key=lambda kv: kv[0])]
            self.clear()
            self.extend(posts)
            return self
        else:
            raise TypeError("Posts can only be added to another instance of Posts.")

    def __radd__(self, other):
        return self.__add__(other)

    def __or__(self, other):
        return self.__add__(other)
