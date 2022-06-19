from typing import Any

from flask import Response
import json


class ApiResponse(Response):
    default_mimetype = "application/json; charset=utf-8"

    def __init__(self, resp_data: Any = None, status=200, **kwargs):
        super().__init__(status=status, **kwargs)
        if status in {200, 201, 202}:
            self.data = json.dumps({"data": resp_data}, default=str)
        else:
            self.data = json.dumps({"error": resp_data}, default=str)



