from dataclasses import dataclass

from main.model.user_model import UserData


@dataclass
class PostRequestData:
    post_type: str
    post_id: int
    current_user: UserData


@dataclass
class AddPostRequest:
    post_type: str
    post_content: str
    current_user: UserData


@dataclass
class PostActionRequest:
    action_type: str
    post_id: int
    current_user: UserData
    action_content: str = str()
