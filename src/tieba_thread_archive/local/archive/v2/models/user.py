from typing import TypedDict, Union

from .....models import User
from ._base import AV2Model


class AV2User(AV2Model):
    class ArchivePart(TypedDict, total=False):
        id: Union[int, str]
        portrait: str
        name: str
        name_show: str
        level_id: Union[int, str]
        is_bawu: Union[int, str]
        bawu_type: str
        ip_address: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return User(
            id=int(archive.get("id", -1)),
            name=archive.get("name", "__V2_ABSENCE__"),
            name_show=archive.get("name_show", "__V2_ABSENCE__"),
            portrait=archive.get("portrait", ""),
            level_id=int(archive.get("level_id", 0)),
            is_bawu=int(archive.get("is_bawu", 0)),
            bawu_type=archive.get("bawu_type", ""),
            ip_address=archive.get("ip_address", ""),
        )
