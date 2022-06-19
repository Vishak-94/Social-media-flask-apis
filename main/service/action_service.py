from typing import List, Tuple

from main.constants.constant import MediaConstants
from main.dao.action_dao import PostActionDao
from main.exception.custom_exceptions import DuplicationError, InvalidRequestData
from main.model.post_model import PostAction
from main.model.user_model import UserData
from main.request_data.post_request import PostActionRequest
from main.service.interface.post_abc import ActionTypeInterface, ActionInterface


class PostActionService(ActionInterface):

    def get_all_actions(self, post_ids: list) -> List[Tuple[PostAction, UserData]]:
        return PostActionDao.get_all_action_by_post_id(post_ids)


class LikeActionService(ActionTypeInterface):
    action_type = MediaConstants.LIKE

    def add_action(self, action_data: PostActionRequest) -> PostAction:
        like_action = PostActionDao.get_like_by_post_and_user_id(action_data.post_id,
                                                                 action_data.current_user.user_id)
        if like_action:
            raise DuplicationError("You have already liked the Post")
        like_action = PostActionDao.add_post_action(action_data)
        return like_action


class CommentActionService(ActionTypeInterface):
    action_type = MediaConstants.COMMENT

    def add_action(self, action_data: PostActionRequest) -> PostAction:
        action_data = PostActionDao.add_post_action(action_data)
        return action_data



