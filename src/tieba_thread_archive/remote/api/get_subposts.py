import concurrent.futures
from functools import reduce
from math import ceil
from typing import Iterable, List

import requests

from .base import get_comments

__all__ = ("get_requests", "call", "parse_responses")


def get_requests(
    tid: int, pid: int, /, *, is_floor: bool = False
) -> List[requests.Request]:
    preload = get_comments.RESPONSE_PROTOBUF.FromString(
        get_comments.call(tid, pid).content
    )
    data = preload.data
    post_num = data.page.page_size * data.page.total_page
    page_size = 30
    pages = range(1, ceil(post_num / page_size) + 1)

    return [
        get_comments.get_request(
            tid,
            pid,
            pn=page,
            is_floor=is_floor,
        )
        for page in pages
    ]


def call(tid: int, pid: int, /, *, is_floor: bool = False):
    prepared_req = [req.prepare() for req in get_requests(tid, pid, is_floor=is_floor)]

    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            processes = [executor.submit(session.send, req) for req in prepared_req]
            results = [
                future.result() for future in concurrent.futures.as_completed(processes)
            ]

    return results


def parse_responses(responses: Iterable[requests.Response]):
    subposts = [get_comments.parse_response(response) for response in responses]
    return reduce(lambda s1, s2: s1 + s2, subposts)
