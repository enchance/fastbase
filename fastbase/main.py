from typing import Type, Annotated, Self, Callable, Awaitable, TypeVar
from fastapi import APIRouter, Header, Depends, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from firebase_admin import auth
from pydantic import EmailStr
from icecream import ic

from .models import *
from .schemas import *
from .dependencies import Dependencies
from .exceptions import InvalidToken



U = TypeVar('U', bound=UserMod)


class Fastbase(APIRouter):
    def __init__(self, *,
                 # firebase: FirebaseConfig,
                 user_model: Type[U],
                 user_defaults: dict | None = None,
                 user_schema: Type[BaseModel] | None = UserSchema,
                 session: Callable[[], AsyncSession],
                 post_create: Callable[[AsyncSession, U], Awaitable[None]]):
        super().__init__()
        self.User = user_model
        self.user_defaults = user_defaults or {}
        self.user_schema = user_schema
        # self.iss = firebase.iss
        # self.project_id = firebase.project_id
        # self.depends = Dependencies(iss=firebase.iss, project_id=firebase.project_id)
        self.get_session = session
        self.post_create = post_create

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
                    await self.post_create(session, user)
                else:
                    user = await self.User.get_by_email(session, email)
                # TODO: cache user
                return user
            raise InvalidToken()

        return router

    @staticmethod
    def get_email_routers() -> APIRouter:
        router = APIRouter()

        # TODO: Placeholder
        @router.post('/email-lostpassword')
        async def email_lost_password():
            # TODO: Email lost password
            return 'PLACEHOLDER: Email lost password'

        # TODO: Placeholder
        @router.post('/email-changepassword')
        async def email_lost_password():
            # TODO: Email change password
            return 'PLACEHOLDER: Email change password'

        return router
