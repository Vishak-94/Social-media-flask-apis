from functools import wraps
from flask import request
import jwt
from flask import current_app as app

from main.constants.response import ApiResponse
from main.dao.user_dao import UserDataDao


def token_required(func):
    @wraps(func)
    def fetch_token(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return ApiResponse(resp_data='Token is missing !!', status=400)

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = UserDataDao.get_user_by_public_key(data['public_id'])

        if not current_user:
            return ApiResponse(resp_data='Token is invalid !!', status=401)

        return func(current_user, *args, **kwargs)

    return fetch_token
