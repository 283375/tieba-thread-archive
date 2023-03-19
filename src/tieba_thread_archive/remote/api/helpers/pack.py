from typing import Any, Dict, List, Tuple, Union

from google.protobuf.message import Message

from .sign import sign_url_params

__all__ = ("pack_mobile_protobuf_data", "pack_mobile_url_encoded_data")


def pack_mobile_protobuf_data(data: Union[bytes, Message]) -> List[Tuple[str, Any]]:
    """
    打包移动端 protobuf 请求至 FormData。

    Arguments:
        data -- protobuf.message.Message 对象，或经 protobuf 序列化后的二进制字符串
    """
    if isinstance(data, Message):
        return [("data", data.SerializeToString())]
    return [("data", data)]


def pack_mobile_url_encoded_data(data: Dict[str, Any]) -> Dict[str, Any]:
    sign_result = sign_url_params(data)
    data["sign"] = sign_result
    return data
