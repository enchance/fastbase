import threading
from typing import Type, Annotated, Self, Callable, Awaitable, TypeVar
from fastapi import APIRouter, Header, Depends, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from firebase_admin import auth
from pydantic import EmailStr
from icecream import ic
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from .models import *
from .schemas import *
from .exceptions import InvalidToken



U = TypeVar('U', bound=UserMod)


class FastbaseV2:
    _instance = None
    _lock = threading.Lock()
    engine: AsyncEngine
    # User: Type[U]
    # Group = Gr
    # Role = Rl

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, engine: AsyncEngine):
        self.engine = engine
        # self.User = user_model


class Fastbase(APIRouter):
    def __init__(self, *,
                 # firebase: FirebaseConfig,
                 user_model: Type[U],
                 user_schema: Type[UserBaseSchema] = UserBaseSchema,
                 user_defaults: dict | None = None,
                 session: Callable[[], AsyncSession],
                 post_create: Callable[[AsyncSession, U], Awaitable[None]] = None):
        super().__init__()
        self.User = user_model
        self.user_defaults = user_defaults or {}
        self.user_schema = user_schema
        # self.iss = firebase.iss
        # self.project_id = firebase.project_id
        # self.depends = Dependencies(iss=firebase.iss, project_id=firebase.project_id)
        self.get_session = session
        self.post_create = post_create

    def __repr__(self):
        return modstr(self)

    @staticmethod
    async def demo():
        # TESTME: Untested
        return 'it works'

    def get_signin_router(self):
        router = APIRouter()
        get_session = self.get_session

        @router.post('/signin', response_model=self.user_schema)
        async def signin(token: Annotated[str, Body()],
                         session: Annotated[AsyncSession, Depends(get_session)]) -> Type[Self]:
            try:
                token_data = auth.verify_id_token(token)
            except Exception:
                raise InvalidToken()

            if email := token_data.get('email'):
                exists = await self.User.exists(session, EmailStr(email))

                if not exists:
                    display, *_ = email.partition('@')
                    user = self.User(email=email, username=email, display=display, **self.user_defaults)
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                    self.post_create and await self.post_create(session, user)
                else:
                    user = await self.User.get_by_email(session, email)
                return user
            raise InvalidToken()

        return router

    # @staticmethod
    # def get_email_routers() -> APIRouter:
    #     router = APIRouter()
    #
    #     # TODO: Placeholder
    #     @router.post('/email-lostpassword')
    #     async def email_lost_password():
    #         # TODO: Email lost password
    #         return 'PLACEHOLDER: Email lost password'
    #
    #     # TODO: Placeholder
    #     @router.post('/email-changepassword')
    #     async def email_lost_password():
    #         # TODO: Email change password
    #         return 'PLACEHOLDER: Email change password'
    #
    #     return router