from main.constants.constant import MediaConstants
from main.dao.post_dao import PostDao
from main.exception.custom_exceptions import AccessForbidden, ResourceNotFound, InvalidRequestData
from main.model.post_model import PostData, PostAction
from main.model.user_model import UserData
from main.request_data.post_request import AddPostRequest, PostRequestData
from main.service.action_service import PostActionService
from main.service.interface.post_abc import PostTypeInterface, PostInterface
from collections import OrderedDict


class PostInfo:
    def __init__(self, post_data: PostData):
        self.post_data = post_data
        self.like_data = []
        self.comment_data = []

    def add_post_action(self, post_action: PostAction, user_data: UserData):
        if not post_action or not user_data:
            return
        if post_action.action_type == MediaConstants.LIKE:
            self.like_data.append(user_data.user_name)
        else:
            self.comment_data.append({user_data.user_name: post_action.action_text})

    def get_data_as_dict(self):
        self.post_data = self.post_data.as_dict()
        return vars(self)


class PostService(PostInterface):
    def get_all_post(self) -> list:
        post_info_map = OrderedDict()
        for post_data in PostDao.get_all_posts():
            post_info_map[post_data.post_id] = PostInfo(post_data=post_data)

        if not post_info_map:
            return []
        action_service = PostActionService()
        all_action_data = action_service.get_all_actions(list(post_info_map.keys()))

        for action_data, user_Data in all_action_data:
            post_info_map[action_data.post_id].add_post_action(action_data, user_Data)

        return [post_info.get_data_as_dict() for post_info in post_info_map.values()]


class TextPostService(PostTypeInterface):
    post_type = MediaConstants.TEXT

    def get_post(self, post_id: int) -> PostData:
        post_data = PostDao.get_post_by_id(post_id)

        if not post_data:
            raise ResourceNotFound("Post Not Found/Deleted")

        return post_data

    def add_post(self, post_data: AddPostRequest) -> PostData:
        return PostDao.add_new_post(post_data)

    def delete_post(self, request_data: PostRequestData):
        post_data = self.get_post(request_data.post_id)

        if post_data.user_id != request_data.current_user.user_id:
            raise AccessForbidden(f"{request_data.current_user.user_name} not allowed to Delete post")
        PostDao.delete_post(post_data)



