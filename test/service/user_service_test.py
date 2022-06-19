from unittest import TestCase, main
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash
from main.dao.user_dao import UserDataDao
from main.exception import ResourceNotFound, AccessForbidden
from main.model.user_model import UserData
from main.request_data.user_request import AddUserRequestData
from main.service.user_service import UserService
from datetime import datetime
from flask import Flask


class UserServiceTest(TestCase):
    user_service = UserService()

    def setUp(self) -> None:
        self.input_email = "test@email.com"
        self.input_password = "testhash"
        self.user_obj = UserData(user_id=1234,
                                 email_id=self.input_email,
                                 user_name="test_user",
                                 password=generate_password_hash(self.input_password),
                                 gender="m",
                                 public_key="test_public_key")

    def test_create_user(self):
        req_data = AddUserRequestData("testmail", self.input_email, "m",
                                      datetime.now().date(), self.input_password)
        user = UserData(user_id=1234,
                        email_id=req_data.email_id,
                        user_name=req_data.user_name,
                        password=req_data.password,
                        gender=req_data.gender,
                        dob=req_data.dob)
        UserDataDao.add_new_user = MagicMock(return_value=user)

        res_obj = self.user_service.add_user(req_data)
        self.assertEqual(type(res_obj), UserData)
        self.assertEqual(res_obj.user_name, req_data.user_name)
        self.assertEqual(res_obj.email_id, req_data.email_id)
        self.assertEqual(res_obj.gender, req_data.gender)
        self.assertEqual(res_obj.password, req_data.password)

    def test_get_token(self):
        app = Flask(__name__)
        with app.app_context():
            app.config["JWT_EXPIRATION_LIMIT"] = 30
            app.config['SECRET_KEY'] = "testsecretkey"
            UserDataDao.get_user_by_email = MagicMock(return_value=self.user_obj)
            token = self.user_service.get_user_token(self.input_email, self.input_password)

        self.assertEqual(3, len(token.split(".")))

    def test_empty_user(self):
        UserDataDao.get_user_by_email = MagicMock(return_value=None)
        with self.assertRaises(ResourceNotFound):
            self.user_service.get_user_token(self.input_email, self.input_password)

    def test_incorrect_password(self):
        UserDataDao.get_user_by_email = MagicMock(return_value=self.user_obj)
        with self.assertRaises(AccessForbidden):
            self.user_service.get_user_token(self.input_email, "mynametest")


if __name__ == '__main__':
    main()
