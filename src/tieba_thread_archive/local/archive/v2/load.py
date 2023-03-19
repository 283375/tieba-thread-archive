import json
from os import PathLike
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple, Union

from ....models.archive import ArchiveOptions, ArchiveThread, ThreadInfo
from ....models.content import ContentAudio, ContentImage
from ....models.post import Posts, SubPosts
from ....models.user import User
from .models import AV2Asset, AV2Post, AV2SubPost, AV2User

__all__ = (
    "load_v2_users",
    "load_v2_info",
    "load_v2_posts",
    "load_v2_assets",
    "load_v2",
)


def load_v2_users(path: Union[str, PathLike]) -> Set[User]:
    path = Path(path)

    users = set()
    with open(path / "users.json", "r", encoding="utf-8") as users_rs:
        loaded_json: Dict[str, AV2User.ArchivePart] = json.load(users_rs)
        for user in loaded_json.values():
            users.add(AV2User.archive_load(user))
    return users


def load_v2_info(
    path: Union[str, PathLike], users: Optional[Iterable[User]] = None
) -> Tuple[ThreadInfo, ArchiveOptions]:
    path = Path(path)

    with open(path / "threadInfo.json", "r", encoding="utf-8") as info_rs:
        info = json.load(info_rs)
        assert isinstance(info, dict)

        author_id = int(info["author"]["id"])
        author_portrait = ""
        if users is not None:
            for user in users:
                if user.id == author_id:
                    author_portrait = user.portrait

        thread_info = ThreadInfo(
            id=int(info["id"]),
            author=User(
                id=author_id,
                name=info["author"]["origName"],
                name_show=info["author"]["displayName"],
                portrait=author_portrait,
                level_id=1,
            ),
            title=info["title"],
            create_time=info["createTime"],
        )

        assets_archived = info["storeOptions"]["assets"]
        archive_info = ArchiveOptions(
            lz_only=info["storeOptions"]["lzOnly"],
            images=assets_archived,
            audios=assets_archived,
            videos=assets_archived,
            portraits=info["storeOptions"]["portraits"],
        )
    return (thread_info, archive_info)


def load_v2_posts(
    path: Union[str, PathLike], user_list: Iterable[User]
) -> Tuple[Posts, Dict[int, SubPosts]]:
    path = Path(path)

    posts = []
    subposts = {}
    with open(path / "posts.json", "r", encoding="utf-8") as posts_rs:
        posts_archives: List[AV2Post.ArchivePart] = json.load(posts_rs)
        for post_archive in posts_archives:
            post = AV2Post.archive_load(post_archive, user_list)
            posts.append(post)
            if post.subpost_num > 0:
                subposts[post.id] = SubPosts(
                    AV2SubPost.archive_load(subpost_archive)
                    for subpost_archive in post_archive["sub_post_list"]
                )

    return (Posts(posts), subposts)


def load_v2_assets(
    path: Union[str, PathLike]
) -> Tuple[Set[ContentImage], Set[ContentAudio]]:
    path = Path(path)

    images = set()
    audios = set()

    if not (path / "assets.json").exists():
        return (images, audios)

    with open(path / "assets.json", "r", encoding="utf-8") as assets_rs:
        assets: List[AV2Asset.ArchivePart] = json.load(assets_rs)

        for asset_archive in assets:
            asset = AV2Asset.archive_load(asset_archive)
            if isinstance(asset, ContentImage):
                images.add(asset)
            elif isinstance(asset, ContentAudio):
                audios.add(asset)

    return (images, audios)


def load_v2(path: Union[str, PathLike]) -> ArchiveThread:
    path = Path(path)

    users = load_v2_users(path)
    posts, subposts = load_v2_posts(path, users)
    thread_info, archive_info = load_v2_info(path, users)
    images, audios = load_v2_assets(path)

    return ArchiveThread(
        thread_info=thread_info,
        archive_options=archive_info,
        users=users,
        posts=posts,
        subposts=subposts,
        images=images,
        audios=audios,
    )
