from hashlib import md5, sha256
from uuid import uuid4

from .android_id import generate_android_id
from .imei import generate_taf_imei


def generate_cuid():
    imei = generate_taf_imei()
    android_id_sha256 = sha256(generate_android_id().encode("utf-8")).hexdigest()
    cuid = imei + android_id_sha256 + str(uuid4())
    cuid = md5(cuid.encode("utf-8")).hexdigest()
    return f"{cuid}|{imei[::-1]}"  # cuid + reversed imei
