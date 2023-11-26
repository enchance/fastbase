from typing import Annotated
from firebase_admin import auth, app_check
from fastapi import Header

from .globals import logger
from .exceptions import InvalidToken
from .models import UserMod



class Dependencies:
    def __init__(self, *, iss, project_id):
        self.firebase_iss = iss
        self.firebase_project_id = project_id

    def verify_device(self, appcheck: Annotated[str, Header()],
                      token: Annotated[str, Header()]) -> dict:
        """
        Verify AppCheck and FirebaseAuth tokens. Both must pass to continue.
        :param appcheck:    App AppCheck jwt
        :param token:       User idtoken jwt
        :return:            Verified token
        """
        try:
            appcheck_data = app_check.verify_token(appcheck)
            if appcheck_data['iss'] != self.firebase_iss:
                raise Exception()
        except Exception as err:
            logger.critical(err)
            raise InvalidToken('INVALID_DEVICE_TOKEN')

        try:
            idtoken_data = auth.verify_id_token(token)
            if idtoken_data['aud'] != self.firebase_project_id:
                raise Exception()
            return idtoken_data
        except auth.RevokedIdTokenError as err:
            logger.critical(err)
            raise InvalidToken('TOKEN_REVOKED')
        except Exception as err:
            logger.critical(err)
            raise InvalidToken()


    # @staticmethod
    # async def current_account(self, idtoken: dict) -> AccountMod:
    #     """
    #     Get the saved Account entry from either the db or redis.
    #     :param idtoken: Verified contents of the idtoken jwt
    #     :return:        AccountMod
    #     """
    #     try:
    #         # TODO: query
    #         # account: AccountMod = await AccountMod.get(docid=idtoken['uid'], is_active=True)
    #         account: AccountMod = ''
    #         return account
    #     except DoesNotExist as _:
    #         logger.error("Account doesn't exist")
    #         raise