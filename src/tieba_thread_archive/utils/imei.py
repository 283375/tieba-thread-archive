import random
from typing import Union

__all__ = ("generate_imei", "generate_taf_imei")


def generate_imei(n: int = 35, x: Union[int, None] = None) -> str:
    """
    生成随机 IMEI 码

    目前流行的 IMEI 码格式为 `NN-XXXXXX-ZZZZZZ-A`。

    `N`: 有能力分配 TAC 码的组织代号，范围 00~99。

    已有有效注册组织如下：
    * 00: 测试设备专用
    * 01: CTIA
    * 35: TÜV SÜD (BABT)
    * 86: TAF (China)
    * 99: Global Hexadecimal Administrator (GHA)

    `X`: 由上述组织分配的设备型号代码，范围 000000~999999。

    `Z`: 设备唯一代码，范围 000000~999999。

    `A`: 由前 14 位数字使用卢恩算法生成的校验码，范围 0~9。

    详见 https://www.gsma.com/newsroom/wp-content/uploads//TS.06-v20.0.pdf
    """

    n_str = str(n).rjust(2, "0")
    x_str = str(x if x is not None else random.randint(0, 999999)).rjust(6, "0")
    z_str = str(random.randint(0, 999999)).rjust(6, "0")

    digits = []
    for i, digit in enumerate(n_str + x_str + z_str):
        digit = int(digit) if i % 2 == 0 else int(digit) * 2
        digits += list(str(digit))
    digits_sum = sum(int(s) for s in digits)

    a = 0 if digits_sum % 10 == 0 else 10 - (digits_sum % 10)

    return n_str + x_str + z_str + str(a)


def generate_taf_imei(x: Union[int, None] = None):
    """
    是中国人，就用中国 IMEI！
    """
    return generate_imei(n=86, x=x)
