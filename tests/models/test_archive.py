import pytest

from tests.models.mock import MockArchiveThread


class Test_ArchiveThread:
    @pytest.mark.repeat(5)
    def test_update(self):
        archive_thread = MockArchiveThread.mock(post_num=10)

        archive_thread_1 = MockArchiveThread.slice(archive_thread, 1, 4)
        archive_thread_2 = MockArchiveThread.slice(archive_thread, 2, 6)
        archive_thread_3 = MockArchiveThread.slice(archive_thread, 6, 10)

        final_updated_thread = archive_thread_1.update(archive_thread_2).update(
            archive_thread_3
        )

        assert final_updated_thread == archive_thread
