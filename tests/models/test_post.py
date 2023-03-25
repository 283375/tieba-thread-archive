from tieba_thread_archive.models import *
from tieba_thread_archive.remote.api.base import get_posts
from tieba_thread_archive.remote.protobuf.response.PbPageResIdl_pb2 import PbPageResIdl


class Test_Post_Posts:
    def test_from_protobuf(self):
        response = get_posts.call(7990569158, pn=1)

        pb = PbPageResIdl.FromString(response.content)
        posts = Posts.from_protobuf(pb.data.post_list, pb.data.user_list)

        assert posts[0].title == "整了个烂活"

    def test_posts_functionality(self):
        pass
