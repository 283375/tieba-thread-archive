from typing import TypedDict, Union

from .....models import Agree
from ._base import AV2Model


class AV2Agree(AV2Model):
    class ArchivePart(TypedDict, total=False):
        agree_num: Union[int, str]
        disagree_num: Union[int, str]
        diff_agree_num: Union[int, str]
        has_agree: Union[int, str]
        agree_type: Union[int, str]

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Agree(
            agree_num=int(archive.get("agree_num", -1)),
            disagree_num=int(archive.get("disagree_num", -1)),
        )
