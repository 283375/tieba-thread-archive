import requests
from yarl import URL

from ....models.post import Posts
from ...protobuf.request import PbPageReqIdl_pb2
from ...protobuf.response import PbPageResIdl_pb2
from ..helpers.constants import APP_MAIN_VERSION, URL_BASE_HOST
from ..helpers.quick_api import mobile_protobuf_call, mobile_protobuf_request

CMD = 302001
RESPONSE_PROTOBUF = PbPageResIdl_pb2.PbPageResIdl


def url():
    return URL.build(
        scheme="https",
        host=URL_BASE_HOST,
        path="/c/f/pb/page",
        query_string=f"cmd={CMD}",
    )


def request_protobuf(
    tid: int,
    /,
    pn: int = 1,
    *,
    rn: int = 30,
    sort: int = 0,
    only_thread_author: bool = False,
    with_comments: bool = False,
    comment_sort_by_agree: bool = False,
    comment_rn: int = 1,
    is_fold: bool = False,
) -> PbPageReqIdl_pb2.PbPageReqIdl:
    pb = PbPageReqIdl_pb2.PbPageReqIdl()
    pb.data.common._client_type = 2
    pb.data.common._client_version = APP_MAIN_VERSION
    pb.data.tid = tid
    pb.data.pn = pn
    pb.data.rn = max(rn, 2)
    pb.data.sort = sort
    pb.data.only_thread_author = only_thread_author
    pb.data.is_fold = is_fold
    if with_comments:
        pb.data.common.BDUSS = ""
        pb.data.with_comments = with_comments
        pb.data.comment_sort_by_agree = comment_sort_by_agree
        pb.data.comment_rn = comment_rn

    return pb


get_request = mobile_protobuf_request(
    method="POST", url=str(url()), protobuf_builder=request_protobuf
)
call = mobile_protobuf_call(get_request)


def parse_response(response: requests.Response) -> Posts:
    res_pb = PbPageResIdl_pb2.PbPageResIdl.FromString(response.content)
    return Posts.from_protobuf(res_pb.data.post_list)
