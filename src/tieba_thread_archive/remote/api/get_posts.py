import concurrent.futures
from functools import reduce
from math import ceil
from typing import Iterable, List

import requests

from .base import get_posts as base_get_posts

__all__ = ("get_requests", "call", "parse_responses")


def get_requests(
    tid: int,
    /,
    *,
    sort: int = 0,
    only_thread_author: bool = False,
    with_comments: bool = False,
    comment_sort_by_agree: bool = False,
    comment_rn: int = 1,
    is_fold: bool = False,
) -> List[requests.Request]:
    preload = base_get_posts.RESPONSE_PROTOBUF.FromString(
        base_get_posts.call(tid, pn=1, rn=2).content
    )
    data = preload.data
    post_num = data.page.page_size * data.page.total_page
    page_size = 30
    pages = range(1, max(2, ceil(post_num / page_size) + 1))

    return [
        base_get_posts.get_request(
            tid,
            pn=page,
            rn=page_size,
            sort=sort,
            only_thread_author=only_thread_author,
            with_comments=with_comments,
            comment_sort_by_agree=comment_sort_by_agree,
            comment_rn=comment_rn,
            is_fold=is_fold,
        )
        for page in pages
    ]


def call(
    tid: int,
    /,
    *,
    sort: int = 0,
    only_thread_author: bool = False,
    with_comments: bool = False,
    comment_sort_by_agree: bool = False,
    comment_rn: int = 1,
    is_fold: bool = False,
):
    prepared_req = [
        req.prepare()
        for req in get_requests(
            tid,
            sort=sort,
            only_thread_author=only_thread_author,
            with_comments=with_comments,
            comment_sort_by_agree=comment_sort_by_agree,
            comment_rn=comment_rn,
            is_fold=is_fold,
        )
    ]

    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            processes = [executor.submit(session.send, req) for req in prepared_req]
            results = [
                future.result() for future in concurrent.futures.as_completed(processes)
            ]

    return results


def parse_responses(responses: Iterable[requests.Response]):
    posts = [base_get_posts.parse_response(response) for response in responses]
    return reduce(lambda p1, p2: p1 + p2, posts)
