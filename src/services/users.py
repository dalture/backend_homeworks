from fastapi import Depends, HTTPException
from typing import List

from schemas import BaseUser, RegistrationUser, LoginUser, AccessToken
from repositories import UserRepository
from core.security import verify_password, create_access_token

class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repo = repository

    def get_all_users(self, limit, offset) -> List[BaseUser] | None:
        return self.repo.get_all_users(limit, offset)
    
    def get_user_by_id(self, user_id: int):
        return self.repo.get_by_id(user_id)
    
    def get_user_by_email(self, user_email: str):
        return self.repo.get_by_email(user_email)

    def create_user(self, user: RegistrationUser):
        if not self.repo.get_by_email(user.user_email):
            return self.repo.create(user)
        else:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )
        
    def login_user(self, user: LoginUser) -> AccessToken | None:
        db_user = self.repo.get_by_email(user.user_email)

        if not verify_password(user.user_password, db_user.user_password_hash):
            raise HTTPException(
                status_code=401, 
                detail="Wrong login data"
            )

        token = create_access_token({"sub": db_user.user_email})

        return AccessToken(access_token=token, token_type="bearer")