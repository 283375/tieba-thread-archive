from os import PathLike
from pathlib import Path
from typing import Union


def detect_version(path: Union[str, PathLike]) -> Union[int, None]:
    path = Path(path)
    subfiles = list(path.iterdir())
    subfile_names = {file.name for file in subfiles}

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

    /version_1
        ?
    """
    if "data.yml" in subfile_names and "info.yml" in subfile_names:
        # version >= 3
        return 3
    elif "posts.json" in subfile_names and "threadInfo.json" in subfile_names:
        # version == 2
        return 2

    return None
