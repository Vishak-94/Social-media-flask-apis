from main.model.user_model import UserData
from main.request_data.user_request import AddUserRequestData
from main.model import db


class UserDataDao:
    @staticmethod
    def add_new_user(user_data: AddUserRequestData) -> UserData:
        """
        :param user_data: AddUserRequestData
        :return: None
        """
        # In future there should be a service which generates unique public_key and
        # unique public key has to be picked up from that service
        user = UserData(email_id=user_data.email_id,
                        user_name=user_data.user_name,
                        password=user_data.password,
                        gender=user_data.gender,
                        dob=user_data.dob)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_email(email_id: str) -> UserData:
        return db.session.query(UserData).filter(UserData.email_id == email_id).one_or_none()

    @staticmethod
    def get_user_by_public_key(public_key: str) -> UserData:
        return db.session.query(UserData).filter(UserData.public_key == public_key).one_or_none()
