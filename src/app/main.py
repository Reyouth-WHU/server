# this is use for debug
import uvicorn

from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VERSION}/openapi.json"
)

app.include_router(
    api_router,
    prefix=settings.API_VERSION
)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)


    # debug
    # from app.models.user import User, UserProfile
    # from fastapi.encoders import jsonable_encoder
    # a = User(username="123")
    # print(jsonable_encoder(a))
    # print(jsonable_encoder(a))