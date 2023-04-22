import requests
from yarl import URL

from ....models.post import SubPosts
from ...protobuf.request import PbFloorReqIdl_pb2
from ...protobuf.response import PbFloorResIdl_pb2
from ..exception import TiebaApiError
from ..helpers.constants import APP_BASE_HOST, APP_MAIN_VERSION
from ..helpers.quick_api import mobile_protobuf_call, mobile_protobuf_request

CMD = 302002
RESPONSE_PROTOBUF = PbFloorResIdl_pb2.PbFloorResIdl


def url():
    return URL.build(
        scheme="https",
        host=APP_BASE_HOST,
        path="/c/f/pb/floor",
        query_string=f"cmd={CMD}",
    )


def request_protobuf(
    tid: int, pid: int, /, pn: int = 1, *, is_floor: bool = False
) -> PbFloorReqIdl_pb2.PbFloorReqIdl:
    pb = PbFloorReqIdl_pb2.PbFloorReqIdl()
    pb.data.common._client_type = 2
    pb.data.common._client_version = APP_MAIN_VERSION
    pb.data.tid = tid
    if is_floor:
        pb.data.spid = pid
    else:
        pb.data.pid = pid
    pb.data.pn = pn

    return pb


get_request = mobile_protobuf_request(
    method="POST", url=str(url()), protobuf_builder=request_protobuf
)
call = mobile_protobuf_call(get_request)


def parse_response(response: requests.Response) -> SubPosts:
    pb = PbFloorResIdl_pb2.PbFloorResIdl.FromString(response.content)
    if pb.error.errorno != 0:
        raise TiebaApiError(pb.error.errorno, pb.error.errmsg)
    return SubPosts.from_protobuf(pb.data.subpost_list)
