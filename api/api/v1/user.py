from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT

from core.security import verify_password

from datetime import datetime, timedelta

from model.database import get_db

from model.user import schemas as user_schemas
from model.user import crud as user_crud

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not found'}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/user/sign-in')

@router.post('/sign-up')
async def sign_up(user: user_schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_users = user_crud.get_users(db)

    for db_user in db_users:
        if db_user.id == user.id:
            raise HTTPException(status_code=400, detail='ID already registered')

    
    user = user_crud.create_user(db, user)
    if not user:
        raise HTTPException(status_code=400, detail='Error')

    return user

@router.post('/sign-in')
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], Authorize: Annotated[AuthJWT, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = user_crud.get_user_by_id(db, form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail='Invalid ID')
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Invalid password')

    try:
        user_claims = {
            'id': user.id,
            'is_admin': user.is_admin,
        }

        access_token = Authorize.create_access_token(subject=user.uid, user_claims=user_claims, fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=user.uid)
        
        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='error')

    return user

@router.post('/refresh')
async def refresh(Authorize: Annotated[AuthJWT, Depends()], db: Annotated[Session, Depends(get_db)]):
    print('Refreshing')
    Authorize.jwt_refresh_token_required()
    
    current_user = Authorize.get_jwt_subject()
    
    user = user_crud.get_user_by_uid(db, current_user)
    if not user:
        print('User not found')
        raise HTTPException(status_code=404, detail='User not found')

    try:
        user_claims = {
            'id': user.id,
            'is_admin': user.is_admin,
        }

        new_access_token = Authorize.create_access_token(
            subject=user.uid, user_claims=user_claims, fresh=False)

        Authorize.set_access_cookies(new_access_token)
    except Exception as e:
        raise HTTPException(status_code=404, detail='error')
    print('Refreshed successfully')
    return {'msg': 'Refreshed successfully'}

@router.get('/me', response_model=user_schemas.User)
async def get_me(Authorize: Annotated[AuthJWT, Depends()], db: Annotated[Session, Depends(get_db)]):
    try:
        Authorize.jwt_required()

        current_user = Authorize.get_jwt_subject()

        user = user_crud.get_user_by_uid(db, current_user)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='error')

    return user

@router.post('/sign-out')
async def sign_out(Authorize: Annotated[AuthJWT, Depends()], db: Annotated[Session, Depends(get_db)]):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()

    Authorize.unset_jwt_cookies()

    return {'msg': 'Signed out successfully'}