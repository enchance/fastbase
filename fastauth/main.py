from typing import Type
from fastapi import APIRouter
from fastapi import FastAPI
from icecream import ic
from pydantic import BaseSettings, PostgresDsn
from sqlmodel import SQLModel

from .models import *
from .dependencies import Dependencies



class FastAuth(APIRouter):
    def __init__(self, *, iss: str, project_id: str, account: Type[UserMod]):
        super().__init__()
        self.account = account
        self.iss = iss
        self.project_id = project_id
        self.depends = Dependencies(iss=iss, project_id=project_id)


    @staticmethod
    async def demo():
        # TESTME: Untested
        return 'it works'


    @staticmethod
    async def email_register():
        # TESTME: Untested
        pass


    @staticmethod
    async def email_signin():
        # TESTME: Untested
        pass