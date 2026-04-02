from fastapi import Depends, HTTPException
from typing import List

from src.schemas import BaseUser, RegistrationUser, LoginUser, AccessToken
from src.repositories import UserRepository
from src.core.security import verify_password, create_access_token
from src.core.exceptions import UserNotFoundException

class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repo = repository

    async def get_all_users(self, limit, offset) -> List[BaseUser] | None:
        return await self.repo.get_all_users(limit, offset)
    
    async def get_user_by_id(self, user_id: int):
        user_db = await self.repo.get_by_id(user_id)

        if not user_db:
            return UserNotFoundException(user_id=user_id)
        
        return user_db
    
    async def get_user_by_email(self, user_email: str):
        return await self.repo.get_by_email(user_email)

    async def create_user(self, user: RegistrationUser):
        if not await self.repo.get_by_email(user.user_email):
            return await self.repo.create(user)
        else:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )
        
    async def login_user(self, user: LoginUser) -> AccessToken | None:
        db_user = await self.repo.get_by_email(user.user_email)

        if not verify_password(user.user_password, db_user.user_password_hash):
            raise HTTPException(
                status_code=401, 
                detail="Wrong login data"
            )

        token = create_access_token({"sub": db_user.user_email})

        return AccessToken(access_token=token, token_type="bearer")