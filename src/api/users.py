from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from services import UserService


router = APIRouter(prefix= "/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(service: UserService = Depends()) -> JSONResponse:
    get_result = service.get_all_users()
    if not get_result:
        return JSONResponse({
            "status": "error",
            "message": "No users found"
        }, status.HTTP_404_NOT_FOUND)

    return get_result