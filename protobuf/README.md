# tieba-post-archive - protobuf

该目录存放所有需要的 protobuf 文件，并提供快速编译脚本，可自动修复编译出 `*_pb2.py` 文件中的 import 问题。

[protobuf 文件来源 - Starry-OvO/aiotieba](https://github.com/Starry-OvO/aiotieba/tree/master/aiotieba/client/_protobuf)

## FAQ

> 运行时报错 `Couldn't build proto file into descriptor pool: duplicate file name`

参见[这个 issue](https://github.com/ValvePython/csgo/issues/8)。

首先卸载已安装的 protobuf `pip uninstall protobuf`，

随后加上 `--no-binary` 项重新下载 protobuf `pip install protobuf --no-binary protobuf`。
