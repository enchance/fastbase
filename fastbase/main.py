import threading
from typing import Type, Annotated, Self, Callable, Awaitable, TypeVar
from fastapi import APIRouter, Header, Depends, Body
from firebase_admin import auth
from pydantic import EmailStr
from icecream import ic
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from redis import Redis

from .models import *
from .schemas import *
from .exceptions import InvalidToken, UserNotFoundError
from .globals import ic


U = TypeVar('U', bound=UserMod)


class Fastbase:
    _instance = None
    _lock = threading.Lock()
    engine: AsyncEngine
    redis: Redis | None
    User: Type[UserMod]
    user_schema: Type[UserBaseSchema]
    user_defaults: dict
    # Group = Gr
    # Role = Rl
    post_create: Callable[[AsyncSession, UserMod], Awaitable[None]]


    def __new__(cls):
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
                   post_create: Callable[[AsyncSession, U], Awaitable[None]] = None):
        self.engine = engine
        self.redis = redis
        self.User = user_model
        self.user_defaults = user_defaults or {}
        self.post_create = post_create


    # async def get_session(self) -> AsyncSession:
    #     async_session = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False, class_=AsyncSession) # noqa
    #     async with async_session() as session:
    #         yield session


    # TESTME: Untested
    @staticmethod
    def verify_idtoken(authorization: Annotated[str, Header()]) -> str:
        """
        Dependency to verify if an idtoken is valid.
        :param authorization:   Google idtoken
        :return:                Token data
        :raises InvalidToken:
        """
        # TESTME: Untested
        try:
            token = authorization.split(' ')[1]
            token_data = auth.verify_id_token(token)
            return token_data.pop('email')
        except Exception:
            raise InvalidToken()


    # TESTME: Untested
    async def current_user(self, email: Annotated[str, Depends(verify_idtoken)]) -> Type[UserMod]:
        """
        Dependency that returns a saved User entry from either redis or db.
        :param email:   Email taken from the idtoken
        :return:        User
        :raises UserNotFoundError:
        """
        # TESTME: Untested
        try:
            async with AsyncSession(self.engine) as session:
                user = await self.User.get_by_email(session, email)
                return user
        except Exception as e:
            ic(e)
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


    # TESTME: Untested
    def get_signin_router(self, user_schema: Type[UserBaseSchema] = UserBaseSchema):
        router = APIRouter()

        @router.post('/signin', response_model=user_schema)
        async def signin(token: Annotated[str, Body()]) -> Type[Self]:
            try:
                token_data = auth.verify_id_token(token)
            except Exception:
                raise InvalidToken()

            if email := token_data.get('email'):
                async with AsyncSession(self.engine) as session:
                    exists = await self.User.exists(session, EmailStr(email))

                    if not exists:
                        display, *_ = email.partition('@')
                        user = self.User(email=email, username=email, display=display, **self.user_defaults)
                        ic(user)
                        session.add(user)
                        await session.commit()
                        await session.refresh(user)
                        self.post_create and await self.post_create(session, user)
                    else:
                        user = await self.User.get_by_email(session, email)
                    return user
            raise InvalidToken()
        return router
