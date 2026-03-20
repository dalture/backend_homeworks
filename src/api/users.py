from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from services import UserService


router = APIRouter(prefix= "/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(service: UserService = Depends()) -> JSONResponse:
    get_result = service.get_all_users()
    if not get_result:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    return JSONResponse({
        jsonable_encoder(get_result)
        })

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, service: UserService = Depends()) -> JSONResponse:
    get_result = service.get_user_by_id(user_id)
    if get_result:
        return JSONResponse(
            jsonable_encoder(get_result)
            )
    else:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")