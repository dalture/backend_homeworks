from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api import tasks_router
from api import users_router

common_router = APIRouter()

@common_router.get("/")
def root():
    return JSONResponse({
        "message": "hello"
        }, status_code = status.HTTP_200_OK)


common_router.include_router(users_router)
common_router.include_router(tasks_router)