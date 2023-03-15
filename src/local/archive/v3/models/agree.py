from typing import TypedDict

from .....models.agree import Agree

__all__ = ("AV3Agree",)


class AV3Agree:
    class ArchivePart(TypedDict):
        agree_num: int
        disagree_num: int

    @staticmethod
    def archive_dump(agree: Agree) -> ArchivePart:
        return {
            "agree_num": agree.agree_num,
            "disagree_num": agree.disagree_num,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Agree(
            agree_num=archive["agree_num"],
            disagree_num=archive["disagree_num"],
        )
