from flask_restful import Resource, request

from main.constants.response import ApiResponse
from main.request_data.user_request import AddUserRequestData
from main.schema.user_schema import AddUserSchema, UserTokenSchema
from main.service.user_service import UserService


class UserController(Resource):
    def get(self):
        email_id = request.headers.get('email_id')
        password = request.headers.get('password')
        if not email_id or not password:
            return ApiResponse(resp_data="Email or/and Password is missing", status=400)
        UserTokenSchema().load({'email_id': email_id, 'password': password})
        service = UserService()
        jwt_token = service.get_user_token(email_id, password)
        return ApiResponse(resp_data={"token": jwt_token})

    def post(self):
        request_data = request.get_json()
        request_data = AddUserSchema().load(request_data)
        request_data = AddUserRequestData(**request_data)

        service = UserService()
        user_data = service.add_user(request_data)
        return ApiResponse(resp_data={"public_key": user_data.public_key})







