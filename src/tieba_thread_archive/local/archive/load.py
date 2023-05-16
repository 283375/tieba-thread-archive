import json
from os import PathLike
from pathlib import Path
from typing import Dict, Type, Union

import yaml

from ...models.archive import ThreadInfo
from .archive import LocalArchive
from .detect import detect_archive_version
from .v2 import AV2LocalArchive, av2_load_threadInfo_json, av2_load_users_json
from .v3 import AV3LocalArchive, av3_load_info_yaml

__all__ = ("load_archive", "load_archive_thread_info_only")

VERSION_CLASS_TABLE: Dict[int, Type[LocalArchive]] = {
    3: AV3LocalArchive,
    2: AV2LocalArchive,
}


def load_archive(
    path: Union[str, PathLike],
    *,
    auto_load: bool = True,
    auto_load_history: bool = False,
) -> LocalArchive:
    path = Path(path)
    version = detect_archive_version(path)

    if version is None:
        raise ValueError("Directory is not an valid archive.")

    cls = VERSION_CLASS_TABLE.get(version)

    if cls is None:
        raise ValueError("Version not supported.")

    return cls(path, auto_load=auto_load, auto_load_history=auto_load_history)


def load_archive_thread_info_only(path: Union[str, PathLike]) -> ThreadInfo:
    path = Path(path)
    version = detect_archive_version(path)

    if version is None:
        raise ValueError("Directory is not an valid archive.")

    if version == 3:
        with open(path / "info.yaml", "r", encoding="utf-8") as info_rs:
            return av3_load_info_yaml(yaml.safe_load(info_rs.read()))[0]
    elif version == 2:
        with open(path / "users.json", "r", encoding="utf-8") as users_rs:
            users = av2_load_users_json(json.loads(users_rs.read()))
        with open(path / "threadInfo.json", "r", encoding="utf-8") as info_rs:
            return av2_load_threadInfo_json(json.loads(info_rs.read()), users)[0]
    else:
        raise ValueError("Version not supported.")
