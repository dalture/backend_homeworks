from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from schemas import RegistrationUser, LoginUser, AccessToken, BaseUser
from services import UserService


router = APIRouter(prefix= "/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user: RegistrationUser,
        service: UserService = Depends()
) -> BaseUser:
    db_user = service.create_user(user)

    return db_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
        response: Response,
        user: LoginUser,
        service: UserService = Depends()
) -> AccessToken:
    token = service.login_user(user)
    response.set_cookie(key="access_token", value=token.access_token, httponly=True)

    return token
