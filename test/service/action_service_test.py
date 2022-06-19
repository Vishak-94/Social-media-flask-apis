from unittest import TestCase, main
from unittest.mock import MagicMock

from werkzeug.security import generate_password_hash

from main.constants.constant import MediaConstants
from main.dao.action_dao import PostActionDao
from main.exception import DuplicationError, InvalidRequestData
from main.factory.post_factory import PostActionFactory
from main.model.post_model import PostAction
from main.model.user_model import UserData
from main.request_data.post_request import PostActionRequest
from main.service.action_service import PostActionService


class ActionServiceTest(TestCase):
    action_factory = PostActionFactory()

    def setUp(self) -> None:
        self.user_obj = UserData(user_id=1234,
                                 email_id="test@gmail.conm",
                                 user_name="test_user",
                                 password=generate_password_hash("testhash"),
                                 gender="m",
                                 public_key="test_public_key")

        self.like_request_data = PostActionRequest(action_type=MediaConstants.LIKE,
                                                   post_id=2,
                                                   current_user=self.user_obj)

        self.comment_request_data = PostActionRequest(action_type=MediaConstants.COMMENT,
                                                      post_id=2,
                                                      current_user=self.user_obj,
                                                      action_content="test comment")

        self.like_action_obj = PostAction(action_id=1,
                                          post_id=2,
                                          user_id=1234,
                                          action_type=MediaConstants.LIKE,
                                          action_text="")

        self.comment_action_obj = PostAction(action_id=1,
                                             post_id=2,
                                             user_id=1234,
                                             action_type=MediaConstants.COMMENT,
                                             action_text="test comment")

    def test_create_like(self):
        post_service = self.action_factory.get_service(MediaConstants.LIKE)
        PostActionDao.get_like_by_post_and_user_id = MagicMock(return_value=[])
        PostActionDao.add_post_action = MagicMock(return_value=self.like_action_obj)
        action_obj = post_service.add_action(self.like_request_data)
        self.assertEqual(PostAction, type(action_obj))
        self.assertEqual(self.like_request_data.action_type, action_obj.action_type)
        self.assertEqual(self.like_request_data.post_id, action_obj.post_id)
        self.assertEqual(self.like_request_data.current_user.user_id, action_obj.user_id)
        self.assertEqual(self.like_request_data.action_content, action_obj.action_text)

    def test_duplicate_like(self):
        with self.assertRaises(DuplicationError):
            post_service = self.action_factory.get_service(MediaConstants.LIKE)
            PostActionDao.get_like_by_post_and_user_id = MagicMock(return_value=self.like_action_obj)
            post_service.add_action(self.like_request_data)

    def test_create_comment(self):
        post_service = self.action_factory.get_service(MediaConstants.COMMENT)
        PostActionDao.add_post_action = MagicMock(return_value=self.comment_action_obj)
        action_obj = post_service.add_action(self.comment_request_data)
        self.assertEqual(PostAction, type(action_obj))
        self.assertEqual(self.comment_request_data.action_type, action_obj.action_type)
        self.assertEqual(self.comment_request_data.post_id, action_obj.post_id)
        self.assertEqual(self.comment_request_data.current_user.user_id, action_obj.user_id)
        self.assertEqual(self.comment_request_data.action_content, action_obj.action_text)

    def test_get_all_action(self):
        post_service = PostActionService()
        return_data = [(self.like_action_obj, self.user_obj), (self.comment_action_obj, self.user_obj)]
        PostActionDao.get_all_action_by_post_id = MagicMock(return_value=return_data)
        post_datas = post_service.get_all_actions([2])

        for post_obj, user_obj in post_datas:
            self.assertEqual(PostAction, type(post_obj))
            self.assertEqual(UserData, type(user_obj))


if __name__ == '__main__':
    main()
