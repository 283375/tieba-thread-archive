import random
import string

from src.tieba_thread_archive.models.user import User

from .common import mock_timestamp

__all__ = ("MockUser",)


class MockUser:
    @classmethod
    def mock(cls):
        name = cls.mock_username()
        name_show = random.choice([cls.mock_username(), name])
        is_bawu = random.choices([True, False], cum_weights=[0.05, 0.95])[0]

        return User(
            id=random.randint(1000000, 2833333375),
            name=name,
            name_show=name_show,
            portrait=cls.mock_portrait(),
            level_id=random.randint(1, 16),
            is_bawu=is_bawu,
            bawu_type=random.choices(["other", "manager"], cum_weights=[0.9, 0.1])[0]
            if is_bawu
            else "",
            ip_address="",
        )

    @staticmethod
    def mock_username():
        return "".join(
            random.choices(
                string.digits + string.ascii_letters, k=random.randint(8, 16)
            )
        )

    @staticmethod
    def mock_portrait():
        # sourcery skip: use-fstring-for-concatenation
        return (
            "tb.1."
            + "".join(random.choices(string.digits + "abcdef", k=8))
            + "."
            + "".join(random.choices(string.digits + string.ascii_letters + "_-", k=22))
            + f"?t={mock_timestamp()}"
        )
