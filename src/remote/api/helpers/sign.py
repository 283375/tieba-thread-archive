from hashlib import md5
from typing import Any, Dict


def sign_url_params(params: Dict[str, Any]) -> str:
    params.pop("sign", None)
    params = dict(sorted(params.items()))
    params_join = "".join(f"{k}={v}" for k, v in params.items()) + "tiebaclient!!!"
    return md5(params_join.encode("utf-8")).hexdigest()
