import json
from unittest import TestCase, main
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api

from main.controller import UserController
from main.exception import init_exc_handlers
from main.model.user_model import UserData
from main.service.user_service import UserService


class UserControllerTest(TestCase):
    def setUp(self) -> None:
        self.media_app = Flask(__name__)
        init_exc_handlers(self.media_app)
        media_api = Api(self.media_app)
        media_api.add_resource(UserController, "/user")
        self.client = self.media_app.test_client()
        self.user_obj = UserData(user_id=1234,
                                 email_id="test@gmail.conm",
                                 user_name="test_user",
                                 password="testhash",
                                 gender="m",
                                 public_key="test_public_key")

        self.add_user_request = {"user_name": "test@123", "gender": "M", "dob": "1971-12-17",
                                 "email_id": "gg@gmail.com", "password": "visha345"}

    def test_get_user_token(self):
        with self.media_app.test_request_context():
            UserService.get_user_token = MagicMock(return_value="testjwttoken")
            resp_data = self.client.get("/user", headers={'Content-Type': 'application/json',
                                                          'email_id': 'ee@gmial.com',
                                                          'password': 'vish123'})
            resp_json = json.loads(resp_data.text)["data"]
            self.assertEqual(200, resp_data.status_code)
            self.assertEqual("testjwttoken", resp_json["token"])

    def test_nopassword_user_token(self):
        with self.media_app.test_request_context():
            UserService.get_user_token = MagicMock(return_value="testjwttoken")
            resp_data = self.client.get("/user", headers={'Content-Type': 'application/json',
                                                          'email_id': 'ee@gmial.com'})
            self.assertEqual(400, resp_data.status_code)

    def test_noemail_user_token(self):
        with self.media_app.test_request_context():
            UserService.get_user_token = MagicMock(return_value="testjwttoken")
            resp_data = self.client.get("/user", headers={'Content-Type': 'application/json',
                                                          'password': 'vish123'})
            self.assertEqual(400, resp_data.status_code)

    def test_create_user(self):
        with self.media_app.test_request_context():
            UserService.add_user = MagicMock(return_value=self.user_obj)
            resp_data = self.client.post("/user", data=json.dumps(self.add_user_request),
                                         headers={'Content-Type': 'application/json'})
            resp_json = json.loads(resp_data.text)["data"]
            self.assertEqual(200, resp_data.status_code)
            self.assertIsNotNone(resp_json.get("public_key"))


if __name__ == '__main__':
    main()