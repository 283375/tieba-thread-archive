from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import List, Optional, Set, Union

from ...models.archive import (
    ArchiveOptions,
    ArchiveThread,
    ArchiveUpdateInfo,
    ThreadInfo,
)
from ...models.content import ContentAudio, ContentImage, ContentVideo
from ...models.progress import Progress


class LocalArchive:
    __slots__ = (
        "_path",
        "_loaded",
        "_history",
        "_history_loaded",
        "_update_progress",
        "_thread_info",
        "_archive_options",
        "_archive_update_info",
        "_archive_thread",
        "_images",
        "_audios",
        "_videos",
    )

    _path: Path
    _loaded: bool
    _history: List[ArchiveThread]
    _history_loaded: bool
    _update_progress: Progress
    _thread_info: Optional[ThreadInfo]
    _archive_options: Optional[ArchiveOptions]
    _archive_update_info: Optional[ArchiveUpdateInfo]
    _archive_thread: Optional[ArchiveThread]
    _images: Set[ContentImage]
    _audios: Set[ContentAudio]
    _videos: Set[ContentVideo]

    @property
    def path(self):
        return self._path

    @property
    def loaded(self):
        return self._loaded

    @property
    def history(self):
        return deepcopy(self._history)

    @property
    def history_loaded(self):
        return self._history_loaded

    @property
    def update_progress(self):
        return self._update_progress

    @property
    def thread_info(self):
        return self._thread_info

    @property
    def archive_options(self):
        return self._archive_options

    @property
    def archive_update_info(self):
        return self._archive_update_info

    @property
    def archive_thread(self):
        return self._archive_thread

    @property
    def images(self):
        return self._images

    @property
    def audios(self):
        return self._audios

    @property
    def videos(self):
        return self._videos

    def __init__(
        self,
        path: Union[str, PathLike],
        *,
        auto_load: bool = True,
        auto_load_info: bool = True,
        auto_load_history: bool = False,
    ):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")

    def set_archive_options(self, new_archive_options: ArchiveOptions):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")

    def dump(self):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")

    def load(self):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")

    def load_info(self):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")

    def load_history(self):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")

    def update(self, new_archive_thread: ArchiveThread):
        raise NotImplementedError("LocalArchive is not meant to be used directly.")
