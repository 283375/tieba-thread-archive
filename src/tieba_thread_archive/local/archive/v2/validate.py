import json
from os import PathLike
from pathlib import Path
from typing import Union

from .file_structure import AV2File_ThreadInfoJson

__all__ = ("av2_validate_path",)


def av2_validate_path(path: Union[str, PathLike]) -> bool:
    path = Path(path)

    try:
        necessary_files = ["threadInfo.json", "posts.json", "users.json"]

        if not all((path / file).exists() for file in necessary_files):
            return False

        with open(path / "threadInfo.json", "r", encoding="utf-8") as info_rs:
            info: AV2File_ThreadInfoJson = json.loads(info_rs.read())
            assert info["storeOptions"]["__VERSION__"] == 2

        return True
    except Exception:
        return False
