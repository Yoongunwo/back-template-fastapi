from datetime import datetime

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError

from psycopg2.errors import InFailedSqlTransaction

from core.security import get_password_hash

from . import models, schemas

import subprocess

from copy import deepcopy
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    try:
        db_user = models.User(
            id=user.id,
            password=get_password_hash(user.password),
            is_admin=user.is_admin,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except InFailedSqlTransaction as e:
        db.rollback()
        print(f"Transaction failed: {e}")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return None

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except ProgrammingError as e:
        print(f'Table not found, {e}')
        return []
    except Exception as e:
        print(e)
        return None

def get_user_by_id(db: Session, id: str) -> models.User:
    try:
        return db.query(models.User).filter(models.User.id == id).first()
    except ProgrammingError as e:
        print(f'Table not found, {e}')
        return None
    except Exception as e:
        print(e)
        return None

def get_user_by_uid(db: Session, uid: int) -> models.User:
    try:
        return db.query(models.User).filter(models.User.uid == uid).first()
    except ProgrammingError as e:
        print(f'Table not found, {e}')
        return None
    except Exception as e:
        print(e)
        return None