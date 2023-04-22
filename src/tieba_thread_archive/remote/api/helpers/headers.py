import random

from .constants import APP_MAIN_VERSION

__all__ = (
    "WEB_USER_AGENTS",
    "MOBILE_USER_AGENTS",
    "web_headers",
    "mobile_headers",
    "mobile_protobuf_headers",
    "mobile_url_encoded_headers",
)

WEB_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
]
MOBILE_USER_AGENTS = [
    f"Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.0.0 Mobile Safari/537.36 tieba/{APP_MAIN_VERSION}",
    f"bdtb for Android {APP_MAIN_VERSION}",
    "okhttp/3.10.10",
]


def web_headers():
    return {"User-Agent": random.choice(WEB_USER_AGENTS)}


def mobile_headers():
    return {"User-Agent": random.choice(MOBILE_USER_AGENTS)}


def mobile_protobuf_headers():
    return {"x_bd_data_type": "protobuf"}


def mobile_url_encoded_headers():
    return {"Content-Type": "application/x-www-form-urlencoded"}
