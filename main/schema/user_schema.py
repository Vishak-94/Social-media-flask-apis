from marshmallow import Schema, fields, pre_load, ValidationError
from werkzeug.security import generate_password_hash

GENDER_TYPE = {"M", "F", "T"}


class AddUserSchema(Schema):
    _defs = {'required': True, "allow_none": False}
    user_name = fields.Str(**_defs)
    email_id = fields.Email(**_defs)
    dob = fields.Date(**_defs)
    gender = fields.Str(**_defs)
    password = fields.Str(**_defs)

    @pre_load
    def encrpt_password(self, data, **kwargs):
        password = data.get("password")
        if password:
            data["password"] = generate_password_hash(password)
        return data

    @pre_load
    def _validate_comment(self, data, **kwargs):
        gender = data.get("gender")
        if gender and gender not in GENDER_TYPE:
            raise ValidationError(f"Gender Supported are :{GENDER_TYPE} ")
        return data


class UserTokenSchema(Schema):
    _defs = {'required': True, "allow_none": False}
    email_id = fields.Email(**_defs)
    password = fields.Str(**_defs)
