from concurrent import futures
from typing import Dict, List, Set

import requests

from ..models.archive import ArchiveInfo, ArchiveThread, ThreadInfo
from ..models.content import ContentAudio, ContentImage
from ..models.post import SubPosts
from ..models.progress import Progress
from ..models.user import User
from ..remote.api import get_posts, get_subposts
from ..remote.api.base.get_posts import RESPONSE_PROTOBUF


class RemoteThread:
    __slots__ = (
        "__tid",
        "__mutex",
        "__progress",
        "__loaded",
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

    def __load_subposts(self, pid: int):
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
        self.info = ThreadInfo.from_protobuf(
            RESPONSE_PROTOBUF.FromString(post_responses[0].content)
        )
        progress.step += 1

        self.subposts: Dict[int, SubPosts] = {}
        request_pids = [post.id for post in self.posts if post.subpost_num > 0]
        progress.total_progress = len(request_pids)

        with futures.ThreadPoolExecutor() as executor:
            for future in futures.as_completed(
                executor.submit(self.__load_subposts, pid) for pid in request_pids
            ):
                pid, subposts = future.result()
                self.subposts[pid] = subposts
                progress += 1

        self.__loaded = True
        self.__progress.invoke_complete_hooks()

    def to_archive_thread(self):
        if not self.loaded:
            raise ValueError("RemoteThread not loaded.")

        # fill info
        thread_info = self.info

        # fill posts
        posts = self.posts
        subposts = self.subposts

        # parse contents & users
        users: Set[User] = set()
        images: Set[ContentImage] = set()
        audios: Set[ContentAudio] = set()
        for post in self.posts:
            if isinstance(post.author, User):
                users.add(post.author)

            for content in post.contents:
                if isinstance(content, ContentImage):
                    images.add(content)
                elif isinstance(content, ContentAudio):
                    audios.add(content)

        for _subposts in self.subposts.values():
            for subpost in _subposts:
                users.add(subpost.author)
                for content in subpost.contents:
                    if isinstance(content, ContentImage):
                        images.add(content)
                    elif isinstance(content, ContentAudio):
                        audios.add(content)

        return ArchiveThread(
            thread_info=thread_info,
            archive_info=ArchiveInfo(
                lz_only=False, images=True, audios=True, videos=True, portraits=True
            ),
            posts=posts,
            subposts=subposts,
            users=users,
            images=images,
            audios=audios,
        )
