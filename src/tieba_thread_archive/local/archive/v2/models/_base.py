from random import randint
from typing import Literal, TypedDict, Union

from typing_extensions import NotRequired

from .....models import User

__all__ = ("AV2Model", "av2_absence_user", "AV2TiebaAsset")


class AV2Model:
    @staticmethod
    def archive_dump(*args, **kwargs):
        raise NotImplementedError("dump not supported for archive version 2.")


def av2_absence_user(id: int = randint(-10000, -1)):
    return User(
        id=id,
        name="__V2_ABSENCE__",
        name_show="V2_ABSENCE",
        portrait="",
        level_id=0,
        is_bawu=0,
        bawu_type="",
        ip_address="",
    )


class AV2TiebaAsset(TypedDict):
    type: Literal["image", "audio", "video", "portrait"]
    src: str
    filename: str

    id: NotRequired[Union[int, str]]
    size: NotRequired[int]
    md5: NotRequired[str]
    portrait: NotRequired[str]
