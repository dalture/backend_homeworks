from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.services import UserService


router = APIRouter(prefix= "/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(service: UserService = Depends()) -> JSONResponse:
    get_result = service.get_all_users(limit=10, offset=0)

    return JSONResponse(
        jsonable_encoder(get_result))

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, service: UserService = Depends()) -> JSONResponse:
    get_result = service.get_user_by_id(user_id)

    return JSONResponse(
            jsonable_encoder(get_result))