from typing import Iterable, Set, Tuple, TypedDict, cast

from ....models import *
from .file_structure import *
from .models import *

__all__ = (
    "av2_load_users_json",
    "av2_load_threadInfo_json",
    "av2_load_posts_json",
    "av2_load_assets_json",
)


def av2_load_users_json(users_json: AV2File_UsersJson) -> Set[User]:
    return {AV2User.archive_load(user_archive) for user_archive in users_json.values()}


def av2_load_threadInfo_json(
    threadInfo_json: AV2File_ThreadInfoJson, user_list: Iterable[User]
) -> Tuple[ThreadInfo, ArchiveOptions, ArchiveUpdateInfo]:
    return (
        AV2ThreadInfo.archive_load(threadInfo_json, user_list),
        AV2ArchiveOptions.archive_load(threadInfo_json["storeOptions"]),
        AV2ArchiveUpdateInfo.archive_load(threadInfo_json["updateInfo"]),
    )


def av2_load_posts_json(
    posts_json: AV2File_PostsJson, user_list: Iterable[User]
) -> Tuple[Posts, DictSubPosts]:
    posts = AV2Posts.archive_load(posts_json, user_list)

    dict_subposts = DictSubPosts(
        {
            post_archive["id"]: AV2SubPosts.archive_load(
                post_archive["sub_post_list"], user_list
            )
            for post_archive in posts_json
            if post_archive.get("sub_post_list")
        }
    )

    return (posts, dict_subposts)


class AV2AssetsJsonLoadResult(TypedDict):
    images: Set[ContentImage]
    audios: Set[ContentAudio]
    videos: Set[ContentVideo]


def av2_load_assets_json(assets_json: AV2File_AssetsJson) -> AV2AssetsJsonLoadResult:
    result_list = {
        "images": [],
        "audios": [],
        "videos": [],
    }

    for asset in assets_json:
        if asset["type"] == "image":
            result_list["images"].append(
                AV2ContentImage.archive_load_from_av2_tieba_asset(asset)
            )
        elif asset["type"] == "audio":
            result_list["audios"].append(
                AV2ContentAudio.archive_load_from_av2_tieba_asset(asset)
            )
        elif asset["type"] == "video":
            result_list["videos"].append(
                AV2ContentVideo.archive_load_from_av2_tieba_asset(asset)
            )

    return cast(
        AV2AssetsJsonLoadResult, {key: set(_list) for key, _list in result_list.items()}
    )
