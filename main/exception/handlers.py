from main.constants.response import ApiResponse


class ExceptionHandler:

    @staticmethod
    def custom_exc_handler(exception):
        return ApiResponse(resp_data=str(exception),
                           status=exception.status if hasattr(exception, 'status') else 500)

    @staticmethod
    def jwt_token_error(exception):
        return ApiResponse(resp_data="Jwt token error: " + str(exception),
                           status=400)

    @staticmethod
    def db_integrity_error_handler(exception):
        err_msg = str(exception).split("\n")[0].split(".")[-1]
        return ApiResponse(resp_data=f"{err_msg} Already Exists !!!",
                           status=exception.status if hasattr(exception, 'status') else 400)

    @staticmethod
    def generic_exc_handler(exception):
        return ApiResponse(resp_data=str(exception), status=500)

    @staticmethod
    def marshmellow_error(exception):
        return ApiResponse(resp_data=str(exception), status=400)

