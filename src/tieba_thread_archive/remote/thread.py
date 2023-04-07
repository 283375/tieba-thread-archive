import time
from concurrent import futures
from typing import Callable, Concatenate, Dict, List, Set, TypedDict, TypeVar

import requests
from typing_extensions import ParamSpec

from ..models.archive import ArchiveThread, ThreadInfo
from ..models.content import ContentAudio, ContentImage, ContentVideo
from ..models.post import SubPosts
from ..models.progress import Progress
from ..models.user import User
from ..remote.api import get_posts, get_subposts
from ..remote.protobuf.response.PbPageResIdl_pb2 import PbPageResIdl

P = ParamSpec("P")
T = TypeVar("T")


class RemoteThread:
    __slots__ = (
        "__tid",
        "__mutex",
        "__progress",
        "__loaded",
        "__loaded_time",
        "add_progress_hook",
        "add_complete_hook",
        "info",
        "posts",
        "subposts",
    )

    def __init__(self, tid: int):
        self.__tid = tid
        self.__progress = Progress(total_step=2)
        self.__loaded = False

        self.add_progress_hook = self.__progress.add_progress_hook
        self.add_complete_hook = self.__progress.add_complete_hook

    @property
    def loaded(self):
        return self.__loaded

    def data_loaded(func: Callable[Concatenate["RemoteThread", P], T]) -> Callable[Concatenate["RemoteThread", P], T]:  # type: ignore
        def wrapper(self: "RemoteThread", *args: P.args, **kwargs: P.kwargs) -> T:
            if not self.loaded:
                raise ValueError(
                    f"{self.__class__.__name__}.{func.__name__} needs data to be loaded first."
                )

            return func(self, *args, **kwargs)

        return wrapper

    @property
    def loaded_time(self):
        return self.__loaded_time

    def __executor_task_load_subposts(self, pid: int):
        with requests.Session() as session:
            with futures.ThreadPoolExecutor() as executor:
                subpost_requests = get_subposts.get_requests(self.__tid, pid)
                responses: List[requests.Response] = [
                    future.result()
                    for future in futures.as_completed(
                        executor.submit(session.send, req.prepare())
                        for req in subpost_requests
                    )
                ]
                return (pid, get_subposts.parse_responses(responses))

    def load_remote_data(self):
        progress = self.__progress

        post_requests = get_posts.get_requests(self.__tid)
        progress.total_progress = len(post_requests)

        with requests.Session() as session:
            with futures.ThreadPoolExecutor() as executor:
                post_responses: List[requests.Response] = []
                for future in futures.as_completed(
                    executor.submit(session.send, req.prepare())
                    for req in post_requests
                ):
                    post_responses.append(future.result())
                    progress += 1

        self.posts = get_posts.parse_responses(post_responses)
        self.posts.sort()
        self.info = ThreadInfo.from_protobuf(
            PbPageResIdl.FromString(post_responses[0].content)
        )
        progress.step += 1

        self.subposts: Dict[int, SubPosts] = {}
        request_pids = [post.id for post in self.posts if post.subpost_num > 0]
        progress.total_progress = len(request_pids)

        with futures.ThreadPoolExecutor() as executor:
            for future in futures.as_completed(
                executor.submit(self.__executor_task_load_subposts, pid)
                for pid in request_pids
            ):
                pid, subposts = future.result()
                self.subposts[pid] = subposts
                progress += 1

        self.__loaded = True
        self.__loaded_time = int(time.time())
        self.__progress.invoke_complete_hooks()

    @data_loaded
    def get_users(self) -> Set[User]:
        return {
            subpost.author
            for subposts in self.subposts.values()
            for subpost in subposts
        } | {post.author for post in self.posts}

    class GetAssetsReturn(TypedDict):
        images: Set[ContentImage]
        audios: Set[ContentAudio]
        videos: Set[ContentVideo]

    @data_loaded
    def get_assets(self) -> GetAssetsReturn:
        images: Set[ContentImage] = set()
        audios: Set[ContentAudio] = set()
        videos: Set[ContentVideo] = set()

        for post in self.posts:
            # users.add(post.author)
            for content in post.contents:
                if isinstance(content, ContentImage):
                    images.add(content)
                if isinstance(content, ContentAudio):
                    audios.add(content)
                if isinstance(content, ContentVideo):
                    videos.add(content)

        for _subposts in self.subposts.values():
            for subpost in _subposts:
                # users.add(subpost.author)
                for content in subpost.contents:
                    if isinstance(content, ContentImage):
                        images.add(content)
                    if isinstance(content, ContentAudio):
                        audios.add(content)
                    if isinstance(content, ContentVideo):
                        videos.add(content)

        return {"images": images, "audios": audios, "videos": videos}

    @data_loaded
    def to_archive_thread(self):
        # fill info
        thread_info = self.info

        # fill posts
        posts = self.posts
        __posts_ids = [post.id for post in posts]
        subposts = {
            id: subpost for id, subpost in self.subposts.items() if id in __posts_ids
        }

        # parse contents & users
        users = self.get_users()
        assets = self.get_assets()

        return ArchiveThread(
            archive_time=self.__loaded_time,
            thread_info=thread_info,
            posts=posts,
            subposts=subposts,
            users=users,
        )
