import json
from concurrent import futures
from functools import wraps
from os import PathLike
from pathlib import Path
from typing import Callable, Set, Tuple, Union

import requests

from ....models import *
from ....models.progress import Progress
from ..archive import LocalArchive
from .file_structure import *
from .load import *
from .validate import *

__all__ = ("AV2LocalArchive",)


def v2_absense(func: Callable):
    @wraps(func)
    def _(self, *args, **kwargs):
        raise NotImplementedError(
            f"{func.__name__} is not supported in archive version 2"
        )

    return _


class AV2LocalArchive(LocalArchive):
    __slots__ = ("__users",)

    __users: Union[Set[User], None]

    @property
    def history_dir(self):
        return self.path / "origData"

    @property
    def info_file(self):
        return self.path / "threadInfo.json"

    @property
    def posts_file(self):
        return self.path / "posts.json"

    @property
    def users_file(self):
        return self.path / "users.json"

    @property
    def images_dir(self):
        return self.path / "assets" / "images"

    @property
    def audios_dir(self):
        return self.path / "assets" / "audios"

    @property
    def videos_dir(self):
        return self.path / "assets" / "videos"

    @property
    def portraits_dir(self):
        return self.path / "portraits"

    @property
    def assets_file(self):
        return self.path / "assets.json"

    def __init__(
        self,
        path: Union[str, PathLike],
        *,
        auto_load: bool = True,
        auto_load_info: bool = True,
        auto_load_history: bool = False,
    ):
        self._update_progress = Progress()

        self._path = Path(path)

        if not self._path.exists():
            raise ValueError(f"Passing in an invalid path {self._path}.")
        if (
            self._path.exists()
            and list(self._path.iterdir())
            and not av2_validate_path(self._path)
        ):
            raise ValueError(f"{path} is not empty and is not a valid archive.")

        self._history = []
        self._archive_options = None
        self._archive_update_info = None

        self._archive_thread = None

        self._images = set()
        self._audios = set()
        self._videos = set()

        if av2_validate_path(self._path) and auto_load:
            self.load()
        if not self._loaded and auto_load_info:
            self.load_info()

    @v2_absense
    def set_archive_options(self, new_archive_options):
        pass

    @v2_absense
    def load_history(self):
        pass

    def load_info(self):
        if not self.__users:
            self.__load_users()

        assert self.__users is not None

        with open(self.info_file, "r", encoding="utf-8") as info_rs:
            (
                thread_info,
                archive_options,
                archive_update_info,
            ) = av2_load_threadInfo_json(json.loads(info_rs.read()), self.__users)
        self._thread_info = thread_info
        self._archive_options = archive_options
        self._archive_update_info = archive_update_info

    def __load_users(self):
        with open(self.users_file, "r", encoding="utf-8") as users_rs:
            self.__users = av2_load_users_json(json.loads(users_rs.read()))

    def __load_archive_thread(self):
        if not self.__users:
            self.__load_users()

        if not self._thread_info or not self._archive_update_info:
            self.load_info()

        assert self.__users is not None
        assert self._thread_info is not None
        assert self._archive_update_info is not None

        with open(self.posts_file, "r", encoding="utf-8") as posts_rs:
            posts, dict_subposts = av2_load_posts_json(
                json.loads(posts_rs.read()), self.__users
            )

        self._archive_thread = ArchiveThread(
            archive_time=self._archive_update_info.archive_time,
            thread_info=self._thread_info,
            posts=posts,
            dict_subposts=dict_subposts,
            users=self.__users,
        )

    def __load_assets(self):
        with open(self.assets_file, "r", encoding="utf-8") as assets_rs:
            assets = av2_load_assets_json(json.loads(assets_rs.read()))

            self._images = assets["images"]
            self._audios = assets["audios"]
            self._videos = assets["videos"]

    def load(self):
        self.__load_users()
        self.load_info()
        self.__load_archive_thread()
        self.__load_assets()
        self._loaded = True

        # TODO:
        # if info.id != archive_thread.id, warning?

    @v2_absense
    def dump(self, with_assets):
        pass

    @v2_absense
    def update(self, new_archive_thread):
        pass

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
