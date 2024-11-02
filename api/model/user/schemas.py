from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

class UserBase(BaseModel):
    id: str
    password: str
    is_admin: bool

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    @validator('id')
    def id_length(cls, v):
        if len(v) < 3:
            raise ValueError('id must be at least 3 characters')
        return v

    @validator('password')
    def password_length(cls, v):
        if len(v) < 8 or len(v) > 16:
            raise ValueError('비밀번호는 8자 이상 16자 이하로 입력해주세요')
        return v

class UserPasswordUpdate(BaseModel):
    uid: int
    password: str

    @validator('password')
    def password_length(cls, v) -> str:
        if len(v) < 8 or len(v) > 16:
            raise ValueError('비밀번호는 8자 이상 16자 이하로 입력해주세요')
        return v

class User(UserBase):
    uid: int
    
    class Config:
        orm_mode = True
        