from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserInfo
from src.schemas import BaseUser, RegistrationUser
from src.core.security import hash_password

from src.core.database import get_db

class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_users(self, limit: int = 10, offset: int = 0) -> List[UserInfo]:
        result = await self.db.execute(select(UserInfo))
        users = result.scalars().all()
        users = users[offset: offset + limit]
        return users

    async def get_by_id(self, user_id: int) -> Optional[UserInfo]:
        result = await self.db.execute(select(UserInfo).where(UserInfo.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, user_email: str) -> Optional[UserInfo]:
        result = await self.db.execute(select(UserInfo).where(UserInfo.user_email == user_email))
        return result.scalar_one_or_none()
    
    async def create(self, new_user: RegistrationUser) -> UserInfo:
        user_dict = new_user.model_dump()
        user_dict["user_password_hash"] = hash_password(new_user.user_password)
        user_dict.pop("user_password")
        db_user = UserInfo(**user_dict)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user