Fastbase
=============

**DEV MESSAGE: Fastbase is currently still in development and in its current state is unfit for production. Check 
back again for updates.**

Role-based Access Contral (RBAC) via Firebase `idtoken` authententication using FastAPI and SQLModel.

Documentation: https://enchance.github.io/fastbase/class/fastbase/


Installation
-----------

```bash
pip install fastbase
```

or
```bash
poetry add fastbase
```


Overview
----------------

Fastbase assumes a headless setup using a frontend such as React, Angular, etc.

- **API Endpoints:** Managed by FastAPI
- **Authentication:** Managed by Firebase Auth
- **Authorization:** Managed by Fastbase
- **Database ORM:** SQLModel

### Fastbase process

1. Authentication happens in the frontend (JS) using the official Firebase JS package. An `idtoken` will be 
   generated if successful.
1. Insert this token in your `Authorization` header (`Bearer <idtoken>`) when hitting restricted APIs.  
1. Upon reaching the server the `idtoken` is verified.


Endpoints
-----------------------------------------
To follow


Dependencies
-----------------------------------------
To follow


Sample Code
-----------------------------------------

### models.py
Your required `User` model. Optional models include `TaxonomyMod` and `OptionMod` which should be extended if you want 
to use them. Add any additional fields you need.

```python
from fastbase.models import UserMod, TaxonomyMod, OptionMod 

# Required
class User(UserMod, table=True):
    __tablename__ = 'auth_user'
    # Add any fields and methods you need

    
# Optional
class Taxonomy(TaxonomyMod, table=True):
   __tablename__ = 'app_taxonomy'
   # Add any fields and methods you need


# Optional
class Option(OptionMod, table=True):
   __tablename__ = 'app_option'
   # Add any fields and methods you need
```

### main.py
Initialize Fastbase

```python
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import FastAPI
from fastbase import Fastbase
from contextlib import asynccontextmanager

from .models import User

# .env file
DATABASE_URL = 'postgresql+asyncpg://user:password@localhost:5432/dbname'

# DB engine
engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10)

@asynccontextmanager
async def lifespan(_: FastAPI):
   """Insert in lifespan events on start: https://fastapi.tiangolo.com/advanced/events/"""
   fbase = Fastbase()
   fbase.initialize(engine=engine, user_model=User)
   print('RUNNING')
   yield
   print('STOPPED')
```