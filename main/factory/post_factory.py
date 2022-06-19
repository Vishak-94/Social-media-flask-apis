from main.constants.constant import MediaConstants
from main.exception import InvalidRequestData
from main.service.action_service import CommentActionService, LikeActionService
from main.service.interface.post_abc import PostTypeInterface, ActionTypeInterface
from main.service.post_service import TextPostService


class PostFactory:
    post_service_map = {MediaConstants.TEXT: TextPostService}

    def get_service(self, post_type=MediaConstants.TEXT) -> PostTypeInterface:
        post_ins = self.post_service_map.get(post_type)
        if not post_ins:
            raise InvalidRequestData(f"Invalid Post Type {post_type}")

        return post_ins()


class PostActionFactory:
    action_map = {MediaConstants.COMMENT: CommentActionService,
                  MediaConstants.LIKE: LikeActionService}

    def get_service(self, action_type: str) -> ActionTypeInterface:
        action_ins = self.action_map.get(action_type)
        if not action_ins:
            raise InvalidRequestData(f"Invalid action type: {action_type}")

        return action_ins()
