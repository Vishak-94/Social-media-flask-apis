from unittest import TestCase, main
from unittest.mock import MagicMock

from werkzeug.security import generate_password_hash

from main.dao.post_dao import PostDao
from main.exception import AccessForbidden, ResourceNotFound
from main.factory.post_factory import PostFactory
from main.model.post_model import PostData, PostAction
from main.model.user_model import UserData
from main.request_data.post_request import AddPostRequest, PostRequestData
from main.service.action_service import PostActionService
from main.service.post_service import PostService


class PostServiceTest(TestCase):
    post_fact = PostFactory()

    def setUp(self) -> None:
        self.user_obj = UserData(user_id=1234,
                                 email_id="test@gmail.conm",
                                 user_name="test_user",
                                 password=generate_password_hash("testhash"),
                                 gender="m",
                                 public_key="test_public_key")
        self.req_data = AddPostRequest(post_type="text", post_content="Test Content", current_user=self.user_obj)
        self.post_obj = PostData(post_id=1,
                                 user_id=1234,
                                 post_type=self.req_data.post_type,
                                 post_content=self.req_data.post_content,
                                 active=1)

        self.post_user_data1 = (PostAction(action_id=1,
                                           post_id=1,
                                           user_id=1234,
                                           action_type="like",
                                           action_text=""), self.user_obj)

        self.post_user_data2 = (PostAction(action_id=2,
                                           post_id=1,
                                           user_id=1234,
                                           action_type="comment",
                                           action_text="Test comment"), self.user_obj)

    def test_add_post(self):
        post_service = self.post_fact.get_service(self.req_data.post_type)
        PostDao.add_new_post = MagicMock(return_value=self.post_obj)
        post_obj = post_service.add_post(self.req_data)
        self.assertEqual(PostData, type(post_obj))
        self.assertEqual(self.post_obj.post_id, post_obj.post_id)

    def test_delete_post(self):
        post_service = self.post_fact.get_service(self.req_data.post_type)
        PostDao.get_post_by_id = MagicMock(return_value=self.post_obj)
        PostDao.delete_post = MagicMock(return_value=None)
        post_resp = post_service.delete_post(PostRequestData(post_type=self.req_data.post_type,
                                                             post_id=self.post_obj.post_id,
                                                             current_user=self.user_obj))

        self.assertEqual(None, post_resp)

    def test_unauthorized_delete_post(self):
        post_service = self.post_fact.get_service(self.req_data.post_type)
        self.post_obj.user_id = 890
        PostDao.get_post_by_id = MagicMock(return_value=self.post_obj)
        PostDao.delete_post = MagicMock(return_value=None)
        with self.assertRaises(AccessForbidden):
            post_service.delete_post(PostRequestData(post_type=self.req_data.post_type,
                                                     post_id=self.post_obj.post_id,
                                                     current_user=self.user_obj))

    def test_invalid_post_id(self):
        PostDao.get_post_by_id = MagicMock(return_value=None)
        with self.assertRaises(ResourceNotFound):
            post_service = self.post_fact.get_service(self.req_data.post_type)
            post_service.delete_post(PostRequestData(post_type=self.req_data.post_type,
                                                     post_id=self.post_obj.post_id,
                                                     current_user=self.user_obj))

    def test_get_all_post(self):
        post_service = PostService()
        all_posts = [self.post_obj, PostData(post_id=2, user_id=123, post_type="text",
                                             post_content="test_content", active=True)]

        PostDao.get_all_posts = MagicMock(return_value=all_posts)

        post_actions = [self.post_user_data2, self.post_user_data1]
        PostActionService.get_all_actions = MagicMock(return_value=post_actions)
        resp = post_service.get_all_post()

        lastest_post = resp[0]["post_data"]
        like_data = resp[0]["like_data"]
        comment_data = resp[0]["comment_data"]
        self.assertEqual(2, len(resp))
        self.assertEqual(1, lastest_post["post_id"])
        self.assertEqual(1234, lastest_post["user_id"])
        self.assertEqual(['test_user'], like_data)
        self.assertEqual([{'test_user': 'Test comment'}], comment_data)

    def test_empty_post(self):
        post_service = PostService()
        PostDao.get_all_posts = MagicMock(return_value=[])
        resp = post_service.get_all_post()
        self.assertEqual([], resp)

    def test_nolike_no_comment_post(self):
        post_service = PostService()
        all_posts = [self.post_obj, PostData(post_id=2, user_id=123, post_type="text",
                                             post_content="test_content", active=True)]
        PostDao.get_all_posts = MagicMock(return_value=all_posts)
        PostActionService.get_all_actions = MagicMock(return_value=[])
        resp = post_service.get_all_post()

        for post_data in resp:
            self.assertEqual([], post_data["like_data"])
            self.assertEqual([], post_data["comment_data"])


if __name__ == '__main__':
    main()
