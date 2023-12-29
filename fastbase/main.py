import threading
from typing import Type, Annotated, Self, Callable, Awaitable, TypeVar
from fastapi import APIRouter, Header, Depends, Body
from firebase_admin import auth
from redis import Redis

from .models import *
from .schemas import *
from .exceptions import InvalidToken, UserNotFoundError, CallbackError
from .globals import ic



U = TypeVar('U', bound=UserMod)


class FastbaseDependency:
    engine: AsyncEngine
    User: Type[UserMod]

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
    async def current_user(self, email: Annotated[str, Depends(verify_idtoken)]) -> Type[U]:
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
        return await self._current_user(email)

    # TESTME: Untested
    async def _current_user(self, email: str) -> Type[U]:
        """
        Get user by email for use in dependencies.
        :param email:   Email taken from the idtoken
        :return:        User
        :raises UserNotFoundError:
        """
        try:
            async with AsyncSession(self.engine) as session:
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
    engine: AsyncEngine
    redis: Redis | None
    User: Type[UserMod]
    user_defaults: dict
    post_create: Callable[[AsyncSession, U], Awaitable[None]] | None


    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    # TESTME: Untested
    def initialize(self, *,
                   engine: AsyncEngine,
                   redis: Redis | None = None,
                   user_model: Type[UserMod],
                   user_defaults: dict | None = None,
                   post_create: Callable[[AsyncSession, U], Awaitable[None]] | None = None):
        """Use instead of __init__ since it uses the singleton pattern."""
        self.engine = engine
        self.redis = redis
        self.User = user_model
        self.user_defaults = user_defaults or {}
        self.post_create = post_create


    # TESTME: Untested
    def get_signin_router(self, user_schema: Type[UserBaseSchema] = UserBaseSchema):
        """
        Router for when user signs in. An account is created in the db if the user doesn't exist.
        :param user_schema: Response model
        :return:
        """
        router = APIRouter()

        @router.post('/signin', response_model=user_schema)
        async def signin(token: Annotated[str, Body(embed=True)]) -> Type[Self]:
            try:
                token_data = auth.verify_id_token(token)
            except Exception:
                raise InvalidToken()

            if email := token_data.get('email'):
                async with AsyncSession(self.engine) as session:
                    exists = await self.User.exists(session, EmailStr(email))   # noqa

                    if not exists:
                        display, *_ = email.partition('@')
                        user = self.User(email=email, display=display, username=email, **self.user_defaults)
                        session.add(user)
                        await session.commit()
                        await session.refresh(user)

                        if self.post_create:
                            try:
                                await self.post_create(session, user)
                            except Exception:
                                raise CallbackError()
                    else:
                        user = await self.User.get_by_email(session, email)
                    return user
            raise InvalidToken()
        return router
