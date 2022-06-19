from main.dao.user_dao import UserDataDao
from main.exception.custom_exceptions import ResourceNotFound, AccessForbidden
from main.model.user_model import UserData
from main.request_data.user_request import AddUserRequestData
from main.service.interface.user_abc import UserInterface
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app as app


class UserService(UserInterface):

    def add_user(self, user_data: AddUserRequestData) -> UserData:
        user_obj = UserDataDao.add_new_user(user_data)
        return user_obj

    def get_user_token(self, email_id: str, password: str) -> str:
        user_obj = UserDataDao.get_user_by_email(email_id)
        if not user_obj:
            raise ResourceNotFound("User does not exist !!")

        if not check_password_hash(user_obj.password, password):
            raise AccessForbidden("Invalid password !!!")

        jwt_token = jwt.encode({'public_id': user_obj.public_key,
                                'exp': datetime.utcnow() + timedelta(minutes=app.config["JWT_EXPIRATION_LIMIT"])},
                               app.config['SECRET_KEY'])

        return jwt_token

