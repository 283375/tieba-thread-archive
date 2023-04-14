from typing import Union

from yarl import URL

from ..remote.protobuf.common import SimpleForum_pb2

__all__ = ("Forum",)


class Forum:
    __slots__ = ("id", "name", "avatar")

    def __init__(self, *, id: int, name: str, avatar: Union[str, URL]):
        self.id = id
        self.name = name
        if isinstance(avatar, URL):
            self.avatar = avatar
        elif isinstance(avatar, str):
            self.avatar = URL(avatar)
        else:
            raise ValueError("model Forum avatar error")

    @classmethod
    def from_protobuf(cls, pb: SimpleForum_pb2.SimpleForum):
        return cls(id=pb.id, name=pb.name, avatar=pb.avatar)

    def __repr__(self):
        return f"Forum(id={repr(self.id)}, name={repr(self.name)})"
