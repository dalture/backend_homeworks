from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api import tasks_router
from src.api import users_router
from src.api import auth_router

common_router = APIRouter()

@common_router.get("/")
def root():
    return JSONResponse({
        "message": "hello"
        }, status_code = status.HTTP_200_OK)


common_router.include_router(users_router)
common_router.include_router(tasks_router)
common_router.include_router(auth_router)