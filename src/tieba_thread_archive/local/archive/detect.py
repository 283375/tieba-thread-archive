from os import PathLike
from pathlib import Path
from typing import Union

import yaml

"""
/version_3
    /.history
    [/.temp]
    [/images]
    [/videos]
    [/audios]
    [/portraits]
    info.yml
    thread.yml
    [assets.yml]


/version_2
    [/assets]
        [/image]
        [/video]
        [/audio]
    /origData
    [/portraits]
    [/assets.json]
    [/portraits.json]
    posts.json
    threadInfo.json
    users.json
"""

__all__ = ("detect_archive_version",)


def detect_archive_version(path: Union[str, PathLike]) -> Union[int, None]:
    path = Path(path)
    subfiles = list(path.iterdir())
    subfile_names = {file.name for file in subfiles}

    if "thread.yml" in subfile_names and "info.yml" in subfile_names:
        # version >= 3
        try:
            with open(path / "info.yml", "r", encoding="utf-8") as info_rs:
                info_archive = yaml.safe_load(info_rs.read())
                version = info_archive.get("version")
                assert version is not None and isinstance(version, int)
                return version
        except Exception:
            return None
    elif "posts.json" in subfile_names and "threadInfo.json" in subfile_names:
        # version == 2
        return 2
