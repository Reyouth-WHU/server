import secrets
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    PROJECT_NAME: str = "reyouth"

    # todo
    # too ugly
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT_DIR}/test.sqlite3"

    USERNAME_TEST_USER = "miaomiaomiao"
    FIRST_SUPERUSER = "string"
    FIRST_SUPERUSER_PASSWORD = "string"


settings = Settings()


