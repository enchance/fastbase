from typing import Optional, Any, Dict
from fastapi.exceptions import HTTPException


class AppException(HTTPException):
    message = 'FAILED_ATTEMPT'
    code = 400

    def __init__(self, message: Any = None, status_code: int = None,
                 headers: Optional[Dict[str, Any]] = None):
        message = message or self.message
        status_code = status_code or self.code
        super().__init__(status_code=status_code, detail=message, headers=headers)


class PermissionsException(AppException):
    code = 403
    message = 'YOU_SHALL_NOT_PASS'


class InvalidToken(AppException):
    code = 403
    message = 'INVALID_TOKEN'


class AuthError(AppException):
    code = 401
    message = 'ACCOUNT_AUTHENTICATION'