import json
from typing import Any, Dict

import requests
from yarl import URL

from ....models.forum import Forum
from ..exception import TiebaApiError
from ..helpers.constants import APP_BASE_HOST
from ..helpers.quick_api import mobile_url_encoded_call, mobile_url_encoded_request


def url():
    return URL.build(
        scheme="http",
        host=APP_BASE_HOST,
        path="/c/f/forum/getforumdetail",
    )


def request_form(fid: int) -> Dict[str, Any]:
    return {"forum_id": fid}


get_request = mobile_url_encoded_request(
    method="POST", url=str(url()), form=request_form
)
call = mobile_url_encoded_call(get_request)


def parse_response(response: requests.Response) -> Forum:
    content_dict = json.loads(response.text)
    assert isinstance(content_dict, dict)

    error_code = content_dict.get("error_code")
    assert isinstance(error_code, (int, str))
    if int(error_code) != 0:
        raise TiebaApiError(int(error_code), content_dict.get("error_msg", ""))

    forum_info = content_dict.get("forum_info")
    assert isinstance(forum_info, dict)
    fid = forum_info.get("forum_id")
    name = forum_info.get("forum_name")
    avatar = forum_info.get("avatar")
    assert isinstance(fid, int)
    assert isinstance(name, str)
    assert isinstance(avatar, str)

    return Forum(id=fid, name=name, avatar=avatar)
