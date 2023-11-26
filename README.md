Fastbase
=============


Role-based Access Contral (RBAC) via Firebase `idtoken` authententication using FastAPI and SQLModel.


Installation
-----------

```bash
pip install fastbase
```

or
```bash
poetry add fastbase
```


Instructions
----------------

Fastbase assumes a headless setup using a frontend such as React, Angular, etc.

- **Authentication:** Managed by Firebase Auth
- **Authorization:** Managed by Fastbase

### Process:

1. Authentication happens in the frontend (JS) using the official Firebase JS package. An `idtoken` will be 
   generated if successful and attach this to your `Authorization` header.  
1. Upon reaching the server the `idtoken` is verified.
1. At first use, using the `/signin` endpoint Fastbase checks if the user alread exists in the database. If user is 
   new then a record is created using SQLModel.

