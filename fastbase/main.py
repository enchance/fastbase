import threading
from typing import Type, Annotated, Self, Callable, Awaitable, TypeVar, TypeAlias
from fastapi import APIRouter, Header, Depends, Body
from firebase_admin import auth
from redis import Redis
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import *
from .schemas import *
from .exceptions import InvalidToken, UserNotFoundError, CallbackError
from .globals import ic



USER = TypeVar('USER', bound=UserMod)


class FastbaseDependency:
    engine: AsyncEngine
    User: Type[USER]

    # TESTME: Untested
    @staticmethod
    def verify_idtoken(authorization: Annotated[str, Header()]) -> str:
        """
        Dependency to verify if a Google **idtoken** is valid. Out of the decrypted data only the email is returned.

        !!! tip "Use with"
            Use with the `current_user` dependency which gets the User based on the email.

        ??? example

            ```python
            @app.get('/', email: Annotated[str, Depends(verify_idtoken)]):
                # Header:  Authorization=Bearer abc123...
                ...
            ```

        :param authorization:   Bearer token taken taken from Google idtoken
        :return:                Decrypted token data
        :raises InvalidToken:   Token cannot be used e.g. it's expired, malformed, etc.
        """
        try:
            token = authorization.split(' ')[1]
            token_data = auth.verify_id_token(token)
            return token_data.pop('email')
        except Exception:
            raise InvalidToken()

    # TESTME: Untested
    async def current_user(self, email: Annotated[str, Depends(verify_idtoken)]) -> Type[USER]:
        """
        Dependency for getting the user by their verified idtoken.

        !!! tip "Use with"
            Use with the `verify_idtoken` dependency which gets the User based on the email.

        ??? example

            ```python
            @app.get('/', user: Annotated[User, Depends(current_user)]):
                ...
            ```
        :param email:   Email taken from the bearer token
        :return:        Valid user
        :raises UserNotFoundError:  The user who owns the email doesn't exist
        """
        try:
            async with self.async_session() as session:                 # noqa
                user = await self.User.get_by_email(session, email)
                return user
        except Exception as _:
            raise UserNotFoundError()


    # TODO: Dependency verify_device for app_check
    # def verify_device(tago_appcheck: Annotated[str, Header()], tago_token: Annotated[str, Header()]) -> dict:
    #     """
    #     Verify AppCheck and FirebaseAuth tokens. Both must pass to continue.
    #     :param tago_appcheck:   App AppCheck jwt
    #     :param tago_token:      User idtoken jwt
    #     :return:                Verified tago_token
    #     """
    #     try:
    #         appcheck_data = app_check.verify_token(tago_appcheck)
    #     except Exception as err:
    #         raise InvalidToken('INVALID_DEVICE_TOKEN')
    #
    #     try:
    #         token_data = auth.verify_id_token(tago_token)
    #         # if token_data['aud'] != s.PROJECT_ID:
    #         #     raise Exception()
    #         return token_data
    #     except auth.RevokedIdTokenError as err:
    #         # logger.critical(err)
    #         raise InvalidToken('TOKEN_REVOKED')
    #     except Exception as err:
    #         # logger.critical(err)
    #         raise InvalidToken()


class Fastbase(FastbaseDependency):
    _instance = None
    _lock = threading.Lock()
    async_session: AsyncSession
    User: Type[USER]

    def __new__(cls):
        """Singleton pattern"""
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    # TESTME: Untested
    def initialize(self, *, async_session: AsyncSession, user_model: Type[USER]):
        """Use instead of __init__ since it uses the singleton pattern."""
        self.async_session = async_session
        self.User = user_model
