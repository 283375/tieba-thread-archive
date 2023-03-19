from .android_id import *
from .cuid import *
from .imei import *


def truncate_text(text: str, length: int):
    return text[:length] + ("…" if len(text) > length else "")
