from marshmallow.exceptions import MarshmallowError, ValidationError
from sqlalchemy.exc import IntegrityError
from jwt.exceptions import PyJWTError
from main.exception.custom_exceptions import DuplicationError, InvalidRequestData, AccessForbidden, ResourceNotFound, \
    BadRequestError, UnAuthorizedRequestError
from main.exception.handlers import ExceptionHandler

exc_handler = ExceptionHandler()


def init_exc_handlers(app):

    app.errorhandler(IntegrityError)(exc_handler.db_integrity_error_handler)
    app.errorhandler(PyJWTError)(exc_handler.jwt_token_error)
    app.errorhandler(Exception)(exc_handler.generic_exc_handler)
    app.errorhandler(MarshmallowError)(exc_handler.marshmellow_error)
    app.errorhandler(ValidationError)(exc_handler.marshmellow_error)
    # customized exceptions
    app.errorhandler(DuplicationError)(exc_handler.custom_exc_handler)
    app.errorhandler(InvalidRequestData)(exc_handler.custom_exc_handler)
    app.errorhandler(AccessForbidden)(exc_handler.custom_exc_handler)
    app.errorhandler(ResourceNotFound)(exc_handler.custom_exc_handler)

    app.errorhandler(BadRequestError)(exc_handler.custom_exc_handler)
    app.errorhandler(UnAuthorizedRequestError)(exc_handler.custom_exc_handler)