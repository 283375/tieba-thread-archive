from typing import Tuple, Dict, Set

from ....models import *
from .file_structure import *
from .models import *


__all__ = ("av3_load_info", "av3_load_thread")


def av3_load_info(
    info_yaml: AV3File_InfoYaml,
) -> Tuple[ThreadInfo, ArchiveOptions, ArchiveUpdateInfo]:
    return (
        AV3ThreadInfo.archive_load(info_yaml["thread_info"]),
        AV3ArchiveOptions.archive_load(info_yaml["archive_options"]),
        AV3ArchiveUpdateInfo.archive_load(info_yaml["archive_update_info"]),
    )


def av3_load_thread(thread_yaml: AV3File_ThreadYaml) -> ArchiveThread:
    return AV3ArchiveThread.archive_load(thread_yaml)
