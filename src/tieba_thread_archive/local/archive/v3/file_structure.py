from typing import List, Literal, TypedDict

from .models import *

__all__ = ("AV3File_InfoYaml", "AV3File_ThreadYaml", "AV3File_AssetsYaml")


class AV3File_InfoYaml(TypedDict):
    version: Literal[3]
    thread_info: AV3ThreadInfo.ArchivePart
    archive_options: AV3ArchiveOptions.ArchivePart
    archive_update_info: AV3ArchiveUpdateInfo.ArchivePart


AV3File_ThreadYaml = AV3ArchiveThread.ArchivePart


class AV3File_AssetsYaml(TypedDict):
    images: List[AV3ContentImage.ArchivePart]
    audios: List[AV3ContentAudio.ArchivePart]
    videos: List[AV3ContentVideo.ArchivePart]
