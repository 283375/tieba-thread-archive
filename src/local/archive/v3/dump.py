from os import PathLike
from pathlib import Path
from typing import Dict, Union

import yaml

from ....models.archive import ArchiveInfo, ArchiveThread, ThreadInfo
from ....models.post import Posts, SubPosts
from .models import *


def dump_v3_info(thread_info: ThreadInfo, archive_info: ArchiveInfo) -> str:
    return yaml.safe_dump(
        {
            AV3ThreadInfo.archive_title(): AV3ThreadInfo.archive_dump(thread_info),
            AV3ArchiveInfo.archive_title(): AV3ArchiveInfo.archive_dump(archive_info),
        },
        allow_unicode=True,
        sort_keys=False,
    )


def dump_v3_posts(posts: Posts, subposts: Dict[int, SubPosts]) -> str:
    return yaml.safe_dump(
        {
            AV3Posts.archive_title(): AV3Posts.archive_dump(posts),
            AV3SubPosts.archive_title(): {
                id: AV3SubPosts.archive_dump(subpost)
                for id, subpost in subposts.items()
            },
        },
        allow_unicode=True,
        sort_keys=False,
    )
