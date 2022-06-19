from marshmallow import Schema, fields, validates, ValidationError, post_load

POST_TYPES = {"text"}
ACTION_TYPES = {"like", "comment"}


class AddPostSchema(Schema):
    _defs = {'required': True, "allow_none": False}
    post_content = fields.Str(**_defs)
    post_type = fields.Str(**_defs)

    @validates('post_type')
    def validate_post_type(self, post_type):
        if post_type not in POST_TYPES:
            raise ValidationError(f"Invalid Post Type !!! , Should be one of {POST_TYPES}")


class PostSchema(Schema):
    _defs = {'required': True, "allow_none": False}
    post_id = fields.Integer(**_defs)
    post_type = fields.Str(**_defs)

    @validates('post_type')
    def validate_post_type(self, post_type):
        if post_type not in POST_TYPES:
            raise ValidationError(f"Invalid Post Type !!! , Should be one of {POST_TYPES}")


class PostActionSchema(Schema):
    _defs = {'required': True, "allow_none": False}
    action_type = fields.Str(**_defs)
    post_id = fields.Integer(**_defs)
    action_content = fields.Str()

    @validates('action_type')
    def validate_action_type(self, action_type):
        if action_type not in ACTION_TYPES:
            raise ValidationError(f"Invalid Action Type !!! , Should be one of {ACTION_TYPES}")

    @post_load
    def _validate_comment(self, data, **kwargs):
        action_type = data.get("action_type")
        action_content = data.get("action_content")
        if action_type and action_type == "comment" and not action_content:
            raise ValidationError(f"Content cannot be empty for comment ")
        return data
