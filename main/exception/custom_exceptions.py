class ResourceNotFound(LookupError):
    status = 404


class AccessForbidden(PermissionError):
    status = 403


class InvalidRequestData(ValueError):
    status = 400


class DuplicationError(ValueError):
    status = 400


class BadRequestError(Exception):
    status = 400


class UnAuthorizedRequestError(Exception):
    status = 401
