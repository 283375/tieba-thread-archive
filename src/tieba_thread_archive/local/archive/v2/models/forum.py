from typing import TypedDict, Union

from .....models import Forum
from ._base import AV2Model


class AV2Forum(AV2Model):
    class ArchivePart(TypedDict):
        id: Union[int, str]
        name: str

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Forum(id=int(archive["id"]), name=archive["name"], avatar="")
