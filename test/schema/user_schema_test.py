from unittest import TestCase
from datetime import date

from marshmallow import ValidationError

from main.schema.user_schema import AddUserSchema, UserTokenSchema


class UserSchemaTest(TestCase):
    def test_valid_user_signup(self):
        req_data = {"user_name": "testuser", "email_id": "test@gmail.com",
                    "dob": "1971-12-17", "gender": "M", "password": "password"}

        schema = AddUserSchema()
        valid_data = schema.load(req_data)
        self.assertEqual(5, len(valid_data))
        self.assertEqual(str, type(valid_data["user_name"]))
        self.assertEqual(str, type(valid_data["email_id"]))
        self.assertEqual(date, type(valid_data["dob"]))
        self.assertEqual(str, type(valid_data["gender"]))
        self.assertEqual(str, type(valid_data["password"]))

        self.assertEqual("testuser", valid_data["user_name"])
        self.assertEqual("test@gmail.com", valid_data["email_id"])
        self.assertEqual(date(1971, 12, 17), valid_data["dob"])
        self.assertEqual("M", valid_data["gender"])
        self.assertEqual("pbkdf2:sha256", valid_data["password"][:13])

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            req_data = {"user_name": "testuser", "email_id": "test.com",
                        "dob": "1971-12-17", "gender": "M", "password": "password"}
            schema = AddUserSchema()
            schema.load(req_data)

    def test_invalid_gender(self):
        with self.assertRaises(ValidationError):
            req_data = {"user_name": "testuser", "email_id": "test@g.com",
                        "dob": "1971-12-17", "gender": "Male", "password": "password"}
            schema = AddUserSchema()
            schema.load(req_data)

    def test_invalid_date(self):
        with self.assertRaises(ValidationError):
            req_data = {"user_name": "testuser", "email_id": "test@g.com",
                        "dob": "1971/12/17", "gender": "M", "password": "password"}
            schema = AddUserSchema()
            schema.load(req_data)

    def test_user_token(self):
        req_data = {"email_id": "test@gmail.com", "password": "testpasse"}
        schema = UserTokenSchema()
        valid_data = schema.load(req_data)
        self.assertEqual(2, len(valid_data))
        self.assertEqual("test@gmail.com", valid_data["email_id"])
        self.assertEqual("testpasse", valid_data["password"])

    def test_user_token_invalid_email(self):
        with self.assertRaises(ValidationError):
            req_data = {"email_id": "testgmail.com", "password": "testpasse"}
            schema = AddUserSchema()
            schema.load(req_data)

    def test_token_no_password(self):
        with self.assertRaises(ValidationError):
            req_data = {"email_id": "test@gmail.com"}
            schema = AddUserSchema()
            schema.load(req_data)
