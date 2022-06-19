from abc import ABC, abstractmethod

from main.request_data.user_request import AddUserRequestData


class UserInterface(ABC):
    @abstractmethod
    def add_user(self, user_data: AddUserRequestData):
        pass

    @abstractmethod
    def get_user_token(self, email_id: str, password: str):
        pass
