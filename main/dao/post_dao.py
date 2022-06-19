from typing import List

from main.model.post_model import PostData
from main.request_data.post_request import AddPostRequest
from main.model import db


class PostDao:
    @staticmethod
    def add_new_post(post_data: AddPostRequest) -> PostData:
        post_data = PostData(user_id=post_data.current_user.user_id,
                             post_type=post_data.post_type,
                             post_content=post_data.post_content)

        db.session.add(post_data)
        db.session.commit()
        return post_data

    @staticmethod
    def delete_post(post_data: PostData):
        post_data.active = 0
        # db.session.delete(post_data)
        db.session.commit()

    @staticmethod
    def get_post_by_id(post_id: int) -> PostData:
        post_data = db.session.query(PostData) \
            .filter(PostData.post_id == post_id) \
            .filter(PostData.active == 1) \
            .one_or_none()

        return post_data

    @staticmethod
    def get_all_posts() -> List[PostData]:
        post_datas = db.session.query(PostData) \
            .filter(PostData.active == 1) \
            .order_by(PostData.created_date.desc()) \
            .all()

        return post_datas
