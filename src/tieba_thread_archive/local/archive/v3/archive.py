import fnmatch
from concurrent import futures
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import List, Optional, Set, Tuple, Union

import requests
import yaml

from ....models import *
from ....models.progress import Progress
from .dump import *
from .file_structure import *
from .load import *
from .validate import *

__all__ = ("AV3LocalArchive",)


class AV3LocalArchive:
    __slots__ = (
        "__assets_progress",
        "__path",
        "__history",
        "archive_options",
        "archive_update_info",
        "archive_thread",
        "images",
        "audios",
        "videos",
    )

    __assets_progress: Progress

    __path: Path
    __history: List[ArchiveThread]

    archive_options: Optional[ArchiveOptions]
    archive_update_info: Optional[ArchiveUpdateInfo]

    archive_thread: Optional[ArchiveThread]

    images: Set[ContentImage]
    audios: Set[ContentAudio]
    videos: Set[ContentVideo]

    def __init__(self, path: Union[str, PathLike]):
        self.__assets_progress = Progress()

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

        if av3_validate_path(self.__path):
            self.load()

    @property
    def assets_progress(self):
        return self.__assets_progress

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
    def images_dir(self):
        return self.path / "images"

    @property
    def audios_dir(self):
        return self.path / "audios"

    @property
    def videos_dir(self):
        return self.path / "videos"

    @property
    def portraits_dir(self):
        return self.path / "portraits"

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
                history_ws.write(av3_dump_thread_yaml_str(archive_thread=history))

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
                    av3_dump_info_yaml_str(
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
                    av3_dump_thread_yaml_str(archive_thread=self.archive_thread)
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
                av3_dump_assets_yaml_str(
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

    def update_archive_thread(self, new_archive_thread: ArchiveThread):
        # sourcery skip: extract-method
        if self.archive_thread is None:
            self.archive_thread = new_archive_thread
            self.images = new_archive_thread.images()
            self.audios = new_archive_thread.audios()
            self.videos = new_archive_thread.videos()

            self.archive_update_info = ArchiveUpdateInfo(
                archive_time=new_archive_thread.archive_time, last_update_time=None
            )
        else:
            if self.archive_thread == new_archive_thread:
                # TODO: log
                return

            self.__history.append(self.archive_thread)

            self.archive_thread.update(new_archive_thread)
            self.images = new_archive_thread.images() | self.images
            self.audios = new_archive_thread.audios() | self.audios
            self.videos = new_archive_thread.videos() | self.videos

            if self.archive_update_info is None:
                raise ValueError("TODO: this should not happen")

            self.archive_update_info.last_update_time = new_archive_thread.archive_time

    def __executor_task_get_task_tuple(
        self, session: requests.Session, content: ContentBase
    ) -> Tuple[requests.Session, requests.PreparedRequest, Path]:
        if isinstance(content, ContentImage):
            task_tuple = (
                session,
                requests.Request("GET", content.origin_src).prepare(),
                self.images_dir / content.filename,
            )
        elif isinstance(content, ContentAudio):
            task_tuple = (
                session,
                requests.Request("GET", content.src).prepare(),
                self.audios_dir / content.filename,
            )
        elif isinstance(content, ContentVideo):
            assert content.filename is not None

            task_tuple = (
                session,
                requests.Request("GET", content.link).prepare(),
                self.videos_dir / content.filename,
            )
        else:
            raise NotImplementedError(
                f"{content.__class__.__name__} not supported yet."
            )

        return task_tuple

    def __executor_task_download_asset(
        self,
        session: requests.Session,
        prepared_request: requests.PreparedRequest,
        filepath: Path,
        overwrite: bool,
    ):
        if filepath.exists() and not overwrite:
            return

        response = session.send(prepared_request)

        filepath.parent.mkdir(exist_ok=True)
        with open(filepath, "wb") as file_ws:
            file_ws.write(response.content)

    def download_assets(self, overwrite_exist=False):
        with requests.Session() as session:
            with futures.ThreadPoolExecutor() as executor:
                self.__assets_progress.reset()

                tasks = (
                    [
                        self.__executor_task_get_task_tuple(session, image)
                        for image in self.images
                    ]
                    + [
                        self.__executor_task_get_task_tuple(session, audio)
                        for audio in self.audios
                    ]
                    + [
                        self.__executor_task_get_task_tuple(session, video)
                        for video in self.videos
                        if video.link is not None
                    ]
                )

                self.__assets_progress.total_progress = len(tasks)

                executor_tasks = [
                    executor.submit(
                        self.__executor_task_download_asset, *task, overwrite_exist
                    )
                    for task in tasks
                ]

                for _ in futures.as_completed(executor_tasks):
                    self.__assets_progress += 1
