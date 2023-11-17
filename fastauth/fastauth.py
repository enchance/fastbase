from fastapi import FastAPI



class Connection:
    connection: str

    def __init__(self, connection_string: str):
        self.connection = connection_string


class FastAuth:
    app: FastAPI

    def __init__(self, app: FastAPI, connection: Connection):
        self.app = app


