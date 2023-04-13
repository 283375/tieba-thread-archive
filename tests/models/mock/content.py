import random
import secrets
import uuid
from hashlib import md5
from typing import List, Optional, Type

from src.tieba_thread_archive.models import User
from src.tieba_thread_archive.models.content import *

from .user import MockUser

__all__ = (
    "MockContentBase",
    "MockContentText",
    "MockContentLink",
    "MockContentEmoticon",
    "MockContentImage",
    "MockContentAt",
    "MockContentVideo",
    "MockContentPhoneNumber",
    "MockContentAudio",
    "MockContentTopic",
    "MockContents",
)


class MockContentBase:
    @staticmethod
    def mock() -> ContentBase:
        raise NotImplementedError()


class MockContentText(MockContentBase):
    @staticmethod
    def mock():
        return ContentText(text=secrets.token_hex(random.randint(8, 32)))


class MockContentLink(MockContentBase):
    @staticmethod
    def mock():
        return ContentLink(text="tieba", link="https://tieba.baidu.com")


class MockContentEmoticon(MockContentBase):
    @staticmethod
    def mock():
        return ContentEmoticon(text="image_emoticon25", c="滑稽")


class MockContentImage(MockContentBase):
    @staticmethod
    def mock():
        return ContentImage(
            origin_size=8493,
            origin_src="https://tb2.bdstatic.com/tb/static-common/img/search_logo_big_v2_d84d082.png",
            filename=f"{str(uuid.uuid4())}.jpg",
        )


class MockContentAt(MockContentBase):
    @staticmethod
    def mock(user: Optional[User] = None):
        user = user or MockUser.mock()
        return ContentAt(text=f"@{user.name_show}", uid=user.id)


class MockContentVideo(MockContentBase):
    @staticmethod
    def mock():
        random_secret = secrets.token_urlsafe(5)
        return ContentVideo(
            text=f"摸了{random_secret}",
            filename=f"摸了{random_secret}.mp4",
            link=f"https://www.baidu.com/s?ie=UTF-8&wd=摸了{random_secret}.mp4",
            src=f"https://www.baidu.com/s?ie=UTF-8&wd=摸了{random_secret}",
            bsize=(1080, 1920),
            origin_size=233333,
        )


class MockContentPhoneNumber(MockContentBase):
    @staticmethod
    def mock(phone_number: Optional[str] = None):
        phone_number = phone_number or (
            str(
                random.choice(
                    [
                        random.randint(130, 139),
                        random.randint(150, 159),
                        random.randint(170, 178),
                        random.randint(180, 189),
                        192,  # random.randint(190, 199)
                    ]
                )
            )
            + str(random.randint(0, 9999)).rjust(4, "0")
            + str(random.randint(0, 9999)).rjust(4, "0")
        )
        return ContentPhoneNumber(text=phone_number)


class MockContentAudio(MockContentBase):
    @staticmethod
    def mock():
        mock_md5 = md5(secrets.token_urlsafe(16).encode("utf-8")).hexdigest()
        random_stamp = str(random.randint(1000000000, 2000000000))
        return ContentAudio(voice_md5=f"{mock_md5}_{random_stamp}")


class MockContentTopic(MockContentBase):
    @staticmethod
    def mock(topic_name: Optional[str] = None):
        topic_name = topic_name or secrets.token_urlsafe(5)
        return ContentTopic(
            text=topic_name,
            link=f"http://tieba.baidu.com/mo/q/hotMessage?topic_id=0&topic_name={topic_name}&is_video_topic=0",
        )


class MockContents:
    @staticmethod
    def mock(*, subpost_contents: bool = False):
        possible_contents: List[Type[MockContentBase]]
        if subpost_contents:
            possible_contents = [
                MockContentText,
                MockContentLink,
                MockContentEmoticon,
                MockContentAt,
                MockContentAudio,
            ]
            contents_weights = [
                70,
                3,
                20,
                6,
                1,
            ]
        else:
            possible_contents = [
                MockContentText,
                MockContentLink,
                MockContentEmoticon,
                MockContentImage,
                MockContentAt,
                MockContentPhoneNumber,
                MockContentAudio,
                MockContentTopic,
            ]
            contents_weights = [
                60,
                5,
                20,
                5,
                5,
                1,
                4,
                1,
            ]

        content_classes = random.choices(
            possible_contents,
            weights=contents_weights,
            k=random.randint(1, 10),
        )
        content_classes = [cls.mock() for cls in content_classes]

        return Contents(content_classes)
