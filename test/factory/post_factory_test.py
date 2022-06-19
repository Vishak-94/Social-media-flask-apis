from unittest import TestCase, main

from main.constants.constant import MediaConstants
from main.exception import InvalidRequestData
from main.factory.post_factory import PostFactory, PostActionFactory
from main.service.action_service import CommentActionService, LikeActionService
from main.service.post_service import TextPostService


class PostFactoryTest(TestCase):
    post_fact = PostFactory()
    post_action_fact = PostActionFactory()

    def test_invalid_post_action(self):
        with self.assertRaises(InvalidRequestData):
            self.post_action_fact.get_service("random_service")

    def test_valid_post_action(self):
        comm_obj = self.post_action_fact.get_service(MediaConstants.COMMENT)
        self.assertEqual(CommentActionService, type(comm_obj))
        like_service = self.post_action_fact.get_service(MediaConstants.LIKE)
        self.assertEqual(LikeActionService, type(like_service))

    def test_invalid_post_type(self):
        with self.assertRaises(InvalidRequestData):
            self.post_fact.get_service("image-v2")

    def test_valid_post_type(self):
        text_service = self.post_fact.get_service(MediaConstants.TEXT)
        self.assertEqual(TextPostService, type(text_service))


if __name__ == '__main__':
    main()

