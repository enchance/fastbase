from typing import Optional, Any, Dict, AnyStr, TypeVar
from fastapi.exceptions import HTTPException


KEY = str | int | float | bool


class AppException(HTTPException):
    message = 'FAILED_ATTEMPT'
    code = 400

    def __init__(self, message: Any | None = None, *, status_code: int | None = None, key: KEY | None = None,
                 headers: dict[str, Any] | None = None,):
        message = message or self.message
        if key:
            message = f'{message} [{key}]'
        status_code = status_code or self.code
        super().__init__(status_code=status_code, detail=message, headers=headers)


class PermissionsException(AppException):
    code = 403
    message = 'YOU_SHALL_NOT_PASS: Insufficient permissions'


class InvalidToken(AppException):
    code = 403
    message = 'INVALID_TOKEN: Your token is bad and you should feel bad (is it expired?)'


class AuthError(AppException):
    code = 401
    message = 'ACCOUNT_AUTHENTICATION: Unable to authenticate the user'


class UserNotFoundError(AppException):
    code = 404
    message = 'USER_NOT_FOUND: That user doesn\'t exist'


class CallbackError(AppException):
    code = 500
    message = 'CALLBACK_ERROR: You heard me'