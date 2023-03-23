from typing import TypedDict
from typing_extensions import NotRequired

from .....models.user import User

__all__ = ("AV3User",)


class AV3User:
    class ArchivePart(TypedDict):
        id: int
        name: str
        name_show: str
        portrait: str
        level_id: int
        is_bawu: int
        bawu_type: NotRequired[str]

    @staticmethod
    def archive_dump(user: User) -> ArchivePart:
        archive_part: AV3User.ArchivePart = {
            "id": user.id,
            "name": user.name,
            "name_show": user.name_show,
            "portrait": user.portrait,
            "level_id": user.level_id,
            "is_bawu": user.is_bawu,
        }

        if user.is_bawu:
            archive_part["bawu_type"] = user.bawu_type

        return archive_part

    @staticmethod
    def archive_load(archive: ArchivePart):
        return User(
            id=archive["id"],
            name=archive["name"],
            name_show=archive["name_show"],
            portrait=archive["portrait"],
            level_id=archive["level_id"],
            is_bawu=archive["is_bawu"],
            bawu_type=archive.get("bawu_type", ""),
        )
