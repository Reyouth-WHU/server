from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION = "/api/v1"
    PROJECT_NAME: str


settings = Settings()


