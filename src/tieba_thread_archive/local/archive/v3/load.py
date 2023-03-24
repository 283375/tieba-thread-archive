from typing import Set, Tuple, TypedDict

from ....models import *
from .file_structure import *
from .models import *

__all__ = ("av3_load_info_yaml", "av3_load_thread_yaml", "av3_load_assets_yaml")


def av3_load_info_yaml(
    info_yaml: AV3File_InfoYaml,
) -> Tuple[ThreadInfo, ArchiveOptions, ArchiveUpdateInfo]:
    return (
        AV3ThreadInfo.archive_load(info_yaml["thread_info"]),
        AV3ArchiveOptions.archive_load(info_yaml["archive_options"]),
        AV3ArchiveUpdateInfo.archive_load(info_yaml["archive_update_info"]),
    )


def av3_load_thread_yaml(thread_yaml: AV3File_ThreadYaml) -> ArchiveThread:
    return AV3ArchiveThread.archive_load(thread_yaml)


class AV3AssetsYamlLoadResult(TypedDict):
    images: Set[ContentImage]
    audios: Set[ContentAudio]
    videos: Set[ContentVideo]


def av3_load_assets_yaml(assets_yaml: AV3File_AssetsYaml) -> AV3AssetsYamlLoadResult:
    return {
        "images": {
            AV3ContentImage.archive_load(image_archive)
            for image_archive in assets_yaml["images"]
        },
        "audios": {
            AV3ContentAudio.archive_load(audio_archive)
            for audio_archive in assets_yaml["audios"]
        },
        "videos": {
            AV3ContentVideo.archive_load(video_archive)
            for video_archive in assets_yaml["videos"]
        },
    }
