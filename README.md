<div align="center">
    <img src="./assets/logo-shadow.png">
    <h1>tieba-thread-archive</h1>
</div>

> 已与 [tieba_post_store](https://github.com/283375/tieba_post_store) 切割 ![emoticon face savoring food](https://gsp0.baidu.com/5aAHeD3nKhI2p27j8IqW0jdnxx1xbK/tb/editor/images/client/image_emoticon3.png 'A tieba emoticon showing a face savoring food which is similar to emoji 😋')

## 简单使用

> **Warning**
> 早期开发阶段，任何方法、类甚至模块名称、布局等都可能发生改变。
> Use it at your own risk.

> **Note**
> 暂时没有上架 pip，待到真正意义的 v0.1.0 时再说（

```sh
$ pip install git+https://github.com/283375/tieba-thread-archive
```

```py
import os

from tieba_thread_archive.local.archive.v3 import AV3LocalArchive
from tieba_thread_archive.models.archive import ArchiveOptions
from tieba_thread_archive.models.progress import Progress
from tieba_thread_archive.remote.thread import RemoteThread

def progress_hook(p: Progress):
    digits = len(str(p.total_progress)) - 1
    if p.progress % (10**digits) == 0 or p.progress == p.total_progress:
        print(f"{p.step} / {p.total_step}: {p.progress} / {p.total_progress}")

tid = 8412677042

remote_thread = RemoteThread(tid)
remote_thread.add_progress_hook(progress_hook)
remote_thread.load_remote_thread_data()
archive_thread = remote_thread.to_archive_thread()

path = f"/to/your/desired/path/{tid}"
if not os.path.exists(path):
    os.makedirs(path, exist_ok=True)

local_archive = AV3LocalArchive(path)
local_archive.set_archive_options(
    ArchiveOptions(images=True, audios=True, videos=True, portraits=True)
)
local_archive.update_progress.add_progress_hook(progress_hook)

local_archive.update(archive_thread)
local_archive.dump()
local_archive.download_assets()

print(f"{tid} done.")
```

## 将会保存贴子的哪些信息？

在最新最热的存档版本 3 中，可以保存以下信息：

| 概要             | 描述                                                   | 备注                           |
| ---------------- | ------------------------------------------------------ | ------------------------------ |
| 基本信息         | 标题、楼主、所在吧、发布时间                           |                                |
| 贴子内容         | 游客可见的<sup>1</sup>楼层、楼中楼                     |                                |
| 用户信息         | 贴吧昵称、百度用户名、吧等级、吧务信息                 |                                |
| 资源（媒体）文件 | 贴子内的图片、语音、视频，用户头像                     | 需要额外调用 download_assets() |
| 历史记录         | 每次更新都会保存一份原有的存档记录，见证贴子的成长（？ |                                |

<sup>1</sup> 由于潜在的封号风险，我们不打算实现任何登录功能。因此，若您的贴子或楼中楼仅对您自己可见（也就是常说的吞楼），tieba-thread-archive 将不能存档它。

## 鸣谢

[HuanCheng65/TiebaLite](https://github.com/HuanCheng65/TiebaLite) - 最初 `tieba_post_store` 的 <kbd>Ctrl</kbd>+<kbd>C</kbd><kbd>V</kbd> 来源

[Starry-OvO/aiotieba](https://github.com/Starry-OvO/aiotieba) - API 实现 (`remote.api`) <kbd>Ctrl</kbd>+<kbd>C</kbd><kbd>V</kbd> 来源、内容类实现 (`models.content`) 参考

[283375/tieba_post_store](https://github.com/283375/tieba_post_store) - 他是我爹，你不许说他 ![emoticon smiley face](https://gsp0.baidu.com/5aAHeD3nKhI2p27j8IqW0jdnxx1xbK/tb/editor/images/client/image_emoticon1.png "A tieba emoticon showing a smiley face")
