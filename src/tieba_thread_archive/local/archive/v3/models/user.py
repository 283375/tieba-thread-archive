from typing import TypedDict

from .....models.user import User

__all__ = ("AV3User",)


class AV3User:
    class ArchivePart(TypedDict):
        id: int
        name: str
        name_show: str
        portrait: str
        level_id: int

    @staticmethod
    def archive_dump(user: User) -> ArchivePart:
        return {
            "id": user.id,
            "name": user.name,
            "name_show": user.name_show,
            "portrait": user.portrait,
            "level_id": user.level_id,
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return User(
            id=archive["id"],
            name=archive["name"],
            name_show=archive["name_show"],
            portrait=archive["portrait"],
            level_id=archive["level_id"],
        )
