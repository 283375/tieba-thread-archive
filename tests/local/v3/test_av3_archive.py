import os
import pickle
import shutil
from pathlib import Path

import pytest

from src.tieba_thread_archive.local.archive.v3 import AV3LocalArchive
from src.tieba_thread_archive.models import ArchiveOptions
from tests.models.mock import MockArchiveThread

# archive_thread_1 = MockArchiveThread.slice(archive_thread, 1, 3)
# archive_thread_2 = MockArchiveThread.slice(archive_thread, 2, 6)


class Test_AV3LocalArchive_CleanDir_FileSensitive:
    archives_root_path = Path("__debug_tests") / "av3_local_archive"

    @pytest.mark.order(1)
    def test_ensure_clean_dir(self):
        if not self.archives_root_path.exists():
            self.archives_root_path.mkdir(parents=True, exist_ok=True)
        else:
            for item in self.archives_root_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(str(item))
                else:
                    os.unlink(item)

    def test_archive_load_integrity(self):
        archive_thread = MockArchiveThread.mock(post_num=5)

        archive_path = self.archives_root_path / str(archive_thread.thread_info.id)
        archive_path.mkdir(exist_ok=True)
        local_archive = AV3LocalArchive(archive_path)
        local_archive.set_archive_options(
            ArchiveOptions(images=False, audios=False, videos=False, portraits=False)
        )
        local_archive.update(archive_thread)

        with open(
            archive_path / f"archive_thread_{archive_thread.thread_info.id}.pickle",
            "wb",
        ) as pickle_ws:
            pickle.dump(archive_thread, pickle_ws)

        local_archive.dump()

        del local_archive

        local_archive_load = AV3LocalArchive(archive_path, auto_load=True)

        assert local_archive_load.archive_thread == archive_thread

    def test_archive_repeat_dump(self):
        archive_thread = MockArchiveThread.mock(post_num=5)

        archive_path = (
            self.archives_root_path / f"repeat_{archive_thread.thread_info.id}"
        )
        archive_path.mkdir(exist_ok=True)
        local_archive = AV3LocalArchive(archive_path)
        local_archive.set_archive_options(
            ArchiveOptions(images=False, audios=False, videos=False, portraits=False)
        )
        local_archive.update(archive_thread)

        with open(
            archive_path / f"archive_thread_{archive_thread.thread_info.id}.pickle",
            "wb",
        ) as pickle_ws:
            pickle.dump(archive_thread, pickle_ws)

        for _ in range(5):
            local_archive.update(archive_thread)
            local_archive.dump()

        del local_archive

        local_archive_load = AV3LocalArchive(archive_path, auto_load=True)

        assert local_archive_load.archive_thread == archive_thread
        assert len(local_archive_load.history) == 0
