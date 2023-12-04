from fastbase.models import UserMod


class User(UserMod, table=True):
    __tablename__ = 'auth_user'