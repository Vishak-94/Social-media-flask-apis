from typing import List, Tuple

from main.constants.constant import MediaConstants
from main.model.post_model import PostAction
from main.model.user_model import UserData
from main.request_data.post_request import PostActionRequest
from main.model import db


class PostActionDao:
    @staticmethod
    def add_post_action(request_data: PostActionRequest) -> PostAction:
        action_data = PostAction(post_id=request_data.post_id,
                                 user_id=request_data.current_user.user_id,
                                 action_type=request_data.action_type,
                                 action_text=request_data.action_content)
        db.session.add(action_data)
        db.session.commit()
        return action_data

    @staticmethod
    def get_all_action_by_post_id(post_ids: list) -> List[Tuple[PostAction, UserData]]:
        action_datas = db.session.query(PostAction, UserData) \
            .join(UserData, PostAction.user_id == UserData.user_id) \
            .filter(PostAction.post_id.in_(post_ids)) \
            .order_by(PostAction.created_date.desc()) \
            .all()

        return action_datas

    @staticmethod
    def get_like_by_post_and_user_id(post_id: int, user_id: int) -> PostAction:
        like_action = db.session.query(PostAction) \
            .filter(PostAction.post_id == post_id) \
            .filter(PostAction.user_id == user_id) \
            .filter(PostAction.action_type == MediaConstants.LIKE) \
            .one_or_none()

        return like_action
