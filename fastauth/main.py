from typing import Type, Annotated, Self
from fastapi import APIRouter, Header, Depends, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from firebase_admin import auth
from pydantic import EmailStr
from icecream import ic

from .models import *
from .schemas import *
from .dependencies import Dependencies
from .exceptions import InvalidToken



class FastAuth(APIRouter):
    def __init__(self, *, firebase: FirebaseConfig, user_model: Type[UserMod],
                 session: callable, post_create: callable,
                 default_groups: set[str] = None, default_permissions: set[str] = None,
                 user_object_schema: Type[BaseModel] | None = None):
        super().__init__()
        self.get_session = session
        self.User = user_model
        self.iss = firebase.iss
        self.project_id = firebase.project_id
        self.starter_groups = default_groups or {}
        self.starter_permissions = default_permissions or {}
        self.depends = Dependencies(iss=firebase.iss, project_id=firebase.project_id)
        self.post_create = post_create
        self.user_object_schema = user_object_schema or UserObjectSchema

    @staticmethod
    async def demo():
        # TESTME: Untested
        return 'it works'

    def get_register_routers(self):
        router = APIRouter()
        get_session = self.get_session

        @router.post('/register', response_model=self.user_object_schema)
        async def register(token: Annotated[str, Body()],
                           session: Annotated[AsyncSession, Depends(get_session)]) -> Type[Self]:
            token_data = auth.verify_id_token(token)
            if token_data['aud'] != self.project_id:
                raise InvalidToken()

            if email := token_data.get('email'):
                exists = await self.User.exists(session, EmailStr(email))

                if not exists:
                    display, *_ = email.partition('@')
                    user = self.User(email=email, username=email, display=display,
                                     groups=self.starter_groups, permissions=self.starter_permissions)
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                    await self.post_create(session, user)
                else:
                    user = await self.User.get_by_email(session, email)
                return user
            raise InvalidToken()

        return router

    @staticmethod
    def get_email_routers() -> APIRouter:
        router = APIRouter()

        # TODO: Placeholder
        @router.post('/email-signin')
        async def email_signin():
            # TODO: Email signin
            return 'PLACEHOLDER: Email signin'

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


    @staticmethod
    def get_google_routers() -> APIRouter:
        router = APIRouter()

        # TODO: Placeholder
        @router.post('/google-register', status_code=201)
        async def email_register():
            # TODO: Google register
            return 'PLACEHOLDER: Google register'

        # TODO: Placeholder
        @router.post('/google-signin')
        async def email_signin():
            # TODO: Google signin
            return 'PLACEHOLDER: Google signin'

        return router


    @staticmethod
    def get_facebook_routers() -> APIRouter:
        router = APIRouter()

        # TODO: Placeholder
        @router.post('/facebook-register', status_code=201)
        async def email_register():
            # TODO: Facebook register
            return 'PLACEHOLDER: Facebook register'

        # TODO: Placeholder
        @router.post('/facebook-signin')
        async def email_signin():
            # TODO: Facebook signin
            return 'PLACEHOLDER: Facebook signin'

        return router
