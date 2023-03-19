from typing import TypedDict

from .....models.forum import Forum

__all__ = ("AV3Forum",)


class AV3Forum:
    class ArchivePart(TypedDict):
        id: int
        name: str
        avatar: str

    @staticmethod
    def archive_dump(forum: Forum) -> ArchivePart:
        return {
            "id": forum.id,
            "name": forum.name,
            "avatar": str(forum.avatar),
        }

    @staticmethod
    def archive_load(archive: ArchivePart):
        return Forum(
            id=archive["id"],
            name=archive["name"],
            avatar=archive["avatar"],
        )
