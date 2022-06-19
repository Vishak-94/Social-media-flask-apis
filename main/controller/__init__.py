from main.controller.post_controller import PostController
from main.controller.user_controller import UserController
from flask_restful import Api


media_api = Api()

media_api.add_resource(UserController, "/user")
media_api.add_resource(PostController, "/post")


