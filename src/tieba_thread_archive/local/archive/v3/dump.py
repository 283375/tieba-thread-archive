from typing import Set

import yaml

from ....models import *
from .file_structure import *
from .load import *
from .models import *

__all__ = (
    "av3_dump_info_yaml_str",
    "av3_dump_thread_yaml_str",
    "av3_dump_assets_yaml_str",
)


def av3_dump_info_yaml_str(
    *,
    thread_info: ThreadInfo,
    archive_options: ArchiveOptions,
    archive_update_info: ArchiveUpdateInfo
) -> str:
    info_yaml: AV3File_InfoYaml = {
        "version": 3,
        "thread_info": AV3ThreadInfo.archive_dump(thread_info),
        "archive_options": AV3ArchiveOptions.archive_dump(archive_options),
        "archive_update_info": AV3ArchiveUpdateInfo.archive_dump(archive_update_info),
    }
    return yaml.safe_dump(info_yaml, allow_unicode=True, sort_keys=False)


def av3_dump_thread_yaml_str(*, archive_thread: ArchiveThread) -> str:
    thread_yaml: AV3File_ThreadYaml = AV3ArchiveThread.archive_dump(archive_thread)
    return yaml.safe_dump(thread_yaml, allow_unicode=True, sort_keys=False)


def av3_dump_assets_yaml_str(
    *, images: Set[ContentImage], audios: Set[ContentAudio], videos: Set[ContentVideo]
) -> str:
    assets_yaml: AV3File_AssetsYaml = {
        "images": [AV3ContentImage.archive_dump(image) for image in images],
        "audios": [AV3ContentAudio.archive_dump(audio) for audio in audios],
        "videos": [AV3ContentVideo.archive_dump(video) for video in videos],
    }
    return yaml.safe_dump(assets_yaml, allow_unicode=True, sort_keys=False)
