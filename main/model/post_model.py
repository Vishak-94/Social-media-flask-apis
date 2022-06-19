from main.model import db
from sqlalchemy.sql import func


class PostData(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'))
    post_type = db.Column(db.String(100), nullable=False, default="text")
    post_content = db.Column(db.String(255), nullable=False)
    active = db.Column(db.SmallInteger, nullable=False, default=1)
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def as_dict(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


class PostAction(db.Model):
    action_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post_data.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)
    action_text = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def as_dict(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
