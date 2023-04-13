import fnmatch
from concurrent import futures
from copy import deepcopy
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import List, Optional, Set, Tuple, Union

import requests
import yaml

from ....models import *
from ....models.progress import Progress
from ..archive import LocalArchive
from .dump import *
from .file_structure import *
from .load import *
from .validate import *

__all__ = ("AV3LocalArchive",)


class AV3LocalArchive(LocalArchive):
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

    def __init__(
        self,
        path: Union[str, PathLike],
        *,
        auto_load: bool = True,
        auto_load_history: bool = False,
    ):
        self._update_progress = Progress()

        self._path = Path(path)

        if not self._path.exists():
            raise ValueError(f"Passing in an invalid path {self._path}.")
        if (
            self._path.exists()
            and list(self._path.iterdir())
            and not av3_validate_path(self._path)
        ):
            raise ValueError(f"{path} is not empty and is not a valid archive.")

        self._history = []
        self._archive_options = None
        self._archive_update_info = None

        self._archive_thread = None

        self._images = set()
        self._audios = set()
        self._videos = set()

        if av3_validate_path(self._path):
            if auto_load:
                self.load()
            if auto_load_history:
                self.load_history()

    def set_archive_options(self, new_archive_options):
        self._archive_options = new_archive_options

    def load_history(self):
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
                        self._history.append(archive_history)

        self._history_loaded = True

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

            self._archive_options = archive_options
            self._archive_update_info = archive_update_info

    def __dump_info(self):
        if not isinstance(self._archive_options, ArchiveOptions):
            raise ValueError("archive_options not set.")

        if self._archive_thread and self._archive_update_info:
            with open(self.info_file, "w", encoding="utf-8") as info_ws:
                info_ws.write(
                    av3_dump_info_yaml_str(
                        thread_info=self._archive_thread.thread_info,
                        archive_options=self._archive_options,
                        archive_update_info=self._archive_update_info,
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
                self._archive_thread
                and self._archive_thread.archive_time == archive_thread.archive_time
                and self._archive_thread.thread_info.id == archive_thread.thread_info.id
            ):
                return

            self._archive_thread = archive_thread

    def __dump_archive_thread(self):
        if self._archive_thread:
            with open(self.path / "thread.yaml", "w", encoding="utf-8") as thread_ws:
                thread_ws.write(
                    av3_dump_thread_yaml_str(archive_thread=self._archive_thread)
                )
        else:
            raise ValueError(
                "Missing required values, probably archive not loaded properly."
            )

    def __load_assets(self):
        with open(self.assets_file, "r", encoding="utf-8") as assets_rs:
            assets = av3_load_assets_yaml(yaml.safe_load(assets_rs.read()))

            self._images = assets["images"]
            self._audios = assets["audios"]
            self._videos = assets["videos"]

    def __dump_assets(self):
        with open(self.assets_file, "w", encoding="utf-8") as assets_ws:
            assets_ws.write(
                av3_dump_assets_yaml_str(
                    images=self._images, audios=self._audios, videos=self._videos
                )
            )

    def load(self):
        self.__load_info()
        self.__load_archive_thread()
        self.__load_assets()
        self._loaded = True

        # TODO:
        # if info.id != archive_thread.id, warning?

    def dump(self):
        self.__dump_history()
        self.__dump_info()
        self.__dump_archive_thread()
        self.__dump_assets()

    def update(self, new_archive_thread):
        # sourcery skip: extract-method
        if self._archive_thread is None:
            self._archive_thread = new_archive_thread
            self._images = new_archive_thread.images()
            self._audios = new_archive_thread.audios()
            self._videos = new_archive_thread.videos()

            self._archive_update_info = ArchiveUpdateInfo(
                archive_time=new_archive_thread.archive_time, last_update_time=None
            )
        else:
            if self._archive_thread == new_archive_thread:
                # TODO: log
                return

            self._history.append(deepcopy(self._archive_thread))

            self._archive_thread.update(new_archive_thread)
            self._images = new_archive_thread.images() | self._images
            self._audios = new_archive_thread.audios() | self._audios
            self._videos = new_archive_thread.videos() | self._videos

            if self._archive_update_info is None:
                raise ValueError("TODO: this should not happen")

            self._archive_update_info.last_update_time = new_archive_thread.archive_time

    def __executor_task_get_tasks(
        self, session: requests.Session
    ) -> List[Tuple[requests.Session, requests.PreparedRequest, Path]]:
        if self._archive_options is None:
            raise ValueError("Need archive_options before downloading assets.")

        tasks = []

        if self._archive_options.images and self._images:
            tasks.extend(
                (
                    session,
                    requests.Request("GET", image.origin_src).prepare(),
                    self.images_dir / image.filename,
                )
                for image in self._images
            )
        if self._archive_options.audios and self._audios:
            tasks.extend(
                (
                    session,
                    requests.Request("GET", audio.src).prepare(),
                    self.audios_dir / audio.filename,
                )
                for audio in self._audios
            )
        if self._archive_options.videos and self._videos:
            tasks.extend(
                (
                    session,
                    requests.Request("GET", video.link).prepare(),
                    self.videos_dir / video.filename,
                )
                for video in self._videos
                if video.link and video.filename
            )
        if (
            self._archive_options.portraits
            and self._archive_thread is not None
            and self._archive_thread.users
        ):
            tasks.extend(
                (
                    session,
                    requests.Request(
                        "GET",
                        f"http://himg.bdimg.com/sys/portraith/item/{user.portrait}",
                    ).prepare(),
                    self.portraits_dir / f"{user.id}.jpg",
                )
                for user in self._archive_thread.users
            )

        return tasks

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
            tasks = self.__executor_task_get_tasks(session)
            if tasks:
                with futures.ThreadPoolExecutor() as executor:
                    self._update_progress.reset()
                    self._update_progress.total_progress = len(tasks)

                    executor_tasks = [
                        executor.submit(
                            self.__executor_task_download_asset, *task, overwrite_exist
                        )
                        for task in tasks
                    ]

                    for _ in futures.as_completed(executor_tasks):
                        self._update_progress += 1
