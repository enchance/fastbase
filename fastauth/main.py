from typing import Type
from fastapi import APIRouter
from fastapi import FastAPI
from icecream import ic
from pydantic import BaseSettings, PostgresDsn
from sqlmodel import SQLModel

from .models import *
from .schemas import *
from .dependencies import Dependencies



class FastAuth(APIRouter):
    def __init__(self, *, firebase: FirebaseConfig, user_model: Type[UserMod],
                 default_groups: set[str] = None, default_permissions: set[str] = None):
        super().__init__()
        self.user = user_model
        self.iss = firebase.iss
        self.project_id = firebase.project_id
        self.starter_groups = default_groups or {}
        self.starter_permissions = default_permissions or {}
        self.depends = Dependencies(iss=firebase.iss, project_id=firebase.project_id)

    @staticmethod
    async def demo():
        # TESTME: Untested
        return 'it works'


    def get_email_routers(self) -> APIRouter:         # noqa
        router = APIRouter()

        # TODO: Placeholder
        @router.post('/email-register', status_code=201)
        async def email_register():
            # TODO: Email register
            return 'PLACEHOLDER: Email register'

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


    # TODO: Placeholder
    def get_google_routers(self) -> APIRouter:            # noqa
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


    # TODO: Placeholder
    def get_facebook_routers(self) -> APIRouter:          # noqa
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
