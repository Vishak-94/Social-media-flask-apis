from main.model import db
from uuid import uuid4
from sqlalchemy.sql import func


class UserData(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.String(100), nullable=False, unique=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.String(1), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    public_key = db.Column(db.String(255), nullable=False, unique=True, default=str(uuid4()))
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    active = db.Column(db.SmallInteger, nullable=False, default=1)

    def as_dict(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
