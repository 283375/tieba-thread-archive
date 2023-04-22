import requests
from yarl import URL

from ....models.user import User
from ...protobuf.request import GetUserInfoReqIdl_pb2
from ...protobuf.response import GetUserInfoResIdl_pb2
from ..exception import TiebaApiError
from ..helpers.constants import APP_BASE_HOST
from ..helpers.quick_api import mobile_protobuf_call, mobile_protobuf_request

CMD = 303024
RESPONSE_PROTOBUF = GetUserInfoResIdl_pb2.GetUserInfoResIdl


def url():
    return URL.build(
        scheme="https",
        host=APP_BASE_HOST,
        path="/c/u/user/getuserinfo",
        query_string=f"cmd={CMD}",
    )


def request_protobuf(user_id: int) -> GetUserInfoReqIdl_pb2.GetUserInfoReqIdl:
    pb = GetUserInfoReqIdl_pb2.GetUserInfoReqIdl()
    pb.data.user_id = user_id

    return pb


get_request = mobile_protobuf_request(
    method="POST", url=str(url()), protobuf_builder=request_protobuf
)
call = mobile_protobuf_call(get_request)


def parse_response(response: requests.Response) -> User:
    pb = GetUserInfoResIdl_pb2.GetUserInfoResIdl.FromString(response.content)
    if pb.error.errorno != 0:
        raise TiebaApiError(pb.error.errorno, pb.error.errmsg)
    return User.from_protobuf(pb.data.user)
