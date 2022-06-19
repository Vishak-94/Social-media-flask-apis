from flask_restful import Resource

from main.constants.decorator import token_required
from main.constants.response import ApiResponse
from main.factory.post_factory import PostFactory, PostActionFactory
from main.model.user_model import UserData
from flask import request

from main.request_data.post_request import AddPostRequest, PostActionRequest, PostRequestData
from main.schema.post_schema import AddPostSchema, PostActionSchema, PostSchema
from main.service.post_service import PostService


class PostController(Resource):
    @staticmethod
    @token_required
    def get(curr_user: UserData):
        post_service = PostService()
        all_post_data = post_service.get_all_post()
        return ApiResponse(resp_data=all_post_data)

    @staticmethod
    @token_required
    def post(curr_user: UserData):
        request_data = request.get_json()
        request_data = AddPostSchema().load(request_data)
        request_data = AddPostRequest(**request_data, current_user=curr_user)
        post_service = PostFactory().get_service(request_data.post_type)
        post_data = post_service.add_post(request_data)
        return ApiResponse(resp_data=post_data.as_dict())

    @staticmethod
    @token_required
    def put(curr_user: UserData):
        request_data = PostActionSchema().load(request.get_json())
        request_data = PostActionRequest(**request_data, current_user=curr_user)
        action_service = PostActionFactory().get_service(request_data.action_type)
        action_data = action_service.add_action(request_data)
        return ApiResponse(resp_data=f"{action_data.action_type} added to post")

    @staticmethod
    @token_required
    def delete(curr_user: UserData):
        request_data = PostSchema().load(request.get_json())
        request_data = PostRequestData(**request_data, current_user=curr_user)
        post_service = PostFactory().get_service(request_data.post_type)
        post_service.delete_post(request_data)
        return ApiResponse(resp_data=f"{request_data.post_id} deleted !!!")
