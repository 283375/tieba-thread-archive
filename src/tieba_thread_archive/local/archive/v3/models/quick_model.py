import builtins
from typing import Generic, TypedDict, TypeVar

from .....models import *

__all__ = ("AV3QuickModel",)

BUILTIN_TYPES = tuple(
    getattr(builtins, t)
    for t in dir(builtins)
    if isinstance(getattr(builtins, t), type)
)

C = TypeVar("C")


class AV3QuickModel(Generic[C]):
    ArchivePart = TypedDict("ArchivePart", __preserve__=bool)

    @classmethod
    def archive_dump(cls, __cls: object) -> ArchivePart:
        __dict = {}
        for key in cls.ArchivePart.__annotations__.keys():
            attr = __cls.__getattribute__(key)
            __dict[key] = attr if type(attr) in BUILTIN_TYPES else attr.archive_dump()
        return __dict  # type: ignore

    @classmethod
    def archive_load(cls, archive: ArchivePart) -> C:
        __dict = {}
        for key in cls.ArchivePart.__annotations__.keys():
            attr = archive[key]
            __dict[key] = attr if type(attr) in BUILTIN_TYPES else attr.archive_load()
        return cls(**__dict)  # type: ignore


class AV3Agree(AV3QuickModel, Agree):
    class ArchivePart(TypedDict):
        agree_num: int
        disagree_num: int
