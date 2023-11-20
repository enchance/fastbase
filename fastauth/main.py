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
        return 'it works'

    @staticmethod
    async def google_register():
        pass

    @staticmethod
    async def google_signin():
        pass

    @staticmethod
    async def private_demo():
        pass