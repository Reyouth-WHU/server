import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    PROJECT_NAME: str = "reyouth"

    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/qiufeng/Desktop/reyouth/test.sqlite3"


settings = Settings()


