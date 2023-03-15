from typing import Any, Callable, Dict, ParamSpec

import requests
from google.protobuf.message import Message

from .headers import mobile_headers, mobile_protobuf_headers, mobile_url_encoded_headers
from .pack import *

P = ParamSpec("P")

THeaders = Dict[str, str]


# region mobile_protobuf


def mobile_protobuf_request(
    method: str,
    url: str,
    protobuf_builder: Callable[P, Message],
    headers: THeaders = {},
) -> Callable[P, requests.Request]:
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        return requests.Request(
            method=method,
            url=url,
            headers={
                **mobile_headers(),
                **mobile_protobuf_headers(),
                **(headers or {}),
            },
            files=pack_mobile_protobuf_data(protobuf_builder(*args, **kwargs)),
        )

    return wrapper


def mobile_protobuf_call(
    proto_request: Callable[P, requests.Request]
) -> Callable[P, requests.Response]:
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        return requests.Session().send(proto_request(*args, **kwargs).prepare())

    return wrapper


# endregion


# region mobile_url_encoded


def mobile_url_encoded_request(
    method: str,
    url: str,
    form: Callable[P, Dict[str, Any]],
    headers: THeaders = {},
) -> Callable[P, requests.Request]:
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        return requests.Request(
            method=method,
            url=url,
            headers={
                **mobile_headers(),
                **mobile_url_encoded_headers(),
                **(headers or {}),
            },
            params=pack_mobile_url_encoded_data(form(*args, **kwargs)),
        )

    return wrapper


def mobile_url_encoded_call(
    form_request: Callable[P, requests.Request]
) -> Callable[P, requests.Response]:
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        return requests.Session().send(form_request(*args, **kwargs).prepare())

    return wrapper


# endregion
