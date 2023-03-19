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
    data.yml


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


def detect_archive_version(path: Union[str, PathLike]):
    path = Path(path)
    subfiles = list(path.iterdir())
    subfile_names = {file.name for file in subfiles}

    if "data.yml" in subfile_names and "info.yml" in subfile_names:
        # version >= 3
        try:
            with open(path, "r", encoding="utf-8") as info_rs:
                info_archive = yaml.safe_load(info_rs.read())

        except Exception:
            return None
    elif "posts.json" in subfile_names and "threadInfo.json" in subfile_names:
        # version == 2
        return 2
