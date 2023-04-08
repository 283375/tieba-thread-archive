import random

from src.tieba_thread_archive.models.agree import Agree


class MockAgree(Agree):
    def __init__(self):
        super().__init__(
            agree_num=random.randint(0, 100), disagree_num=random.randint(0, 100)
        )
