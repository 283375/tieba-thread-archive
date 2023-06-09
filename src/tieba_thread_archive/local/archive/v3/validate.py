from os import PathLike
from pathlib import Path
from typing import Union

import yaml

from .file_structure import AV3File_InfoYaml

__all__ = ("av3_validate_path",)


def av3_validate_path(path: Union[str, PathLike]) -> bool:
    path = Path(path)

    try:
        necessary_files = ["info.yaml", "thread.yaml"]

        if not all((path / file).exists() for file in necessary_files):
            return False

        with open(path / "info.yaml", "r", encoding="utf-8") as info_rs:
            info: AV3File_InfoYaml = yaml.safe_load(info_rs)
            assert info["version"] == 3

        return True
    except Exception:
        return False
