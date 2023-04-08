import random
import secrets
from hashlib import md5
from typing import Optional

from src.tieba_thread_archive.models import User
from src.tieba_thread_archive.models.content import *

from .user import MockUser


class MockContentText(ContentText):
    def __init__(self):
        super().__init__(text=secrets.token_hex(random.randint(8, 32)))


class MockContentLink(ContentLink):
    def __init__(self):
        super().__init__(text="tieba", link="https://tieba.baidu.com")


class MockContentEmoticon(ContentEmoticon):
    def __init__(self):
        super().__init__(text="image_emoticon25", c="滑稽")


class MockContentImage(ContentImage):
    def __init__(self):
        super().__init__(
            origin_size=8493,
            origin_src="https://tb2.bdstatic.com/tb/static-common/img/search_logo_big_v2_d84d082.png",
            filename="233e0aed08fa513db9ffab14786d55fbb0fbd9d3.jpg",
        )


class MockContentAt(ContentAt):
    def __init__(self, user: Optional[User] = None):
        user = user or MockUser()
        super().__init__(text=f"@{user.name_show}", uid=user.id)


class MockContentVideo(ContentVideo):
    def __init__(self):
        random_secret = secrets.token_urlsafe(5)
        super().__init__(
            text=f"摸了{random_secret}",
            filename=f"摸了{random_secret}.mp4",
            link=f"https://www.baidu.com/s?ie=UTF-8&wd=摸了{random_secret}.mp4",
            src=f"https://www.baidu.com/s?ie=UTF-8&wd=摸了{random_secret}",
            bsize=(1080, 1920),
            origin_size=233333,
        )


class MockContentPhoneNumber(ContentPhoneNumber):
    def __init__(self):
        phone_number = (
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
        super().__init__(text=phone_number)


class MockContentAudio(ContentAudio):
    def __init__(self):
        mock_md5 = md5(secrets.token_urlsafe(16).encode("utf-8")).hexdigest()
        random_stamp = str(random.randint(1000000000, 2000000000))
        super().__init__(voice_md5=f"{mock_md5}_{random_stamp}")


class MockContentTopic(ContentTopic):
    def __init__(self):
        topic_name = secrets.token_urlsafe(5)
        super().__init__(
            text=topic_name,
            link=f"http://tieba.baidu.com/mo/q/hotMessage?topic_id=0&topic_name={topic_name}&is_video_topic=0",
        )


class MockContents(Contents):
    def __init__(self):
        content_classes = random.choices(
            [
                MockContentText,
                MockContentLink,
                MockContentEmoticon,
                MockContentImage,
                MockContentAt,
                MockContentPhoneNumber,
                MockContentAudio,
                MockContentTopic,
            ],
            weights=[
                60,
                5,
                20,
                5,
                5,
                1,
                4,
                1,
            ],
            k=random.randint(1, 10),
        )
        content_classes = [cls() for cls in content_classes]

        super().__init__(content_classes)
