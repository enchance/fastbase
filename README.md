Fastbase
=============


Role-based Access Contral (RBAC) via Firebase `idtoken` authententication using FastAPI and SQLModel.


Installation
-----------

```bash
pip install fastbase/home/enchance/Dev/venv/fastbase-_XKMLCSM-py3.11/bin/python
``

or
```bash
poetry add fastbase
```


Instructions
----------------

Fastbase assumes a headless setup using a frontend such as React, Angular, etc.

- `Firebase Auth`: Authentication.
- `Fastbase`: Authorization.

Process:

1. Actual authentication happens in the frontend (JS) after which an `idtoken` is recieved.
1. The `idtoken` is sent to the server for authorization purposes.
1. At first use using the `/signin` endpoint Fastbase checks if the user alread exists in the database. If user is new then a record is created using SQLModel.

