import json
from unittest import TestCase, main
from unittest.mock import MagicMock

import jwt
from flask import Flask
from flask_restful import Api

from main.controller import PostController
from main.dao.user_dao import UserDataDao
from main.model.post_model import PostData, PostAction
from main.model.user_model import UserData
from main.service.action_service import LikeActionService, CommentActionService
from main.service.post_service import PostService, TextPostService


class PostControllerTest(TestCase):
    def setUp(self) -> None:
        self.media_app = Flask(__name__)
        media_api = Api(self.media_app)
        media_api.add_resource(PostController, "/post")

        self.media_app.config['SECRET_KEY'] = "testsecretkey"
        self.client = self.media_app.test_client()
        self.user_obj = UserData(user_id=1234,
                                 email_id="test@gmail.conm",
                                 user_name="test_user",
                                 password="testhash",
                                 gender="m",
                                 public_key="test_public_key")

        self.headers = {'Content-Type': 'application/json',
                        "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI1"
                                          "ZTk2YTY2YS1hYzc2LTRjOTMtYjJhZi1jYmMzOGEyYzhkZDciLCJleHAiOj"
                                          "E2NTU5NzY5ODN9.AC5Khds1Ki6bskI2f52B4koAzlTBB9tnpzlKZie4vAU"}

        self.add_user_request = {"user_name": "test@123", "gender": "M", "dob": "1971-12-17",
                                 "email_id": "gg@gmail.com", "password": "visha345"}

        self.post_test_obj = PostData(post_id=1,
                                      user_id=1234,
                                      post_type="text",
                                      post_content="test_content",
                                      active=True)

        self.like_obj = PostAction(action_id=1,
                                   post_id=1,
                                   user_id=1234,
                                   action_type="like",
                                   action_text="")

        self.comment_obj = PostAction(action_id=2,
                                      post_id=1,
                                      user_id=1234,
                                      action_type="comment",
                                      action_text="Test comment")

        jwt.decode = MagicMock(return_value={"public_id": "testjwttoken"})
        UserDataDao.get_user_by_public_key = MagicMock(return_value=self.user_obj)

    def test_get_user_token(self):
        with self.media_app.test_request_context():
            PostService.get_all_post = MagicMock(return_value=[vars(self.post_test_obj)])
            resp_data = self.client.get("/post", headers=self.headers)
            resp_json = json.loads(resp_data.text)["data"][0]
            self.assertEqual(200, resp_data.status_code)
            self.assertEqual(dict, type(resp_json))
            self.assertEqual(1, resp_json["post_id"])
            self.assertEqual(1234, resp_json["user_id"])
            self.assertEqual("text", resp_json["post_type"])

    def test_no_token(self):
        with self.media_app.test_request_context():
            resp_data = self.client.get("/post")
            self.assertEqual(400, resp_data.status_code)

    def test_invalid_token(self):
        with self.media_app.test_request_context():
            jwt.decode = MagicMock(return_value={"public_id": "testjwttoken"})
            UserDataDao.get_user_by_public_key = MagicMock(return_value=None)
            resp_data = self.client.get("/post", headers=self.headers)
            self.assertEqual(401, resp_data.status_code)

    def test_new_post(self):
        req_data = {"post_content": "test_content", "post_type": "text"}
        with self.media_app.test_request_context():
            TextPostService.add_post = MagicMock(return_value=self.post_test_obj)
            resp_data = self.client.post("/post", headers=self.headers, data=json.dumps(req_data))
            resp_data = resp_data.json["data"]
            self.assertEqual(1234, resp_data["user_id"])
            self.assertEqual("text", resp_data["post_type"])
            self.assertEqual("test_content", resp_data["post_content"])

    def test_new_post_action(self):
        like_data = {"action_type": "like", "post_id": 1}
        comment_data = {"action_type": "comment", "post_id": 1, "action_content": "This is test comment !!!"}
        with self.media_app.test_request_context():
            LikeActionService.add_action = MagicMock(return_value=self.like_obj)
            resp_data1 = self.client.put("/post", headers=self.headers, data=json.dumps(like_data))
            resp_json1 = resp_data1.json
            self.assertEqual(200, resp_data1.status_code)
            self.assertEqual({"data": "like added to post"}, resp_json1)
            CommentActionService.add_action = MagicMock(return_value=self.comment_obj)
            resp_data2 = self.client.put("/post", headers=self.headers, data=json.dumps(comment_data))
            resp_json2 = resp_data2.json
            self.assertEqual({"data": "comment added to post"}, resp_json2)

    def test_delete_post(self):
        with self.media_app.test_request_context():
            TextPostService.delete_post = MagicMock(return_value=None)
            req_data = {"post_id": 1, "post_type": "text"}
            resp_data = self.client.delete("/post", headers=self.headers, data=json.dumps(req_data))
            resp_json = resp_data.json
            self.assertEqual(200, resp_data.status_code)
            self.assertEqual({"data": '1 deleted !!!'}, resp_json)


if __name__ == '__main__':
    main()
