from abc import ABC, abstractmethod

from main.model.post_model import PostAction, PostData
from main.request_data.post_request import AddPostRequest, PostActionRequest, PostRequestData


class PostInterface(ABC):
    @abstractmethod
    def get_all_post(self) -> list:
        pass


class PostTypeInterface(ABC):

    @abstractmethod
    def get_post(self, post_id: int) -> PostData:
        pass

    @abstractmethod
    def add_post(self, req_data: AddPostRequest) -> PostData:
        pass

    @abstractmethod
    def delete_post(self, request_data: PostRequestData):
        pass


class ActionTypeInterface(ABC):
    @abstractmethod
    def add_action(self, action_data: PostActionRequest) -> PostAction:
        pass


class ActionInterface(ABC):
    @abstractmethod
    def get_all_actions(self, post_ids: list):
        pass
