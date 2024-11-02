import json

import os

from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session

from core.config import settings

from model.database import engine, get_db, Base
from model.user import models as user_models
from model.user import schemas as user_schemas
from model.user import crud as user_crud

PATH = os.path.abspath(os.pardir)

def init_database(engine: engine, db: Annotated[Session, Depends(get_db)]):
    # Create Tables
    Base.metadata.create_all(bind=engine)

    # Create Admin User if not exists
    # admin_user = user_crud.get_user_by_id(db, settings.ADMIN_ID)
    # if not admin_user:
    #     admin_user = user_schemas.UserCreate(
    #         id=settings.ADMIN_ID,
    #         password=settings.ADMIN_PASSWORD,
    #         is_admin=True,
    #     )

    #     admin_user = user_crud.create_user(db, admin_user)