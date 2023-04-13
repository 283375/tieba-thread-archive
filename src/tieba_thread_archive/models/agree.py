from ..remote.protobuf.common import Agree_pb2

__all__ = ("Agree",)


class Agree:
    __slots__ = ("agree_num", "disagree_num")

    def __init__(self, *, agree_num: int, disagree_num: int):
        self.agree_num = agree_num
        self.disagree_num = disagree_num

    @classmethod
    def from_protobuf(cls, pb: Agree_pb2.Agree):
        return cls(agree_num=pb.agree_num, disagree_num=pb.disagree_num)

    def __repr__(self):
        return f"Agree({self.agree_num - self.disagree_num})"
