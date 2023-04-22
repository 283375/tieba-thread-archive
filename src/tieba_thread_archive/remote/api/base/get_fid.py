import json
from typing import Any, Dict

import requests
from yarl import URL

from ..exception import TiebaApiError
from ..helpers.constants import WEB_BASE_HOST
from ..helpers.quick_api import web_call, web_request


def url():
    return URL.build(
        scheme="http",
        host=WEB_BASE_HOST,
        path="/f/commit/share/fnameShareApi",
    )


def request_params(fname: str, ie: str = "utf-8") -> Dict[str, Any]:
    return {"fname": fname, "ie": ie}


get_request = web_request(method="GET", url=str(url()), params=request_params)
call = web_call(get_request)


def parse_response(response: requests.Response) -> int:
    response_dict = json.loads(response.text)
    assert isinstance(response_dict, dict)

    no = response_dict.get("no")
    assert isinstance(no, int)
    if no != 0:
        raise TiebaApiError(no, response_dict.get("error", ""))

    fid = response_dict.get("data", {}).get("fid")
    assert isinstance(fid, int)
    if fid == 0:
        raise TiebaApiError(0, "fid 为 0，可能该吧已被封禁")
    return fid
