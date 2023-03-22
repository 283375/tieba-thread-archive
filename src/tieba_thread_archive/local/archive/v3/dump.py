from os import PathLike
from pathlib import Path
from typing import Union

import yaml

from ....models import *
from .file_structure import *
from .load import *
from .models import *
from .validate import av3_validate_path


def av3_get_info_yaml_dump_str(
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


def av3_get_thread_yaml_dump_str(*, archive_thread: ArchiveThread) -> str:
    thread_yaml: AV3File_ThreadYaml = AV3ArchiveThread.archive_dump(archive_thread)
    return yaml.safe_dump(thread_yaml, allow_unicode=True, sort_keys=False)


def av3_dump_archive(
    path: Union[str, PathLike],
    archive_thread: ArchiveThread,
    archive_options: ArchiveOptions,
):
    path = Path(path)

    if av3_validate_path(path):
        with open(path / "thread.yml", "r+", encoding="utf-8") as thread_yaml_rws:
            _archive_thread = av3_load_thread(yaml.safe_load(thread_yaml_rws.read()))
            _archive_thread |= archive_thread
            thread_yaml_rws.truncate()
            thread_yaml_rws.write(
                av3_get_thread_yaml_dump_str(archive_thread=_archive_thread)
            )

        with open(path / "info.yml", "r+", encoding="utf-8") as info_yaml_rws:
            _, _, archive_update_info = av3_load_info(
                yaml.safe_load(info_yaml_rws.read())
            )
            archive_update_info.last_update_time = archive_thread.archive_time
            info_yaml_rws.truncate()
            info_yaml_rws.write(
                av3_get_info_yaml_dump_str(
                    thread_info=archive_thread.thread_info,
                    archive_options=archive_options,
                    archive_update_info=archive_update_info,
                )
            )
    else:
        with open(path / "thread.yml", "w", encoding="utf-8") as thread_yaml_ws:
            thread_yaml_ws.write(
                av3_get_thread_yaml_dump_str(archive_thread=archive_thread)
            )

        with open(path / "info.yml", "w", encoding="utf-8") as info_yaml_ws:
            info_yaml_ws.write(
                av3_get_info_yaml_dump_str(
                    thread_info=archive_thread.thread_info,
                    archive_options=archive_options,
                    archive_update_info=ArchiveUpdateInfo(
                        archive_time=archive_thread.archive_time, last_update_time=None
                    ),
                )
            )
