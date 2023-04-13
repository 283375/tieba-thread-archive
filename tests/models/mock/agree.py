import random

from src.tieba_thread_archive.models.agree import Agree

__all__ = ("MockAgree",)


class MockAgree:
    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def mock(
        *,
        agree_num: int = random.randint(0, 100),
        disagree_num: int = random.randint(0, 100),
    ):
        return Agree(agree_num=agree_num, disagree_num=disagree_num)
