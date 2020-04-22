from fastapi import FastAPI

from .api.api_v1.api import api_router
from .core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VERSION}/openapi.json"
)

app.include_router(
    api_router,
    prefix=settings.API_VERSION
)