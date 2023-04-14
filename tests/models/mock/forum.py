import random
import secrets
from typing import Union

from yarl import URL

from src.tieba_thread_archive.models import Forum


class MockForum:
    @staticmethod
    def mock(
        *,
        id: int = random.randint(10000000, 27963826),
        name: str = secrets.token_hex(7),
        avatar: Union[
            str, URL
        ] = "https://himg.bdimg.com/sys/portrait/item/tb.1.b6830f00.DOHaq7Xe7jTX-uAtheyghA",
    ) -> Forum:
        return Forum(id=id, name=name, avatar=avatar)
