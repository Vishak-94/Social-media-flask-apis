from unittest import TestCase

from marshmallow import ValidationError

from main.schema.post_schema import AddPostSchema, PostSchema, PostActionSchema


class PostSchemaTest(TestCase):
    def test_add_post(self):
        req_data = {"post_content": "This is a test message", "post_type": "text"}
        schema = AddPostSchema()
        valid_data = schema.load(req_data)
        self.assertEqual(2, len(valid_data))
        self.assertEqual(str, type(valid_data["post_content"]))
        self.assertEqual(str, type(valid_data["post_type"]))
        self.assertEqual("This is a test message", valid_data["post_content"])
        self.assertEqual("text", valid_data["post_type"])

    def test_invalid_add_post(self):
        req_data = {"post_content": "test.jpeg", "post_type": "image"}
        schema = AddPostSchema()
        with self.assertRaises(ValidationError):
            schema.load(req_data)

    def test_post_request(self):
        req_data = {"post_type": "text", "post_id": 1}
        schema = PostSchema()
        valid_data = schema.load(req_data)
        self.assertEqual(2, len(valid_data))
        self.assertEqual(int, type(valid_data["post_id"]))
        self.assertEqual(str, type(valid_data["post_type"]))
        self.assertEqual(1, valid_data["post_id"])
        self.assertEqual("text", valid_data["post_type"])

    def test_invalid_post(self):
        req_data = {"post_type": "image", "post_id": 1}
        with self.assertRaises(ValidationError):
            schema = PostSchema()
            schema.load(req_data)

        req_data = {"post_type": "image", "post_id": "hRTRYRYTR"}
        with self.assertRaises(ValidationError):
            schema = PostSchema()
            schema.load(req_data)

    def test_like_post_actions(self):
        like_req_data = {"action_type": "like", "post_id": 1}
        schema = PostActionSchema()
        valid_data = schema.load(like_req_data)
        self.assertEqual(2, len(valid_data))
        self.assertEqual(int, type(valid_data["post_id"]))
        self.assertEqual(str, type(valid_data["action_type"]))
        self.assertEqual("like", valid_data["action_type"])
        self.assertEqual(1, valid_data["post_id"])

    def test_comment_post_actions(self):
        comment_req_data = {"action_type": "comment", "post_id": 1, "action_content": "This is test"}

        schema = PostActionSchema()
        valid_data = schema.load(comment_req_data)
        self.assertEqual(3, len(valid_data))
        self.assertEqual(int, type(valid_data["post_id"]))
        self.assertEqual(str, type(valid_data["action_type"]))
        self.assertEqual(str, type(valid_data["action_content"]))
        self.assertEqual("comment", valid_data["action_type"])
        self.assertEqual("This is test", valid_data["action_content"])
        self.assertEqual(1, valid_data["post_id"])

    def test_empty_comment_action(self):

        with self.assertRaises(ValidationError):
            comment_req_data = {"action_type": "comment", "post_id": 1}
            schema = PostActionSchema()
            schema.load(comment_req_data)

    def test_invalid_post_action(self):

        with self.assertRaises(ValidationError):
            comment_req_data = {"action_type": "image", "post_id": 1}
            schema = PostActionSchema()
            schema.load(comment_req_data)

    def test_invalid_post_id_type(self):

        with self.assertRaises(ValidationError):
            comment_req_data = {"action_type": "image", "post_id": "test"}
            schema = PostActionSchema()
            schema.load(comment_req_data)

    def test_empty_post_action(self):

        with self.assertRaises(ValidationError):
            comment_req_data = {}
            schema = PostActionSchema()
            schema.load(comment_req_data)

    def test_no_post_id_action(self):

        with self.assertRaises(ValidationError):
            comment_req_data = {"action_type": "like"}
            schema = PostActionSchema()
            schema.load(comment_req_data)



