import fnmatch
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import List, Optional, Set, Union

import yaml

from ....models import *
from .dump import *
from .file_structure import *
from .load import *
from .validate import *

__all__ = ("AV3LocalArchive",)


class AV3LocalArchive:
    __slots__ = (
        "__path",
        "__history",
        "archive_options",
        "archive_update_info",
        "archive_thread",
        "images",
        "audios",
        "videos",
    )

    __path: Path
    __history: List[ArchiveThread]

    archive_options: Optional[ArchiveOptions]
    archive_update_info: Optional[ArchiveUpdateInfo]

    archive_thread: Optional[ArchiveThread]

    images: Set[ContentImage]
    audios: Set[ContentAudio]
    videos: Set[ContentVideo]

    def __init__(self, path: Union[str, PathLike]):
        self.__path = Path(path)

        if not self.__path.exists():
            raise ValueError(f"Passing in an invalid path {self.__path}.")
        if (
            self.__path.exists()
            and list(self.__path.iterdir())
            and not av3_validate_path(self.__path)
        ):
            raise ValueError(f"{path} is not empty and is not a valid archive.")

        self.__history = []
        self.archive_options = None
        self.archive_update_info = None

        self.archive_thread = None

        self.images = set()
        self.audios = set()
        self.videos = set()

        self.load()

    @property
    def path(self):
        return self.__path

    @property
    def history_dir(self):
        return self.path / ".history"

    @property
    def info_file(self):
        return self.path / "info.yaml"

    @property
    def thread_file(self):
        return self.path / "thread.yaml"

    @property
    def assets_file(self):
        return self.path / "assets.yaml"

    @property
    def history(self):
        return self.__history

    def set_archive_options(self, archive_options: ArchiveOptions):
        self.archive_options = archive_options

    def __load_history(self):
        if not (self.history_dir.exists() and self.history_dir.is_dir()):
            # TODO: warning
            return

        files = self.history_dir.iterdir()
        existing_history_times = [
            archive_history.archive_time for archive_history in self.history
        ]

        for file in files:
            if fnmatch.fnmatch(file.name, "*.yaml"):
                with open(file, "r", encoding="utf-8") as history_rs:
                    archive_history = av3_load_thread_yaml(
                        yaml.safe_load(history_rs.read())
                    )

                    if archive_history.archive_time in existing_history_times:
                        continue
                    else:
                        self.__history.append(archive_history)

    def __dump_history(self):
        if not self.history:
            return

        self.history_dir.mkdir(exist_ok=True)

        existing_files = [path.name for path in self.history_dir.iterdir()]

        for history in self.history:
            filepath = self.history_dir / (
                datetime.fromtimestamp(history.archive_time).strftime(
                    "%Y-%m-%d_%H-%M-%S"
                )
                + ".yaml"
            )

            if filepath.name in existing_files:
                continue

            with open(filepath, "w", encoding="utf-8") as history_ws:
                history_ws.write(av3_get_thread_yaml_dump_str(archive_thread=history))

    def __load_info(self):
        with open(self.info_file, "r", encoding="utf-8") as info_rs:
            _, archive_options, archive_update_info = av3_load_info_yaml(
                yaml.safe_load(info_rs.read())
            )

            self.archive_options = archive_options
            self.archive_update_info = archive_update_info

    def __dump_info(self):
        if self.archive_thread and self.archive_options and self.archive_update_info:
            with open(self.info_file, "w", encoding="utf-8") as info_ws:
                info_ws.write(
                    av3_get_info_yaml_dump_str(
                        thread_info=self.archive_thread.thread_info,
                        archive_options=self.archive_options,
                        archive_update_info=self.archive_update_info,
                    )
                )
        else:
            raise ValueError(
                "Missing required values, probably archive not loaded properly."
            )

    def __load_archive_thread(self):
        with open(self.path / "thread.yaml", "r", encoding="utf-8") as thread_rs:
            archive_thread = av3_load_thread_yaml(yaml.safe_load(thread_rs.read()))

            if (
                self.archive_thread
                and self.archive_thread.archive_time == archive_thread.archive_time
                and self.archive_thread.thread_info.id == archive_thread.thread_info.id
            ):
                return

            self.archive_thread = archive_thread

    def __dump_archive_thread(self):
        if self.archive_thread:
            with open(self.path / "thread.yaml", "w", encoding="utf-8") as thread_ws:
                thread_ws.write(
                    av3_get_thread_yaml_dump_str(archive_thread=self.archive_thread)
                )
        else:
            raise ValueError(
                "Missing required values, probably archive not loaded properly."
            )

    def __load_assets(self):
        with open(self.assets_file, "r", encoding="utf-8") as assets_rs:
            assets = av3_load_assets_yaml(yaml.safe_load(assets_rs.read()))

            self.images = assets["images"]
            self.audios = assets["audios"]
            self.videos = assets["videos"]

    def __dump_assets(self):
        with open(self.assets_file, "w", encoding="utf-8") as assets_ws:
            assets_ws.write(
                av3_get_assets_yaml_dump_str(
                    images=self.images, audios=self.audios, videos=self.videos
                )
            )

    def load(self):
        self.__load_history()
        self.__load_info()
        self.__load_archive_thread()
        self.__load_assets()

        # TODO:
        # if info.id != archive_thread.id, warning?

    def dump(self):
        self.__dump_history()
        self.__dump_info()
        self.__dump_archive_thread()
        self.__dump_assets()

    def update_archive_thread(self, archive_thread: ArchiveThread):
        # sourcery skip: extract-method
        if self.archive_thread is None:
            self.archive_thread = archive_thread
            self.images = archive_thread.images()
            self.audios = archive_thread.audios()
            self.videos = archive_thread.videos()

            self.archive_update_info = ArchiveUpdateInfo(
                archive_time=archive_thread.archive_time, last_update_time=None
            )
        else:
            self.__history.append(self.archive_thread)

            self.archive_thread.update(archive_thread)
            self.images = archive_thread.images() | self.images
            self.audios = archive_thread.audios() | self.audios
            self.videos = archive_thread.videos() | self.videos

            if self.archive_update_info is None:
                raise ValueError("TODO: this should not happen")

            self.archive_update_info.last_update_time = archive_thread.archive_time
