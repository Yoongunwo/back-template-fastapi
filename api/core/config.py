from pydantic import BaseSettings, BaseModel
from typing import Optional
import os

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = 'SAVE - API'
    API_V1_STR: str = '/api/v1'
    
    # Database Settings
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
    DB_NAME: str = os.getenv('DB_NAME', 'template_db')
    DB_USER: str = os.getenv('DB_USER', 'template_user')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '5KaAme3BT1dHAOimu9lFF05ceR4Bx9fjHB2mbWtbXQDVIaYt0C3KWOqOIHdRzGS55sJ1RLg5evoMscapQeGJwGLodlUz7yTIICMPqEtQdkbHjTfkQmftrWHuI9M93jUp')

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    # JWT Settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default-secret-key')
    TOKEN_LOCATION: set = {os.getenv('TOKEN_LOCATION', 'cookies')}
    CSRF_PROTECT: bool = os.getenv('CSRF_PROTECT', 'False').lower() == 'true'
    COOKIE_SECURE: bool = os.getenv('COOKIE_SECURE', 'False').lower() == 'true'
    COOKIE_SAMESITE: str = os.getenv('COOKIE_SAMESITE', 'lax')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '1200'))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', '10080'))
    
    # ADMIN Settings
    ADMIN_ID: str = os.getenv('ADMIN_ID', 'admin')
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', '12341234')

    class Config:
        case_sensitive = True
        env_file = '.env'

settings = Settings()

class AuthJWTSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_token_location: set = settings.TOKEN_LOCATION
    authjwt_cookie_csrf_protect: bool = settings.CSRF_PROTECT
    authjwt_cookie_secure: bool = settings.COOKIE_SECURE
    authjwt_cookie_samesite: str = settings.COOKIE_SAMESITE
    authjwt_access_token_expires: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    authjwt_refresh_token_expires: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES